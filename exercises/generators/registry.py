"""Registre : associe le slug d'un chapitre à sa fonction génératrice."""

GENERATORS = {}


def register(slug):
    def decorator(fn):
        GENERATORS[slug] = fn
        return fn

    return decorator


def generate(slug, difficulty):
    """Renvoie un dict prêt à créer un Exercise. KeyError si le chapitre n'a pas de générateur."""
    return GENERATORS[slug](difficulty)
