from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100, null=True, blank=True)
    chief_full_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.name}: {self.address}"


class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    date = models.DateField()
    dish = models.TextField()

    def __str__(self):
        return f"{self.restaurant}: {self.date}"


class Employee(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Vote(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.employee} voted for {self.menu}"
