import re
from typing import Dict, Tuple, Optional

from src.macros import has_macro, expand_macro

# ========================
# Regex Patterns
# ========================

COMMENT_PATTERN = re.compile(r"\s*(//.*|#.*)$")
TEST_PATTERN = re.compile(r"^\s*(\d+)\s*:\s*se\s+zero_([a-z])\s+ent[aã]o\s+v[áa]_para\s+(\d+)\s+sen[aã]o\s+v[áa]_para\s+(\d+)\s*$", re.I)
OPERATION_PATTERN = re.compile(r"^\s*(\d+)\s*:\s*f(aç|ac)a\s+(add|sub)_([a-z])\s+v[áa]_para\s+(\d+)\s*$", re.I)
HALT_PATTERN = re.compile(r"^\s*(\d+)\s*:\s*(fim)\s*$", re.I)
MACRO_PATTERN = re.compile(r"^\s*(\d+)\s*:\s*f(?:aç|ac)a\s+([A-Z]+)\s*\(?\s*([a-z](?:\s+[a-z]){2,3})\s*\)?\s+v[áa]_para\s+(\d+)\s*$", re.I)

def remove_comment(line: str) -> str:
    return COMMENT_PATTERN.sub("", line).strip()

# ========================
# Parsers de linha
# ========================

def parse_macro_line(line: str) -> Optional[Tuple[int, str, dict]]:
    m = MACRO_PATTERN.match(line)
    if not m:
        return None
    lbl, name, regs_str, nxt = m.groups()
    lbl, nxt = int(lbl), int(nxt)
    name = name.upper()
    regs = [r.lower() for r in regs_str.split()]
    if len(regs) not in (3, 4):
        raise ValueError(f"Macro '{name}' requer 3 ou 4 registradores, recebeu {len(regs)}.")
    if not has_macro(name):
        raise ValueError(f"Macro '{name}' não suportada.")
    return lbl, "macro", {"name": name, "args": regs, "next": nxt}


def parse_test_line(line: str) -> Optional[Tuple[int, str, dict]]:
    m = TEST_PATTERN.match(line)
    if not m:
        return None
    lbl, reg, t, f_ = m.groups()
    return int(lbl), "test_zero", {
        "reg": reg.lower(),
        "t": int(t),
        "f": int(f_),
        "text": f"se zero_{reg.lower()} então vá_para {t} senão vá_para {f_}",
    }


def parse_op_line(line: str) -> Optional[Tuple[int, str, dict]]:
    m = OPERATION_PATTERN.match(line)
    if not m:
        return None
    lbl, _, op, reg, goto = m.groups()
    op, lbl, goto = op.lower(), int(lbl), int(goto)
    return lbl, op, {
        "reg": reg.lower(),
        "goto": goto,
        "text": f"faça {op}_{reg.lower()} vá_para {goto}",
    }


def parse_halt_line(line: str) -> Optional[Tuple[int, str, dict]]:
    m = HALT_PATTERN.match(line)
    if not m:
        return None
    lbl, _ = m.groups()
    return int(lbl), "halt", {"text": "fim"}


# ========================
# Normalização
# ========================

def normalize_instruction(kind: str, data: dict) -> dict:
    """Transforma tuplas intermediárias em instruções finais."""
    if kind == "test_zero":
        return {
            "type": "test_zero",
            "reg": data["reg"],
            "goto_true": data["t"],
            "goto_false": data["f"],
            "text": data["text"],
        }
    elif kind in ("add", "sub"):
        return {
            "type": kind,
            "reg": data["reg"],
            "goto": data["goto"],
            "text": data["text"],
        }
    elif kind == "halt":
        return {"type": "halt", "text": "fim"}
    else:
        raise ValueError(f"Tipo de instrução inesperado: {kind}")


def expand_macro_entry(lbl: int, data: dict, next_label: int) -> Tuple[Dict[int, dict], int]:
    """Expande uma macro em instruções concretas."""
    name, regs, goto_after = data["name"], data["args"], data["next"]
    rel_code = expand_macro(name, regs)

    rel_to_abs = {0: lbl}
    for i in range(1, len(rel_code)):
        rel_to_abs[i] = next_label
        next_label += 1

    expanded: Dict[int, dict] = {}
    for i, instr in enumerate(rel_code):
        abs_lbl = rel_to_abs[i]
        itype = instr["type"]

        if itype == "test_zero":
            expanded[abs_lbl] = {
                "type": "test_zero",
                "reg": instr["reg"],
                "goto_true": goto_after if instr["goto_true"] == len(rel_code) else rel_to_abs[instr["goto_true"]],
                "goto_false": goto_after if instr["goto_false"] == len(rel_code) else rel_to_abs[instr["goto_false"]],
                "text": instr.get("text") or f"se zero_{instr['reg']} então vá_para {goto_after}",
            }
        elif itype in ("add", "sub"):
            expanded[abs_lbl] = {
                "type": itype,
                "reg": instr["reg"],
                "goto": goto_after if instr["goto"] == len(rel_code) else rel_to_abs[instr["goto"]],
                "text": instr.get("text") or f"faça {itype}_{instr['reg']} vá_para {goto_after}",
            }
        elif itype in ("goto", "halt"):
            expanded[abs_lbl] = {
                "type": "goto",
                "goto": goto_after,
                "text": f"vá_para {goto_after}",
            }
        else:
            raise ValueError(f"Tipo de instrução desconhecido em macro: {itype}")

    return expanded, next_label


def parse_program(path: str) -> Dict[int, dict]:
    """Lê um programa em texto e retorna um dicionário {label: instrução}."""
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    entries = []
    labels_seen = set()

    for line in lines:
        line = remove_comment(line)
        if not line:
            continue

        for parser in (parse_macro_line, parse_test_line, parse_op_line, parse_halt_line):
            entry = parser(line)
            if entry:
                entries.append(entry)
                labels_seen.add(entry[0])
                break
        else:
            raise ValueError(f"Linha inválida: '{line}'")

    next_label = (max(labels_seen) + 1) if labels_seen else 1
    program: Dict[int, dict] = {}

    for lbl, kind, data in entries:
        if kind == "macro":
            expanded, next_label = expand_macro_entry(lbl, data, next_label)
            program.update(expanded)
        else:
            program[lbl] = normalize_instruction(kind, data)

    return program