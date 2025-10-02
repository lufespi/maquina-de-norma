import tkinter as tk
from tkinter import messagebox
import os
from core.executor import run_program
from core.trace_formatter import format_trace

def start_gui():
    # ---------- JANELA PRINCIPAL ----------
    root = tk.Tk()
    root.title("Simulador Máquina Norma")
    root.configure(bg="#e9eef5")

    # ---------- DIMENSÕES/POSIÇÃO DA JANELA ----------
    w, h = 1280, 760
    x = (root.winfo_screenwidth() // 2) - (w // 2)
    y = (root.winfo_screenheight() // 2) - (h // 2)
    root.geometry(f"{w}x{h}+{x}+{y}")
    root.resizable(True, True)

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

    frame_main.columnconfigure(0, weight=0)
    frame_main.columnconfigure(1, weight=1)
    frame_main.columnconfigure(2, weight=0)
    frame_main.columnconfigure(3, weight=0)
    frame_main.rowconfigure(3, weight=1)
    frame_main.rowconfigure(5, weight=2)

    # ---------- CONTROLES SUPERIORES ----------
    tk.Label(frame_main, text="Programa:", **label_style).grid(row=0, column=0, sticky="w", pady=5)
    programas = [f[:-4] for f in os.listdir("programs") if f.endswith(".txt")]
    if not programas:
        programas = ["Nenhum programa encontrado"]
    selected_program = tk.StringVar(value=programas[0])
    dropdown = tk.OptionMenu(frame_main, selected_program, *programas)
    dropdown.config(bg="#ffffff", fg="#333", relief="solid", width=35, font=("Segoe UI", 12))
    dropdown.grid(row=0, column=1, columnspan=3, sticky="ew", pady=5, padx=10)

    tk.Label(frame_main, text="Qtd Registradores:", **label_style).grid(row=1, column=0, sticky="w", pady=5)
    qtd_var = tk.IntVar(value=2)
    qtd_spin = tk.Spinbox(frame_main, from_=1, to=100, textvariable=qtd_var, width=5, **entry_style)
    qtd_spin.grid(row=1, column=1, sticky="w", pady=5, padx=10)

    min_warning_label = tk.Label(frame_main, text="", fg="#c0392b", bg="#e9eef5", font=("Segoe UI", 11, "bold"))
    min_warning_label.grid(row=2, column=0, columnspan=4, sticky="w", padx=5)

    btn_frame = tk.Frame(frame_main, bg="#e9eef5")
    btn_frame.grid(row=1, column=2, columnspan=2, sticky="w", padx=10)

    # ---------- ÁREA DE REGISTRADORES ----------
    canvas_frame = tk.Frame(frame_main, bg="#e9eef5")
    canvas_frame.grid(row=3, column=0, columnspan=4, sticky="nsew", pady=5)

    canvas = tk.Canvas(canvas_frame, bg="#e9eef5", highlightthickness=0, height=220)
    scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    frame_regs = tk.Frame(canvas, bg="#e9eef5")
    window_id = canvas.create_window((0, 0), window=frame_regs, anchor="nw")

    def _on_canvas_configure(event):
        canvas.itemconfig(window_id, width=event.width)
        canvas.configure(scrollregion=canvas.bbox("all"))
    canvas.bind("<Configure>", _on_canvas_configure)

    reg_entries = []

    import re

    RE_SE_ZERO = re.compile(r"se\s+zero_([a-zA-Z_][\w]*)", re.I)
    RE_ADD_SUB = re.compile(r"fa[cç]a\s+(?:add|sub)_([a-zA-Z_][\w]*)", re.I)
    RE_MACRO_PAREN = re.compile(
        r"fa[cç]a\s+[A-Z_]+\s*\(\s*([a-zA-Z_][\w]*(?:\s*,\s*[a-zA-Z_][\w]*)*)\s*\)",
        re.I
    )
    RE_MACRO_SPACE = re.compile(
        r"fa[cç]a\s+[A-Z_]+((?:\s+[a-zA-Z_][\w]*){1,8})",
        re.I
    )

    # ---------- FUNÇÃO PARA CALCULAR MÍNIMO DE REGISTRADORES ----------
    def compute_min_regs_for_program(path: str) -> int:
        if not os.path.exists(path):
            return 1
        with open(path, "r", encoding="utf-8") as fh:
            text = fh.read()

        text = re.sub(r"(//.*|#.*)$", "", text, flags=re.MULTILINE).lower()

        regs = set()

        for m in RE_SE_ZERO.finditer(text):
            regs.add(m.group(1))

        for m in RE_ADD_SUB.finditer(text):
            regs.add(m.group(1))

        for m in RE_MACRO_PAREN.finditer(text):
            args = m.group(1)
            for token in [t.strip() for t in args.split(",")]:
                if token:
                    regs.add(token)

        for m in RE_MACRO_SPACE.finditer(text):
            args_str = m.group(1)
            tokens = [t.strip() for t in args_str.split()]
            for token in tokens:
                if token:
                    regs.add(token)

        return max(1, len(regs))

    current_min_required = {"val": 1}

    # ---------- FUNÇÃO PARA DETECTAR MUDANÇAS NA INSTRUÇÃO ESCOLHIDA ----------
    def on_program_change(*_args):
        path = f"programs/{selected_program.get()}.txt"
        min_needed = compute_min_regs_for_program(path)
        min_needed = max(1, min_needed - 1)

        current_min_required["val"] = min_needed

        try:
            qtd_spin.config(from_=min_needed)
        except Exception:
            pass

        if min_needed > 1:
            min_warning_label.config(text=f"Este programa requer no mínimo {min_needed} registradores.", fg="#c0392b")
        else:
            min_warning_label.config(text="")

        if qtd_var.get() < min_needed:
            qtd_var.set(min_needed)
            messagebox.showwarning("Aviso", f"O programa selecionado requer pelo menos {min_needed} registradores. O valor foi ajustado.")

    selected_program.trace_add("write", on_program_change)
    on_program_change()

    # ---------- FUNÇÃO PARA GERAR CAMPOS DOS REGISTRADORES ----------
    def gerar_campos():
        min_needed = current_min_required["val"]
        qtd = qtd_var.get()
        if qtd < min_needed:
            messagebox.showwarning("Aviso", f"Não é possível usar menos que {min_needed} registradores para o programa selecionado.")
            qtd_var.set(min_needed)
            qtd = min_needed

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

    # ---------- FUNÇÃO PARA EXCLUIR CAMPOS DOS REGISTRADORES ----------
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

    btn_executar = tk.Button(frame_main, text="Executar", **button_blue)
    btn_executar.grid(row=4, column=0, columnspan=4, pady=10)

    # ---------- SAÍDA (TRACE) ----------
    output_frame = tk.Frame(frame_main, bg="#000000", bd=1, relief="sunken")
    output_frame.grid(row=5, column=0, columnspan=4, pady=(10, 22), sticky="nsew")

    output_vscroll = tk.Scrollbar(output_frame, orient="vertical")
    output_hscroll = tk.Scrollbar(output_frame, orient="horizontal")
    output_vscroll.pack(side="right", fill="y")
    output_hscroll.pack(side="bottom", fill="x")

    output = tk.Text(output_frame, wrap="none", width=150, height=16, bg="#1e1e1e", fg="#ffffff",
                     insertbackground="white", font=("Consolas", 12), relief="flat",
                     yscrollcommand=output_vscroll.set, xscrollcommand=output_hscroll.set)
    output.pack(side="left", fill="both", expand=True)

    output_vscroll.config(command=output.yview)
    output_hscroll.config(command=output.xview)

    spacer = tk.Frame(frame_main, height=8, bg="#e9eef5")
    spacer.grid(row=6, column=0, columnspan=4)

    # ---------- FUNÇÃO PARA EXECUTAR O PROGRAMA ----------
    def run():
        path = f"programs/{selected_program.get()}.txt"
        if not os.path.exists(path):
            messagebox.showerror("Erro", f"Arquivo '{path}' não encontrado!")
            return
        min_needed = current_min_required["val"]
        if qtd_var.get() < min_needed:
            messagebox.showwarning("Aviso", f"O programa selecionado requer pelo menos {min_needed} registradores. Ajuste antes de executar.")
            return

        registers = {nome_var.get(): valor_var.get() for nome_var, valor_var in reg_entries}
        try:
            trace, final_registers = run_program(path, registers)
            output.delete(1.0, tk.END)
            output.insert(tk.END, format_trace(trace, final_registers))
            canvas.configure(scrollregion=canvas.bbox("all"))
        except ZeroDivisionError:
            messagebox.showerror("Erro de Execução", "Não é possível dividir por zero!")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

    btn_executar.config(command=run)

    root.mainloop()
