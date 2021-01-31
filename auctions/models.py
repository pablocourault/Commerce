from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime

class Category(models.Model):  # categorías de los artículos a vender

    description = models.TextField(max_length=64, blank=False)

    def __str__(self):
        return f"{self.description}"

class User(AbstractUser):

    def __str__(self):
        return f"{self.username}"


class Auction(models.Model): # la subasta, el objeto a vender

    state = models.TextChoices('condition', 'active inactive')

    title = models.CharField(max_length=64, blank=False)
    description = models.TextField(max_length=640, blank=False)
    starting_bid = models.DecimalField(blank=False, max_digits=6, decimal_places=2)
    maxim_bid = models.DecimalField(blank=False, max_digits=6, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, related_name="categories")
    image_url = models.URLField(blank=True)
    condition = models.CharField(blank=False, choices=state.choices, max_length=8)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, related_name="publishers")
    posted_date = models.DateField(blank=False, default=datetime.date.today)
    won_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="purchasers")
    followed_by = models.ManyToManyField(User, blank=True, related_name="followers")

    def __str__(self):
        return f"{self.title} - Starting bid: {self.starting_bid}"


class Oferta(models.Model): # lo que ofrece pagar por una subasta cada usuario
    oferta = models.ForeignKey(Auction, on_delete=models.CASCADE, blank=False)
    offerer = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    bid =  models.DecimalField(blank=False, max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.oferta} - Offerer: {self.offerer} - Bid: {self.bid} "


class Comentario(models.Model): # realizados en una subasta
    said_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, blank=False)