from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Review, Ticket


from django import forms
from .models import Review, Ticket


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }


class AutonomousReviewForm(forms.Form):
    # Champs pour le Livre/Article
    ticket_title = forms.CharField(
        label="Titre",
        max_length=128,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    ticket_description = forms.CharField(
        label="Description", widget=forms.Textarea(attrs={"class": "form-control"})
    )
    ticket_image = forms.ImageField(
        label="Image",
        required=False,
        widget=forms.ClearableFileInput(attrs={"class": "form-control"}),
    )

    # Champs pour la Critique
    review_headline = forms.CharField(
        label="Titre de la critique",
        max_length=128,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    review_rating = forms.ChoiceField(
        label="Note", choices=[(i, str(i)) for i in range(6)], widget=forms.RadioSelect
    )
    review_body = forms.CharField(
        label="Commentaire", widget=forms.Textarea(attrs={"class": "form-control"})
    )


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["headline", "rating", "body"]
        widgets = {
            "headline": forms.TextInput(attrs={"class": "form-control"}),
            "rating": forms.RadioSelect(choices=[(i, str(i)) for i in range(6)]),
            "body": forms.Textarea(attrs={"class": "form-control"}),
        }


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Nom d'utilisateur"}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Mot de passe"}
        )
    )


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Adresse email"}
        ),
    )
    avatar = forms.ImageField(
        required=False, widget=forms.FileInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "avatar"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
