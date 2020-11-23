#### Filip Dratwiński 237999, Piotr Gramacki 238493
# Porównanie wybranych miar semantycznego podobieństwa / powiązania słów


## Wykorzystywane miary podobieństwa semantycznego

### Wektory semantyki dystrybucyjnej

 - Odległość euklidesowa:

<img src="https://latex.codecogs.com/gif.latex? Sim(s1, s2) = |emb(s1) - emb(s2)|," \>

gdzie $emb(x)$ oznacza wektor osadzeń dla słowa $x$. Miara ta jest odwrotnie proporcjonalna do podobieństwa słów ($Sim(x, x) = 0$), więc przeskalowano je liniowo aby $Sim(x, x)$ przyjmowało wartość maksymalną. Wykorzystano przekształcenie:

<img src="https://latex.codecogs.com/gif.latex? Sim(s1, s2) = 1.5 - Sim(s1, s2)." \>
 - Miara cosinusowa:

\begin{equation}
    Sim(s1, s2) = \frac{emb(s1) \cdot emb(s2)}{|emb(s1)||emb(s2)|},
\end{equation}

Miara ta przyjmuje wartości z zakresu $[-1, 1]$. Aby porównać ją łatwo z miarami ze zbioru `Simlex999` przekształcono ją do zakresu $[0, 10]$ korzystając z przekształcenia:

\begin{equation}
    Sim(s1, s2) = (Sim(s1, s2) + 1) * 5.
\end{equation}

### Sieć leksykalna
 - Miara Wu-Palmer: 
 
\begin{equation}
Sim(s1,s2) = 2 * \frac{depth(lcs(s1,s2))}{depth(s1) + depth(s2)},
\end{equation} 

gdzie *lcs(s1,s2)* to *Least Common Subsumer*. Można to przetłumaczyć jako najbliższy wspólny przodek wierzchołków *s1* i *s2*. *depth(s1)* to głębokość drzewa taksonomicznego, na którym znajduje się wierzchołek *s1*. Miara ta przyjmuje wartości od 0 do 1, gdzie 0 oznacza, że Synset'y są całkowicie niepodobne do siebie, a 1 oznacza, że jest to dokładnie ten sam Synset.

 - Miara Leacock-Chodorow:

\begin{equation}
Sim(s1,s2) = -\log\frac{length(s1,s2)}{2D},
\end{equation}

gdzie *length(s1,s2)* oznacza najkrótszą ścieżkę pomiędzy wierzchołkami *s1* i *s2*. *D* oznacza największą głębokość drzewa taksonomicznego. Zakres miary zależy od współczynnika *D*. Minimalną wartością jest zawsze 0, co oznacza, że Synset'y są całkowicie niepodobne do siebie (ścieżka pomiędzy nimi jest maksymalna). W przypadku sieci `PLWN` największą głębokością jest 32. Jeżeli wierzchołki znajdują się koło siebie to wartość miary wyniesie 1.8062. Gdy porównywany jest ze sobą ten sam Synset to przyjmowana jest stała wartość 2.0, jako maksymalna.


## Wyniki oceny siły podobieństwa dla par słów na zbiorze danych SimLex999

Miara cosinusowa została przeskalowana do zakresu $[0, 10]$ więc możliwe było porównanie jej bezpośrednio z wartościami miar w zbiorze *SimLex999*. Obliczono średnią wartość bezwzględną z różnicy między miarą cosinusową a miarami z *SimLex999*. Wyniki pokazano poniżej.


|             |   cosine_metric |
|:------------|----------------:|
| similarity  |         4.61717 |
| relatedness |         1.74491 |

### Korelacja pomiędzy zdefiniowanymi miarami, a wartościami simmilarity i relatedness ze zbioru *SimLex999*

|             |   euclidean_metric |   cosine_metric |   wu_palmer |   leacock_chodorow |
|:------------|-------------------:|----------------:|------------:|-------------------:|
| similarity  |           0.370449 |        0.39001  |    0.358705 |           0.436089 |
| relatedness |           0.599525 |        0.627853 |    0.37754  |           0.355072 |


## Przykładowe wygenerowane listy `k` podobnych słów według wszystkich miar podobieństwa
W poniższym badaniu przyjęto `k=10`.


