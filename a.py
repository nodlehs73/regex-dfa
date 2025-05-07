EPSILON = 'ε'
CONCAT_OP = '.'
class State:
    _id_counter = 0

    def __init__(self, is_final=False):
        self.id = State._id_counter
        State._id_counter += 1
        self.is_final = is_final
        self.transitions = {}

    def add_transition(self, symbol, next_state_target):
        if symbol not in self.transitions:
            self.transitions[symbol] = []
        current_transitions_for_symbol = self.transitions[symbol]
        if isinstance(next_state_target, list):
            for s_id in next_state_target:
                if s_id not in current_transitions_for_symbol:
                    current_transitions_for_symbol.append(s_id)
        else:
            if next_state_target not in current_transitions_for_symbol:
                current_transitions_for_symbol.append(next_state_target)

    @classmethod
    def reset_id_counter(cls):
        cls._id_counter = 0
class NFA:
    def __init__(self, start_state_id, final_state_id, states):
        self.start_state_id = start_state_id
        self.final_state_id = final_state_id
        self.states = states
        self.alphabet = set()

    def get_state(self, state_id):
        return self.states.get(state_id)

class DFA:
    def __init__(self, start_state_id, final_state_ids, states, alphabet):
        self.start_state_id = start_state_id
        self.final_state_ids = final_state_ids
        self.states = states
        self.alphabet = alphabet

    def get_state(self, state_id):
        return self.states.get(state_id)

def preprocess_regex(regex):
    output = []
    for i, char in enumerate(regex):
        output.append(char)
        if i + 1 < len(regex):
            next_char = regex[i + 1]
            if (char.isalnum() or char in [')', '?', '*', '+']) and (next_char.isalnum() or next_char == '('):
                output.append(CONCAT_OP)
    return "".join(output)


def regex_to_postfix(regex):
    precedence = {'|': 1, CONCAT_OP: 2, '?': 3, '*': 3, '+': 3}
    postfix = []
    operators = []
    processed_regex = preprocess_regex(regex)
    for char in processed_regex:
        if char.isalnum() or char == EPSILON:
            postfix.append(char)
        elif char == '(':
            operators.append(char)
        elif char == ')':
            while operators and operators[-1] != '(':
                postfix.append(operators.pop())
            operators.pop()
        else:
            while (operators and operators[-1] != '(' and
                    precedence.get(operators[-1], 0) >= precedence.get(char, 0)):
                postfix.append(operators.pop())
            operators.append(char)
    while operators:
        postfix.append(operators.pop())
    return "".join(postfix)
