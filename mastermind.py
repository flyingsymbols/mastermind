import math
from collections import namedtuple, defaultdict

from columnize import columnize

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
    for c in color_list:
        i = i * 6 + COLOR_INDS[c]
    return i

def num_to_colors(i):
    s = ''
    for x in color_inds(i):
        s = COLORS[x] + s
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

def next_partitions(answers, i):
    """
    The idea behind this is to, for a given set of answers, and a potential next guess i,
    return the partitions {(red, white): set(nums)}
    """
    parts = defaultdict(set)
    for num in yield_consistent(answers):
        res = match(i, num)
        parts[res].add(num)
    return parts

def minmax_metric(parts):
    return -max(len(v) for v in parts.values())

def best_partitions(prev_answers, metric=minmax_metric):
    """
    Takes the previous_answers, returns a set of values that maximize the given metric

    metric(answer_partitions) -> value
    """
    best_val = -math.inf
    values = []
    for i in range(6**4):
        parts = next_partitions(prev_answers, i)
        metric_val = metric(parts)
        if metric_val > best_val:
            best_val = metric_val
            values = [i]
        elif metric_val == best_val:
            values.append(i)
        # else metric_val < best_val so we can ignore
    return best_val, values

def main():
    cur_answers = []
    answer_tree = {}

    metric_val, best_next = best_partitions(cur_answers, minmax_metric)
    print('After {}, {} with value {}:'.format(cur_answers, len(best_next), metric_val))
    print(columnize(
        [num_to_colors(v) for v in best_next],
        displaywidth=80
    ))

    cur_answer = best_next[0]
    answer_tree[cur_answer] = {}

    next_parts = next_partitions([], cur_answer)
    for res, values in next_parts.items():
        print('|{}| = {}'.format(Answer(cur_answer, res), len(values)))
        print(columnize(
            [num_to_colors(v) for v in values],
            displaywidth=80
        ))

def analyze_game_20190222():
    ANSWERS = [
        Answer(colors_to_num('OOGP'), (0,1)),
        Answer(colors_to_num('RYWW'), (1,2)),
        Answer(colors_to_num('PRPR'), (1,0)),
        Answer(colors_to_num('GRYW'), (1,1)),
        Answer(colors_to_num('WRWO'), (0,2)),
        Answer(colors_to_num('YWPW'), (4,0))
    ]

    for i in range(1, len(ANSWERS) + 1):
        answers = ANSWERS[:i]
        possible = count_consistent(answers)
        print('After {}, {}/{} possible'.format(
            answers,
            possible,
            6**4
        ))

        if possible < 100:
            color_list = [
                num_to_colors(val) 
                for val in yield_consistent(answers)
            ]
            print(columnize(color_list, displaywidth=80))



if __name__ == '__main__':
    main()
