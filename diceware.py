"""Module for generating passphrases by simulating dice rolls"""
import os.path
import secrets

_DICE_SIDES = 6
_WORDLIST_DIR = './wordlist'

_WORDLISTS = {'en': 'eff_large_wordlist.txt', 'sv': 'diceware-sv.txt'}


def new_passphrase(size=6, dices=5, wordlist='en'):
    """
    Generate passphrase. Keyword arguments:
    wordlist: dictionary to chose words from (default 'en')
    size: number of words in the passphrase (default 6)
    dices: number of dices to roll dices (default 5)
    """
    if not _WORDLISTS.get(wordlist):
        return []

    wordlist_path = os.path.join(_WORDLIST_DIR, _WORDLISTS[wordlist])
    with open(wordlist_path, encoding='utf-8') as wordlist_file:
        return numbers_to_words(wordlist_file, *generate_numbers(size, dices))


def generate_numbers(numbers, dices):
    """
    Generate numbers by rolling dices. Each number will have
    dices digits. Each digit is in range [1, _DICE_SIDES]
    numbers: how many numbers will be generated
    dices: number of dices that are used for generating numbers
    """
    word_ids = []
    for _ in range(numbers):
        word_id = 0
        for _ in range(dices):
            word_id = word_id * 10 + roll_dice()

        word_ids.append(word_id)
    return word_ids


def roll_dice():
    """Simulate a single roll of the dice. Returns number in range [1, _DICE_SIDES]"""
    return secrets.randbelow(_DICE_SIDES) + 1


def numbers_to_words(wordlist, *numbers):
    """
    Map dice numbers to words from the wordlist
    wordlist: file descriptor to the dictionary containing dice numbers and words
    numbers: dice numbers to map to words.
    Returns a list where each input number is mapped to the dictionary word. If
    there were no input numbers empty list is returned
    """
    if not numbers:
        return []

    result = {}
    sorted_ids = sorted(set(numbers))

    for line in wordlist:
        if line.startswith(str(sorted_ids[0])):
            word = line.split()[1]
            result[sorted_ids[0]] = word
            sorted_ids.pop(0)
            if not sorted_ids:
                break

    return [result[k] for k in numbers]


if __name__ == '__main__':
    print(new_passphrase(6, wordlist='en'))
