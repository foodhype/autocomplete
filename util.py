"""util is a module containing utility functions for autocomplete."""


def edit_distance(string1, string2):
    """Calculate edit distance between string1 and string2."""
    distance = []
    for _ in xrange(len(string1) + 1):
        distance.append([0 for _ in xrange(len(string2) + 1)])
    
    for i in xrange(1, len(string1) + 1):
        distance[i][0] = i
    for i in xrange(1, len(string2) + 1):
        distance[0][i] = i
    
    for i in xrange(1, len(string1) + 1):
        for j in xrange(1, len(string2) + 1):
            delete_min = distance[i - 1][j] + 1
            insert_min = distance[i][j - 1] + 1
            replacement_min = None
            if string1[i - 1] == string2[j - 1]:
                replacement_min = distance[i - 1][j - 1]
            else:
                replacement_min = distance[i - 1][j - 1] + 1

            distance[i][j] = min(delete_min, insert_min, replacement_min)

    return distance[len(string1)][len(string2)]
