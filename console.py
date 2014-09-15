import autocomplete
import cPickle
import curses
from curses import wrapper
import os.path
import re


def read_words(filenames):
    """Read newline-separated words from file."""
    for filename in filenames:
        words = []
        with open(filename) as word_file:
            words += [word.lower().rstrip() for word
                in word_file.readlines()
                if re.match("^[a-z]+$", word)]

        return words


def load_bk_tree(filename):
    """Load pickled BK-tree from file."""
    return cPickle.load(open(filename, "rb"))


def gen_bk_tree(words):
    """Generate BK-tree from words."""
    return autocomplete.build_bktree(words)


def dump_bk_tree(bk_tree, filename):
    """Pickle BK-tree and dump to file."""
    cPickle.dump(bk_tree, open(filename, "wb"))


def load_trie(filename):
    """Load pickled BK-tree from file."""
    return cPickle.load(open(filename, "rb"))


def gen_trie(words):
    """Generate BK-tree from words."""
    return autocomplete.build_trie(words)


def dump_trie(trie, filename):
    """Pickle BK-tree and dump to file."""
    cPickle.dump(trie, open(filename, "wb"))


def run_autocomplete_console(stdscr, trie, bk_tree):
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

        top_matches = autocomplete.autocomplete(trie, bk_tree, prefix)

        stdscr.clear()
        stdscr.addstr(message)
        if len(prefix) >= 1:
            stdscr.addstr(prefix + "\n")
            stdscr.addstr(str(top_matches) + "\n")
        stdscr.refresh()


def main(stdscr):
    curses.cbreak()
    stdscr.keypad(True)

    trie = None
    bk_tree = None
    trie_filename = "trie.p"
    bktree_filename = "bk_tree.p"
    words_filenames = ["words", "connectives"]
    if os.path.isfile(trie_filename) and os.path.isfile(bktree_filename):
        stdscr.addstr("Loading serialized Trie and BK-tree from file...\n")
        stdscr.refresh()
        trie = load_trie(trie_filename)
        bk_tree = load_bk_tree(bktree_filename)
    else:
        stdscr.addstr("Building Trie and BK-tree...\n")
        stdscr.refresh()
        words = read_words(words_filenames)
        trie = gen_trie(words)
        bk_tree = gen_bk_tree(words)
        dump_trie(trie, trie_filename)
        dump_bk_tree(bk_tree, bktree_filename)

    run_autocomplete_console(stdscr, trie, bk_tree)


wrapper(main)
