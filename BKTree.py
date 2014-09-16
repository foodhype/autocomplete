class BKTree(object):
    def __init__(self, words):
        """Build a BK-tree from list of words."""
        self.root = (words[0], 0)
        self.tree = {self.root: {}}
        for i in xrange(1, len(words)):
            self.__add(self.tree, self.root, words[i])
        
    def __add(self, tree, root, word):
        """Add a word."""
        distance = self.edit_distance(root[0], word)
        collision = False
        for (child, child_distance) in tree[root].keys():
            if distance == child_distance:
                self.__add(tree[root], (child, child_distance), word)
                collision = True
                break
        if not collision:
            tree[root][(word, distance)] = {}

    def search(self, prefix, tolerance=2, tree=None, root=None, matches=None):
        """Search BK-tree for words within a given edit distance of prefix."""
        if tree is None:
            tree = self.tree
        if root is None:
            root = self.root
        if matches is None:
            matches = set()
        root_distance = self.edit_distance(prefix, root[0])
        if root_distance <= tolerance:
            matches.add(root[0])

        for word, distance in tree.keys():
            if root_distance - tolerance <= distance <= root_distance + tolerance:
                child = (word, distance)
                self.search(prefix, tolerance, tree[child], child, matches)

        return matches

    def edit_distance(self, prefix, word):
        """Calculate edit distance between prefix and word."""
        dp = [[0 for _ in xrange(len(word) + 1)] for _ in xrange(len(prefix) + 1)]
        for i in xrange(1, len(prefix) + 1):
            dp[i][0] = i
        for i in xrange(1, len(word) + 1):
            dp[0][i] = i
        for i in xrange(1, len(prefix) + 1):
            for j in xrange(1, len(word) + 1):
                delete_min = dp[i - 1][j] + 1
                insert_min = dp[i][j - 1] + 1
                replacement_min = None
                if prefix[i - 1] == word[j - 1]:
                    replacement_min = dp[i - 1][j - 1]
                else:
                    replacement_min = dp[i - 1][j - 1] + 1

                dp[i][j] = min(delete_min, insert_min, replacement_min)

        return dp[len(prefix)][len(word)] 
