"""Vérification des réponses de l'élève."""
import re
from fractions import Fraction

from sympy import Symbol, nsimplify, simplify
from sympy.parsing.sympy_parser import (
    convert_xor,
    implicit_multiplication_application,
    parse_expr,
    standard_transformations,
)

class UnreadableAnswer(ValueError):
    """La réponse n'a pas pu être lue (mauvais format) : elle n'est pas comptée comme fausse."""


x = Symbol("x")
TRANSFORMS = standard_transformations + (implicit_multiplication_application, convert_xor)
NUMBER = re.compile(r"-?\d+(?:\.\d+)?(?:/[1-9]\d*)?")
ALLOWED = re.compile(r"^[0-9x+\-*/^().\s]+$")


def _clean(raw):
    """Unifie le moins typographique et la virgule décimale."""
    return raw.strip().replace("−", "-").replace(",", ".")


def _to_fraction(text):
    """'7/2', '-2.5' ou '3' -> Fraction ; None si illisible."""
    try:
        return Fraction(_clean(text).replace(" ", ""))
    except (ValueError, ZeroDivisionError):
        return None


def _numbers(text):
    return [Fraction(m) for m in NUMBER.findall(_clean(text))]


def _norm_interval(text):
    t = _clean(text).lower().replace(" ", "")
    return t.replace("infini", "∞").replace("inf", "∞").replace("+∞", "∞")


def _parse_expression(text):
    """Lit une expression en x. Renvoie None si elle est illisible ou suspecte."""
    t = text.strip().lower().replace("−", "-").replace(",", ".")
    t = t.replace("²", "^2").replace("³", "^3")
    if not t or len(t) > 60 or not ALLOWED.match(t):
        return None  # seuls les chiffres, x et + - * / ^ ( ) sont acceptés
    if "**" in t or re.search(r"\^\s*\d\s*\^", t):
        return None  # pas de puissances en cascade (calculs géants)
    if any(len(m.group(1)) != 1 for m in re.finditer(r"\^\s*(\d*)", t)):
        return None  # exposants d'un seul chiffre
    try:
        return parse_expr(t, local_dict={"x": x}, transformations=TRANSFORMS)
    except Exception:
        return None


def check_answer(answer_type, expected, raw):
    """True si la réponse est correcte, False sinon. UnreadableAnswer si elle est illisible."""
    if answer_type == "number":
        value = _to_fraction(raw)
        if value is None:
            raise UnreadableAnswer("Écris un nombre (5 ou -2,5) ou une fraction (7/2).")
        return value == Fraction(expected)
    if answer_type == "interval":
        got = _norm_interval(raw)
        if not re.fullmatch(r"[\[\]].+;.+[\[\]]", got):
            raise UnreadableAnswer(
                "Écris un intervalle avec ses crochets et un point-virgule, par exemple ]-∞ ; 3[."
            )
        return got == _norm_interval(expected)
    if answer_type == "set":
        got = _numbers(raw)
        if not got:
            raise UnreadableAnswer(
                "Écris les solutions séparées par des points-virgules, par exemple {-1 ; 4}."
            )
        return sorted(set(got)) == sorted({Fraction(e) for e in expected})
    if answer_type == "vector":
        got = _numbers(raw)
        if len(got) != len(expected):
            raise UnreadableAnswer("Écris les deux coordonnées, par exemple (2 ; -3).")
        return got == [Fraction(e) for e in expected]
    if answer_type == "expression":
        student = _parse_expression(raw)
        if student is None:
            raise UnreadableAnswer(
                "Écris une expression en x, par exemple 3x^2 - 6x (utilise ^ pour les puissances)."
            )
        target = parse_expr(expected, local_dict={"x": x})
        return simplify(nsimplify(student, rational=True) - target) == 0
    raise ValueError(f"Type de réponse inconnu : {answer_type}")
