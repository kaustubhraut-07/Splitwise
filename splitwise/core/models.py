from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator


class User(AbstractUser):
    username = None
    name = models.CharField(max_length=100 , null=False, blank=False)
    email = models.EmailField(unique=True , null=False, blank=False)
    password = models.CharField(max_length=100, null=False, blank=False)
    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = ['name'] 

    def __self__(self):        
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User, related_name="split_groups")

    def __str__(self):
        return self.name


class Expense(models.Model):
    name = models.CharField(max_length=100)
    amount = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    paid_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="paid_expenses")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="expenses")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.amount}"


class Settlement(models.Model):
    amount = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    paid_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="settlements_paid")
    paid_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="settlements_received")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="settlements")
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Settlement of {self.amount} from {self.paid_by} to {self.paid_to}"
