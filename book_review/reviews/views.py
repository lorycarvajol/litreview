from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm  # Corrige l'importation ici
from .models import Profile
from django.contrib.auth import logout
from django.shortcuts import redirect


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
    print(
        f"User authenticated: {request.user.is_authenticated}"
    )  # Vérification de l'authentification
    return render(request, "reviews/home.html")


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
