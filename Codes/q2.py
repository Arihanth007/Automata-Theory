import pandas as pd
import json
import sys
import itertools
import os


def sort_string(s):

    temp = []
    for i in range(len(s)):
        temp.append(s[i])
    temp.sort()

    t = ''
    for it in temp:
        t += str(it)

    return t


def findsubsets(s):
    superset = []
    s.sort()
    for n in range(1, len(s)+1):
        for ele in list(itertools.combinations(s, n)):
            temp = []
            for i in ele:
                temp.append(i[1:])
            superset.append(temp)
    # print(superset)
    return superset


def unique(list1):
    unique_list = []
    for x in list1:
        if x not in unique_list:
            unique_list.append(x)
    return unique_list


def main():

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    f = open(input_file)
    data = json.load(f)

    epsilon = '$'
    states = data['states']
    letters = data['letters']
    start_states = data['start_states']
    final_states = data['final_states']
    nfa = {}

    for state in states:
        state = state[1:]
        nfa[state] = {}
        for letter in letters:
            nfa[state][letter] = []

    # for entry in data['transition_matrix']:
    for entry in data['transition_function']:
        start = entry[0][1:]
        _letter = entry[1]
        end = entry[2][1:]
        nfa[start][_letter].append(end)

    start_set = [ele[1:] for ele in states]
    start_set.sort()

    superset = findsubsets(states)
    superset.append([epsilon])

    # print(superset)
    # print()

    print("\nNFA :- \n")
    print(nfa)
    print("\nPrinting NFA table :- ")
    nfa_table = pd.DataFrame(nfa)
    print(nfa_table.transpose())

    ###################################################

    nfa_start_state = [ele[1:] for ele in start_states]
    nfa_final_state = [ele[1:] for ele in final_states]
    states_in_nfa = [[ele[1:]] for ele in states]
    states_in_nfa.sort()
    new_states_list = []
    done_states = []
    dfa = {}

    for i, st in enumerate(superset):
        i = str(i)
        dfa[i] = {}
        for _let in letters:
            dfa[i][_let] = []

    while len(states_in_nfa) != 0:
        cur_st = str(superset.index(states_in_nfa[0]))
        states_in_nfa.remove(superset[int(cur_st)])

        for _let in letters:

            temp_list = []
            for indi in superset[int(cur_st)]:
                for ele in nfa[indi][_let]:
                    if ele not in temp_list:
                        temp_list.append(ele)
            # print('state:', cur_st, 'letter:', _let, 'final:', temp_list)

            temp_list.sort()

            if temp_list == []:
                continue

            if temp_list not in dfa[cur_st][_let]:
                dfa[cur_st][_let] = temp_list.copy()
            if temp_list not in new_states_list:
                new_states_list.append(temp_list)
                done_states.append(temp_list)

            temp = temp_list.copy()
            for ele in superset[int(cur_st)]:
                if ele not in temp:
                    temp.append(ele)
            temp.sort()
            if temp not in new_states_list:
                new_states_list.append(temp)
                done_states.append(temp)

    # print("\nInitial DFA table :- ")
    # dfa_table = pd.DataFrame(dfa)
    # print(dfa_table.transpose())

    ###################################################

    print()
    print(new_states_list)
    # print(done_states)
    print()

    # for i, x in enumerate(new_states_list):
    #     if type(x) == type([]):
    #         new_states_list[i] = unique(x)

    while len(new_states_list) != 0:
        cur_st = str(superset.index(new_states_list[0]))
        new_states_list.remove(new_states_list[0])

        for _let in letters:

            temp_list2 = []

            for indi in superset[int(cur_st)]:
                for ele in dfa[indi][_let]:
                    if ele not in temp_list2:
                        temp_list2.append(ele)
            # print('state:', cur_st, 'letter:', _let, 'final:', temp_list2)

            temp_list2.sort()

            if temp_list2 == []:
                continue

            if temp_list2 not in dfa[cur_st][_let]:
                dfa[cur_st][_let] = temp_list2.copy()
            if temp_list2 not in new_states_list and temp_list2 not in done_states:
                new_states_list.append(temp_list2)
                done_states.append(temp_list2)

            temp1 = temp_list2.copy()
            for ele in superset[int(cur_st)]:
                if ele not in temp1:
                    temp1.append(ele)
            temp1.sort()
            if temp1 not in new_states_list and temp1 not in done_states:
                new_states_list.append(temp1)
                done_states.append(temp1)

    # print("\nNext DFA table :- ")
    # dfa_table = pd.DataFrame(dfa)
    # print(dfa_table.transpose())

    ###################################################

    for i, x in enumerate(superset):
        i = str(i)

        for _let in letters:

            if _let == epsilon:
                dfa[i].pop(epsilon)
                continue

            temp = dfa[i][_let]

            if temp == []:
                t = str(superset.index([epsilon]))
                dfa[i][_let].append(t)

    print("\nDFA :- \n")
    print(dfa)
    print("\nFinal DFA table :- ")
    dfa_table = pd.DataFrame(dfa)
    print(dfa_table.transpose())

    ###################################################

    new_states = []
    for ele in superset:
        temp = []
        for i in ele:
            if i == epsilon:
                continue
            temp.append('Q'+i)
        new_states.append(temp)

    dfa_start_states = [['Q'+ele for ele in nfa_start_state]]

    dfa_final_states = []
    for ele in nfa_final_state:
        for st in superset:
            if ele in st:
                dfa_final_states.append(['Q'+i for i in st])

    ###################################################

    transisiton_matrix = []

    for ele in list(dfa.keys()):
        for _let in letters:
            temp = []
            for st in dfa[ele][_let]:
                if st != str(len(superset)-1):
                    temp.append('Q' + st)
            transisiton_matrix.append(
                [['Q'+i for i in superset[int(ele)] if i != epsilon], _let, temp])

    output = {
        'states': new_states,
        'letters': letters,
        'transition_matrix': transisiton_matrix,
        'start_states': dfa_start_states,
        'final_states': dfa_final_states
    }

    with open(output_file, 'w') as fp:
        json.dump(output, fp)


if __name__ == "__main__":
    os.system('clear')
    main()
