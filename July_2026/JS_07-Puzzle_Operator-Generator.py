def explore(score, height, move_numbers, index=0, path=()):
    if index == len(move_numbers):
        yield score, path  # all the moves checked therefore return the path now
        return

    N = move_numbers[index]

    # Same floor : Always legal
    yield from explore(score + N, height, move_numbers, index+1, path+('+',))

    # Up move : Only legal if currently at height 1
    if height == 1:
        yield from explore(score * N, 2, move_numbers, index+1, path+('x',))

    # Down move : Only legal if currently at height 2, and only if it divides evenly
    if height == 2 and score % N == 0:
        yield from explore(score // N, 1, move_numbers, index+1, path+('/',))

results = list(explore(750, 1, [47,48,49,50,51,52,53]))

# Distinct reachable values only:
values = {r[0] for r in results}

# Which paths hit a specific target:
#[r for r in results if r[0] == target]

for score, path in sorted(results):
    print(f"{score}: {path}")