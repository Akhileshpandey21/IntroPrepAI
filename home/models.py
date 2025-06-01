from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Contact(models.Model):
    firstName = models.CharField(max_length=120)
    lastName = models.CharField(max_length=120)
    email = models.EmailField(max_length=120)
    phone= models.CharField(max_length=12)
    
    message = models.TextField()
    created_at = models.DateTimeField()

    def __str__(self):
        return self.firstName+" "+self.lastName


class ImageUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)+" "+"Profile Image("+self.title+")"



class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to User
    user_message = models.TextField()
    bot_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    needs_admin = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}: {self.user_message} | Bot: {self.bot_response} | Needs Admin: {self.needs_admin}"
    


class Review(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, blank=True, null=True)
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.rating}★)"
