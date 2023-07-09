from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class TaskStatus(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Task(models.Model):
    STATUS_CHOICES = (
        ('completed', 'Completada'),
        ('pending', 'Pendiente'),
        ('in_progress', 'Realizando'),
    )

    title = models.CharField(max_length=100)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    due_date = models.DateField()

    # Relaciones con otros modelos
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.ForeignKey(TaskStatus, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

class Etiqueta(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


