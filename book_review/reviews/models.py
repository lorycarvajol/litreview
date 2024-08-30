from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver

from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)

    def __str__(self):
        return self.user.username


class Ticket(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(blank=True, max_length=2048)
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="tickets"
    )  # Association à User
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    ticket = models.ForeignKey(Ticket, null=True, blank=True, on_delete=models.SET_NULL)
    headline = models.CharField(max_length=128)
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(6)])
    body = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    time_created = models.DateTimeField(auto_now_add=True)


class Subscription(models.Model):
    follower = models.ForeignKey(
        User, related_name="following", on_delete=models.CASCADE
    )
    followed = models.ForeignKey(
        User, related_name="followers", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.follower.username} suit {self.followed.username}"
