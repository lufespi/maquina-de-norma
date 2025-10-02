
from typing import Dict, List

class NormaVM:
    def __init__(self, registers: Dict[str, int], max_steps: int = 100000):
        # normaliza nomes e garante inteiros >= 0
        self.registers = {str(k).lower(): int(v) if int(v) >= 0 else 0 for k, v in registers.items()}
        self.max_steps = max_steps

    def _get(self, r: str) -> int:
        return int(self.registers.get(r, 0))

    def _set(self, r: str, v: int):
        self.registers[r] = max(0, int(v))

    def run(self, program: Dict[int, dict]) -> List[dict]:
        if not program:
            raise ValueError("Programa vazio.")

        # Determina rótulo inicial: o menor rótulo numérico do programa
        label = min(program.keys())

        # Loop detection opcional (estado = (label, tuple(sorted(registers.items())))
        seen = set()

        trace: List[dict] = []
        steps = 0

        while True:
            steps += 1
            if steps > self.max_steps:
                raise RuntimeError(f"Limite de passos excedido ({self.max_steps}). Possível laço infinito.")

            if label not in program:
                raise ValueError(f"Rótulo {label} não existe no programa.")

            instr = program[label]
            before = self.registers.copy()

            itype = instr["type"]
            next_label = None
            text = instr.get("text", "")

            if itype == "test_zero":
                r = instr["reg"]
                if self._get(r) == 0:
                    next_label = instr["goto_true"]
                else:
                    next_label = instr["goto_false"]

            elif itype == "add":
                r = instr["reg"]
                self._set(r, self._get(r) + 1)
                next_label = instr["goto"]

            elif itype == "sub":
                r = instr["reg"]
                self._set(r, max(0, self._get(r) - 1))
                next_label = instr["goto"]

            elif itype == "goto":
                next_label = instr["goto"]

            elif itype == "halt":
                # Registro do último estado e término
                trace.append({
                    "step": steps, "label": label, "instr_text": text or "fim",
                    "registers_before": before, "registers_after": self.registers.copy(),
                    "next_label": "HALT"
                })
                break

            else:
                raise ValueError(f"Instrução desconhecida: {itype}")

            trace.append({
                "step": steps, "label": label, "instr_text": text,
                "registers_before": before, "registers_after": self.registers.copy(),
                "next_label": next_label
            })

            # detecção simples de ciclo
            state_key = (next_label, tuple(sorted(self.registers.items())))
            if state_key in seen:
                # evita loop infinito sem explodir
                raise RuntimeError("Ciclo detectado na execução (estado repetido).")
            seen.add(state_key)

            label = next_label

        return trace
