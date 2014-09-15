from collections import Counter
import heapq


def autocomplete(trie, bk_tree, prefix, count=5):
    for c in prefix:
        if c in trie.children.keys():
            trie = trie.children[c]
        else:
            matches = bktree_search(bk_tree, prefix)
            proximity = lambda completion: edit_distance(prefix, completion)
            return heapq.nsmallest(count, matches, key=proximity)

    freq = lambda completion: trie.completion_frequencies[completion]
    proximity = lambda completion: completion_proximity_score(
            prefix, completion)
    selection_criteria = lambda completion: (
            freq(completion), proximity(completion))
    completions = trie.completion_frequencies.keys()

    return heapq.nlargest(count, completions, key=selection_criteria)


def build_trie(words):
    """Build a Trie from list of words."""
    trie = Trie()
    for word in words:
        trie_add(trie, word)

    return trie


def trie_add(trie, word):
    """Add a word to a Trie."""
    current = trie
    for c in word:
        if c not in current.children.keys():
            current.children[c] = Trie()
        current = current.children[c]
        current.completion_frequencies[word] += 1


class Trie(object):
    def __init__(self):
        self.children = {}
        self.completion_frequencies = Counter()


def build_bktree(words):
    """Build a BK-tree from list of words."""
    root = (words[0], 0)
    bk_tree = {root: {}}
    for i in xrange(1, len(words)):
        bktree_add(bk_tree, words[i])

    return bk_tree


def bktree_add(bk_tree, word, root=None):
    """Add a word to a BK-tree."""
    if root is None:
        root = bk_tree.keys()[0]
    distance = edit_distance(root[0], word)
    collision = False
    for (child, child_distance) in bk_tree[root].keys():
        if distance == child_distance:
            bktree_add(bk_tree[root], word, (child, child_distance))
            collision = True
            break
    if not collision:
        bk_tree[root][(word, distance)] = {}


def bktree_search(bk_tree, prefix, tolerance=2, root=None, matches=None):
    """Search BK-tree for words within a given edit distance of prefix."""
    if root is None:
        root = bk_tree.keys()[0]
    if matches is None:
        matches = []

    root_distance = edit_distance(prefix, root[0])
    if root_distance <= tolerance:
        matches.append(root[0])

    for word, distance in bk_tree.keys():
        if root_distance - tolerance <= distance <= root_distance + tolerance:
            child = (word, distance)
            bktree_search(bk_tree[child], prefix, tolerance, child, matches)

    return matches


def edit_distance(prefix, word):
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


def completion_proximity_score(prefix, completion):
    """Calculate a score based on suffix length where a shorter length always
    yields a higher score."""
    if prefix == completion:
        return float("inf")
    else:
        return 1.0 / float(len(completion))
