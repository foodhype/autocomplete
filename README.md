autocomplete
============

Python implementation of auto-complete using suggest tree and BK tree.

To run:
make run

See Makefile for other commands. 

What are suggest trees?

Suggest trees are tries where nodes keep track of word completions including a weight associated with each completion.

See: http://suggesttree.sourceforge.net/

My suggest tree implementation includes additional indexing for better space efficiency.

What are BK-trees?

In practice, BK Trees are mainly used to avoid computing Levenshtein distance for every word in a large set.

See: http://blog.notdot.net/2007/4/Damn-Cool-Algorithms-Part-1-BK-Trees

Possible future enhancements: (1) re-weighting completions after some form of user selection; (2) Using finite state automata rather than BK trees to make Levenshtein lookups even faster (based on http://blog.notdot.net/2010/07/Damn-Cool-Algorithms-Levenshtein-Automata); (3) completion based on sentence context or phonetics might be interesting (possibly using Google n-grams?).
