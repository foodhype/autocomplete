import autocomplete
import cPickle
import curses
from curses import wrapper
import os.path
import re


def read_words(filename):
    """Read newline-separated words from file."""
    with open(filename) as word_file:
        words = [word.lower().rstrip() for word
            in word_file.readlines()
            if re.match("^[A-Za-z]+$", word)]

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


def run_autocomplete_console(stdscr, bk_tree):
    """Run console for testing basic auto-complete functionality."""
    prefix = ""
    root = bk_tree.keys()[0]
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

        matches = autocomplete.bktree_search(bk_tree[root], root, prefix)
        top_matches = autocomplete.autocomplete(prefix, matches)

        stdscr.clear()
        stdscr.addstr(message)
        if len(prefix) >= 1:
            stdscr.addstr(prefix + "\n")
            stdscr.addstr(str(top_matches) + "\n")
        stdscr.refresh()


def main(stdscr):
    curses.cbreak()
    stdscr.keypad(True)

    bk_tree = None
    filename = "bk_tree.p"
    if os.path.isfile(filename):
        stdscr.addstr("Loading serialized BK-tree from file...\n")
        stdscr.refresh()
        bk_tree = load_bk_tree(filename)
    else:
        stdscr.addstr("Building BK-tree...\n")
        stdscr.refresh()
        words = read_words(filename)
        bk_tree = gen_bk_tree(words)
        dump_bk_tree(bk_tree, filename)

    run_autocomplete_console(stdscr, bk_tree)


wrapper(main)
