class TuringMachine:
    def __init__(self, states, input_symbols, tape_symbols, transitions, start_state, accept_state, reject_state):
        self.states = states
        self.input_symbols = input_symbols
        self.tape_symbols = tape_symbols
        self.transitions = transitions
        self.start_state = start_state
        self.accept_state = accept_state
        self.reject_state = reject_state
        self.tapes1 = [[' '] * 100 for _ in range(10)]  # 10 cintas para 10 cadenas
        self.tapes2 = [[' '] * 100 for _ in range(10)]  # 10 cintas para 10 cadenas
        self.heads1 = [0] * 10  # Cabezal para cada cinta 1
        self.heads2 = [0] * 10  # Cabezal para cada cinta 2

    def step(self, tape_index):
        current_symbol1 = self.tapes1[tape_index][self.heads1[tape_index]]
        current_symbol2 = self.tapes2[tape_index][self.heads2[tape_index]]
        if (self.current_state, current_symbol1, current_symbol2) in self.transitions:
            next_state, write_symbol1, write_symbol2, move1, move2 = self.transitions[
                (self.current_state, current_symbol1, current_symbol2)
            ]
            # Actualizar las cintas con los nuevos símbolos
            self.tapes1[tape_index][self.heads1[tape_index]] = write_symbol1
            self.tapes2[tape_index][self.heads2[tape_index]] = write_symbol2
            # Mover cabezales
            self.heads1[tape_index] += 1 if move1 == 'R' else -1 if move1 == 'L' else 0
            self.heads2[tape_index] += 1 if move2 == 'R' else -1 if move2 == 'L' else 0
            # Cambiar estado actual
            self.current_state = next_state
            return (self.current_state, write_symbol1, write_symbol2, move1, move2)
        else:
            # Si no hay transición válida, la máquina se mueve al estado de rechazo
            self.current_state = self.reject_state
            return None

    def run(self, input_strings):
        derivation_trees = []
        results = []
        for tape_index, input_string in enumerate(input_strings):
            for i, symbol in enumerate(input_string):
                self.tapes1[tape_index][i] = symbol
            self.current_state = self.start_state
            tree = []
            while self.current_state not in [self.accept_state, self.reject_state]:
                result = self.step(tape_index)
                if result:
                    tree.append(result)
                else:
                    break
            # Añadimos el último estado para indicar aceptación o rechazo en el árbol
            if self.current_state == self.accept_state:
                tree.append((self.accept_state, '', '', '', ''))
            else:
                tree.append((self.reject_state, '', '', '', ''))
            derivation_trees.append(tree)
            results.append("Aceptado" if self.current_state == self.accept_state else "Rechazado")
        return derivation_trees, results

    def show_transition_table(self):
        print("Tabla de Transición:")
        for (state, symbol1, symbol2), (next_state, write1, write2, move1, move2) in self.transitions.items():
            print(f"({state}, {symbol1}, {symbol2}) -> ({next_state}, {write1}, {write2}, {move1}, {move2})")

    def show_symbols(self):
        print("Simbología de la Máquina de Turing (M):")
        print("Estados (Q):", self.states)
        print("Símbolos de entrada (Σ):", self.input_symbols)
        print("Símbolos de cinta (Γ):", self.tape_symbols)
        print("Estado de inicio (q0):", self.start_state)
        print("Estado de aceptación (aceptado):", self.accept_state)
        print("Estado de rechazo (rechazado):", self.reject_state)

    def generate_derivation_tree(self, derivation_trees, results):
        print("Árbol de Derivación:")
        for tape_index, (tree, result) in enumerate(zip(derivation_trees, results)):
            print(f"\nCadena {tape_index + 1} ({result}):")
            level = 1
            for state, write1, write2, move1, move2 in tree:
                if state in [self.accept_state, self.reject_state]:
                    print(f"Nivel {level}: Estado {state} (Final - {result})")
                else:
                    print(f"Nivel {level}: Estado {state}, escribe '{write1}' en cinta 1, '{write2}' en cinta 2, mueve cinta 1 '{move1}', mueve cinta 2 '{move2}'")
                level += 1
            # Mostrar cómo se lee la cinta en ambos sentidos
            self.read_tapes_both_directions(tape_index)
        print("Final de la derivación.")

    def read_tapes_both_directions(self, tape_index):
        # Leer la cinta 1 de izquierda a derecha
        content_lr = ''.join(self.tapes1[tape_index]).strip()
        content_rl = content_lr[::-1]
        print(f"\nCinta {tape_index + 1} de izquierda a derecha: {content_lr}")
        print(f"Cinta {tape_index + 1} de derecha a izquierda: {content_rl}")

# Definición de los componentes de la máquina de Turing
states = {'q0', 'q1', 'q2', 'aceptado', 'rechazado'}
input_symbols = {'a', 'b', '#', '*'}
tape_symbols = {'a', 'b', '#', '*', ' '}
transitions = {
    # Transiciones para cadenas válidas
    ('q0', 'a', ' '): ('q1', 'a', 'a', 'R', 'R'),
    ('q1', 'b', ' '): ('q2', 'b', 'b', 'R', 'R'),
    ('q2', '*', ' '): ('aceptado', '*', '*', 'R', 'R'),
    # Transiciones para cadenas inválidas
    ('q0', '#', ' '): ('rechazado', '#', '#', 'R', 'R'),
    ('q1', '*', ' '): ('rechazado', '*', '*', 'R', 'R')
}
start_state = 'q0'
accept_state = 'aceptado'
reject_state = 'rechazado'

# Crear la máquina de Turing
tm = TuringMachine(states, input_symbols, tape_symbols, transitions, start_state, accept_state, reject_state)

# Procesar un conjunto de 10 cadenas de ejemplo (algunas válidas, otras inválidas)
input_strings = ["abaab*#ab*", "ab#*ab", "ab#*b", "abaab*", "#ab*", "ab*b", "*aab#", "abaab*ab", "ab*", "ab*#*"]
derivation_trees, results = tm.run(input_strings)

# Mostrar resultados
tm.show_symbols()
tm.show_transition_table()
tm.generate_derivation_tree(derivation_trees, results)
 



