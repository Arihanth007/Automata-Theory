from q2 import unique
import pandas as pd
import json
import sys
import itertools
import os


def main():

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    f = open(input_file)
    data = json.load(f)

    states = data['states']
    letters = data['letters']
    start_states = data['start_states']
    final_states = data['final_states']
    dfa = {}

    for state in states:
        state = state
        dfa[state] = {}
        for letter in letters:
            dfa[state][letter] = []

    # for entry in data['transition_matrix']:
    for entry in data['transition_function']:
        start = entry[0]
        _letter = entry[1]
        end = entry[2]
        dfa[start][_letter].append(end)

    print('states:', states)
    print('start_states:', start_states)
    print('final_states:', final_states)

    print("\nInitial DFA table :- ")
    dfa_table = pd.DataFrame(dfa)
    print(dfa_table.transpose())

    # trap_states = []

    # for st in list(dfa.keys()):
    #     for _let in letters:
    #         if st != dfa[st][_let][0]:
    #             break
    #     else:
    #         trap_states.append(st)

    can_be_reached = [ele for ele in start_states]
    my_queue = [ele for ele in start_states]

    while len(my_queue) != 0:
        cur_st = str(my_queue[0])
        my_queue.remove(my_queue[0])

        # print('current state:', cur_st, type(cur_st))

        for _let in letters:
            if str(dfa[cur_st][_let][0]) not in can_be_reached:
                can_be_reached.append(dfa[cur_st][_let][0])
                my_queue.append(dfa[cur_st][_let][0])

    for i in list(dfa.keys()):
        if i not in can_be_reached:
            dfa.pop(i)
            try:
                final_states.remove(i)
            except:
                pass
            try:
                states.remove(i)
            except:
                pass

    # for st in trap_states:
    #     dfa.pop(st)

    # for st in list(dfa.keys()):
    #     for tp in trap_states:
    #         for _let in letters:
    #             if tp != dfa[st][_let][0]:
    #                 break
    #         else:
    #             trap_states.append(st)

    # print()
    # print('traps:', trap_states)
    # print()

    to_combine = []

    for x in list(dfa.keys()):
        tmp = [x]
        for y in list(dfa.keys()):
            if x == y:
                continue
            if dfa[x] == dfa[y]:
                tmp.append(y)
            elif x in final_states and y in final_states:
                tmp.append(y)
        tmp.sort()
        if len(tmp) > 1 and tmp not in to_combine:
            to_combine.append(tmp)

    refer_dict = {}

    for comb in to_combine:
        x = comb[0]
        refer_dict[x] = comb
        can_be_reached.append(comb)

        for ele in comb[1:]:
            try:
                can_be_reached.remove(ele)
            except:
                pass
            for st in list(dfa.keys()):
                for _let in letters:
                    if dfa[st][_let][0] == ele:
                        dfa[st][_let][0] = x

    for comb in to_combine:
        x = comb[0]
        try:
            final_states.remove(x)
            final_states.append(comb)
        except:
            pass
        try:
            states.remove(x)
            states.append(comb)
        except:
            pass
        try:
            start_states.remove(x)
            start_states.append(comb)
        except:
            pass
        try:
            can_be_reached.remove(x)
        except:
            pass
        for i in comb[1:]:
            dfa.pop(i)
            try:
                final_states.remove(i)
            except:
                pass
            try:
                states.remove(i)
            except:
                pass

    print()
    print('to combine:', to_combine)

    # print("\nReduced DFA table :- ")
    # dfa_table = pd.DataFrame(dfa)
    # print(dfa_table.transpose())

    # transition_function = []

    # for comb in to_combine:
    #     x = comb[0]
    #     for i in range(len(states)):
    #         if x == states[i]:
    #             states[i] = comb
    #     for i in list(dfa.keys()):
    #         if x == i:
    #             for _let in letters:
    #                 if x == dfa[i][_let][0]:
    #                     transition_function.append([comb, _let, comb])
    #                 else:
    #                     transition_function.append([comb, _let, dfa[i][_let]])
    #         else:
    #             for _let in letters:
    #                 if x == dfa[i][_let][0]:
    #                     transition_function.append([[i], _let, comb])
    #                 else:
    #                     transition_function.append([[i], _let, dfa[i][_let]])

    print('\nPrinting reachable states')
    print(can_be_reached)

    different = {}
    for st1 in can_be_reached:
        if type(st1) == type([]):
            st1 = st1[0]
        different[st1] = {}

        for st2 in can_be_reached:
            if type(st2) == type([]):
                st2 = st2[0]
            different[st1][st2] = False

    isFound = True
    while isFound:
        isFound = False
        for st1 in can_be_reached:
            for st2 in can_be_reached:
                if st1 == st2:
                    continue
                for _let in letters:
                    if type(st1) == type([]):
                        st1 = st1[0]
                    if type(st2) == type([]):
                        st2 = st2[0]

                    if dfa[st1][_let][0] == dfa[st2][_let][0]:
                        continue
                    elif st2 == dfa[st1][_let][0] and st1 == dfa[st2][_let][0]:
                        continue
                    else:
                        break
                else:
                    different[st1][st2] = True
                    different[st2][st1] = True

    combined = to_combine.copy()
    # to_combine.clear()
    print('\nCombined')
    print(combined)
    print('\nNew remove')
    for dicts, vals in list(different.items()):
        print(dicts, vals)
        for d2, v2 in list(vals.items()):
            if v2 and dicts != d2:
                print(d2, v2)
                break
        else:
            different.pop(dicts)
        print()

    print('To combine:')
    print(different)
    print()

    for dicts, vals in list(different.items()):
        for d2, v2 in list(vals.items()):
            if v2:
                if dicts not in to_combine:
                    temp3 = [dicts, d2]
                    temp3.sort()
                    to_combine.append(temp3)
                else:
                    for ii, xx in to_combine:
                        if dicts in xx:
                            if d2 not in xx:
                                to_combine[ii].append(d2)
                                to_combine[ii].sort()

    print('To combine:')
    to_combine = unique(to_combine)
    to_combine.sort()
    print(to_combine)
    print()

    for comb in to_combine:
        x = comb[0]
        try:
            final_states.remove(x)
            final_states.append(comb)
        except:
            pass
        # try:
        #     states.remove(x)
        #     states.append(comb)
        # except:
        #     pass
        try:
            start_states.remove(x)
            start_states.append(comb)
        except:
            pass
        try:
            can_be_reached.remove(x)
        except:
            pass
        for i in comb[1:]:
            try:
                dfa.pop(i)
            except:
                pass
            try:
                final_states.remove(i)
            except:
                pass
            try:
                states.remove(i)
            except:
                pass

    for comb in to_combine:
        x = comb[0]
        for ii, xx in enumerate(states):
            if type(xx) == type([]):
                continue
            if x == xx:
                states.append(comb)
            for xxx in comb:
                try:
                    states.remove(xxx)
                except:
                    pass

    make_life_easier = {}
    for comb in to_combine:
        for ele in comb:
            make_life_easier[ele] = comb

    for ii, st in enumerate(states):
        if type(st) != type([]):
            make_life_easier[st] = [st]
            states[ii] = [st]

    transition_function = []

    for i in list(dfa.keys()):
        for _let in letters:

            j = dfa[i][_let][0]
            print(i, _let, j)

            transition_function.append(
                [make_life_easier[i], _let, make_life_easier[j]])

    transition_function = unique(transition_function)

    print("\nReduced DFA table :- ")
    dfa_table = pd.DataFrame(dfa)
    print(dfa_table.transpose())

    print()
    print()
    print('states:', states)
    print('start_states:', start_states)
    print('final_states:', final_states)
    print('transition_function:')
    for _ in transition_function:
        print(_)

    output = {
        'states': states,
        'letters': letters,
        'transition_function': transition_function,
        'start_states': start_states,
        'final_states': final_states
    }

    with open(output_file, 'w') as fp:
        json.dump(output, fp)


if __name__ == "__main__":
    os.system('clear')
    main()
