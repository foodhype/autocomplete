import autocomplete
from BKTree import BKTree
import cPickle
import curses
from curses import wrapper
import os.path
import re
from SuggestTree import SuggestTree


def read_words(filename):
    """Read newline-separated words from file."""
    words = []
    with open(filename) as word_file:
        for word in word_file.readlines():
            if re.match("^[a-z]+$", word):
                words.append(word.lower().rstrip())

    return words


def dump(obj, filename):
    """Pickle object and dump to file."""
    cPickle.dump(obj, open(filename, "wb"))


def load(filename):
    """Load pickled object from file."""
    return cPickle.load(open(filename, "rb"))


def gen_suggest_tree(words):
    """Generate SuggestTree from words."""
    suggest_tree = SuggestTree()
    for word in words:
        suggest_tree.add(word)

    return suggest_tree


def gen_bktree(words):
    """Generate BKTree from words."""
    return BKTree(words)


def run_autocomplete_console(stdscr, suggest_tree, bktree):
    """Run console for testing basic auto-complete functionality."""
    prefix = ""
    message = "\n".join(["Auto-complete ready.",
            "Start typing a word...",
            "Ctrl+D to exit."]) + "\n"
    stdscr.addstr(message)

    while True:
        c = stdscr.getch()
        if c == 3 or c == 4 or c == ord("\n"):
            break
        # KEY_BACKSPACE constant is OS-dependent (i.e. unreliable).
        elif c == curses.KEY_BACKSPACE or c == curses.KEY_DC:
            prefix = "" if len(prefix) <= 1 else prefix[:-1]
        elif 0 <= c < 128:
            prefix += chr(c)
        else:
            continue

        stdscr.clear()
        stdscr.addstr(message)
        if len(prefix) >= 1:
            top_matches = autocomplete.autocomplete(suggest_tree, bktree, prefix)
            stdscr.addstr(prefix + "\n")
            stdscr.addstr(str(top_matches) + "\n")
        stdscr.refresh()


def main(stdscr):
    curses.cbreak()
    stdscr.keypad(True)

    suggest_tree = None
    bktree = None
    suggest_tree_filename = "suggest_tree.p"
    bktree_filename = "bktree.p"
    words_filename = "words"
    if (os.path.isfile(suggest_tree_filename) and
            os.path.isfile(bktree_filename)):
        stdscr.addstr("Loading serialized SuggestTree and BKTree from "
                "file...\n")
        stdscr.refresh()
        suggest_tree = load(suggest_tree_filename)
        bktree = load(bktree_filename)
    else:
        stdscr.addstr("Building SuggestTree and BKTree...\n")
        stdscr.refresh()
        words = read_words(words_filename)
        suggest_tree = gen_suggest_tree(words)
        bktree = gen_bktree(words)
        dump(suggest_tree, suggest_tree_filename)
        dump(bktree, bktree_filename)

    run_autocomplete_console(stdscr, suggest_tree, bktree)


wrapper(main)
