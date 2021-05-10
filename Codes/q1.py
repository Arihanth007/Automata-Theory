import json
import sys
import os


# epsilon = 'epsilon'
epsilon = '$'
isDebug = False
# isPrint = False
isPrint = True

all_start_states = []
all_transition_input = []
all_end_states = []
transition_matrix = []


def unique(list1):
    unique_list = []
    for x in list1:
        if x not in unique_list:
            unique_list.append(x)
    return unique_list


class Type:
    SYMBOL = 1
    CONCAT = 2
    UNION = 3
    KLEENE = 4


class ExpressionTree:

    def __init__(self, _type, value=None):
        self._type = _type
        self.value = value
        self.left = None
        self.right = None


class FiniteAutomataState:

    def __init__(self):
        self.next_state = {}


class ConstructExressionTree:

    def __init__(self, regexp):
        self.regexp = regexp
        self.isDebug = False

    def higherPrecedence(self, a, b):
        p = ["+", ".", "*"]
        return p.index(a) > p.index(b)

    # adding dot "." between consecutive symbols
    def handle_concatenation(self, regexp):

        temp = []
        for i in range(len(regexp)):
            if i != 0\
                    and (regexp[i-1].isalpha() or (regexp[i-1] >= str(0) and regexp[i-1] <= str(9)) or regexp[i-1] == ")" or regexp[i-1] == "*")\
                    and (regexp[i].isalpha() or (regexp[i] >= str(0) and regexp[i] <= str(9)) or regexp[i] == "("):
                temp.append(".")
            temp.append(regexp[i])

        return temp

    # converts expression to postfix
    def postfix(self):

        regexp = self.handle_concatenation(self.regexp)
        stack = []
        output = ""

        for c in regexp:
            if c.isalpha() or (c >= str(0) and c <= str(9)):
                output = output + c
                continue

            if c == ")":
                while len(stack) != 0 and stack[-1] != "(":
                    output = output + stack.pop()
                stack.pop()
            elif c == "(":
                stack.append(c)
            elif c == "*":
                output = output + c
            elif len(stack) == 0 or stack[-1] == "(" or self.higherPrecedence(c, stack[-1]):
                stack.append(c)
            else:
                while len(stack) != 0 and stack[-1] != "(" and not self.higherPrecedence(c, stack[-1]):
                    output = output + stack.pop()
                stack.append(c)

        while len(stack) != 0:
            output = output + stack.pop()

        return output

    def constructTree(self, regexp):
        stack = []
        count = 0

        for c in regexp:

            count += 1
            if self.isDebug:
                print()

            if c.isalpha() or (c >= str(0) and c <= str(9)):
                stack.append(ExpressionTree(Type.SYMBOL, c))
                if self.isDebug:
                    print_states(c, stack, count)

            else:
                if c == "+":
                    z = ExpressionTree(Type.UNION)
                    z.right = stack.pop()
                    z.left = stack.pop()
                    if self.isDebug:
                        print_states(c, stack, count)

                elif c == ".":
                    z = ExpressionTree(Type.CONCAT)
                    z.right = stack.pop()
                    z.left = stack.pop()
                    if self.isDebug:
                        print_states(c, stack, count)

                elif c == "*":
                    z = ExpressionTree(Type.KLEENE)
                    z.left = stack.pop()
                    if self.isDebug:
                        print_states(c, stack, count)

                stack.append(z)
                if self.isDebug:
                    print_states(c, stack, count)

        return stack[0]


class RegToNFA:

    def __init__(self) -> None:
        pass

    # returns equivalent E-NFA for given expression tree
    # (representing a Regular Expression)
    def evalRegex(self, et):
        if et._type == Type.SYMBOL:
            return self.evalRegexSymbol(et)
        elif et._type == Type.CONCAT:
            return self.evalRegexConcat(et)
        elif et._type == Type.UNION:
            return self.evalRegexUnion(et)
        elif et._type == Type.KLEENE:
            return self.evalRegexKleene(et)

    def evalRegexSymbol(self, et):
        start_state = FiniteAutomataState()
        end_state = FiniteAutomataState()

        start_state.next_state[et.value] = [end_state]
        return start_state, end_state

    def evalRegexConcat(self, et):
        left_nfa = self.evalRegex(et.left)
        right_nfa = self.evalRegex(et.right)

        left_nfa[1].next_state[epsilon] = [right_nfa[0]]
        return left_nfa[0], right_nfa[1]

    def evalRegexUnion(self, et):
        start_state = FiniteAutomataState()
        end_state = FiniteAutomataState()

        up_nfa = self.evalRegex(et.left)
        down_nfa = self.evalRegex(et.right)

        start_state.next_state[epsilon] = [up_nfa[0], down_nfa[0]]
        up_nfa[1].next_state[epsilon] = [end_state]
        down_nfa[1].next_state[epsilon] = [end_state]

        return start_state, end_state

    def evalRegexKleene(self, et):
        start_state = FiniteAutomataState()
        end_state = FiniteAutomataState()

        sub_nfa = self.evalRegex(et.left)

        start_state.next_state[epsilon] = [sub_nfa[0], end_state]
        sub_nfa[1].next_state[epsilon] = [sub_nfa[0], end_state]

        return start_state, end_state


