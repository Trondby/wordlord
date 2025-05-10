import math
import sys

trie = dict()

end_char = '.'

def load_dictionary(filename):
    print('Loading words from ' + filename, end='...')
    with open(filename, 'r') as f:
        count = 0
        for word in f.readlines():
            count += 1
            node = trie
            for letter in word.strip():
                if letter not in node:
                    node[letter] = dict()
                node = node[letter]
            node[end_char] = dict()
    print(' Loaded ' + str(count) + ' words')


def is_word(word):
    node = trie
    for c in word:
        if c not in node:
            return False
        node = node[c]
    return True


def find_words(letters, node, words, current_word):
    if end_char in node:
        words.append(current_word)
    for letter in letters:
        if letter in node:
            find_words(letters, node[letter], words, current_word + letter)

   
def list_words(letters):
    words = list()
    find_words(letters, trie, words, '')
    return words

    
def unique_letters(letters):
    unique = dict()
    for letter in letters:
        unique[letter] = True
    return unique


def is_pangram(word, letters):
    for letter in letters:
        if letter not in word:
            return False
    return True


def print_pangrams(words, letters):
    for word in words:
        if is_pangram(word, letters):
            print(word.upper(), end=' ')
    print()


def obfuscate_word(word, visible_letters):
    censored_word = ''
    for c in word:
        if c in visible_letters:
            censored_word += c
        else:
            censored_word += '*'
    return censored_word


def spelling_bee(letters, hint_limit=math.inf, hint_letters=None):
    valid_letters = unique_letters(letters)
    if len(valid_letters) is not len(letters):
        print('warning: duplicate letters')
    if len(valid_letters) != 7:
        print('warning: number of letters is ' + str(len(valid_letters)) + ' not 7')
    words = list_words(valid_letters)
    words = sorted(list(filter(lambda word: len(word) >= 4 and letters[0] in word, words)))
    print(len(words))
    if hint_limit < math.inf:
        words = [word[:hint_limit] for word in words]
    if hint_letters:
        words = [obfuscate_word(word, hint_letters) for word in words]
    print(words)
    print_pangrams(words, valid_letters)


def print_words(letters):
    letters = unique_letters(letters)
    words = list_words(letters)
    print(len(words))
    print(words)
    print_pangrams(words, letters)


def main():
    default_dictionary_file = 'dictionary.txt'
    dictionary_file = sys.argv[1] if len(sys.argv) > 1 else default_dictionary_file
    load_dictionary(dictionary_file)
    for line in sys.stdin:
        line = line.strip().split()
        if not line:
            continue
        letters = line[0]
        hint_limit = math.inf
        hint_letters = None
        if len(line) > 1:
            if line[1].isdigit():
                hint_limit = int(line[1])
            else:
                hint_letters = unique_letters(line[1])
        if len(line) > 2:
            if line[2].isdigit():
                hint_limit = int(line[2])
            else:
                hint_letters = unique_letters(line[2])
        spelling_bee(letters, hint_limit, hint_letters)


if __name__ == '__main__':
    main()
