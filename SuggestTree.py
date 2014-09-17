from collections import Counter


class SuggestTree(object):
    def __init__(self):
        self.root = WeightedCompletionTrie()
        self.completion_table = []
        self.inverted_index = {}
        self.last_index = 0

    def add(self, word):
        """Add a word with a weight of 1 to tree if the it hasn't already
        been added."""
        if word not in self.inverted_index:
            self.root.add(word, self.last_index)
            self.completion_table.append(word)
            self.inverted_index[word] = self.last_index
            self.last_index += 1

    def increment(self, word):
        """Increment the weight of a word in the tree by one; if the word is
        not in the tree, add it with a weight of 1."""
        if word in self.inverted_index:
            self.root.add(word, self.inverted_index[word])
        else:
            self.add(word) 

    def completion_weights(self, prefix):
        """Get a map from prefix completions to their weights"""
        trie = self.root
        for letter in prefix:
            if letter in trie.children.keys():
                trie = trie.children[letter]
            else:
                return Counter()

        completion_weights = Counter()
        for completion_index, weight in trie.completion_weights.items():
            completion = self.completion_table[completion_index]
            completion_weights[completion] = weight

        return completion_weights


class WeightedCompletionTrie(object):
    def __init__(self):
        self.children = {}
        self.completion_weights = Counter()

    def add(self, word, index):
        """Add a word and its completion table index in the suggest tree."""
        current = self
        for letter in word:
            if letter not in current.children.keys():
                current.children[letter] = WeightedCompletionTrie()
            current = current.children[letter]
            current.completion_weights[index] += 1.0
