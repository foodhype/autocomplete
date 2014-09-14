import heapq


def autocomplete(prefix, words, count=5):
    proximity = lambda word: edit_distance(prefix, word)
    return heapq.nsmallest(count, words, key=proximity)


def build_bktree(words):
    """Build a BK-tree from list of words."""
    root = (words[0], 0)
    bk_tree = {root: {}}
    for i in xrange(1, len(words)):
        bktree_add(bk_tree, root, words[i])
    return bk_tree


def bktree_add(bk_tree, root, word):
    """Add a word to a BK-tree."""
    distance = edit_distance(root[0], word)
    collision = False
    for (child, child_distance) in bk_tree[root].keys():
        if distance == child_distance:
            bktree_add(bk_tree[root], (child, child_distance), word)
            collision = True
            break
    if not collision:
        bk_tree[root][(word, distance)] = {}


def bktree_search(bk_tree, root, prefix, tolerance=2, matches=None):
    """Search BK-tree for words within a given edit distance of prefix."""
    if matches is None:
        matches = []
    distance =  edit_distance(prefix, root[0])
    if distance <= tolerance:
        matches.append(root[0])

    for word, root_distance in bk_tree.keys():
        if distance - tolerance <= root_distance <= distance + tolerance:
            child = (word, root_distance)
            bktree_search(bk_tree[child], child, prefix, tolerance, matches)

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
