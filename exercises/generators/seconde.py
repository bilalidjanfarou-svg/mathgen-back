from .registry import register
from .utils import make, num, nz, par, pick, rnd, sgn, term_x


@register("equations-inequations")
def equations_inequations(d):
    a = pick([2, 3, 4, 5]) * (pick([-1, 1]) if d == 3 else 1)
    b = nz(5 * d)
    x0 = rnd(-5, 5)
    c = a * x0 + b
    if a > 0:
        interval, sign = f"]-∞;{x0}[", "<"
    else:
        interval, sign = f"]{x0};+∞[", ">"
    tex = interval.replace("∞", r"\infty")
    return make(
        rf"Résoudre dans $\mathbb{{R}}$ : ${a}x {sgn(b)} < {c}$",
        "interval",
        interval,
        f"${a}x < {c - b}$ donc $x {sign} {x0}$, soit $S = {tex}$",
        "Si tu divises par un nombre négatif, le sens de l’inégalité change.",
    )


@register("fonctions-affines")
def fonctions_affines(d):
    m = rnd(-3 * d, 3 * d) or 2
    x1, dx, y1 = rnd(-3, 3), rnd(1, 4), rnd(-5, 5)
    x2, y2 = x1 + dx, y1 + m * dx
    return make(
        rf"Calculer le coefficient directeur de la droite $(AB)$ avec $A({x1}\,;\,{y1})$ et $B({x2}\,;\,{y2})$.",
        "number",
        num(m),
        rf"$m = \frac{{{y2} - {par(y1)}}}{{{x2} - {par(x1)}}} = {m}$",
        "m = (yB − yA) / (xB − xA)",
    )


@register("equations-second-degre")
def equations_second_degre(d):
    r1, r2 = nz(3 * d + 1), nz(3 * d + 1)
    s, p = r1 + r2, r1 * r2
    mid = "" if s == 0 else f"{term_x(-s)} "
    eq = f"x^{{2}} {mid}{sgn(p)} = 0"
    sol = sorted({r1, r2})
    joined = " ; ".join(str(r) for r in sol)
    return make(
        rf"Résoudre dans $\mathbb{{R}}$ : ${eq}$ (solutions séparées par des points-virgules)",
        "set",
        [str(r) for r in sol],
        rf"$(x {sgn(-r1)})(x {sgn(-r2)}) = 0$ donc $S = \{{{joined}\}}$",
        "Cherche deux nombres de somme S et de produit P, ou utilise le discriminant.",
    )


@register("vecteurs")
def vecteurs(d):
    a, b, c, e = (rnd(-4 * d, 4 * d) for _ in range(4))
    k = 1 if d == 1 else rnd(2, 3)
    x, y = k * a + c, k * b + e
    coef = "" if k == 1 else str(k)
    return make(
        rf"Soit $\vec{{u}}({a}\,;\,{b})$ et $\vec{{v}}({c}\,;\,{e})$. Calculer les coordonnées de ${coef}\vec{{u}} + \vec{{v}}$.",
        "vector",
        [str(x), str(y)],
        rf"$({k}\times{par(a)} + {par(c)}\,;\,{k}\times{par(b)} + {par(e)}) = ({x}\,;\,{y})$",
        "Calcule l’abscisse, puis l’ordonnée. Réponse sous la forme (x ; y).",
    )
