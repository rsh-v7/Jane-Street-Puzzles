start = (1, 1)
towers = {
    (1, 1), (3, 2), (5, 3), (1, 5), (5, 6), (4, 8)
}
non_towers = {
    (2, 1), (3, 1), (4, 1),
    (1, 2), (2, 2), (4, 2), (5, 2),
    (1, 3), (2, 3), (4, 3), (6, 3), (7, 3),
    (1, 4), (2, 4), (5, 4), (6, 4), (7, 4),
    (6, 5),
    (1, 6), (4, 6), (6, 6),
    (1, 7), (3, 7), (4, 7), (5, 7),
    (1, 8), (2, 8), (3, 8), (5, 8), (6, 8), (8, 8)
}
region_candidates = {
    1: [(7, 8), (8, 7), (8, 6)],
    2: [(2, 7), (3, 6)],
    3: [(6, 7), (7, 7), (7, 6), (7, 5), (8, 5)],
    4: [(2, 6), (2, 5), (3, 5), (3, 4), (3, 3)],
    5: [(4, 4), (4, 5), (5, 5)],
    6: [(8, 4), (8, 3), (8, 2), (8, 1), (7, 1)],
    7: [(7, 2), (6, 2), (6, 1), (5, 1)]
}
known_scores = {
    3: (7, 3),
    6: (5, 4),
    9: (4, 6),
    12: (1, 5),
    15: (6, 8),
    18: (4, 3),
    25: (6, 6),
    32: (6, 3),
    39: (2, 4),
    46: (2, 3),
    53: (8, 8)
}
known_ops = [ # generated via Puzzle Operator Generator
    '+', '+', '/',
    '+', '+', '+',
    'x', '/', '+',
    '+', '+', 'x',
    '+', '+', '/',
    '+', '+', '+',
    '+', '+', 'x', '+', '+', '/', '+',
    '+', '+', '+', '+', 'x', '/', '+',
    'x', '/', '+', '+', '+', '+', '+',
    '+', '+', '+', '+', '+', '+', '+',
    '+', '+', '+', '+', '+', '+', '+'
]
# print(len(known_ops))

known_height = {}
for t in towers: known_height[t] = 2
for t in non_towers: known_height[t] = 1
# for cells, height in known_height.items():
#     print(f"Cell {cells} height: {height}")

cell_to_region = {}
for rid, cells in region_candidates.items():
    for sq in cells:
        cell_to_region[sq] = rid
# print(cell_to_region)

same_height_offsets = [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]
height_change_offsets = [(0, 2), (0, -2), (2, 0), (-2, 0)]


def on_board(pos):
    r, c = pos
    return 1 <= r <= 8 and 1 <= c <= 8


def height_of(cell, tower_assigned):
    if cell in known_height:
        return known_height[cell]
    region = cell_to_region.get(cell)
    if region is None or region not in tower_assigned:
        return None
    return 2 if tower_assigned[region] == cell else 1


def is_complete(tower_assigned, visited):
    return set(tower_assigned.values()) <= visited and set(tower_assigned.keys()) == set(region_candidates.keys())


def search(position, move_num, score,
    tower_assigned, visited, path, score_list):
    if known_scores.get(move_num - 1) not in (None, position):
        return []

    if is_complete(tower_assigned, visited) and move_num > max(known_scores.keys()):
        return [(dict(tower_assigned), list(path), list(score_list))]

    all_results = []
    ops_to_try = [known_ops[move_num - 1]] if move_num <= len(known_ops) else ['+', 'x', '/']
    current_height = height_of(position, tower_assigned)

    for op in ops_to_try:
        if op == '/' and score % move_num != 0:
            continue
        needed_height = current_height if op == '+' else (2 if op == 'x' else 1)
        new_score = {'+': score + move_num, 'x': score * move_num, '/': score // move_num}[op]
        offsets = same_height_offsets if op == '+' else height_change_offsets

        for dr, dc in offsets:
            npos = (position[0] + dr, position[1] + dc)
            if not on_board(npos) or npos in visited:
                continue
            region = cell_to_region.get(npos)
            if npos in known_height or (region is not None and region in tower_assigned):
                if height_of(npos, tower_assigned) == needed_height:
                    results = search(npos, move_num + 1, new_score, tower_assigned, visited | {npos}, path + [npos], score_list + [(npos, new_score)])
                    all_results.extend(results)
            elif region is not None:
                for candidate in region_candidates[region]:
                    if (2 if candidate == npos else 1) == needed_height:
                        tower_assigned[region] = candidate
                        results = search(npos, move_num + 1, new_score, tower_assigned, visited | {npos}, path + [npos], score_list + [(npos, new_score)])
                        all_results.extend(results)
                        del tower_assigned[region]
    return all_results


results = search(start, 1, 0, {}, {start}, [start], [])
print(f"Found {len(results)} solution(s):\n")
for i, (assignment, path, score_list) in enumerate(results, 1):
    print(f"Solution {i}:")
    print(f"  Assignment: {assignment}")
    print(f"  Path: {path}")
    print(f"  Scores by cell:")
    for cell, score in score_list:
        print(f"    {cell} → {score}")
    print()