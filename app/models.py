from django.db import models

from user.models import User


class Restaurant(models.Model):
    name = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    chief_full_name = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"{self.name}: {self.address}"


class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    date = models.DateField()
    menu = models.FileField(upload_to='menus/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    votes = models.IntegerField(default=0)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"{self.restaurant}: {self.date}"


class Vote(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="menus")
    voted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee} voted for {self.menu}"
