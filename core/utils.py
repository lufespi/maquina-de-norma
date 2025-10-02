
import re

RE_INT = re.compile(r"^\d+$")

def is_int(s: str) -> bool:
    return bool(RE_INT.match(str(s).strip()))

def normalize_reg_name(s: str) -> str:
    s = s.strip().lower()
    if not s:
        raise ValueError("Nome de registrador vazio.")
    # Só letras (a..z) para simplificar
    if not re.match(r"^[a-z]$", s):
        raise ValueError(f"Registrador inválido: '{s}'. Use letras 'a'..'z'.")
    return s
