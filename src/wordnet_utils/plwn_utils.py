import plwn

# Even when we filter out synsets to specific lemma with variant 1,
# there are cases when this returns multiple synsets. It happens because
# some words are used as different parts of speech. For example, "stary"
# in Słowosieć is defined as a noun and as an adjective. To make sure that
# every lemma returns only one synset we defined dictionary that points
# a more commonly used part of speech. There are a few more words added that
# have their plural form defined in SimLex data. In Słowosieć these words are defined
# in singular.
synsets_ids_for_words_with_multiple_pos = {
    "stary": 9965,
    "nowy": 9968,
    "obłąkany": 417149,
    "miły": 9347,
    "winny": 9099,
    "młody": 1733,
    "chory": 356,
    "dorosły": 6336,
    "gitara": 921,
    "żal": 19965,
    "brać": 67697,
    "meble": 7242,
    "mężczyźni": 6709,
    "nasiona": 4722,
    "ubrania": 3289,
    "wyobrażać": 3977,
    "pojawiać": 4051,
    "modlić": 1689
}


def load_plwn_data():
    wn = plwn.load_default()
    synsets = wn.synsets()
    return wn, synsets


def get_synsets_from_lemma(all_synsets, lemma: str, use_dict: bool):
    if not use_dict or (use_dict and synsets_ids_for_words_with_multiple_pos.get(lemma) is None):
        all_appropriate_synsets = [(all_synsets[syn_idx], all_synsets[syn_idx].lexical_units[unit_idx].variant)
                   for syn_idx in range(len(all_synsets))
                   for unit_idx in range(len(all_synsets[syn_idx].lexical_units))
                   if all_synsets[syn_idx].lexical_units[unit_idx].lemma == lemma
                   and not str(all_synsets[syn_idx].lexical_units[unit_idx].pos).endswith("_en")]
        if len(all_appropriate_synsets) == 0:
            return None
        else:
            syn = min(all_appropriate_synsets, key=lambda x: x[1])[0]
    else:
        syn = [syn for syn in all_synsets if syn.id == synsets_ids_for_words_with_multiple_pos[lemma]][0]

    return syn
