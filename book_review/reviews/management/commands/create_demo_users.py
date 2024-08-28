from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Create demo users for demonstration purposes"

    def handle(self, *args, **kwargs):
        # Définir les utilisateurs avec leurs noms amusants
        demo_users = [
            ("coolcat", "coolcat@example.com"),
            ("funnybunny", "funnybunny@example.com"),
            ("smartyfox", "smartyfox@example.com"),
            ("crazydog", "crazydog@example.com"),
            ("chillpanda", "chillpanda@example.com"),
            ("gigglesnail", "gigglesnail@example.com"),
            ("whistlemouse", "whistlemouse@example.com"),
            ("dancingdolphin", "dancingdolphin@example.com"),
            ("happylemur", "happylemur@example.com"),
            ("wittywalrus", "wittywalrus@example.com"),
        ]

        # Mot de passe commun pour tous les utilisateurs
        password = "demo1234"

        # Créer chaque utilisateur
        for username, email in demo_users:
            if not User.objects.filter(username=username).exists():
                User.objects.create_user(
                    username=username, email=email, password=password
                )
                self.stdout.write(
                    self.style.SUCCESS(f"User {username} created successfully.")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"User {username} already exists.")
                )
