import heapq


def autocomplete(suggest_tree, bktree, prefix, count=5):
    completion_frequencies = suggest_tree.search(prefix)
    if completion_frequencies:
        freq = lambda completion: completion_frequencies[completion]
        proximity = lambda completion: completion_proximity_score(
                prefix, completion)
        selection_criteria = lambda completion: (
                freq(completion), proximity(completion))
        completions = completion_frequencies.keys()
        return heapq.nlargest(count, completions, key=selection_criteria)
    else:
        matches = bktree.search(prefix)
        proximity = lambda completion: bktree.edit_distance(prefix, completion)
        return heapq.nsmallest(count, matches, key=proximity)

    
def completion_proximity_score(prefix, completion):
    """Calculate a score based on suffix length where a shorter length always
    yields a higher score."""
    if prefix == completion:
        return float("inf")
    else:
        return 1.0 / float(len(completion))
