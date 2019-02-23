from collections import namedtuple

COLORS = [
    'W', # white
    'R', # red/pink
    'O', # orange
    'Y', # yellow
    'G', # green
    'P', # Purple
]
COLOR_INDS = dict((v, i) for i, v in enumerate(COLORS))

def color_inds(i):
    for _ in range(4):
        yield i % 6
        i = i // 6

def colors_to_num(color_list):
    i = 0
    for c in reversed(color_list):
        i = i * 6 + COLOR_INDS[c]

def colors(i):
    for x in color_inds(i):
        yield COLORS[x]

def match(i, j):
    """
    returns (red, white) count,
    where red is matches in color and position, 
    and white is a match in color but not position
    """
    red_count = 0

    # these are counts only of the items that are not exact matches
    i_colors = [0]*6
    j_colors = [0]*6

    for i_c, j_c in zip(color_inds(i), color_inds(j)):
        if i_c == j_c: 
            red_count += 1
        else:
            i_colors[i_c] += 1
            j_colors[j_c] += 1

    white_count = 0
    for i_c, j_c in zip(i_colors, j_colors):
        white_count += min(i_c, j_c)

    return (red_count, white_count)

Answer = namedtuple('Answer', ['guess', 'result'])

ANSWERS = [
    Answer('OOGP', (0,1)),
    Answer('RYWW', (1,2)),
    Answer('PRPR', (1,0)),
    Answer('GRYW', (1,1)),
    Answer('WRWO', (0,2)),
    Answer('YWPW', (4,0))
]

def consistent(i, answer):
    return match(i, answer.guess) == match.result

def count_consistent(answers):
    count = 0
    for i in range(6**4):
        if all(consistent(i, answer) for answer in answers):
            count += 1
    return count

def main():
    for i in range(6**4):
        if (i % 100) == 0:
            red, white = match(i, 1111)
            print('{}: {} match against {} = r:{} w:{}'.format(
                i, ':'.join(colors(i)),
                ':'.join(colors(1111)), red, white
            ))

if __name__ == '__main__':
    main()
