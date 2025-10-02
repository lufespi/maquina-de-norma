
"""
Implementações de macros com rótulos *explícitos* (leitura direta dos rótulos).
Cada macro é descrita por um dicionário: label:int -> instrução primitiva.
As instruções usam o *dialeto* interno da VM/Parser:
    type: "test_zero" | "add" | "sub" | "halt"
    reg: nome (a..z)              (para test/add/sub)
    goto / goto_true / goto_false (rótulos *relativos* dentro da macro)
    text: string legível para o traço

Observação: rótulos aqui são *relativos à macro* e começar de 0 (ou 1, conforme fornecido)
não é problema; o parser fará o remapeamento para rótulos absolutos e ligará o "fim" comum
ao NEXT informado na chamada no programa.
"""

def _T(reg, t, f):  # test_zero
    return {"type": "test_zero", "reg": reg, "goto_true": t, "goto_false": f}

def _A(reg, g):     # add
    return {"type": "add", "reg": reg, "goto": g}

def _S(reg, g):     # sub
    return {"type": "sub", "reg": reg, "goto": g}

def _H():           # halt (fim relativo da macro)
    return {"type": "halt"}

# ---------- MENOR(a,b,c): menor valor em c ----------
# Macro escrita (do enunciado):
# 0: se zero_c então vá_para 3 senão vá_para 1
# 1: faça sub_c vá_para 0
# 2: se zero_a então vá_para 7 senão vá_para 3
# 3: se zero_b então vá_para 7 senão vá_para 4
# 4: faça sub_a vá_para 5
# 5: faça sub_b vá_para 6
# 6: faça add_c vá para 2
# 7: # fim
def _MENOR_layout(a,b,c):
    M = {
        0: _T(c, 3, 1),
        1: _S(c, 0),
        2: _T(a, 7, 3),
        3: _T(b, 7, 4),
        4: _S(a, 5),
        5: _S(b, 6),
        6: _A(c, 2),
        7: _H(),
    }
    # mensagens legíveis (apenas para o traço)
    M[0]["text"] = f"se zero_{c} então vá_para 3 senão vá_para 1"
    M[1]["text"] = f"faça sub_{c} vá_para 0"
    M[2]["text"] = f"se zero_{a} então vá_para 7 senão vá_para 3"
    M[3]["text"] = f"se zero_{b} então vá_para 7 senão vá_para 4"
    M[4]["text"] = f"faça sub_{a} vá_para 5"
    M[5]["text"] = f"faça sub_{b} vá_para 6"
    M[6]["text"] = f"faça add_{c} vá_para 2"
    M[7]["text"] = "fim"
    return M

# ---------- MAIOR(a,b,c,d): maior valor em d (usa c como auxiliar) ----------
# Macro escrita (do enunciado):
# 0..18 conforme especificado
def _MAIOR_layout(a,b,c,d):
    M = {
        0: _T(c, 3, 1),
        1: _S(c, 0),
        2: _T(d, 4, 3),
        3: _S(d, 2),
        4: _T(a, 9, 5),
        5: _T(b, 12, 6),
        6: _S(a, 7),
        7: _S(b, 8),
        8: _A(c, 4),
        9: _T(b, 15, 10),
        10:_S(b, 11),
        11:_A(d, 9),
        12:_T(a, 15, 13),
        13:_S(a, 14),
        14:_A(d, 12),
        15:_T(c, 18, 16),
        16:_S(c, 17),
        17:_A(d, 15),
        18:_H(),
    }
    M[0]["text"]  = f"se zero_{c} então vá_para 3 senão vá_para 1"
    M[1]["text"]  = f"faça sub_{c} vá_para 0"
    M[2]["text"]  = f"se zero_{d} então vá_para 4 senão vá_para 3"
    M[3]["text"]  = f"faça sub_{d} vá_para 2"
    M[4]["text"]  = f"se zero_{a} então vá_para 9 senão vá_para 5"
    M[5]["text"]  = f"se zero_{b} então vá_para 12 senão vá_para 6"
    M[6]["text"]  = f"faça sub_{a} vá_para 7"
    M[7]["text"]  = f"faça sub_{b} vá_para 8"
    M[8]["text"]  = f"faça add_{c} vá_para 4"
    M[9]["text"]  = f"se zero_{b} vá_para 15 senão vá_para 10"
    M[10]["text"] = f"faça sub_{b} vá_para 11"
    M[11]["text"] = f"faça add_{d} vá_para 9"
    M[12]["text"] = f"se zero_{a} então vá_para 15 senão vá_para 13"
    M[13]["text"] = f"faça sub_{a} vá_para 14"
    M[14]["text"] = f"faça add_{d} vá_para 12"
    M[15]["text"] = f"se zero_{c} então vá_para 18 senão vá_para 16"
    M[16]["text"] = f"faça sub_{c} vá_para 17"
    M[17]["text"] = f"faça add_{d} vá_para 15"
    M[18]["text"] = "fim"
    return M

