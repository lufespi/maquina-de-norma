from src.parser import parse_program
from src.virtual_machine import NormaVM

def run_program(program_file: str, registers: dict):
    """
    Carrega um programa, cria a VM e executa.
    :param program_file: caminho para o .txt do programa
    :param registers: dicionário com valores iniciais
    :return: tuple (trace, registers_finais)
    """
    program = parse_program(program_file)
    vm = NormaVM(program, registers)
    vm.run()
    return vm.trace, vm.registers
