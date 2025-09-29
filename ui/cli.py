# ui/cli.py
import os
from src.parser import parse_program
from src.virtual_machine import NormaVM

def start_cli():
    while True:
        print("\n=== Simulador Máquina Norma (CLI) ===")
        print("1 - Listar programas disponíveis")
        print("2 - Executar programa")
        print("3 - Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            listar_programas()
        elif opcao == "2":
            executar_programa()
        elif opcao == "3":
            print("Saindo... 👋")
            break
        else:
            print("Opção inválida, tente novamente.")

def listar_programas():
    print("\n=== Programas disponíveis ===")
    try:
        arquivos = os.listdir("programs")
        arquivos = [arq for arq in arquivos if arq.endswith(".txt")]
        if not arquivos:
            print("Nenhum programa encontrado em 'programs/'.")
        else:
            for i, arq in enumerate(arquivos, 1):
                print(f"{i}. {arq}")
    except FileNotFoundError:
        print("A pasta 'programs/' não foi encontrada.")

def executar_programa():
    fname = input("Digite o nome do programa (sem extensão): ")
    path = f"programs/{fname}.txt"

    if not os.path.exists(path):
        print(f"Erro: o arquivo '{path}' não existe!")
        return

    try:
        program = parse_program(path)
    except Exception as e:
        print(f"Erro ao carregar programa: {e}")
        return

    registers = {}
    qtd = int(input("Quantos registradores deseja usar? "))
    for i in range(qtd):
        nome = input(f"Nome do registrador {i+1}: ")
        valor = int(input(f"Valor inicial de {nome}: "))
        registers[nome] = valor

    vm = NormaVM(program, registers)
    vm.run()
    print("\n=== TRACE DE EXECUÇÃO ===")
    for label, regs in vm.trace:
        print(f"Rótulo {label}: {regs}")
    print("=== FIM ===")
