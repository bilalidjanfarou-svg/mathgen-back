from fractions import Fraction

from .registry import register
from .utils import make, num, nz, par, pick, poly, rnd, sgn, sympy_poly


@register("second-degre")
def second_degre(d):
    a, b, c = nz(2 * d), nz(6 * d), nz(3 * d)
    delta = b * b - 4 * a * c
    return make(
        f"Calculer le discriminant du trinôme ${poly({2: a, 1: b, 0: c})}$.",
        "number",
        num(delta),
        rf"$\Delta = {par(b)}^{{2}} - 4\times{par(a)}\times{par(c)} = {delta}$",
        "Δ = b² − 4ac",
    )


@register("derivation")
def derivation(d):
    if d == 1:
        cs = {2: nz(4), 1: nz(5), 0: nz(6)}
    elif d == 2:
        cs = {3: nz(3), 2: nz(4), 0: nz(6)}
    else:
        cs = {3: nz(3), 2: nz(4), 1: nz(5), 0: nz(6)}
    ds = {p - 1: p * c for p, c in cs.items() if p > 0}
    return make(
        f"Calculer la dérivée de la fonction $f(x) = {poly(cs)}$.",
        "expression",
        sympy_poly(ds),
        f"$f'(x) = {poly(ds)}$",
        "Écris x^2 pour x². La dérivée de x^n est n·x^(n−1).",
    )


@register("suites-numeriques")
def suites_numeriques(d):
    if d < 3:
        u0, r, n = rnd(-5, 10), nz(2 * d), rnd(5, 10 + 5 * d)
        v = u0 + n * r
        return make(
            rf"La suite $(u_n)$ est arithmétique, de premier terme $u_0 = {u0}$ et de raison $r = {r}$. Calculer $u_{{{n}}}$.",
            "number",
            num(v),
            rf"$u_{{{n}}} = {u0} + {n}\times{par(r)} = {v}$",
            "u_n = u_0 + n × r",
        )
    u0, q, n = rnd(1, 3), pick([2, 3]), rnd(3, 5)
    v = u0 * q**n
    return make(
        rf"La suite $(u_n)$ est géométrique, de premier terme $u_0 = {u0}$ et de raison $q = {q}$. Calculer $u_{{{n}}}$.",
        "number",
        num(v),
        rf"$u_{{{n}}} = {u0}\times {q}^{{{n}}} = {v}$",
        "u_n = u_0 × q^n",
    )


@register("trigonometrie")
def trigonometrie(d):
    a = rnd(1, 4) if d == 1 else nz(5)
    b = rnd(1, 4) if d == 1 else nz(5)
    c = nz(4)
    v = Fraction(a + b, 2) + (c if d == 3 else 0)
    extra = rf" {sgn(c)}\sin\frac{{\pi}}{{2}}" if d == 3 else ""
    extra_x = rf" {sgn(c)}\times 1" if d == 3 else ""
    return make(
        rf"Calculer ${a}\cos\frac{{\pi}}{{3}} {sgn(b)}\sin\frac{{\pi}}{{6}}{extra}$.",
        "number",
        num(v),
        rf"${a}\times\frac{{1}}{{2}} {sgn(b)}\times\frac{{1}}{{2}}{extra_x} = {num(v)}$",
        "cos(π/3) = 1/2, sin(π/6) = 1/2, sin(π/2) = 1. Tu peux écrire une fraction, ex : 5/2.",
    )
