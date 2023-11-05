from django.db import models

class registered_data(models.Model):
    first_name=models.CharField(max_length=80)
    last_name=models.CharField(max_length=80)
    email=models.EmailField(unique=True)
    uid=models.CharField(max_length=20,unique=True)
    phone=models.CharField(max_length=10)
    description=models.CharField(max_length=200)

    def __str__(self):
        return f"{self.first_name}{self.last_name}"