import math

def macro_mult(regs, a, b, res):
    """Multiplica registradores a * b e armazena em res."""
    regs[res] = regs.get(a, 0) * regs.get(b, 0)

def macro_div(regs, dividend, divisor, quotient, remainder):
    """Divide dividend/divisor, armazenando quociente e resto."""
    if regs.get(divisor, 0) == 0:
        raise ZeroDivisionError("Divisor é zero!")
    regs[quotient] = regs[dividend] // regs[divisor]
    regs[remainder] = regs[dividend] % regs[divisor]

def macro_equal(regs, a, b, res):
    """Retorna 1 se a == b, senão 0."""
    regs[res] = 1 if regs.get(a, 0) == regs.get(b, 0) else 0

def cantor_pair(x, y):
    s = x + y
    return (s * (s + 1)) // 2 + y

def inverse_cantor(z):
    w = int((math.isqrt(8*z + 1) - 1) // 2)
    t = (w * (w + 1)) // 2
    y = z - t
    x = w - y
    return x, y

def macro_encode(regs, x, y, res):
    """Codifica dois números em um único valor."""
    regs[res] = cantor_pair(regs.get(x, 0), regs.get(y, 0))

def macro_decode(regs, z, x, y):
    """Decodifica o valor de z e recupera x e y."""
    xv, yv = inverse_cantor(regs.get(z, 0))
    regs[x] = xv
    regs[y] = yv

MACRO_IMPL = {
    "MULT": (macro_mult, 3),
    "DIV": (macro_div, 4),
    "EQUAL": (macro_equal, 3),
    "ENCODE": (macro_encode, 3),
    "DECODE": (macro_decode, 3)
}
