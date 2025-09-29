DFA = {
    0: {'0': 1, '1': 0},  
    1: {'0': 1, '1': 2},  
    2: {'0': 1, '1': 0}   
}

start_state = 0
accept_states = {2}

def validate(s):
    state = start_state
    for ch in s:
        if ch not in DFA[state]:
            return False
        state = DFA[state][ch]
    return state in accept_states

strings = ["1101", "111", "0001"]
for s in strings:
    print(f"{s}: {'Accepted' if validate(s) else 'Rejected'}")
