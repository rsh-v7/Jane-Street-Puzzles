# Also See Hand_Work.pdf as the Support Material

from fractions import Fraction

def color(q, r):
    return (q - r) % 3


def white_neighbors_ordered(q, r):
    c = color(q, r)
    if c == 0:
        return [(q, r - 1), (q - 1, r + 1), (q + 1, r)]
    else:
        return [(q - 1, r), (q, r + 1), (q + 1, r - 1)]


def hc_turn(pos, arrived_from, turn):
    nbrs = white_neighbors_ordered(*pos)
    i = nbrs.index(arrived_from)
    if turn == 'L':
        return nbrs[(i + 1) % 3], pos
    if turn == 'R':
        return nbrs[(i - 1) % 3], pos
    return arrived_from, pos  # 'B'


k4_rot = {'a': ('c', 'b', 'd'), 'b': ('d', 'a', 'c'), 'c': ('b', 'a', 'd'), 'd': ('c', 'a', 'b')}
def k4_turn(v, arrived_from, turn):
    lst = k4_rot[v]
    i = lst.index(arrived_from)
    if turn == 'L':
        return lst[(i + 1) % 3]
    if turn == 'R':
        return lst[(i - 1) % 3]
    return arrived_from  # 'B'


def joint_BFS(Max_Steps):
    home_hc = (0, 0)
    first_hc_pos = white_neighbors_ordered(*home_hc)[0]
    start = (('c', 'a'), first_hc_pos, home_hc)

    State = {start: Fraction(1)}
    p_detect = Fraction(0)

    for step in range(2, Max_Steps + 1):
        new_State = {}
        for (k4s, hc_pos, hc_from), weight in State.items():
            v, frm = k4s
            for turn in ('L', 'R', 'B'):
                nv = k4_turn(v, frm, turn)
                n_hc_pos, n_hc_from = hc_turn(hc_pos, hc_from, turn)
                w = weight * Fraction(1, 3)
                k4_home = (nv == 'a')
                hc_home = (n_hc_pos == home_hc)
                if k4_home ^ hc_home:
                    p_detect += w
                elif not (k4_home or hc_home):
                    key = ((nv, v), n_hc_pos, n_hc_from)
                    new_State[key] = new_State.get(key, Fraction(0)) + w
        State = new_State
    return p_detect, State


if __name__ == "__main__":
    p_Detect, remaining = joint_BFS(7777)
    print("p =", float(p_Detect), " \nremaining unresolved mass:", float(sum(remaining.values())))
