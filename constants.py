from numpy import random

'''
This file defines the all chords, which are useful for accompaniment
'''


def get_next_state(prob_array):
    normalize = sum(prob_array)
    rand = random.rand(1)
    state = 0
    for i in range(len(prob_array)):
        state += prob_array[i]/normalize
        if rand < state:
            return i
    return -1


# chord_name = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4']

chords = [[0, 4, 7],
          [2, 5, 9],
          [4, 7, 11],
          [5, 9, 12],
          [7, 11, 14],
          [9, 12, 16],
          [11, 14, 17]]

CHORDS = [[0, 4, 7, 11],
          [2, 5, 9, 12],
          [4, 7, 11, 14],
          [5, 9, 12, 16],
          [7, 11, 14, 17],
          [9, 12, 16, 19],
          [11, 14, 17, 21]]

STATE_PROB = [[0.0, 0.0, 0.1, 0.2, 0.6, 0.1, 0.0],
              [0.0, 0.0, 0.0, 0.1, 0.7, 0.1, 0.1],
              [0.1, 0.1, 0.0, 0.1, 0.3, 0.2, 0.1],
              [0.3, 0.0, 0.0, 0.0, 0.5, 0.2, 0.0],
              [0.4, 0.0, 0.0, 0.2, 0.0, 0.4, 0.0],
              [0.5, 0.1, 0.0, 0.0, 0.1, 0.2, 0.1],
              [0.4, 0.1, 0.1, 0.1, 0.2, 0.1, 0.0]]

melody_prob = [[0.1, 0.5, 0.2, 0.1, 0.1, 0.0, 0.0],
               [0.3, 0.1, 0.3, 0.1, 0.1, 0.0, 0.0],
               [0.1, 0.3, 0.1, 0.3, 0.1, 0.1, 0.0],
               [0.1, 0.0, 0.3, 0.1, 0.4, 0.1, 0.0],
               [0.0, 0.1, 0.3, 0.1, 0.3, 0.1, 0.1],
               [0.0, 0.0, 0.1, 0.3, 0.3, 0.1, 0.2],
               [0.0, 0.0, 0.0, 0.3, 0.3, 0.4, 0.0]]


if __name__ == '__main__':
    INIT_STATE = 0

    cur_state = INIT_STATE
    for i in range(1, 5):
        cur_state = get_next_state(STATE_PROB[cur_state])
        print('State {0} :'.format(i), str(cur_state+1))

    cur_state = INIT_STATE
    for i in range(1, 20):
        cur_state = get_next_state(melody_prob[cur_state])
        print('State {0} :'.format(i), str(cur_state+1))

    print(STATE_PROB[1][1])
