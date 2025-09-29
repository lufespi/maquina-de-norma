import tkinter as tk
from tkinter import messagebox
import os
from src.parser import parse_program
from src.virtual_machine import NormaVM

def start_gui():
    root = tk.Tk()
    root.title("Simulador Máquina Norma")
    root.geometry("520x550")
    root.configure(bg="#f0f2f5")
    root.resizable(False, False)

    # -------- Centralizar janela no Windows --------
    root.update_idletasks()
    w = 520
    h = 550
    x = (root.winfo_screenwidth() // 2) - (w // 2)
    y = (root.winfo_screenheight() // 2) - (h // 2)
    root.geometry(f"{w}x{h}+{x}+{y}")

    # -------- Estilo Geral --------
    label_style = {"bg": "#f0f2f5", "fg": "#333", "font": ("Segoe UI", 10, "bold")}
    entry_style = {"bg": "#fff", "fg": "#333", "relief": "solid", "bd": 1}
    button_style = {"bg": "#4CAF50", "fg": "white", "activebackground": "#45a049",
                    "activeforeground": "white", "relief": "raised", "font": ("Segoe UI", 10, "bold")}

    frame_main = tk.Frame(root, bg="#f0f2f5", padx=10, pady=10)
    frame_main.pack(fill="both", expand=True)

    # ------------------------------
    # 1. Dropdown de Programas
    # ------------------------------
    tk.Label(frame_main, text="Programa:", **label_style).grid(row=0, column=0, sticky="w", pady=5)

    programas = [f[:-4] for f in os.listdir("programs") if f.endswith(".txt")]
    if not programas:
        programas = ["Nenhum programa encontrado"]

    selected_program = tk.StringVar(value=programas[0])
    dropdown = tk.OptionMenu(frame_main, selected_program, *programas)
    dropdown.config(bg="#fff", fg="#333", relief="solid", width=25)
    dropdown.grid(row=0, column=1, columnspan=2, sticky="ew", pady=5)

    # ------------------------------
    # 2. Quantidade de Registradores + Botão Gerar
    # ------------------------------
    tk.Label(frame_main, text="Qtd Registradores:", **label_style).grid(row=1, column=0, sticky="w", pady=5)
    qtd_var = tk.IntVar(value=2)
    qtd_spin = tk.Spinbox(frame_main, from_=1, to=10, textvariable=qtd_var, width=5, **entry_style)
    qtd_spin.grid(row=1, column=1, sticky="w", pady=5)

    frame_regs = tk.Frame(frame_main, bg="#f0f2f5")
    reg_entries = []

    def gerar_campos():
        for widget in frame_regs.winfo_children():
            widget.destroy()
        reg_entries.clear()

        qtd = qtd_var.get()
        for i in range(qtd):
            frame = tk.Frame(frame_regs, bg="#f0f2f5", pady=2)
            frame.pack(anchor="w")
            nome_var = tk.StringVar(value=chr(97 + i))
            valor_var = tk.IntVar(value=0)

            tk.Label(frame, text=f"Reg {i+1}:", **label_style).pack(side=tk.LEFT, padx=2)
            tk.Entry(frame, textvariable=nome_var, width=5, **entry_style).pack(side=tk.LEFT, padx=2)
            tk.Label(frame, text="=", **label_style).pack(side=tk.LEFT, padx=2)
            tk.Entry(frame, textvariable=valor_var, width=5, **entry_style).pack(side=tk.LEFT, padx=2)

            reg_entries.append((nome_var, valor_var))

        frame_regs.grid(row=3, column=0, columnspan=3, sticky="w", pady=5)
        btn_executar.grid(row=4, column=0, columnspan=3, pady=10)

    btn_gerar = tk.Button(frame_main, text="Gerar Campos", command=gerar_campos, **button_style)
    btn_gerar.grid(row=1, column=2, padx=5)

    # ------------------------------
    # 3. Output estilizado
    # ------------------------------
    output = tk.Text(frame_main, width=60, height=15, bg="#1e1e1e", fg="#ffffff",
                     insertbackground="white", font=("Consolas", 10), relief="solid", bd=1)
    output.grid(row=5, column=0, columnspan=3, pady=10)

    # ------------------------------
    # 4. Botão Executar
    # ------------------------------
    def run_program():
        fname = selected_program.get()
        path = f"programs/{fname}.txt"

        if not os.path.exists(path):
            messagebox.showerror("Erro", f"O arquivo '{path}' não foi encontrado!")
            return

        try:
            program = parse_program(path)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar programa: {e}")
            return

        registers = {}
        for nome_var, valor_var in reg_entries:
            registers[nome_var.get()] = valor_var.get()

        vm = NormaVM(program, registers)
        vm.run()

        output.delete(1.0, tk.END)
        output.insert(tk.END, "=== TRACE DE EXECUÇÃO ===\n")
        for label, regs in vm.trace:
            estado = ", ".join(f"{k}={v}" for k, v in regs.items())
            output.insert(tk.END, f"Rótulo {label}: {estado}\n")
            output.see(tk.END)

        output.insert(tk.END, "\n=== ESTADO FINAL ===\n")
        estado_final = ", ".join(f"{k}={v}" for k, v in vm.registers.items())
        output.insert(tk.END, estado_final + "\n")
        output.insert(tk.END, "=== FIM ===")

    btn_executar = tk.Button(frame_main, text="Executar", command=run_program,
                             bg="#0078D7", fg="white", activebackground="#005A9E",
                             activeforeground="white", font=("Segoe UI", 11, "bold"), relief="raised")

    root.mainloop()
