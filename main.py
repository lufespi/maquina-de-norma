from ui.cli import start_cli
from ui.gui import start_gui

def main():
    print("=== Simulador Máquina Norma ===")
    print("1 - Modo CLI (console)")
    print("2 - Modo GUI (janela)")
    modo = input("Escolha o modo: ")

    if modo == "1":
        start_cli()
    elif modo == "2":
        start_gui()
    else:
        print("Opção inválida!")

if __name__ == "__main__":
    main()
