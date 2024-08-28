import random
from django.contrib.auth.models import User
from reviews.models import Ticket, Review
from django.core.files import File
from pathlib import Path

# Liste des utilisateurs existants
users = User.objects.all()

# Liste étendue des livres historiques et leurs images correspondantes
books = [
    ("Les Misérables", "media/images/les_miserables.png"),
    ("War and Peace", "media/images/war_and_peace.png"),
    ("Moby Dick", "media/images/moby_dick.png"),
    ("Pride and Prejudice", "media/images/pride_and_prejudice.png"),
    ("The Odyssey", "media/images/the_odyssey.png"),
    ("Don Quixote", "media/images/don_quixote.png"),
    ("Ulysses", "media/images/ulysses.png"),
    ("The Divine Comedy", "media/images/divine_comedy.png"),
    # ("Hamlet", "media/images/hamlet.png"),
    # ("The Iliad", "media/images/iliad.png"),
    # ("Crime and Punishment", "media/images/crime_and_punishment.png"),
    # ("Madame Bovary", "media/images/madame_bovary.png"),
    # ("The Brothers Karamazov", "media/images/brothers_karamazov.png"),
    # ("The Great Gatsby", "media/images/great_gatsby.png"),
    # ("One Hundred Years of Solitude", "media/images/one_hundred_years_of_solitude.png"),
    # ("To Kill a Mockingbird", "media/images/to_kill_a_mockingbird.png"),
    # ("The Catcher in the Rye", "media/images/catcher_in_the_rye.png"),
    # ("The Grapes of Wrath", "media/images/grapes_of_wrath.png"),
    # ("The Hobbit", "media/images/hobbit.png"),
    # ("Jane Eyre", "media/images/jane_eyre.png"),
    # ("Wuthering Heights", "media/images/wuthering_heights.png"),
    # ("Anna Karenina", "media/images/anna_karenina.png"),
    # ("The Picture of Dorian Gray", "media/images/picture_of_dorian_gray.png"),
    # ("The Count of Monte Cristo", "media/images/count_of_monte_cristo.png"),
    # ("1984", "media/images/1984.png"),
    # ("Brave New World", "media/images/brave_new_world.png"),
    # ("Fahrenheit 451", "media/images/fahrenheit_451.png"),
    # ("The Old Man and the Sea", "media/images/old_man_and_the_sea.png"),
    # ("Heart of Darkness", "media/images/heart_of_darkness.png"),
    # ("Frankenstein", "media/images/frankenstein.png"),
    # ("Dracula", "media/images/dracula.png"),
    # ("Moby Dick", "media/images/moby_dick.png"),
    # ("Gulliver's Travels", "media/images/gullivers_travels.png"),
    # ("The Scarlet Letter", "media/images/scarlet_letter.png"),
    # ("The Canterbury Tales", "media/images/canterbury_tales.png"),
]

# Liste des exemples de critiques et de réponses
reviews_content = [
    ("Incroyable lecture ! Un chef-d'œuvre littéraire.", 5),
    ("Assez ennuyeux par moments, mais l'intrigue est captivante.", 3),
    ("J'ai adoré les personnages et l'écriture est magnifique.", 4),
    ("Une critique sociale impressionnante et bien développée.", 5),
    ("Pas vraiment ce à quoi je m'attendais, mais pas mal.", 3),
    ("Une lecture longue mais enrichissante.", 4),
    ("Absolument fascinant du début à la fin.", 5),
    ("Un livre à lire absolument.", 5),
    ("Un peu long, mais mérite l'effort.", 4),
    ("Certainement pas pour tout le monde, mais j'ai adoré.", 4),
    ("Une œuvre majeure de la littérature.", 5),
    ("Trop complexe pour moi.", 2),
]

# Créer 50 posts au total
total_posts = 50
posts_per_user = total_posts // len(users)

for user in users:
    for _ in range(posts_per_user):  # Répartir les posts par utilisateur
        # Sélectionner un livre au hasard
        book_title, book_image_path = random.choice(books)

        # Créer un ticket
        ticket = Ticket.objects.create(
            title=f"Demande de critique pour {book_title}",
            description=f"Quelqu'un a-t-il déjà lu {book_title} ? J'aimerais connaître vos avis.",
            user=user,
        )

        # Ajouter une image au ticket
        with open(book_image_path, "rb") as f:
            ticket.image.save(Path(book_image_path).name, File(f))

        # Décider aléatoirement si une critique autonome ou une réponse sera créée
        if random.choice([True, False]):
            # Créer une critique pour ce ticket
            review_content, rating = random.choice(reviews_content)
            Review.objects.create(
                ticket=ticket,
                headline=f"Mon avis sur {book_title}",
                rating=rating,
                body=review_content,
                user=user,
            )
        else:
            # Créer une critique autonome
            review_content, rating = random.choice(reviews_content)
            Review.objects.create(
                headline=f"Critique autonome de {book_title}",
                rating=rating,
                body=review_content,
                user=user,
            )

print(f"{total_posts} posts (tickets et critiques) ont été créés avec succès.")
