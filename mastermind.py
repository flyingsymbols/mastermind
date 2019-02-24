import math
from collections import namedtuple, defaultdict

from columnize import columnize

# I want to figure out a way to make the following operation more efficient:
# Given: [Answers] ~ set(ValidGuess), NextGuess return
# { Result : set(ValidGuess) }
# 
# MM(4,6), mastermind with 4 peg locations and 6 colors:
# num_guesses: there are 6**4 or 1296 guess possibilities at the start
# num_results: there are the following results :
# 0,0 0,1 0,2 0,3 0,4
# 1,0 1,1 1,2 1,3
# 2,0 2,1 2,2
# 3,0 
# 4,0
# This is the same as T(n+1) - 1, where T() is the triangular numbers
# (the -1 is because if all the colors are right, and the positions
#  are right for every other peg, then the position must be right for the
#  last peg, so 3,1 is impossible)
# For 4 pegs, this is T(4+1) - 1 = T(5) - 1 = (5 * (5 + 1))/2 - 1 = 5*6/2 - 1 = 15 - 1 = 14

# The total number of pairs of colors, if we wanted to store a result matrix, would be (because symmetric, we can without loss of generality
# assume that a <= b
# T(num_guesses) = 840456
# if we pack results to 4 bits (enough for the 14 possibilities), we get 420 KB for a result table.

# what is the expected size of the following data structure:
# {result: [(a,b)]} where a <= b ?
# Every (a,b) would be there, which is 840456. We could store 3 pairs of a,b in 8 bytes = 2.2 MB packed that way
# I think this data structure would be more useful in later rounds

# Let's just think of it like abstract datastructures
# 
# Arrangement	= A configuration of pegs
# Match			= A (red, white) response comparing two Arrangements (typically a guess and the secret Arrangement)
# Round			= Arrangement x Match
# GameState = [Round]
#  - correlated information: set(Arrangement) of remaining valid guesses
# We want a function
# partition(GameState, Arrangement) that returns {Match: set(Arrangement)} ({} when the arrangement is impossible)
#
# GameTree = Arrangement x [Match x GameTree] | Solved
#  - also correlated is a count of options at each node	
#
# given a metric, we should be able to construct a GameTree
# 
# representation: 
#	Arrangement ~ int [0, 1296) (11 bits)
#   Match ~ int red*5 + white = 0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 15, 20 (5 bits)
#	Round ~ int (Arrangement | Match << 11) (16 bits)
#	GameState = class
#   GameTree = class

class Arrangement:
	@classmethod
	def from_str(cls, s):
		i = 0
		for c in s:
			i = i * 6 + COLOR_INDS[c]
		return i

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
