from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .forms import AutonomousReviewForm, CustomUserCreationForm, TicketForm, ReviewForm
from .models import Ticket, Review, Subscription
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import JsonResponse


@login_required
def followed_user_posts_view(request, user_id):
    followed_user = get_object_or_404(User, id=user_id)
    posts = followed_user.posts.all().order_by("-time_created")

    context = {
        "followed_user": followed_user,
        "posts": posts,
    }
    return render(request, "reviews/followed_user_posts.html", context)


@login_required
def search_users(request):
    query = request.GET.get("q", "")
    if query:
        users = User.objects.filter(username__icontains=query).exclude(
            id=request.user.id
        )
        users_data = [{"id": user.id, "username": user.username} for user in users]
        return JsonResponse({"users": users_data})
    return JsonResponse({"users": []})


@login_required
def subscription_view(request):
    query = request.GET.get("q")
    users = User.objects.exclude(username=request.user.username)
    if query:
        users = users.filter(username__icontains=query)

    following = Subscription.objects.filter(follower=request.user)
    following_users = [sub.followed for sub in following]

    context = {
        "users": users,
        "following_users": following_users,
    }
    return render(request, "reviews/subscription.html", context)


@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    Subscription.objects.get_or_create(follower=request.user, followed=user_to_follow)

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"success": True, "username": user_to_follow.username})

    return redirect("subscription")


@login_required
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)
    Subscription.objects.filter(
        follower=request.user, followed=user_to_unfollow
    ).delete()
    return redirect("subscription")


@login_required
def followed_user_posts_view(request, user_id):
    followed_user = get_object_or_404(User, id=user_id)
    tickets = Ticket.objects.filter(user=followed_user).order_by("-time_created")
    reviews = Review.objects.filter(user=followed_user).order_by("-time_created")

    context = {
        "followed_user": followed_user,
        "tickets": tickets,
        "reviews": reviews,
    }
    return render(request, "reviews/followed_user_posts.html", context)


@login_required
def user_posts_view(request):
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
            ticket = Ticket.objects.create(
                title=form.cleaned_data["ticket_title"],
                description=form.cleaned_data["ticket_description"],
                image=form.cleaned_data["ticket_image"],
                user=request.user,
            )

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
            return redirect("home")
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
            return redirect("home")
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
        login(self.request, form.get_user())
        return redirect("/home/")


@login_required
def home_view(request):
    search_query = request.GET.get(
        "q", ""
    )  # Récupérer la recherche depuis les paramètres GET

    # Récupérer tous les tickets et critiques de tous les utilisateurs
    tickets = Ticket.objects.all().order_by("-time_created")
    reviews = Review.objects.all()

    if search_query:
        # Filtrer les tickets et critiques par titre et en-tête si une recherche est spécifiée
        tickets = tickets.filter(title__icontains=search_query)
        reviews = reviews.filter(headline__icontains=search_query)

    # Créer une liste de tickets avec la critique associée si elle existe
    tickets_with_reviews = []
    for ticket in tickets:
        ticket_review = reviews.filter(
            ticket=ticket
        ).first()  # On suppose qu'un seul review par ticket
        tickets_with_reviews.append((ticket, ticket_review))

    # Critiques autonomes
    autonomous_reviews = Review.objects.filter(ticket__isnull=True)

    context = {
        "tickets_with_reviews": tickets_with_reviews,
        "autonomous_reviews": autonomous_reviews,
        "search_query": search_query,  # Passer la recherche dans le contexte
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
            return redirect("home")
        else:
            print("Form is not valid")
    else:
        form = CustomUserCreationForm()
    return render(request, "reviews/register.html", {"form": form})
