# Definições de macros em forma de funções que retornam listas de instruções.

def test_zero(reg, goto_true, goto_false):
    return {
        "type": "test_zero",
        "reg": reg,
        "goto_true": goto_true,
        "goto_false": goto_false
    }


def add(reg, goto):
    return {
        "type": "add",
        "reg": reg,
        "goto": goto
    }


def sub(reg, goto):
    return {
        "type": "sub",
        "reg": reg,
        "goto": goto
    }


def halt():
    return {
        "type": "halt"
    }


def layout_to_instruction_list(layout_dict):
    # Converte dict(label->instr) em lista 0..N de instruções relativas
    labels = sorted(layout_dict.keys())
    idx_map = {lbl: i for i, lbl in enumerate(labels)}
    rel = []
    for lbl in labels:
        ins = layout_dict[lbl].copy()
        if ins["type"] == "test_zero":
            ins["goto_true"] = idx_map.get(ins["goto_true"], ins["goto_true"])
            ins["goto_false"] = idx_map.get(ins["goto_false"], ins["goto_false"])
        elif ins["type"] in ("add", "sub"):
            ins["goto"] = idx_map.get(ins["goto"], ins["goto"])
        rel.append(ins)
    return rel


# ---------- MENOR(a,b,c): menor valor em c ----------
def macro_min(a, b, c):
    layout = {
        0: test_zero(c, 2, 1),
        1: sub(c, 0),
        2: test_zero(a, 7, 3),
        3: test_zero(b, 7, 4),
        4: sub(a, 5),
        5: sub(b, 6),
        6: add(c, 2),
        7: halt(),
    }
    layout[0]["text"] = f"se zero_{c} então vá_para 2 senão vá_para 1"
    layout[1]["text"] = f"faça sub_{c} vá_para 0"
    layout[2]["text"] = f"se zero_{a} então vá_para 7 senão vá_para 3"
    layout[3]["text"] = f"se zero_{b} então vá_para 7 senão vá_para 4"
    layout[4]["text"] = f"faça sub_{a} vá_para 5"
    layout[5]["text"] = f"faça sub_{b} vá_para 6"
    layout[6]["text"] = f"faça add_{c} vá_para 2"
    layout[7]["text"] = "fim"
    return layout_to_instruction_list(layout)


# ---------- MAIOR(a,b,c,d): maior valor em d (usa c como auxiliar) ----------
def macro_max(a, b, c, d):
    layout = {
        0: test_zero(c, 2, 1),
        1: sub(c, 0),
        2: test_zero(d, 4, 3),
        3: sub(d, 2),
        4: test_zero(a, 9, 5),
        5: test_zero(b, 12, 6),
        6: sub(a, 7),
        7: sub(b, 8),
        8: add(c, 4),
        9: test_zero(b, 15, 10),
        10: sub(b, 11),
        11: add(d, 9),
        12: test_zero(a, 15, 13),
        13: sub(a, 14),
        14: add(d, 12),
        15: test_zero(c, 18, 16),
        16: sub(c, 17),
        17: add(d, 15),
        18: halt(),
    }
    layout[0]["text"] = f"se zero_{c} então vá_para 2 senão vá_para 1"
    layout[1]["text"] = f"faça sub_{c} vá_para 0"
    layout[2]["text"] = f"se zero_{d} então vá_para 4 senão vá_para 3"
    layout[3]["text"] = f"faça sub_{d} vá_para 2"
    layout[4]["text"] = f"se zero_{a} então vá_para 9 senão vá_para 5"
    layout[5]["text"] = f"se zero_{b} então vá_para 12 senão vá_para 6"
    layout[6]["text"] = f"faça sub_{a} vá_para 7"
    layout[7]["text"] = f"faça sub_{b} vá_para 8"
    layout[8]["text"] = f"faça add_{c} vá_para 4"
    layout[9]["text"] = f"se zero_{b} vá_para 15 senão vá_para 10"
    layout[10]["text"] = f"faça sub_{b} vá_para 11"
    layout[11]["text"] = f"faça add_{d} vá_para 9"
    layout[12]["text"] = f"se zero_{a} então vá_para 15 senão vá_para 13"
    layout[13]["text"] = f"faça sub_{a} vá_para 14"
    layout[14]["text"] = f"faça add_{d} vá_para 12"
    layout[15]["text"] = f"se zero_{c} então vá_para 18 senão vá_para 16"
    layout[16]["text"] = f"faça sub_{c} vá_para 17"
    layout[17]["text"] = f"faça add_{d} vá_para 15"
    layout[18]["text"] = "fim"
    return layout_to_instruction_list(layout)


# ---------- IGUAL(a,b,c): c=1 se a==b, senão c=0 ----------
def macro_equal(a, b, c):
    layout = {
        1: test_zero(c, 3, 2),
        2: sub(c, 1),
        3: test_zero(a, 7, 4),
        4: test_zero(b, 9, 5),
        5: sub(a, 6),
        6: sub(b, 3),
        7: test_zero(b, 8, 9),
        8: add(c, 9),
        9: halt(),
    }
    layout[1]["text"] = f"se zero_{c} então vá_para 3 senão vá_para 2"
    layout[2]["text"] = f"faça sub_{c} vá_para 1"
    layout[3]["text"] = f"se zero_{a} vá_para 7 senão vá_para 4"
    layout[4]["text"] = f"se zero_{b} vá_para 9 senão vá_para 5"
    layout[5]["text"] = f"faça sub_{a} vá_para 6"
    layout[6]["text"] = f"faça sub_{b} vá_para 3"
    layout[7]["text"] = f"se zero_{b} vá_para 8 senão vá_para 9"
    layout[8]["text"] = f"faça add_{c} vá_para 9"
    layout[9]["text"] = "fim"
    return layout_to_instruction_list(layout)


# ---------- Tabela de macros ----------
MACROS = {
    "MENOR": macro_min,
    "MAIOR": macro_max,
    "IGUAL": macro_equal,
}

def has_macro(name: str) -> bool:
    return name.upper() in MACROS


def expand_macro(name: str, args: list[str]):
    name = name.upper()
    if name not in MACROS:
        raise ValueError(f"Macro '{name}' não encontrada.")
    return MACROS[name](*args)
