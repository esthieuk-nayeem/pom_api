from django.db import models
from authentication.models import User
# Create your models here.



class Messege(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(null=False, max_length = 250)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.full_name}-{self.created_at}"

