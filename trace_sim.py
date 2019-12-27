import math
from typing import Dict, List, Any


def compare(alpha: float, beta: float, gamma: float, trace1: List[Any], trace2: List[Any], idf: Dict[Any, float]):

    weights1 = _weights(alpha, beta, gamma, trace1, idf)
    weights2 = _weights(alpha, beta, gamma, trace2, idf)

    max_dist = sum(weights1) + sum(weights2)

    return 0 if max_dist == 0 else 1 - _dist(trace1, weights1, trace2, weights2) / max_dist


def _weights(alpha: float, beta: float, gamma: float, trace: List[Any], idf: Dict[Any, float]) -> List[float]:

    lws = [1.0 / (1 + i) ** alpha for i in range(len(trace))]
    gws = [1.0 / (1.0 + math.exp(-beta * idf[frame] + gamma)) for frame in trace]

    return [lw * gw for lw, gw in zip(lws, gws)]


def _dist(trace1: List, weights1: List, trace2: List, weights2: List) -> float:

    matrix = [[0.0 for _ in range(len(trace1) + 1)] for _ in range(len(trace2) + 1)]

    prev_column = matrix[0]

    for i in range(len(trace1)):
        prev_column[i + 1] = prev_column[i] + weights1[i]

    if len(trace1) == 0 or len(trace2) == 0:
        return 0.0

    curr_column = matrix[1]

    for i2 in range(len(trace2)):

        frame2 = trace2[i2]
        weight2 = weights2[i2]

        curr_column[0] = prev_column[0] + weight2

        for i1 in range(len(trace1)):

            frame1 = trace1[i1]
            weight1 = weights1[i1]

            if frame1 == frame2:
                curr_column[i1 + 1] = prev_column[i1]
            else:
                change = weight1 + weight2 + prev_column[i1]
                remove = weight2 + prev_column[i1 + 1]
                insert = weight1 + curr_column[i1]

                curr_column[i1 + 1] = min(change, remove, insert)

        if i2 != len(trace2) - 1:
            prev_column = curr_column
            curr_column = matrix[i2 + 1]

    return curr_column[-1]
