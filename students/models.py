from django.db import models

class Subject(models.TextChoices):
    FINANCE = "Finance"
    PHILOSOPHY = "Philosophy"
    SALES = "Sales"
    ENGINEERING = "Engineering"
    INTERIOR_DESIGN = "Interior Design"
    FILM_MAKING = "Film Making"
    GRAPHIC_DESIGN = "Graphic Design"
    FASHION_DESIGN = "Fashion Design"

class Students(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    age = models.IntegerField()
    course = models.CharField(max_length=20, choices=Subject.choices)
    teacher = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.course} - {self.teacher.name}"
