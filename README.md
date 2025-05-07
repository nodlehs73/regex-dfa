# Regex to DFA Converter and Simulator

This project implements a regular expression engine that:

✅ Parses a regular expression  
✅ Converts it to postfix notation  
✅ Builds an NFA using Thompson's construction  
✅ Converts the NFA into a DFA (subset construction)  
✅ Simulates the DFA on any input string to check if it is accepted

---

## 🚀 Features

- Supports standard regex operators:
  - Concatenation (`ab`)
  - Alternation (`a|b`)
  - Kleene star (`a*`)
  - Plus (`a+`)
  - Optional (`a?`)
  - Grouping with parentheses
- Handles epsilon (`ε`) transitions internally
- Deterministic simulation of resulting DFA
- Clean and modular Python 3 implementation

---

## 📦 Requirements

Just Python 3 — no external libraries required.

---

## 🛠 Usage

Clone this repository and run the script:

```bash
python3 main.py
