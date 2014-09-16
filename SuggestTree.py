from collections import Counter


class SuggestTree(object):
    def __init__(self):
        self.root = CompletionFrequencyTrie()
        self.completion_table = []
        self.inverted_index = {}
        self.last_index = 0

    def add(self, word):
        self.root.add(word, self.last_index)
        self.completion_table.append(word)
        self.inverted_index[word] = self.last_index
        self.last_index += 1

    def increment(self, word):
        if word in inverted_index:
            self.root.add(word, inverted_index[word])
        else:
            self.add(word) 

    def search(self, prefix):
        trie = self.root
        for c in prefix:
            if c in self.root.children.keys():
                trie = trie.children[c]
            else:
                return Counter()

        completion_frequencies = Counter()
        for completion_index, frequency in trie.completion_frequencies.items():
            completion = self.completion_table[completion_index]
            completion_frequencies[completion] = frequency

        return completion_frequencies


class CompletionFrequencyTrie():
    def __init__(self):
        self.children = {}
        self.completion_frequencies = Counter()

    def add(self, word, index):
        current = self
        for c in word:
            if c not in current.children.keys():
                current.children[c] = CompletionFrequencyTrie()
            current = current.children[c]
            current.completion_frequencies[index] += 1.0
