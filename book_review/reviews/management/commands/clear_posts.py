from django.core.management.base import BaseCommand
from reviews.models import Ticket, Review


class Command(BaseCommand):
    help = "Supprime tous les tickets et critiques de la base de données"

    def handle(self, *args, **kwargs):
        Review.objects.all().delete()
        Ticket.objects.all().delete()
        self.stdout.write(
            self.style.SUCCESS(
                "Tous les posts (tickets et critiques) ont été supprimés avec succès."
            )
        )
