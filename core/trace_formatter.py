
def format_trace(trace, final_registers):
    """
    Formata o traço de execução com um layout legível.
    trace: lista de dicionários com chaves:
      - step, label, instr_text, registers_before, registers_after, next_label
    final_registers: dict com o estado final
    """
    lines = []
    lines.append("==== TRAÇO DE EXECUÇÃO ====")
    for ev in trace:
        before = ", ".join(f"{k}={v}" for k,v in sorted(ev["registers_before"].items()))
        after  = ", ".join(f"{k}={v}" for k,v in sorted(ev["registers_after"].items()))
        lines.append(
            f"#{ev['step']:04d}  L{ev['label']:<5} | {ev['instr_text']:<55} | "
            f"antes: [{before}] -> depois: [{after}] | próximo: {ev['next_label']}"
        )
    lines.append("")
    lines.append("==== REGISTRADORES FINAIS ====")
    lines.append(", ".join(f"{k}={v}" for k,v in sorted(final_registers.items())))
    return "\n".join(lines)