def postfix_to_nfa(postfix_regex):
    State.reset_id_counter()
    nfa_stack = []
    nfa_states_collection = {}
    alphabet = set()

    def add_state_to_collection(state):
        nfa_states_collection[state.id] = state

    for char in postfix_regex:
        if char.isalnum():
            alphabet.add(char)
            s0 = State()
            s1 = State(is_final=True)
            s0.add_transition(char, s1.id)
            add_state_to_collection(s0)
            add_state_to_collection(s1)
            nfa_stack.append(NFA(s0.id, s1.id, {s0.id: s0, s1.id: s1}))
        elif char == EPSILON:
            s0 = State()
            s1 = State(is_final=True)
            s0.add_transition(EPSILON, s1.id)
            add_state_to_collection(s0)
            add_state_to_collection(s1)
            nfa_stack.append(NFA(s0.id, s1.id, {s0.id: s0, s1.id: s1}))
        elif char == CONCAT_OP:
            nfa2 = nfa_stack.pop()
            nfa1 = nfa_stack.pop()
            nfa1_final_state = nfa_states_collection[nfa1.final_state_id]
            nfa1_final_state.is_final = False
            nfa1_final_state.add_transition(EPSILON, nfa2.start_state_id)
            combined_states_map_for_nfa_object = {**nfa1.states, **nfa2.states}
            nfa_stack.append(NFA(nfa1.start_state_id, nfa2.final_state_id, combined_states_map_for_nfa_object))
        elif char == '|':
            nfa2 = nfa_stack.pop()
            nfa1 = nfa_stack.pop()
            s_start = State()
            s_final = State(is_final=True)
            add_state_to_collection(s_start)
            add_state_to_collection(s_final)
            s_start.add_transition(EPSILON, [nfa1.start_state_id, nfa2.start_state_id])
            nfa1_final_state = nfa_states_collection[nfa1.final_state_id]
            nfa1_final_state.is_final = False
            nfa1_final_state.add_transition(EPSILON, s_final.id)
            nfa2_final_state = nfa_states_collection[nfa2.final_state_id]
            nfa2_final_state.is_final = False
            nfa2_final_state.add_transition(EPSILON, s_final.id)
            combined_states_map_for_nfa_object = {**nfa1.states, **nfa2.states, s_start.id: s_start, s_final.id: s_final}
            nfa_stack.append(NFA(s_start.id, s_final.id, combined_states_map_for_nfa_object))
        elif char == '*':
            nfa1 = nfa_stack.pop()
            s_start = State()
            s_final = State(is_final=True)
            add_state_to_collection(s_start)
            add_state_to_collection(s_final)
            s_start.add_transition(EPSILON, [nfa1.start_state_id, s_final.id])
            nfa1_final_state = nfa_states_collection[nfa1.final_state_id]
            nfa1_final_state.is_final = False
            nfa1_final_state.add_transition(EPSILON, [nfa1.start_state_id, s_final.id])
            combined_states_map_for_nfa_object = {**nfa1.states, s_start.id: s_start, s_final.id: s_final}
            nfa_stack.append(NFA(s_start.id, s_final.id, combined_states_map_for_nfa_object))
        elif char == '+':
            nfa_op = nfa_stack.pop()
            s_start = State()
            s_final = State(is_final=True)
            add_state_to_collection(s_start)
            add_state_to_collection(s_final)
            nfa_op_final_state = nfa_states_collection[nfa_op.final_state_id]
            nfa_op_final_state.is_final = False
            s_start.add_transition(EPSILON, nfa_op.start_state_id)
            nfa_op_final_state.add_transition(EPSILON, [nfa_op.start_state_id, s_final.id])
            combined_states_map_for_nfa_object = {**nfa_op.states, s_start.id: s_start, s_final.id: s_final}
            nfa_stack.append(NFA(s_start.id, s_final.id, combined_states_map_for_nfa_object))
        elif char == '?':
            nfa1 = nfa_stack.pop()
            s_start = State()
            s_final = State(is_final=True)
            add_state_to_collection(s_start)
            add_state_to_collection(s_final)
            s_start.add_transition(EPSILON, [nfa1.start_state_id, s_final.id])
            nfa1_final_state = nfa_states_collection[nfa1.final_state_id]
            nfa1_final_state.is_final = False
            nfa1_final_state.add_transition(EPSILON, s_final.id)
            combined_states_map_for_nfa_object = {**nfa1.states, s_start.id: s_start, s_final.id: s_final}
            nfa_stack.append(NFA(s_start.id, s_final.id, combined_states_map_for_nfa_object))
    final_nfa_wrapper = nfa_stack.pop()
    final_nfa_wrapper.states = nfa_states_collection
    final_nfa_wrapper.alphabet = alphabet
    if final_nfa_wrapper.final_state_id in nfa_states_collection:
        nfa_states_collection[final_nfa_wrapper.final_state_id].is_final = True
    else:
        pass
    return final_nfa_wrapper
def epsilon_closure(nfa, state_ids_input):
    if isinstance(state_ids_input, frozenset):
        state_ids = set(state_ids_input)
    elif isinstance(state_ids_input, set):
        state_ids = set(state_ids_input)
    elif isinstance(state_ids_input, (list, tuple)):
        state_ids = set(state_ids_input)
    else:
        state_ids = {state_ids_input}
    closure = set(state_ids)
    stack = list(state_ids)
    while stack:
        current_id = stack.pop()
        current_state = nfa.get_state(current_id)
        if current_state:
            epsilon_next_states = current_state.transitions.get(EPSILON, [])
            for next_id in epsilon_next_states:
                if next_id not in closure:
                    closure.add(next_id)
                    stack.append(next_id)
    return frozenset(closure)
def move(nfa, state_ids, symbol):
    reachable_states = set()
    for state_id in state_ids:
        state = nfa.get_state(state_id)
        if state:
            next_states_on_symbol = state.transitions.get(symbol, [])
            reachable_states.update(next_states_on_symbol)
    return frozenset(reachable_states)
