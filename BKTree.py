from util import edit_distance


class BKTree(object):
    def __init__(self, words):
        """Build a tree from list of words."""
        self.root = (words[0], 0)
        self.tree = {self.root: {}}
        for i in xrange(1, len(words)):
            self.__add(self.tree, self.root, words[i])
        
    def __add(self, tree, root, word):
        """Add a word."""
        distance = edit_distance(root[0], word)
        collision = False
        for (child, child_distance) in tree[root].keys():
            if distance == child_distance:
                self.__add(tree[root], (child, child_distance), word)
                collision = True
                break
        if not collision:
            tree[root][(word, distance)] = {}

    def search(self, prefix, tolerance=2, tree=None, root=None, matches=None):
        """Search for words within a given edit distance of prefix."""
        # TODO: Number of arguments can be reduced by defining BKTree
        # recursively (i.e. root and tree args shouldn't be necessary).
        if root is None:
            root = self.root
        if tree is None:
            tree = self.tree[self.root]
        if matches is None:
            matches = set()

        prefix_distance = edit_distance(prefix, root[0])
        if prefix_distance <= tolerance:
            matches.add(root[0])

        for word, distance in tree.keys():
            if abs(prefix_distance - distance) <= tolerance:
                child = (word, distance)
                self.search(prefix, tolerance, tree[child], child, matches)

        return matches

    def __str__(self):
        return self.__format_tree(self.tree, self.root, 0)

    def __format_tree(self, tree, root, indentation):
        """Format tree for printing."""
        formatted =  " " * indentation + str(root) + "\n"
        if root in tree:
            subtree = tree[root]
            for word, distance in subtree.keys():
                formatted += self.__format_tree(
                        subtree, (word, distance), indentation + 2)

        return formatted
