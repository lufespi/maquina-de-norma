import tkinter as tk
from tkinter import messagebox
import os
from core.executor import run_program
from core.trace_formatter import format_trace
import time, pathlib
def salvar_traco(program_path, trace_text):
    base = pathlib.Path(program_path).stem
    ts = time.strftime('%Y%m%d-%H%M%S')
    out = pathlib.Path(__file__).resolve().parents[1] / 'runs' / f'{base}_{ts}.txt'
    out.write_text(trace_text, encoding='utf-8')
    # GUI: feedback no console; a UI já mostra o texto
    print(f'[OK] Traço salvo em: {out}')


def start_gui():
    root = tk.Tk()
    root.title("Simulador Máquina Norma")
    root.configure(bg="#e9eef5")
    root.resizable(False, False)

    # Centraliza a janela
    w, h = 1280, 720
    x = (root.winfo_screenwidth() // 2) - (w // 2)
    y = (root.winfo_screenheight() // 2) - (h // 2)
    root.geometry(f"{w}x{h}+{x}+{y}")

    # ---------- ESTILOS ----------
    title_style = {"bg": "#2c3e50", "fg": "white", "font": ("Segoe UI", 20, "bold")}
    label_style = {"bg": "#e9eef5", "fg": "#2c3e50", "font": ("Segoe UI", 12, "bold")}
    entry_style = {"bg": "#ffffff", "fg": "#333", "relief": "solid", "bd": 1, "font": ("Segoe UI", 12)}
    button_green = {"bg": "#27ae60", "fg": "white", "activebackground": "#1e8449",
                    "activeforeground": "white", "relief": "flat", "font": ("Segoe UI", 12, "bold"), "width": 15}
    button_blue = {"bg": "#2980b9", "fg": "white", "activebackground": "#1f618d",
                   "activeforeground": "white", "relief": "flat", "font": ("Segoe UI", 14, "bold"), "width": 16}
    button_red_disabled = {"bg": "#e57373", "fg": "white", "relief": "flat",
                           "font": ("Segoe UI", 12, "bold"), "width": 15, "state": "disabled"}
    button_red_enabled = {"bg": "#c0392b", "fg": "white", "activebackground": "#922b21",
                          "activeforeground": "white", "relief": "flat", "font": ("Segoe UI", 12, "bold"), "width": 15}

    # ---------- CABEÇALHO ----------
    header = tk.Frame(root, bg="#2c3e50", height=60)
    header.pack(fill="x")
    tk.Label(header, text="Simulador Máquina Norma", **title_style).pack(pady=10)

    # ---------- FRAME PRINCIPAL ----------
    frame_main = tk.Frame(root, bg="#e9eef5", padx=20, pady=10)
    frame_main.pack(fill="both", expand=True)

    # Linha 1: Programas
    tk.Label(frame_main, text="Programa:", **label_style).grid(row=0, column=0, sticky="w", pady=5)
    programas = [f[:-4] for f in os.listdir("programs") if f.endswith(".txt")]
    if not programas:
        programas = ["Nenhum programa encontrado"]
    selected_program = tk.StringVar(value=programas[0])
    dropdown = tk.OptionMenu(frame_main, selected_program, *programas)
    dropdown.config(bg="#ffffff", fg="#333", relief="solid", width=35, font=("Segoe UI", 12))
    dropdown.grid(row=0, column=1, columnspan=3, sticky="ew", pady=5, padx=10)

    # Linha 2: Quantidade + Botões
    tk.Label(frame_main, text="Qtd Registradores:", **label_style).grid(row=1, column=0, sticky="w", pady=5)
    qtd_var = tk.IntVar(value=2)
    qtd_spin = tk.Spinbox(frame_main, from_=1, to=100, textvariable=qtd_var, width=5, **entry_style)
    qtd_spin.grid(row=1, column=1, sticky="w", pady=5, padx=10)

    # Frame para botões lado a lado
    btn_frame = tk.Frame(frame_main, bg="#e9eef5")
    btn_frame.grid(row=1, column=2, columnspan=2, sticky="w", padx=10)

    canvas_frame = tk.Frame(frame_main, bg="#e9eef5")
    canvas_frame.grid(row=3, column=0, columnspan=4, sticky="nsew", pady=5)

    canvas = tk.Canvas(canvas_frame, bg="#e9eef5", highlightthickness=0, height=220)
    scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    frame_regs = tk.Frame(canvas, bg="#e9eef5")
    canvas.create_window((0, 0), window=frame_regs, anchor="nw")

    reg_entries = []

    # ---------- FUNÇÕES ----------
    def gerar_campos():
        for widget in frame_regs.winfo_children():
            widget.destroy()
        reg_entries.clear()
        qtd = qtd_var.get()
        for i in range(qtd):
            frame = tk.Frame(frame_regs, bg="#e9eef5", pady=2)
            frame.pack(anchor="w", pady=3)
            nome_var = tk.StringVar(value=chr(97 + (i % 26)))
            valor_var = tk.IntVar(value=0)
            tk.Label(frame, text=f"Registrador {i+1}:", **label_style).pack(side=tk.LEFT, padx=5)
            tk.Entry(frame, textvariable=nome_var, width=6, **entry_style).pack(side=tk.LEFT, padx=5)
            tk.Label(frame, text="=", **label_style).pack(side=tk.LEFT, padx=5)
            tk.Entry(frame, textvariable=valor_var, width=10, **entry_style).pack(side=tk.LEFT, padx=5)
            reg_entries.append((nome_var, valor_var))
        frame_regs.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))
        btn_excluir.config(**button_red_enabled, state="normal")

    def excluir_campos():
        if messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir todos os registradores?"):
            for widget in frame_regs.winfo_children():
                widget.destroy()
            reg_entries.clear()
            canvas.configure(scrollregion=(0, 0, 0, 0))
            btn_excluir.config(**button_red_disabled)

    btn_gerar = tk.Button(btn_frame, text="Gerar Campos", command=gerar_campos, **button_green)
    btn_gerar.pack(side=tk.LEFT, padx=5)

    btn_excluir = tk.Button(btn_frame, text="Excluir Campos", command=excluir_campos, **button_red_disabled)
    btn_excluir.pack(side=tk.LEFT, padx=5)

    # ---------- BOTÃO EXECUTAR ----------
    btn_executar = tk.Button(frame_main, text="Executar", **button_blue)
    btn_executar.grid(row=4, column=0, columnspan=4, pady=10)

    # ---------- OUTPUT ----------
    output_frame = tk.Frame(frame_main, bg="#000000", bd=1, relief="sunken")
    output_frame.grid(row=5, column=0, columnspan=4, pady=10, sticky="nsew")

    output_scroll = tk.Scrollbar(output_frame)
    output_scroll.pack(side="right", fill="y")

    output = tk.Text(output_frame, width=120, height=12, bg="#1e1e1e", fg="#ffffff",
                     insertbackground="white", font=("Consolas", 12), relief="flat",
                     yscrollcommand=output_scroll.set)
    output.pack(side="left", fill="both", expand=True)
    output_scroll.config(command=output.yview)

    def run():
        path = f"programs/{selected_program.get()}.txt"
        if not os.path.exists(path):
            messagebox.showerror("Erro", f"Arquivo '{path}' não encontrado!")
            return
        registers = {nome_var.get(): valor_var.get() for nome_var, valor_var in reg_entries}
        try:
            trace, final_registers = run_program(path, registers)
            output.delete(1.0, tk.END)
            output.insert(tk.END, format_trace(trace, final_registers))
        except ZeroDivisionError:
            messagebox.showerror("Erro de Execução", "Não é possível dividir por zero!")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

    btn_executar.config(command=run)

    root.mainloop()
