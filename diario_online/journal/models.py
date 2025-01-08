from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=100)
    foto = models.ImageField(upload_to='fotos')

    def __str__(self):
        return self.name
    
class Journal(models.Model):
    tittle = models.CharField(max_length=100)
    tags = models.TextField()
    text = models.TextField()
    person = models.ManyToManyField(Person, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tittle