from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Todo(models.Model):
    title = models.CharField(max_length=100)
    memo = models.TextField(blank=True)
    created_date_time = models.DateTimeField(auto_now_add=True) # this records the date automatically and not editable
    date_completed = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    # link the user id to access only user specific models
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
