
from src.parser import parse_program
from src.virtual_machine import NormaVM

def run_program(program_path: str, initial_registers: dict, max_steps: int = 100000):
    """
    Carrega, expande macros, valida e executa o programa Norma.
    Retorna (trace, final_registers).
    """
    program = parse_program(program_path)
    vm = NormaVM(initial_registers, max_steps=max_steps)
    trace = vm.run(program)
    return trace, vm.registers.copy()
