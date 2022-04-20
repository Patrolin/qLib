from qLib.math import log

def string_similarity(filter: str, option: str) -> float:
    '''return a string similarity of value, option in O(len(filter) + len(option))'''
    length_sum = len(filter) + len(option)
    if length_sum == 0: return 1.0

    counts = dict()
    for char in filter:
        counts[char] = counts[char] + 1 if (char in counts) else 1
    matches, bad_mismatches, okay_mismatches = 0, 0, 0
    for char in option:
        if (char in counts):
            if (counts[char] > 0):
                counts[char] -= 1
                matches += 1
            else:
                okay_mismatches += 1
        else:
            bad_mismatches += 1
    for count in counts.values():
        bad_mismatches += count

    if (bad_mismatches + okay_mismatches) == 0: return 1.0
    return (2 * matches / length_sum) / log(1 + bad_mismatches + okay_mismatches / 2)

def filter_options(filter: str, options: list[str], cutoff: float = 0.1) -> list[str]:
    '''return options filtered and sorted by string_similarity() in O((len(filter) + len(option)) * len(options))'''
    acc = []
    acc_similarities = dict()
    for option in options:
        similarity = string_similarity(filter, option)
        if similarity >= cutoff:
            acc.append(option)
            acc_similarities[option] = similarity
    return sorted(acc, key=lambda option: acc_similarities[option], reverse=True)

# other options:
# https://handwiki.org/wiki/Gestalt_Pattern_Matching
# https://handwiki.org/wiki/Damerau–Levenshtein_distance