# ---------- IGUAL(a,b,c): c=1 se a==b, senão c=0 ----------
# Macro escrita (do enunciado):
# 1..9 conforme especificado
def _IGUAL_layout(a,b,c):
    M = {
        1: _T(c, 3, 2),
        2: _S(c, 1),
        3: _T(a, 7, 4),
        4: _T(b, 9, 5),
        5: _S(a, 6),
        6: _S(b, 3),
        7: _T(b, 8, 9),
        8: _A(c, 9),
        9: _H(),
    }
    M[1]["text"] = f"se zero_{c} então vá_para 3 senão vá_para 2"
    M[2]["text"] = f"faça sub_{c} vá_para 1"
    M[3]["text"] = f"se zero_{a} vá_para 7 senão vá_para 4"
    M[4]["text"] = f"se zero_{b} vá_para 9 senão vá_para 5"
    M[5]["text"] = f"faça sub_{a} vá_para 6"
    M[6]["text"] = f"faça sub_{b} vá_para 3"
    M[7]["text"] = f"se zero_{b} vá_para 8 senão vá_para 9"
    M[8]["text"] = f"faça add_{c} vá_para 9"
    M[9]["text"] = "fim"
    return M

# Utilitário: converte um layout (dict label->instr) em lista 0..N de instruções relativas
def _layout_to_list(layout_dict):
    labels = sorted(layout_dict.keys())
    # Reindexa para 0..N preservando a ordem e reescrevendo destinos
    idx_map = {lbl: i for i, lbl in enumerate(labels)}
    rel = []
    for lbl in labels:
        ins = layout_dict[lbl].copy()
        if ins["type"] == "test_zero":
            ins["goto_true"]  = idx_map.get(ins["goto_true"], ins["goto_true"])
            ins["goto_false"] = idx_map.get(ins["goto_false"], ins["goto_false"])
        elif ins["type"] in ("add", "sub"):
            ins["goto"] = idx_map.get(ins["goto"], ins["goto"])
        # "halt" não precisa de reescrita
        rel.append(ins)
    return rel

def expand_MENOR(a,b,c):
    return _layout_to_list(_MENOR_layout(a,b,c))

def expand_MAIOR(a,b,c,d):
    return _layout_to_list(_MAIOR_layout(a,b,c,d))

def expand_IGUAL(a,b,c):
    return _layout_to_list(_IGUAL_layout(a,b,c))

MACRO_TABLE = {
    "MENOR": expand_MENOR,
    "MAIOR": expand_MAIOR,
    "IGUAL": expand_IGUAL,
}

def has_macro(name: str) -> bool:
    return name.upper() in MACRO_TABLE

def expand_macro(name: str, args: list[str]):
    name = name.upper()
    if name not in MACRO_TABLE:
        raise ValueError(f"Macro '{name}' não encontrada.")
    return MACRO_TABLE[name](*args)
