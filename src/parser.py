import re
from typing import Dict
from src.macros import has_macro, expand_macro

COMMENT_PATTERN = re.compile(r"\s*(//.*|#.*)$")
TEST_PATTERN    = re.compile(r"^\s*(\d+)\s*:\s*se\s+zero_([a-z])\s+ent[aã]o\s+v[áa]_para\s+(\d+)\s+sen[aã]o\s+v[áa]_para\s+(\d+)\s*$", re.I)
OPERATION_PATTERN = re.compile(r"^\s*(\d+)\s*:\s*f(aç|ac)a\s+(add|sub)_([a-z])\s+v[áa]_para\s+(\d+)\s*$", re.I)
HALT_PATTERN   = re.compile(r"^\s*(\d+)\s*:\s*(fim)\s*$", re.I)

# Macro com 3 ou 4 registradores
MACRO_PATTERN  = re.compile(
    r"^\s*(\d+)\s*:\s*f(?:aç|ac)a\s+([A-Z]+)\s*\(?\s*([a-z](?:\s+[a-z]){2,3})\s*\)?\s+v[áa]_para\s+(\d+)\s*$",
    re.I
)

def remove_comment(line: str) -> str:
    return COMMENT_PATTERN.sub("", line).strip()

def parse_program(path: str) -> Dict[int, dict]:
    with open(path, "r", encoding="utf-8") as f:
        raw_lines = f.readlines()

    entries = []
    labels_seen = set()

    for raw in raw_lines:
        line = remove_comment(raw)
        if not line:
            continue

        m = MACRO_PATTERN.match(line)
        if m:
            lbl, name, regs_str, nxt = m.groups()
            lbl = int(lbl); nxt = int(nxt)
            name = name.upper()
            regs = [r.lower() for r in regs_str.split()]
            if len(regs) not in (3,4):
                raise ValueError(f"Macro '{name}' requer 3 ou 4 registradores, recebeu {len(regs)}.")
            if not has_macro(name):
                raise ValueError(f"Macro '{name}' não suportada.")
            entries.append((lbl, "macro", {"name": name, "args": regs, "next": nxt}))
            labels_seen.add(lbl)
            continue

        m = TEST_PATTERN.match(line)
        if m:
            lbl, reg, t, f_ = m.groups()
            lbl = int(lbl); t = int(t); f_ = int(f_)
            entries.append((lbl, "test_zero", {"reg": reg.lower(), "t": t, "f": f_,
                                               "text": f"se zero_{reg.lower()} então vá_para {t} senão vá_para {f_}"}))
            labels_seen.add(lbl)
            continue

        m = OPERATION_PATTERN.match(line)
        if m:
            lbl, _, op, reg, goto = m.groups()
            lbl = int(lbl); goto = int(goto); op = op.lower()
            entries.append((lbl, op, {"reg": reg.lower(), "goto": goto,
                                      "text": f"faça {op}_{reg.lower()} vá_para {goto}"}))
            labels_seen.add(lbl)
            continue

        m = HALT_PATTERN.match(line)
        if m:
            lbl, _ = m.groups()
            lbl = int(lbl)
            entries.append((lbl, "halt", {"text": "fim"}))
            labels_seen.add(lbl)
            continue

        raise ValueError(f"Linha inválida: '{line}'")

    next_label = (max(labels_seen) + 1) if labels_seen else 1
    program: Dict[int, dict] = {}

    for (lbl, kind, data) in entries:
        if kind != "macro":
            if kind == "test_zero":
                program[lbl] = {"type": "test_zero", "reg": data["reg"],
                                "goto_true": data["t"], "goto_false": data["f"],
                                "text": data["text"]}
            elif kind in ("add", "sub"):
                program[lbl] = {"type": kind, "reg": data["reg"],
                                "goto": data["goto"], "text": data["text"]}
            elif kind == "halt":
                program[lbl] = {"type": "halt", "text": "fim"}
            continue

        # Macro encontrada
        name  = data["name"]
        regs  = data["args"]
        goto_after = data["next"]

        rel_code = expand_macro(name, regs)
        rel_to_abs = {0: lbl}
        for i in range(1, len(rel_code)):
            rel_to_abs[i] = next_label
            next_label += 1

        for i, instr in enumerate(rel_code):
            abs_lbl = rel_to_abs[i]
            itype = instr["type"]
            out = {"type": itype}

            if itype == "test_zero":
                out["reg"] = instr["reg"]
                out["goto_true"]  = goto_after if instr["goto_true"] == len(rel_code) else rel_to_abs[instr["goto_true"]]
                out["goto_false"] = goto_after if instr["goto_false"] == len(rel_code) else rel_to_abs[instr["goto_false"]]
                out["text"] = instr.get("text") or f"se zero_{out['reg']} então vá_para {out['goto_true']} senão vá_para {out['goto_false']}"
            elif itype in ("add", "sub"):
                out["reg"] = instr["reg"]
                out["goto"] = goto_after if instr["goto"] == len(rel_code) else rel_to_abs[instr["goto"]]
                out["text"] = instr.get("text") or f"faça {itype}_{out['reg']} vá_para {out['goto']}"
            elif itype in ("goto", "halt"):
                out = {"type": "goto", "goto": goto_after, "text": f"vá_para {goto_after}"}
            else:
                raise ValueError(f"Tipo de instrução desconhecido em macro: {itype}")

            program[abs_lbl] = out

    return program