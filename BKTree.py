class BKTree(object):
    def __init__(self):
        """Build a BK-tree from list of words."""
        self.tree = {}
        
    def add(self, word, root=None):
        """Add a word."""
        if root is None:
            if self.tree:
                root = self.tree.keys()[0]
            else:
                self.root = (word, 0)
                self.tree = {root: {}}
        else:
            distance = self.edit_distance(root[0], word)
            collision = False
            for (child, child_distance) in self.tree[root].keys():
                if distance == child_distance:
                    bktree_add(self.tree[root], word, (child, child_distance))
                    collision = True
                    break
            if not collision:
                self.tree[root][(word, distance)] = {}


    def search(self, prefix, tolerance=2, root=None, matches=None):
        """Search BK-tree for words within a given edit distance of prefix."""
        if root is None:
            root = self.tree.keys()[0]
        if matches is None:
            matches = []

        root_distance = self.edit_distance(prefix, root[0])
        if root_distance <= tolerance:
            matches.append(root[0])

        for word, distance in self.tree.keys():
            if root_distance - tolerance <= distance <= root_distance + tolerance:
                child = (word, distance)
                self.search(self.tree[child], prefix, tolerance, child, matches)

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
