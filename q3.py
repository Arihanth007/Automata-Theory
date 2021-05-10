import json
import sys
import os
import pandas as pd


def unique(list1):
    unique_list = []
    for x in list1:
        if x not in unique_list:
            unique_list.append(x)
    return unique_list


def make_dictionary(transition_funct):
    transition_dict = {}
    for row in transition_funct:
        x = row[0]
        l = row[1]
        y = row[2]
        try:
            transition_dict[x][l] = y
        except:
            transition_dict[x] = {}
            transition_dict[x][l] = y
    return transition_dict


def print_table(transition_funct):
    print("\nDFA table :- ")
    dfa_table = pd.DataFrame(make_dictionary(transition_funct))
    print(dfa_table.transpose())
    print()


def handle_multiple_edges(states, transition_funct):
    for s1 in states:
        for s2 in states:

            multiple_edges_let = []
            to_remove = []

            for row in transition_funct:
                _x = row[0]
                _l = row[1]
                _y = row[2]
                if s2 == _y and s1 == _x:
                    multiple_edges_let.append(
                        [ele for ele in [_l] if ele not in multiple_edges_let][0])
                    to_remove.append(row)

            edge = '('
            for i, _let in enumerate(multiple_edges_let):
                if i == len(multiple_edges_let)-1:
                    edge += (_let + ')')
                else:
                    edge += (_let + '+')

            if len(multiple_edges_let) < 2:
                continue

            transition_funct.append([s1, edge, s2])
            for _row in to_remove:
                transition_funct.remove(_row)

    return transition_funct


def main():

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    f = open(input_file)
    data = json.load(f)

    r = ''
    states = data['states'] + [data['states'][0][0]+'-1']
    states.append(data['states'][0][0]+'{}'.format(len(states)+1))
    states.sort()
    states_copy = states.copy()
    letters = data['letters']
    start_states = states[0]
    final_states = states[-1]
    transition_funct = data['transition_function'] + [[start_states, '$',
                                                       data['start_states'][0]]] + [[st, '$', final_states] for st in data['final_states']]
    transition_dict = {}

    # print('states :', states)
    # print('letters :', letters)
    # print('start_states :', start_states)
    # print('final_states :', final_states)
    # print('transition funct : ')
    # for a in transition_funct:
    #     print(a)
    # print()
    # print()

    transition_funct = handle_multiple_edges(states, transition_funct)
    transition_dict = make_dictionary(transition_funct)

    while len(states_copy) > 2:
        # print_table(transition_funct)

        for st in states_copy:
            if st in [start_states, final_states]:
                continue

            transition_dict = make_dictionary(transition_funct)
            from_states = []
            to_states = []

            r = ''
            if st in list(transition_dict[st].values()):
                for _let, s in transition_dict[st].items():
                    if st != s:
                        continue
                    if _let[0] == '(' and _let[-1] == ')':
                        r += '{}*'.format(_let)
                    else:
                        r += '({})*'.format(_let)

            states_copy.remove(st)

            for row in transition_funct:
                if row[0] == row[2] and st == row[0]:
                    transition_funct.remove(row)

            for s1 in states_copy:
                for s2 in states_copy:
                    for r1 in transition_funct:
                        for r2 in transition_funct:
                            if r2[0] == r1[2] and st in [r1[2]] and r1[0] == s1 and r2[2] == s2:
                                from_states.append(r1)
                                from_states = unique(from_states)
                                to_states.append(r2)
                                to_states = unique(to_states)

            for r1 in from_states:
                for r2 in to_states:
                    r1[1] = '' if r1[1] == '$' else r1[1]
                    r2[1] = '' if r2[1] == '$' else r2[1]
                    _r = '({}{}{})'.format(r1[1], r, r2[1])
                    if _r == '()':
                        continue
                    transition_funct.append([r1[0], _r, r2[2]])

            for _ in from_states + to_states:
                transition_funct.remove(_)

            transition_funct = handle_multiple_edges(states, transition_funct)

            break

    # for a in transition_funct:
    #     print(a)

    regex = [row[1] for row in transition_funct if row[0]
             == start_states and row[2] == final_states][0]
    for _ in letters:
        regex = regex.replace('({})'.format(_), _)
    print(regex)

    output = {'regex': regex}

    with open(output_file, 'w') as fp:
        json.dump(output, fp)


if __name__ == '__main__':
    os.system('clear')
    main()
