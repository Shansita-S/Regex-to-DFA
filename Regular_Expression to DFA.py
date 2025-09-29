from collections import defaultdict, deque
class State:
    def __init__(self):
        self.transitions = defaultdict(list)

class NFA:
    def __init__(self, start, accept):
        self.start = start
        self.accept = accept

def symbol_nfa(symbol):
    s, e = State(), State()
    s.transitions[symbol].append(e)
    return NFA(s, e)

def concat(nfa1, nfa2):
    nfa1.accept.transitions['ε'].append(nfa2.start)
    return NFA(nfa1.start, nfa2.accept)

def union(nfa1, nfa2):
    s, e = State(), State()
    s.transitions['ε'] += [nfa1.start, nfa2.start]
    nfa1.accept.transitions['ε'].append(e)
    nfa2.accept.transitions['ε'].append(e)
    return NFA(s, e)

def star(nfa):
    s, e = State(), State()
    s.transitions['ε'] += [nfa.start, e]
    nfa.accept.transitions['ε'] += [nfa.start, e]
    return NFA(s, e)

ab = concat(symbol_nfa('a'), symbol_nfa('b'))
abb = concat(ab, symbol_nfa('b'))
alt = union(symbol_nfa('a'), symbol_nfa('b'))
closure = star(alt)
final_nfa = concat(closure, abb)

def epsilon_closure(states):
    stack, closure = list(states), set(states)
    while stack:
        state = stack.pop()
        for nxt in state.transitions.get('ε', []):
            if nxt not in closure:
                closure.add(nxt)
                stack.append(nxt)
    return closure

def move(states, symbol):
    nxt_states = set()
    for state in states:
        nxt_states.update(state.transitions.get(symbol, []))
    return nxt_states

def nfa_to_dfa(nfa):
    start_closure = frozenset(epsilon_closure([nfa.start]))
    dfa_states = {start_closure: 0}
    dfa_transitions = {}
    accept_states = set()

    queue = deque([start_closure])
    state_id = 1

    while queue:
        current = queue.popleft()
        dfa_transitions[dfa_states[current]] = {}

        if nfa.accept in current:
            accept_states.add(dfa_states[current])

        for symbol in ['a', 'b']:
            nxt = frozenset(epsilon_closure(move(current, symbol)))
            if not nxt:
                continue
            if nxt not in dfa_states:
                dfa_states[nxt] = state_id
                state_id += 1
                queue.append(nxt)
            dfa_transitions[dfa_states[current]][symbol] = dfa_states[nxt]

    return dfa_transitions, 0, accept_states
transitions, start, accepts = nfa_to_dfa(final_nfa)

print("DFA Transition Table:")
print("State\t a \t b")
for state in transitions:
    print(f"{state}\t {transitions[state].get('a', '-')}\t {transitions[state].get('b', '-')}")
print("Accepting States:", accepts)
