# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Profile(models.Model):
    #user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    #username = models.CharField(max_length=200, blank=True, null=True)
   # email = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    profile_pic = models.ImageField(null=True, blank=True, upload_to="images", default="/user.png")
    twitter = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
   # balance = models.CharField(max_length=30, blank=True)



class Post(models.Model):
    cardnumber = models.CharField(max_length=200)
    bank = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=300, blank=True)
    price = models.TextField( null=True ,blank=True)
    location = models.CharField(max_length=300,  blank=True)
    balance = models.CharField(max_length=30, blank=True)
    cvv = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.cardnumber


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username}'s Wallet"

class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'failed'),

    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    timestamp = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Transaction ID: {self.id} - Type: {self.transaction_type} - Amount: ${self.amount}"

