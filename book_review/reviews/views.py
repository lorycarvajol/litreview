from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .forms import (
    AutonomousReviewForm,
    CustomUserCreationForm,
)  # Corrige l'importation ici
from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from .models import Ticket, Review
from .forms import TicketForm, ReviewForm


@login_required
def user_posts_view(request):
    # Récupérer les tickets et critiques de l'utilisateur connecté
    tickets = Ticket.objects.filter(user=request.user).order_by("-time_created")
    reviews = Review.objects.filter(user=request.user).order_by("-time_created")

    context = {
        "tickets": tickets,
        "reviews": reviews,
    }
    return render(request, "reviews/user_posts.html", context)


@login_required
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)
    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect("user_posts")
    else:
        form = TicketForm(instance=ticket)
    return render(request, "reviews/edit_ticket.html", {"form": form})


@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)
    if request.method == "POST":
        ticket.delete()
        return redirect("user_posts")
    return render(request, "reviews/delete_ticket.html", {"ticket": ticket})


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect("user_posts")
    else:
        form = ReviewForm(instance=review)
    return render(request, "reviews/edit_review.html", {"form": form})


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    if request.method == "POST":
        review.delete()
        return redirect("user_posts")
    return render(request, "reviews/delete_review.html", {"review": review})


@login_required
def create_review_autonomous(request):
    if request.method == "POST":
        form = AutonomousReviewForm(request.POST, request.FILES)
        if form.is_valid():
            # Créer le ticket
            ticket = Ticket.objects.create(
                title=form.cleaned_data["ticket_title"],
                description=form.cleaned_data["ticket_description"],
                image=form.cleaned_data["ticket_image"],
                user=request.user,
            )

            # Créer la critique associée
            Review.objects.create(
                ticket=ticket,
                headline=form.cleaned_data["review_headline"],
                rating=form.cleaned_data["review_rating"],
                body=form.cleaned_data["review_body"],
                user=request.user,
            )

            return redirect("home")
    else:
        form = AutonomousReviewForm()

    return render(request, "reviews/create_review_autonomous.html", {"form": form})


@login_required
def create_review(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            return redirect(
                "home"
            )  # Redirige vers la page d'accueil après la création de la critique
    else:
        form = ReviewForm()
    return render(
        request, "reviews/create_review.html", {"form": form, "ticket": ticket}
    )


@login_required
def create_ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect(
                "home"
            )  # Redirige vers la page d'accueil après la création du ticket
    else:
        form = TicketForm()
    return render(request, "reviews/create_ticket.html", {"form": form})


def custom_logout_view(request):
    logout(request)
    return redirect("login")


class CustomLoginView(LoginView):
    template_name = "reviews/login.html"

    def form_valid(self, form):
        print(f"Authenticating user: {form.get_user()}")
        login(self.request, form.get_user())  # Authentifier l'utilisateur manuellement
        return redirect("/home/")  # Rediriger explicitement vers la page d'accueil


@login_required
def home_view(request):
    tickets = Ticket.objects.filter(user=request.user).order_by("-time_created")
    reviews = Review.objects.filter(user=request.user)

    # Créer une liste de tickets avec la critique associée si elle existe
    tickets_with_reviews = []
    for ticket in tickets:
        ticket_review = reviews.filter(
            ticket=ticket
        ).first()  # On suppose qu'un seul review par ticket
        tickets_with_reviews.append((ticket, ticket_review))

    # Critiques autonomes
    autonomous_reviews = Review.objects.filter(ticket__isnull=True, user=request.user)

    context = {
        "tickets_with_reviews": tickets_with_reviews,
        "autonomous_reviews": autonomous_reviews,
    }
    return render(request, "reviews/home.html", context)


def register(request):
    if request.method == "POST":
        print("Form submitted")
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            print("Form is valid")
            user = form.save()
            if "avatar" in request.FILES:
                user.profile.avatar = request.FILES["avatar"]
                user.profile.save()
            login(request, user)
            return redirect("home")  # Redirection après inscription
        else:
            print("Form is not valid")
    else:
        form = CustomUserCreationForm()
    return render(request, "reviews/register.html", {"form": form})
