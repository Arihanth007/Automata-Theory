# Automata Theory

## Programming Assignment

- Arihanth Srikar Tadanki
- 2019113005

### Task 1

- The code converts a given regular expression to a NFA.
- First it converts the given expression to postfix.
- Uses recursion to build a tree that contains information of parent and child nodes.
- It makes use of epsilon transitions to make the calculations simpler.
- The resulting NFA will have only final state.

### Task 2

- The code converts NFA to DFA.
- It doesn't handle eplison transitions.
- The resulting DFA will have $2^k$ states.
- it check all the states that the current iteration can reach from the given state.
- Further it check for the closure of the same state. This is widely known as `epsilon closure`.

### Task 3

- The code converts DFA to regex
- We add two new states - starting and final to which the current starting and endng states are joined to.
- This can be thought of as generation a psuedo NFA.
- We check for a pair of states having multiple transistions between them and merge them via `union`.
- We then check for all states apart from the start and final ones and replace the transitions by `concatenation`.
- Self loops are replaced by `*`.
- Finally we get rid of unnecessary brackets.

### Task 4

- The code minimizes a DFA.
- We first get rid of all the states that are unreachable from the start state.
- We then determine what all states are indistinguishable.
- Then we sort the array and represent the array by the first element.
- We update the transition matrix for all states that go to these indistinguishable states.

### Video

The video demonstrates the input taken by the program and the output generated.
<https://iiitaphyd-my.sharepoint.com/:v:/g/personal/arihanth_srikar_research_iiit_ac_in/Efp-TZWy0BxNibGcQCxibUsBcfyxUtyK-Ji-U3fAJRePJQ?e=6PYMr8>

### Executing the files

Each python file takes two arguments, input and output `JSON` files . It returns a dictionary.

Syntax to run the file:
`python3 q<i>.py <input_file>.json <output_file>.json`
