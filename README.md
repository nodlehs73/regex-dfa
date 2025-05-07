# Regex to DFA Converter and Simulator

This Python project implements a simple regex engine that converts regular expressions into Nondeterministic Finite Automata (NFA), then into Deterministic Finite Automata (DFA), and finally simulates the DFA to check if a given string matches the original regex.

## Features

*   **Regex Preprocessing**: Automatically adds explicit concatenation operators.
*   **Infix to Postfix Conversion**: Converts regex from infix to postfix notation using a Shunting-yard like algorithm.
*   **Postfix to NFA**: Constructs an NFA from a postfix regex using Thompson's construction algorithm.
*   **NFA to DFA**: Converts an NFA to an equivalent DFA using the subset construction algorithm (powerset construction), including epsilon-closure computation.
*   **DFA Simulation**: Simulates the generated DFA to determine if an input string is accepted.
*   **Supported Regex Operators**:
    *   Concatenation (e.g., `ab`)
    *   Alternation (`|`) (e.g., `a|b`)
    *   Kleene Star (`*`) (e.g., `a*`)
    *   Kleene Plus (`+`) (e.g., `a+`)
    *   Optional (`?`) (e.g., `a?`)
    *   Parentheses for grouping (`()`) (e.g., `(ab)*c`)

## Code Structure

*   **`State.py` (Implicitly, within the main script)**: Defines the `State` class used for both NFA and DFA states. Each state has an ID, a final status, and transitions.
*   **`NFA.py` (Implicitly, within the main script)**: Defines the `NFA` class, including its start state, final state, a collection of all its states, and the alphabet.
*   **`DFA.py` (Implicitly, within the main script)**: Defines the `DFA` class, including its start state, a set of final state IDs, a collection of all its states, and the alphabet.
*   **Core Logic Functions**:
    *   `preprocess_regex(regex)`: Adds explicit concatenation operators.
    *   `regex_to_postfix(regex)`: Converts infix regex to postfix.
    *   `postfix_to_nfa(postfix_regex)`: Builds an NFA from postfix regex.
    *   `epsilon_closure(nfa, state_ids_input)`: Computes the epsilon-closure for a set of NFA states.
    *   `move(nfa, state_ids, symbol)`: Computes states reachable from a set of NFA states on a given symbol.
    *   `nfa_to_dfa(nfa)`: Converts an NFA to a DFA.
    *   `simulate_dfa(dfa, input_string)`: Simulates the DFA with an input string.
*   **`process_single_regex_input()`**: Main function to take regex and string input from the user and print the result.

## How to Run

1.  **Save the code**: Save the Python code as a `.py` file (e.g., `regex_engine.py`).
2.  **Run from the command line**:
    ```bash
    python regex_engine.py
    ```
3.  **Provide input**: The script will prompt you to enter:
    *   The regular expression.
    *   The string to check against the regex.

    Example:
    ```
    Introduceți expresia regulată: (a|b)*c
    Introduceți șirul de verificat: aabc
    ```
4.  **View output**: The script will output:
    *   The postfix form of the regex.
    *   A representation of the constructed NFA (if uncommented).
    *   A representation of the constructed DFA.
    *   Whether the input string is ACCEPTED or REJECTED.

## Example Usage

**Input:**
