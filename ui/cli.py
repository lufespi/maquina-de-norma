import os
from core.executor import run_program
from core.trace_formatter import format_trace
import time, pathlib
def salvar_traco(program_path, trace_text):
    base = pathlib.Path(program_path).stem
    ts = time.strftime('%Y%m%d-%H%M%S')
    out = pathlib.Path(__file__).resolve().parents[1] / 'runs' / f'{base}_{ts}.txt'
    out.write_text(trace_text, encoding='utf-8')
    print(f'\n[OK] Traço salvo em: {out}')


def start_cli():
    while True:
        print("\n=== Simulador Máquina Norma (CLI) ===")
        print("1 - Listar programas")
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
            print("Opção inválida!")

def listar_programas():
    print("\n=== Programas disponíveis ===")
    arquivos = [f for f in os.listdir("programs") if f.endswith(".txt")]
    for i, arq in enumerate(arquivos, 1):
        print(f"{i}. {arq}")

def executar_programa():
    fname = input("Digite o nome do programa (sem extensão): ")
    path = f"programs/{fname}.txt"

    if not os.path.exists(path):
        print(f"Erro: arquivo '{path}' não encontrado!")
        return

    registers = {}
    qtd = int(input("Quantos registradores deseja usar? "))
    for i in range(qtd):
        nome = input(f"Nome do registrador {i+1}: ")
        valor = int(input(f"Valor inicial de {nome}: "))
        registers[nome] = valor

    try:
        trace, final_registers = run_program(path, registers)
        print(format_trace(trace, final_registers))
    except ZeroDivisionError:
        print("Erro: Divisão por zero!")
    except Exception as e:
        print(f"Erro de execução: {e}")
