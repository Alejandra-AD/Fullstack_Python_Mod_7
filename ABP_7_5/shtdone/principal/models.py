from django.db import models
from django.contrib.auth.models import User

class TaskStatus(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Etiqueta(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

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
    etiqueta = models.ForeignKey(Etiqueta, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


