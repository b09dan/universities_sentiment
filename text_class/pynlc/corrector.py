from functools import lru_cache
from bisect import bisect_left
from Levenshtein import distance
from .hashable_list_wrapper import HashableListWrapper

def _index(container, value):
    """
    Locate the leftmost value exactly equal to x
    """
    i = bisect_left(container, value)
    if i != len(container) and container[i] == value:
        return i
    raise ValueError


def _contains(container, value):
    """
    Contains value exactly equal to x
    """
    try:
        _index(container, value)
        return True
    except ValueError:
        return False


def prepare_dictionary(words, first_letter_group=True):
    """
    Returns dictionary
    :param words: collection of strings
    :param first_letter_group: group to dictiionary by first letter?
    :return: dictionary
    :rtype: dict[str, list[str]]|list[str]
    """
    if not first_letter_group:
        result = list(words)
        result.sort()
        return result
    else:
        result = {}
        letters = set([word[0] for word in words])
        for letter in letters:
            result[letter] = []
        for word in words:
            result[word[0]].append(word)
        for letter in letters:
            result[letter].sort()
        return result


@lru_cache(maxsize=1000)
def _correct(word, words_to_search, min_correction_length, max_distance):
    assert len(word) > 0
    if _contains(words_to_search, word):
        return word
    if len(word) < min_correction_length:
        return None
    found_words = []
    found_distance = -1
    for iter_word in words_to_search:
        iter_distance = distance(word, iter_word)
        if len(found_words) == 0 or found_distance > iter_distance:
            found_words = [iter_word]
            found_distance = iter_distance
        elif found_distance == iter_distance:
            found_words.append(iter_word)
    if found_distance > max_distance:
        return None
    return found_words[0]


def correct(word, dictionary, min_correction_length=3, max_distance=4):
    """
    Correct word (if have mistake)
    :param word: word
    :type word: str
    :param dictionary: dictionary object : [firstLetter]->words \
      or just words. Words must be ordered.
    :type dictionary: dict[str, list[str]]|list[str]
    :param max_distance: maximum distance
    :type max_distance: int
    :return: word or None
    :rtype: str
    """
    if isinstance(dictionary, dict):
        words_to_search = dictionary[word[0]]
    else:
        words_to_search = dictionary
    return _correct(word, HashableListWrapper(words_to_search),
                    min_correction_length, max_distance)
