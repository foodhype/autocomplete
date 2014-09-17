import heapq
from util import edit_distance


def autocomplete(suggest_tree, bktree, prefix, count=5):
    """Suggest top completions for a prefix given a SuggestTree and BKTree.
    
    Completions for a given prefix are weighted primarily by their weight in the 
    suggest tree, and secondarily by their Levenshtein distance to words in the
    BK-tree (where nearby words are weighted higher)."""
    completion_weights = suggest_tree.completion_weights(prefix)
    if completion_weights:
        weight = lambda completion: completion_weights[completion]
        proximity = lambda completion: completion_proximity_score(
                prefix, completion)
        selection_criteria = lambda completion: (
                weight(completion), proximity(completion))
        completions = completion_weights.keys()
        return heapq.nlargest(count, completions, key=selection_criteria)
    else:
        matches = bktree.search(prefix)
        proximity = lambda completion: edit_distance(prefix, completion)
        return heapq.nsmallest(count, matches, key=proximity)

    
def completion_proximity_score(prefix, completion):
    """Calculate a score based on suffix length where a shorter length always
    yields a higher score."""
    if prefix == completion:
        return float("inf")
    else:
        return 1.0 / float(len(completion))
