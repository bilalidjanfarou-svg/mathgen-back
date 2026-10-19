from django.core.management.base import BaseCommand

from exercises.models import Chapter, Level

CHAPTERS = [
    ("equations-inequations", "Équations et inéquations", Level.SECONDE),
    ("fonctions-affines", "Fonctions affines", Level.SECONDE),
    ("equations-second-degre", "Équations du second degré", Level.SECONDE),
    ("vecteurs", "Vecteurs", Level.SECONDE),
    ("second-degre", "Second degré", Level.PREMIERE),
    ("derivation", "Dérivation", Level.PREMIERE),
    ("suites-numeriques", "Suites numériques", Level.PREMIERE),
    ("trigonometrie", "Trigonométrie", Level.PREMIERE),
    ("limites", "Limites de fonctions", Level.TERMINALE),
    ("etude-de-fonctions", "Étude de fonctions", Level.TERMINALE),
    ("log-exp", "Logarithme et exponentielle", Level.TERMINALE),
    ("integrales", "Intégrales", Level.TERMINALE),
]


class Command(BaseCommand):
    help = "Crée ou met à jour les 12 chapitres du lycée"

    def handle(self, *args, **options):
        for order, (slug, name, level) in enumerate(CHAPTERS, start=1):
            Chapter.objects.update_or_create(
                slug=slug, defaults={"name": name, "level": level, "order": order}
            )
        self.stdout.write(self.style.SUCCESS(f"{len(CHAPTERS)} chapitres prêts."))