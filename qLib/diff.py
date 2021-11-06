from math import log
# https://handwiki.org/wiki/Gestalt_Pattern_Matching
# https://handwiki.org/wiki/Damerau–Levenshtein_distance

def string_similarity(a: str, b: str) -> float:
  '''return a string similarity of a, b in O(len(a) + len(b))'''
  length_sum = len(a) + len(b)
  if length_sum == 0: return 1.0

  counts = dict()
  for char in a:
    counts[char] = counts[char] + 1 if (char in counts) else 1
  matches, bad_mismatches, okay_mismatches = 0, 0, 0
  for char in b:
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
  #print(mismatches, a_mismatches, b_mismatches)
  return (2 * matches / length_sum) / log(1 + bad_mismatches + okay_mismatches / 2)

def match_options(value: str, options: list[str]) -> list[str]:
  acc = []
  acc_similarities = dict()
  for s in options:
    similarity = string_similarity(value, s)
    if similarity > 0.1:
      acc.append(s)
      acc_similarities[s] = similarity
  return sorted(acc, key=lambda s: acc_similarities[s])

if __name__ == '__main__':
  print(string_similarity('app', 'no'))
  print(string_similarity('app', 'orange'))
  print(string_similarity('app', 'pineapple'))
  print(string_similarity('app', 'apole'))
  print(string_similarity('app', 'apple'))
  print(match_options('app', [x for x in ['no', 'orange', 'pineapple', 'apole', 'apple']]))
  print()
  print(string_similarity('i', 'else'))
  print(string_similarity('i', 'while'))
  print(string_similarity('i', 'if'))
  print(match_options('i', [x for x in ['', 'if', 'else', 'while']]))
  print()
  print(string_similarity('whi', 'else'))
  print(string_similarity('whi', 'if'))
  print(string_similarity('whi', 'while'))
  print(match_options('whi', [x for x in ['', 'if', 'else', 'while']]))
  print()
  print(string_similarity('x', 'y'))
  print(string_similarity('x', 'y_index'))
  print(string_similarity('x', 'x_index'))
  print(string_similarity('x', 'x'))
  print(match_options('x', [x for x in ['', 'x', 'x_index', 'y', 'y_index']]))
  print()
  print(string_similarity('x_', 'y'))
  print(string_similarity('x_', 'y_index'))
  print(string_similarity('x_', 'x_index'))
  print(string_similarity('x_', 'x'))
  print(match_options('x_', [x for x in ['', 'x', 'x_index', 'y', 'y_index']]))
  print()
  print(string_similarity('x_index', 'y'))
  print(string_similarity('x_index', 'x'))
  print(string_similarity('x_index', 'y_index'))
  print(string_similarity('x_index', 'x_index'))
  print(match_options('x_index', [x for x in ['', 'x', 'x_index', 'y', 'y_index']]))
  print()
  print(string_similarity('y', 'x_index'))
  print(string_similarity('y', 'x'))
  print(string_similarity('y', 'y_index'))
  print(string_similarity('y', 'y'))
  print(match_options('y', [x for x in ['', 'x', 'x_index', 'y', 'y_index']]))
  print()
  print(string_similarity('y_', 'x'))
  print(string_similarity('y_', 'x_index'))
  print(string_similarity('y_', 'y_index'))
  print(string_similarity('y_', 'y'))
  print(match_options('y_', [x for x in ['', 'x', 'x_index', 'y', 'y_index']]))
