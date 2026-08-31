# Also See Hand_Work.pdf as the Support Material

def color(q, r):
    return (q - r) % 3


def white_neighbors(q, r):
    c = color(q, r)
    if c == 0:
        return (q + 1, r), (q, r - 1), (q - 1, r + 1)
    else:
        return (q - 1, r), (q + 1, r - 1), (q, r + 1)


def BFS(start, Max_Steps):
    State = {start: 1}
    return_count = []
    for step in range(1, Max_Steps + 1):
        new_State = {}
        for pos, count in State.items():
            for nb in white_neighbors(*pos):
                new_State[nb] = new_State.get(nb, 0) + count
        return_count.append(new_State.pop(start, 0))
        State = new_State
    return return_count


if __name__ == "__main__":
    Max = 20
    home = (0, 0)
    return_Count = BFS(home, Max)
    print(return_Count)

    cumNum = sum(c * 3 ** (Max - i) for i, c in enumerate(return_Count, start=1))
    deNum = 3 ** Max
    p  = (deNum - cumNum) / deNum
    print(f'p = {deNum - cumNum}/{deNum} = {p}')
