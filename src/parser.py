# src/parser.py
import re

def parse_program(file_path):
    """
    Lê um programa monolítico (arquivo .txt) e retorna um dicionário {rótulo: instrução}.
    Ignora linhas em branco ou comentários (#).
    """
    program = {}
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip().lower()
            if not line or line.startswith("#"):
                continue

            match = re.match(r"(\d+):\s*(.*)", line)
            if not match:
                raise ValueError(f"Linha inválida no programa: {line}")

            label = int(match.group(1))
            instr = match.group(2)
            program[label] = instr

    if not program:
        raise ValueError("Programa vazio ou inválido.")

    return program