class ConvertTOeNFA:

    def __init__(self, finite_automata):
        self.finite_automata = finite_automata
        self.isPrint = False
        pass

    def printStateTransitions(self, state, states_done, symbol_table):
        if state in states_done:
            return

        states_done.append(state)

        for symbol in list(state.next_state):

            all_start_states.append('q' + str(symbol_table[state]))
            all_transition_input.append(symbol)
            t = ''

            line_output = "q" + \
                str(symbol_table[state]) + "\t\t" + symbol + "\t\t\t"

            for ns in state.next_state[symbol]:
                if ns not in symbol_table:
                    symbol_table[ns] = 1 + sorted(symbol_table.values())[-1]

                t += "q" + str(symbol_table[ns]) + ","
                line_output = line_output + "q" + str(symbol_table[ns]) + " "

            all_end_states.append(t.split(',')[:-1])

            if self.isPrint:
                print(line_output)

            for ns in state.next_state[symbol]:
                self.printStateTransitions(ns, states_done, symbol_table)

    def printTransitionTable(self):
        if self.isPrint:
            print("State\t\tSymbol\t\t\tNext state")
        self.printStateTransitions(self.finite_automata[0], [], {
                                   self.finite_automata[0]: 0})


def print_states(c, s, count):
    cnt = 0
    for i in s:
        cnt += 1
        l, r = i.left, i.right
        if i.left is not None:
            l = 'obj'
        if i.right is not None:
            r = 'obj'
        print(str(count)+".", {'char': c, 'stack': [
            i._type, i.value, l, r]}, len(s))
    if cnt == 0:
        print(str(count)+".", {'char': c, 'stack': []})


def print_states(i):
    l, r = i.left, i.right
    if i.left is not None:
        l = 'obj'
    if i.right is not None:
        r = 'obj'
    print({'stack': [i._type, i.value, l, r]}, len(i))


def inorder(et):
    if et._type == Type.SYMBOL:
        print(et.value)
    elif et._type == Type.CONCAT:
        inorder(et.left)
        print(".")
        inorder(et.right)
    elif et._type == Type.UNION:
        inorder(et.left)
        print("+")
        inorder(et.right)
    elif et._type == Type.KLEENE:
        inorder(et.left)
        print("*")


def main():

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    f = open(input_file)
    data = json.load(f)

    r = data['regex']

    exp_tree = ConstructExressionTree(r)
    pr = exp_tree.postfix()
    et = exp_tree.constructTree(pr)

    if isDebug:
        print('Entered:', r)
        print()

    # inorder(et)

    rfa = RegToNFA()
    fa = rfa.evalRegex(et)

    eNFA = ConvertTOeNFA(fa)
    eNFA.printTransitionTable()

    if isPrint:
        print()
        print("State\t\tSymbol\t\tNext state")

    for i in range(len(all_start_states)):
        for dest in all_end_states[i]:
            transition_matrix.append(
                [all_start_states[i], all_transition_input[i], dest])

        if isPrint:
            print('', all_start_states[i], '\t\t',
                  all_transition_input[i], '\t\t', all_end_states[i])

    starting_state = [all_start_states[0]]
    ending_state = ''

    for arr in all_end_states:
        for ele in arr:
            if ele not in all_start_states:
                ending_state = [ele]

    if isPrint:
        print()
        print('Start state:', starting_state[0])
        print('Final state:', ending_state[0])
        print()

    all_states = all_start_states.copy()
    all_states.append(ending_state[0])

    letters = unique(all_transition_input)
    try:
        letters.remove(epsilon)
    except:
        pass

    output = {
        'states': all_states,
        'letters': letters,
        'transition_function': transition_matrix,
        'start_states': starting_state,
        'final_states': ending_state
    }

    if not isPrint:
        print(output)

    with open(output_file, 'w') as fp:
        json.dump(output, fp)


if __name__ == "__main__":
    os.system('clear')
    main()
