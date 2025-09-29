def format_trace(trace, final_registers):
    """
    Formata o trace de execução e o estado final dos registradores
    em uma string bonita para CLI ou GUI.
    """
    lines = ["=== TRACE DE EXECUÇÃO ==="]
    for label, regs in trace:
        estado = ", ".join(f"{k}={v}" for k, v in regs.items())
        lines.append(f"Rótulo {label}: {estado}")
    lines.append("")
    lines.append("=== ESTADO FINAL ===")
    estado_final = ", ".join(f"{k}={v}" for k, v in final_registers.items())
    lines.append(estado_final)
    lines.append("=== FIM ===")
    return "\n".join(lines)
