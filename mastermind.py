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
    return i

def num_to_colors(i):
    s = ''
    for x in color_inds(i):
        s += COLORS[x]
    return s

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

class Answer(namedtuple('Answer', ['guess', 'result'])):
    def __repr__(self):
        return '{}({},{})'.format(
            num_to_colors(self.guess), 
            self.result[0], self.result[1]
        )

ANSWERS = [
    Answer(colors_to_num('OOGP'), (0,1)),
    Answer(colors_to_num('RYWW'), (1,2)),
    Answer(colors_to_num('PRPR'), (1,0)),
    Answer(colors_to_num('GRYW'), (1,1)),
    Answer(colors_to_num('WRWO'), (0,2)),
    Answer(colors_to_num('YWPW'), (4,0))
]

def consistent(i, answer):
    return match(i, answer.guess) == answer.result

def yield_consistent(answers):
    for i in range(6**4):
        if all(consistent(i, answer) for answer in answers):
            yield i

def count_consistent(answers):
    c = 0
    for _ in yield_consistent(answers):
        c += 1
    return c


def main():
    for i in range(1, len(ANSWERS)):
        answers = ANSWERS[:i]
        possible = count_consistent(answers)
        print('After {}, {}/{} possible'.format(
            answers,
            possible,
            6**4
        ))

        if possible < 20:
            color_list = [
                num_to_colors(val) 
                for val in yield_consistent(answers)
            ]
            print(color_list)



if __name__ == '__main__':
    main()