Słowo             |  10 najbardziej podobnych słów - Euklides | 10 najbardziej podobnych słów - Cosinus | 10 najbardziej podobnych słów - Wu-Palmer | 10 najbardziej podobnych słów - Leacock-Chodorow
:-------------------------:|:-------------------------:|:-------------------------:|:-------------------------:|:-------------------------:
drewno      | tektura - 0.5727  </br> cegła - 0.5506  </br> drzewo - 0.5360  </br> tkanina - 0.5193  </br> węgiel - 0.5134  </br> szkło - 0.4827  </br> mech - 0.4590  </br> mebel - 0.4562  </br> żelazo - 0.4520  </br> zboże - 0.4517 | tektura - 7.8504  </br> cegła - 7.7465  </br> drzewo - 7.6769  </br> tkanina - 7.5954  </br> węgiel - 7.5667  </br> szkło - 7.4126  </br> mech - 7.2910  </br> mebel - 7.2764  </br> żelazo - 7.2541  </br> zboże - 7.2525 | drzewo - 1.0 <br/>kłoda - 0.8571 <br/> miód - 0.8333 <br/> słoma - 0.8333 <br/> materiał - 0.8 <br/> papier - 0.7273 <br/> perła - 0.7273 <br/> aluminium - 0.7273 <br/> bawełna - 0.7143 <br/> cegła - 0.6667 <br/> | drzewo - 2.0 <br/> materiał - 1.5051 <br/> miód - 1.5051 <br/> kłoda - 1.5051 <br/> słoma - 1.5051 <br/> papier - 1.3291 <br/> cegła - 1.3291 <br/> korzeń - 1.3291 <br/> perła - 1.3291 <br/> aluminium - 1.3291 
długopis    | kubek - 0.6217  </br> pudełko - 0.5718  </br> torba - 0.5071  </br> szuflada - 0.4813  </br> torebka - 0.4722  </br> tektura - 0.4566  </br> słoik - 0.4556  </br> cukierek - 0.4546  </br> kanapka - 0.4493  </br> butelka - 0.4445 | kubek - 8.0713  </br> pudełko - 7.8460  </br> torba - 7.5353  </br> szuflada - 7.4058  </br> torebka - 7.3590  </br> tektura - 7.2781  </br> słoik - 7.2730  </br> cukierek - 7.2678  </br> kanapka - 7.2400  </br> butelka - 7.2148 | papier - 0.8571 <br/> tektura - 0.8 <br/> ser - 0.7143 <br/> cygaro - 0.7143 <br/> papieros - 0.7143 <br/> masło - 0.7143 <br/> fajka - 0.7143 <br/> pieniądz - 0.6667 <br/> drzwi - 0.6667 <br/> tkanina - 0.6667 <br/>  | papier - 1.5051 <br/> tektura - 1.3291 <br/> materiał - 1.3291 <br/> pieniądz - 1.2041 <br/> garnek - 1.2041 <br/> obiektyw - 1.2041 <br/> aluminium - 1.2041 <br/> ser - 1.2041 <br/> talerz - 1.2041 <br/> filiżanka - 1.2041
ekran       | kino - 0.4908  </br> kamera - 0.4760  </br> film - 0.4365  </br> komputer - 0.4359  </br> telewizja - 0.4285  </br> obraz - 0.3816  </br> aktor - 0.3769  </br> kanapa - 0.3745  </br> okno - 0.3685  </br> mysz - 0.3654 | kino - 7.4539  </br> kamera - 7.3787  </br> film - 7.1723  </br> komputer - 7.1692  </br> telewizja - 7.1297  </br> obraz - 6.8727  </br> aktor - 6.8467  </br> kanapa - 6.8333  </br> okno - 6.7995  </br> mysz - 6.7817 | komputer - 0.8571 <br/> maszyna - 0.8571 <br/> aparat - 0.8571 <br/> telefon - 0.8571 <br/> winda - 0.8 <br/> silnik - 0.8 <br/> klatka - 0.8 <br/> dzwon - 0.7692 <br/> dekoracja - 0.7692 <br/> pręt - 0.7692 <br/>  | komputer - 1.5051 <br/> maszyna - 1.5051 <br/> aparat - 1.5051 <br/> telefon - 1.5051 <br/> winda - 1.3291 <br/> dzwon - 1.3291 <br/> silnik - 1.3291 <br/> dekoracja - 1.3291 <br/> klatka - 1.3291 <br/> pręt - 1.3291
głupi       | głupawy - 0.6743  </br> mądry - 0.6419  </br> głupol - 0.6357  </br> tępy - 0.5048  </br> zabawny - 0.4901  </br> nudny - 0.4883  </br> dziecinny - 0.4784  </br> motłoch - 0.4586  </br> facet - 0.4552  </br> smutny - 0.4540 | głupawy - 8.2955  </br> mądry - 8.1593  </br> głupol - 8.1325  </br> tępy - 7.5240  </br> zabawny - 7.4503  </br> nudny - 7.4414  </br> dziecinny - 7.3908  </br> motłoch - 7.2888  </br> facet - 7.2707  </br> smutny - 7.2649 | człowiek - 0.8889 <br/> pisarz - 0.8 <br/> mąż - 0.8 <br/> dziewczynka - 0.8 <br/> mężczyzna - 0.8 <br/> facet - 0.8 <br/> robotnik - 0.8 <br/> opiekun - 0.8 <br/> szef - 0.8 <br/> kandydat - 0.8 <br/>  | człowiek - 1.8062 <br/> pisarz - 1.5051 <br/> mąż - 1.5051 <br/> dziewczynka - 1.5051 <br/> mężczyzna - 1.5051 <br/> facet - 1.5051 <br/> zwierzę - 1.5051 <br/> robotnik - 1.5051 <br/> opiekun - 1.5051 <br/> szef - 1.5051
kapusta     | ziemniak - 0.7577  </br> fasola - 0.6846  </br> sałatka - 0.6564  </br> zupa - 0.6180  </br> masło - 0.5980  </br> cebulka - 0.5853  </br> ryż - 0.5777  </br> jabłko - 0.5637  </br> indyk - 0.5613  </br> ciasto - 0.5500 | ziemniak - 8.6226  </br> fasola - 8.3377  </br> sałatka - 8.2210  </br> zupa - 8.0552  </br> masło - 7.9662  </br> cebulka - 7.9085  </br> ryż - 7.8735  </br> jabłko - 7.8083  </br> indyk - 7.7972  </br> ciasto - 7.7438 | fiołek - 0.8235 <br/> len - 0.8235 <br/> ziemniak - 0.7778 <br/> zboże - 0.75 <br/> tytoń - 0.75 <br/> kwiat - 0.75 <br/> fasola - 0.75 <br/> trawa - 0.75 <br/> pszenica - 0.7059 <br/> ryż - 0.7059 <br/>  | fiołek - 1.3291 <br/> len - 1.3291 <br/> zboże - 1.2041 <br/> tytoń - 1.2041 <br/> kwiat - 1.2041 <br/> fasola - 1.2041 <br/> trawa - 1.2041 <br/> ziemniak - 1.2041 <br/> ser - 1.1072 <br/> posiłek - 1.1072
kot         | zwierzak - 0.7099  </br> pies - 0.6793  </br> królik - 0.5902  </br> szczur - 0.5815  </br> zwierzę - 0.5492  </br> lis - 0.5081  </br> kura - 0.5005  </br> koza - 0.4727  </br> mysz - 0.4520  </br> ptak - 0.4517 | zwierzak - 8.4393  </br> pies - 8.3160  </br> królik - 7.9309  </br> szczur - 7.8911  </br> zwierzę - 7.7402  </br> lis - 7.5401  </br> kura - 7.5027  </br> koza - 7.3614  </br> mysz - 7.2540  </br> ptak - 7.2525 | lew - 0.9412 <br/> norka - 0.875 <br/> pies - 0.875 <br/> lis - 0.8235 <br/> jastrząb - 0.75 <br/> ogar - 0.7 <br/> zwierzę - 0.6667 <br/> ogier - 0.5714 <br/> królik - 0.5714 <br/> cielak - 0.5714 <br/>  | lew - 1.8062 <br/> norka - 1.5051 <br/> pies - 1.5051 <br/> lis - 1.3291 <br/> potwór - 1.2041 <br/> zboże - 1.2041 <br/> głupi - 1.2041 <br/> ogier - 1.2041 <br/> jastrząb - 1.2041 <br/> królik - 1.2041
książka     | esej - 0.7001  </br> opowiadanie - 0.6895  </br> czasopismo - 0.5978  </br> literatura - 0.5460  </br> biografia - 0.5348  </br> autor - 0.5239  </br> opowieść - 0.5202  </br> film - 0.5184  </br> pisarz - 0.5121  </br> artykuł - 0.4682 | esej - 8.4004  </br> opowiadanie - 8.3579  </br> czasopismo - 7.9651  </br> literatura - 7.7248  </br> biografia - 7.6708  </br> autor - 7.6183  </br> opowieść - 7.6000  </br> film - 7.5910  </br> pisarz - 7.5601  </br> artykuł - 7.3385 | artykuł - 0.8333 <br/> esej - 0.8333 <br/> rozprawa - 0.8333 <br/> tekst - 0.8 <br/> piosenka - 0.7692 <br/> uwaga - 0.7273 <br/> hymn - 0.7143 <br/> film - 0.7143 <br/> duma - 0.7143 <br/> drzwi - 0.6667 <br/>  | artykuł - 1.5051 <br/> tekst - 1.5051 <br/> esej - 1.5051 <br/> rozprawa - 1.5051 <br/> uwaga - 1.3291 <br/> piosenka - 1.3291 <br/> drzwi - 1.2041 <br/> kalendarz - 1.2041 <br/> woda - 1.2041 <br/> pierś - 1.2041
rower       | samochód - 0.5374  </br> pojazd - 0.4814  </br> taksówka - 0.4497  </br> autobus - 0.4469  </br> wycieczka - 0.4365  </br> powóz - 0.4309  </br> wóz - 0.4215  </br> torba - 0.4163  </br> barierka - 0.4006  </br> kurtka - 0.3964 | samochód - 7.6833  </br> pojazd - 7.4062  </br> taksówka - 7.2423  </br> autobus - 7.2274  </br> wycieczka - 7.1723  </br> powóz - 7.1427  </br> wóz - 7.0920  </br> torba - 7.0638  </br> barierka - 6.9783  </br> kurtka - 6.9551 | powóz - 0.875 <br/> motor - 0.875 <br/> pojazd - 0.7692 <br/> wóz - 0.7059 <br/> samochód - 0.7059 <br/> autobus - 0.6667 <br/> rakieta - 0.5714 <br/> łódź - 0.5714 <br/> balon - 0.5 <br/> samolot - 0.4706 <br/>  | powóz - 1.5051 <br/> motor - 1.5051 <br/> pojazd - 1.3291 <br/> wóz - 1.2041 <br/> samochód - 1.2041 <br/> rakieta - 1.1072 <br/> maszyna - 1.1072 <br/> autobus - 1.1072 <br/> wieża - 1.028 <br/> rzadki - 1.028
tapeta      | karnisz - 0.5376  </br> sufit - 0.5314  </br> dywan - 0.5082  </br> tkanina - 0.4971  </br> podłoga - 0.4878  </br> mebel - 0.4752  </br> tektura - 0.4451  </br> paznokieć - 0.4193  </br> ściana - 0.4193  </br> ubranie - 0.4176 | karnisz - 7.6844  </br> sufit - 7.6547  </br> dywan - 7.5406  </br> tkanina - 7.4855  </br> podłoga - 7.4388  </br> mebel - 7.3743  </br> tektura - 7.2178  </br> paznokieć - 7.0804  </br> ściana - 7.0802  </br> ubranie - 7.0711 | wierzch - 0.8 <br/> strona - 0.6667 <br/> kąt - 0.4444 <br/> stopa - 0.4444 <br/> brzuch - 0.4444 <br/> pierś - 0.4444 <br/> kolano - 0.4444 <br/> okoliczność - 0.4 <br/> serce - 0.4 <br/> jelito - 0.4 <br/>  | materiał - 1.5051 <br/> wierzch - 1.5051 <br/> papier - 1.3291 <br/> aluminium - 1.3291 <br/> strona - 1.3291 <br/> perła - 1.3291 <br/> drzewo - 1.2041 <br/> diament - 1.2041 <br/> tkanina - 1.2041 <br/> miód - 1.2041
wycieczka   | drzwi - 0.5014  </br> kanapa - 0.4533  </br> podłoga - 0.4424  </br> pudełko - 0.4355  </br> torebka - 0.4293  </br> klakson - 0.4285  </br> miska - 0.4230  </br> torba - 0.4225  </br> szuflada - 0.4200  </br> kabina - 0.4166 | drzwi - 7.5072  </br> kanapa - 7.2613  </br> podłoga - 7.2036  </br> pudełko - 7.1672  </br> torebka - 7.1341  </br> klakson - 7.1295  </br> miska - 7.1004  </br> torba - 7.0975  </br> szuflada - 7.0837  </br> kabina - 7.0658 | podróż - 0.8571 <br/> stan - 0.8333 <br/> kąpiel - 0.8 <br/> lot - 0.8 <br/> emocja - 0.7692 <br/> spokój - 0.7692 <br/> ignorancja - 0.7692 <br/> postawa - 0.7692 <br/> obecność - 0.7692 <br/> nastrój - 0.7692 <br/>  | podróż - 1.5051 <br/> stan - 1.5051 <br/> emocja - 1.3291 <br/> spokój - 1.3291 <br/> okoliczność - 1.3291 <br/> ignorancja - 1.3291 <br/> kąpiel - 1.3291 <br/> postawa - 1.3291 <br/> lot - 1.3291 <br/> obecność - 1.3291
zamek       | wieża - 0.4756  </br> książę - 0.4606  </br> kaplica - 0.4266  </br> wzgórze - 0.4233  </br> brama - 0.4125  </br> kościół - 0.3784  </br> most - 0.3773  </br> zajazd - 0.3718  </br> król - 0.3554  </br> ogród - 0.3551 | wieża - 7.3766  </br> książę - 7.2989  </br> kaplica - 7.1197  </br> wzgórze - 7.1017  </br> brama - 7.0431  </br> kościół - 6.8552  </br> most - 6.8489  </br> zajazd - 6.8179  </br> król - 6.7249  </br> ogród - 6.7228 | szałas - 0.8571 <br/> dom - 0.8571 <br/> budka - 0.8571 <br/> kino - 0.8571 <br/> wieża - 0.8571 <br/> lotnisko - 0.8333 <br/> szkoła - 0.8 <br/> kaplica - 0.8 <br/> kościół - 0.8 <br/> domek - 0.8 <br/>  | szałas - 1.5051 <br/> dom - 1.5051 <br/> konstrukcja - 1.5051 <br/> lotnisko - 1.5051 <br/> budka - 1.5051 <br/> kino - 1.5051 <br/> wieża - 1.5051 <br/> kręgielnia - 1.5051 <br/> brama - 1.3291 <br/> szkoła - 1.3291
żniwa       | zboże - 0.6834  </br> pszenica - 0.5718  </br> ziemniak - 0.4644  </br> ziarno - 0.4434  </br> zima - 0.4347  </br> bydło - 0.4344  </br> chleb - 0.3854  </br> jagnię - 0.3845  </br> obfitość - 0.3809  </br> len - 0.3769 | zboże - 8.3329  </br> pszenica - 7.8459  </br> ziemniak - 7.3188  </br> ziarno - 7.2091  </br> zima - 7.1628  </br> bydło - 7.1613  </br> chleb - 6.8941  </br> jagnię - 6.8890  </br> obfitość - 6.8692  </br> len - 6.8468 | miesiąc - 0.5714 <br/> tydzień - 0.5714 <br/> data - 0.5714 <br/> dzień - 0.5714 <br/> sezon - 0.5714 <br/> rok - 0.5714 <br/> wiek - 0.5714 <br/> dekada - 0.5714 <br/> sierpień - 0.5 <br/> lato - 0.5 <br/>  | miesiąc - 1.3291 <br/> tydzień - 1.3291 <br/> data - 1.3291 <br/> dzień - 1.3291 <br/> sezon - 1.3291 <br/> rok - 1.3291 <br/> wiek - 1.3291 <br/> dekada - 1.3291 <br/> rzadki - 1.2041 <br/> mądry - 1.2041
