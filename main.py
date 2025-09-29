from ui.cli import start_cli
from ui.gui import start_gui

if __name__ == "__main__":
    print("=== Simulador Máquina Norma ===")
    print("1 - Modo CLI (console)")
    print("2 - Modo GUI (janela)")
    modo = input("Escolha o modo: ")

    if modo == "2":
        start_gui()
    else:
        start_cli()