def nfa_to_dfa(nfa):
    State.reset_id_counter()
    dfa_states_map = {}
    dfa_states_obj = {}
    dfa_final_state_ids = set()
    dfa_alphabet = nfa.alphabet
    initial_nfa_closure = epsilon_closure(nfa, {nfa.start_state_id})
    if not initial_nfa_closure:
        s_dead = State()
        dfa_states_obj[s_dead.id] = s_dead
        return DFA(s_dead.id, set(), dfa_states_obj, dfa_alphabet)
    s0_dfa_obj = State()
    start_dfa_id = s0_dfa_obj.id
    dfa_states_map[initial_nfa_closure] = start_dfa_id
    dfa_states_obj[start_dfa_id] = s0_dfa_obj
    if nfa.final_state_id in initial_nfa_closure:
        dfa_final_state_ids.add(start_dfa_id)
        s0_dfa_obj.is_final = True
    unprocessed_dfa_q = [initial_nfa_closure]
    processed_nfa_sets = set()
    while unprocessed_dfa_q:
        current_nfa_state_set = unprocessed_dfa_q.pop(0)
        if current_nfa_state_set in processed_nfa_sets:
            continue
        processed_nfa_sets.add(current_nfa_state_set)
        current_dfa_state_id = dfa_states_map[current_nfa_state_set]
        current_dfa_state_obj = dfa_states_obj[current_dfa_state_id]
        for symbol in sorted(list(dfa_alphabet)):
            if symbol == EPSILON: continue
            move_result = move(nfa, current_nfa_state_set, symbol)
            if not move_result:
                continue
            target_nfa_state_set_closure = epsilon_closure(nfa, move_result)
            if not target_nfa_state_set_closure:
                continue
            target_dfa_state_id = -1
            if target_nfa_state_set_closure not in dfa_states_map:
                new_dfa_obj = State()
                target_dfa_state_id = new_dfa_obj.id
                dfa_states_map[target_nfa_state_set_closure] = target_dfa_state_id
                dfa_states_obj[target_dfa_state_id] = new_dfa_obj
                unprocessed_dfa_q.append(target_nfa_state_set_closure)
                if nfa.final_state_id in target_nfa_state_set_closure:
                    dfa_final_state_ids.add(target_dfa_state_id)
                    new_dfa_obj.is_final = True
            else:
                target_dfa_state_id = dfa_states_map[target_nfa_state_set_closure]
            current_dfa_state_obj.add_transition(symbol, target_dfa_state_id)
    return DFA(start_dfa_id, dfa_final_state_ids, dfa_states_obj, dfa_alphabet)
def simulate_dfa(dfa, input_string):
    if dfa is None or dfa.start_state_id is None or not dfa.states:
        if input_string == "":
            if dfa and dfa.start_state_id in dfa.final_state_ids:
                start_state_obj = dfa.get_state(dfa.start_state_id)
                if start_state_obj and not any(sym != EPSILON for sym in start_state_obj.transitions):
                    return True
        return False
    current_state_id = dfa.start_state_id
    current_state = dfa.get_state(current_state_id)
    if current_state is None:
        return False
    for symbol in input_string:
        if symbol not in dfa.alphabet:
            return False
        next_state_ids_list = current_state.transitions.get(symbol)
        if not next_state_ids_list:
            return False
        if len(next_state_ids_list) != 1:
            return False
        current_state_id = next_state_ids_list[0]
        current_state = dfa.get_state(current_state_id)
        if current_state is None:
            return False
    return current_state.id in dfa.final_state_ids
def process_single_regex_input():
    regex_input = input("Introduceți expresia regulată: ")
    string_to_check = input("Introduceți șirul de verificat: ")
    postfix_expr = regex_to_postfix(regex_input)
    nfa = postfix_to_nfa(postfix_expr)
    dfa = nfa_to_dfa(nfa)
    if string_to_check is None:
        string_to_check = ""
    actual = simulate_dfa(dfa, string_to_check)
    if actual:
        print(f"Rezultat: Șirul '{string_to_check}' ESTE ACCEPTAT de regex '{regex_input}'.")
    else:
        print(f"Rezultat: Șirul '{string_to_check}' ESTE RESPINS de regex '{regex_input}'.")

process_single_regex_input()