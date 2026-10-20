"""Petits outils partagés par les générateurs."""
import random
from fractions import Fraction


def rnd(a, b):
    return random.randint(a, b)


def pick(items):
    return random.choice(items)


def nz(m):
    """Entier non nul entre -m et m."""
    return rnd(1, m) * pick([-1, 1])


def sgn(n):
    """'+ 3' ou '- 3' : pour écrire 'x + 3' ou 'x - 3' en LaTeX."""
    return f"- {-n}" if n < 0 else f"+ {n}"


def term_x(n):
    """'+ 3x', '- x' : terme en x avec son signe (coefficient 1 sans le '1')."""
    m = abs(n)
    return f"{'-' if n < 0 else '+'} {'' if m == 1 else m}x"


def par(n):
    """Met les négatifs entre parenthèses : (-3)."""
    return f"({n})" if n < 0 else str(n)


def poly(coeffs):
    """{3: 2, 1: -5, 0: 4} -> '2x^{3} - 5x + 4' (LaTeX)."""
    out = ""
    for p in (3, 2, 1, 0):
        c = coeffs.get(p, 0)
        if not c:
            continue
        m = abs(c)
        if p == 0:
            body = str(m)
        else:
            body = ("" if m == 1 else str(m)) + "x" + (f"^{{{p}}}" if p > 1 else "")
        if out:
            out += (" - " if c < 0 else " + ") + body
        else:
            out += ("-" if c < 0 else "") + body
    return out or "0"


def sympy_poly(coeffs):
    """{2: 6, 1: -4} -> '(6)*x**2 + (-4)*x**1' : texte que SymPy sait lire."""
    return " + ".join(f"({c})*x**{p}" for p, c in coeffs.items()) or "0"


def num(x):
    """Écriture exacte d'un nombre : '5' ou '7/2' (jamais de flottant)."""
    return str(Fraction(x))


def make(statement, answer_type, expected, explanation, hint=""):
    """Dict dont les clés correspondent aux champs du modèle Exercise."""
    return {
        "statement_latex": statement,
        "answer_type": answer_type,
        "expected": expected,
        "explanation_latex": explanation,
        "hint": hint,
    }
