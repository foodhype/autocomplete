autocomplete
============

Python implementation of auto-complete using a Trie and BK tree.

Future enhancements:
-The trie would be much more time- and space-efficient if each node stored indexes into a table of completions rather than storing completions at the node for every prefix of the completion.
-Auto-complete would produce better results if it re-weighted completions after some kind of selection.
