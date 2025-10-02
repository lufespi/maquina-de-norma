import sys

def main():
    mode = None
    if len(sys.argv) >= 2:
        mode = sys.argv[1].strip().lower()
    else:
        print("Uso: python main.py [cli|gui]")
        mode = input("Escolha o modo (cli/gui): ").strip().lower()

    if mode == "cli":
        from ui.cli import start_cli
        start_cli()
    elif mode == "gui":
        from ui.gui import start_gui
        start_gui()
    else:
        print("Modo inválido. Use 'cli' ou 'gui'.")

if __name__ == "__main__":
    main()
