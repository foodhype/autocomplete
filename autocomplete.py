import cPickle
import curses
from curses import wrapper
import heapq
import os.path
import re
import sys
import textwrap


def read_words():
    with open("words") as dict_file:
        words = [word.lower().rstrip() for word
                in dict_file.readlines()
                if re.match("^[A-Za-z]+$", word)]

        return words


def build_trie(words):
    trie = {}
    for word in words:
        current = trie
        for c in word:
            if c not in current:
                current[c] = {}
            current = current[c]

    return trie


def build_bktree(words):
    root = (words[0], 0)
    bk_tree = {root: {}}
    for i in xrange(1, len(words)):
        bktree_add(bk_tree, root, words[i])
    return bk_tree


def bktree_add(bk_tree, root, word):
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


def autocomplete(prefix, words):
    return closest_matches(prefix, words)


def edit_distance(prefix, word):
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


def nclosest_matches(count, prefix, words):
    #proximity = lambda word: edit_distance(prefix, word)
    return heapq.nsmallest(count, words, key=lambda word: edit_distance(prefix, word))


def main(stdscr):
    curses.cbreak()
    stdscr.keypad(True)
    bk_tree = None
    if os.path.isfile("bk_tree.p"):
        stdscr.addstr("Loading serialized BK-tree from file...\n")
        bk_tree = cPickle.load(open("bk_tree.p", "rb"))
    else:
        stdscr.addstr("Reading words from file...\n")
        stdscr.refresh()
        words = read_words()
        stdscr.addstr("Building BK-tree...\n")
        stdscr.refresh()
        bk_tree = build_bktree(words)
        stdscr.addstr("Dumping serialized BK-tree to file...\n")
        stdscr.refresh()
        cPickle.dump(bk_tree, open("bk_tree.p", "wb"))

    prefix = ""
    root = bk_tree.keys()[0]

    message = "\n".join(["Auto-complete ready.",
            "Start typing a word...",
            "Ctrl+D to exit."]) + "\n"
    stdscr.addstr(message)

    while True:
        c = stdscr.getch()
        if c == 4 or c == 3:
            break
        if c == ord("\n"):
            prefix = ""
        else:
            prefix += chr(c)

        matches = bktree_search(bk_tree[root], root, prefix)

        stdscr.clear()
        stdscr.addstr(message)
        stdscr.addstr(prefix + "\n")
        stdscr.addstr(str(nclosest_matches(5, prefix, matches)) + "\n")


wrapper(main)
