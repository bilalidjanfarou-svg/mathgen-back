from fractions import Fraction

from .registry import register
from .utils import make, num, nz, pick, rnd, sgn, term_x


@register("limites")
def limites(d):
    a, c, b = rnd(1, 3 * d), rnd(1, 4), rnd(2, 5) * pick([-1, 1])
    ca, cc = "" if a == 1 else a, "" if c == 1 else c
    return make(
        rf"Calculer $\lim_{{x\to+\infty}}\frac{{{ca}x^{{2}} {term_x(b)} + 1}}{{{cc}x^{{2}} - 3}}$ (nombre ou fraction).",
        "number",
        num(Fraction(a, c)),
        rf"$\lim = \frac{{{a}}}{{{c}}}$",
        "Au numérateur et au dénominateur, seul le terme de plus haut degré compte.",
    )


@register("etude-de-fonctions")
def etude_de_fonctions(d):
    a = rnd(1, 3 + 2 * d) * pick([-1, 1])
    b = rnd(1, 9)
    return make(
        f"Soit $f(x) = x^{{2}} {sgn(-2 * a)}x + {b}$. Pour quelle valeur de $x$ la fonction $f$ admet-elle son minimum ?",
        "number",
        num(a),
        f"$f'(x) = 2x {sgn(-2 * a)}$ s’annule en $x = {a}$",
        "Calcule f′(x) et cherche où elle s’annule.",
    )


@register("log-exp")
def log_exp(d):
    a, b = rnd(1, 4), nz(3 * d)
    c = nz(3) if d == 3 else 0
    v = a + b + 2 * c
    extra = rf" {sgn(c)}\ln(e^{{2}})" if c else ""
    extra_x = f" {sgn(2 * c)}" if c else ""
    return make(
        rf"Simplifier : $\ln(e^{{{b}}}) + {a}\ln(e){extra} - \ln(1)$",
        "number",
        num(v),
        f"${b} + {a}{extra_x} - 0 = {v}$",
        "ln(e^k) = k, ln(e) = 1 et ln(1) = 0.",
    )


@register("integrales")
def integrales(d):
    a, c, k = rnd(1, 3), nz(5), rnd(1, 2 + d)
    v = a * k * k + c * k
    ca = "" if a == 1 else a
    return make(
        rf"Calculer $\int_{{0}}^{{{k}}} ({2 * a}x {sgn(c)})\,dx$.",
        "number",
        num(v),
        rf"$\left[{ca}x^{{2}} {term_x(c)}\right]_{{0}}^{{{k}}} = {v}$",
        "Une primitive de 2ax + c est ax² + cx.",
    )
