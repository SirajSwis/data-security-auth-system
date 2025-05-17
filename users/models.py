from django.db import models

class User(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('user', 'User'),
    ]
    
    username = models.CharField(max_length=150, unique=True)
    password_hash = models.CharField(max_length=64)
    role = models.CharField(max_length=5, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.username} ({self.role})"
