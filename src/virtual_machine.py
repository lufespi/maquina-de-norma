import re
from src.macros import MACRO_IMPL  # importa o dicionário de macros

class NormaVM:
    def __init__(self, program, registers):
        """
        Inicializa a Máquina Norma.
        :param program: dicionário {rotulo: instrução}
        :param registers: dicionário {nome: valor_inicial}
        """
        self.program = program
        self.registers = registers
        self.current_label = min(program.keys())
        self.trace = []  # guarda o histórico de execução (rótulo, estado dos registradores)

    def run(self):
        """Executa o programa até terminar."""
        while self.current_label in self.program:
            instr = self.program[self.current_label]
            self.execute(instr)

    def execute(self, instr):
        """Executa uma única instrução."""
        # Salva o estado antes de executar
        self.trace.append((self.current_label, self.registers.copy()))
        s = instr.strip()

        # 1) Teste condicional: se zero_X então vá_para ...
        if s.startswith("se zero_"):
            parts = s.split("vá_para")
            reg = s.split("_", 1)[1].split()[0]
            true_jump = int(parts[1].split()[0])
            false_jump = int(parts[2].split()[0])
            self.current_label = true_jump if self.registers.get(reg, 0) == 0 else false_jump
            return

        # 2) Operações add/sub com salto explícito
        m = re.match(r"faça\s+(add|sub)_(\w+)\s+vá_para\s+(\d+)", s)
        if m:
            op, reg, jmp = m.groups()
            if op == "add":
                self.registers[reg] = self.registers.get(reg, 0) + 1
            else:
                self.registers[reg] = max(0, self.registers.get(reg, 0) - 1)
            self.current_label = int(jmp)
            return

        # 3) Chamadas de macro registradas no MACRO_IMPL
        m = re.match(r"faça\s+([A-Za-z_]\w*)\(([^)]*)\)(?:\s+vá_para\s+(\d+))?", s)
        if m:
            nome_macro, args_str, jmp = m.groups()
            nome_macro = nome_macro.upper()  # normaliza para maiúsculo
            if nome_macro not in MACRO_IMPL:
                raise ValueError(
                    f"Macro '{nome_macro}' não encontrada. "
                    f"Macros disponíveis: {', '.join(MACRO_IMPL.keys())}"
                )

            func, arity = MACRO_IMPL[nome_macro]
            args = [a.strip() for a in args_str.split(",")] if args_str else []
            if len(args) != arity:
                raise ValueError(
                    f"Macro '{nome_macro}' espera {arity} argumentos, recebeu {len(args)} ({args})"
                )

            # Executa a macro passando os registradores
            func(self.registers, *args)
            # Se houver vá_para, usa o rótulo. Senão, vai para o próximo.
            self.current_label = int(jmp) if jmp else self.current_label + 1
            return

        # 4) Comentário ou fim de programa
        if s.startswith("#"):
            self.current_label = None
            return

        # 5) Caso nenhuma regra reconheça
        raise ValueError(f"Instrução desconhecida: {instr}")

    def print_trace(self):
        """Imprime o trace de execução."""
        print("\n=== TRACE DE EXECUÇÃO ===")
        for label, regs in self.trace:
            estado = ", ".join(f"{k}={v}" for k, v in regs.items())
            print(f"Rótulo {label} -> {estado}")
        print("=== FIM ===")
