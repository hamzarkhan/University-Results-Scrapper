from django.db import models

# Create your models here.
# resultapp/models.py
from django.db import models

class StudentResult(models.Model):
    college_code = models.CharField(max_length=10)
    field_code = models.CharField(max_length=10)
    hall_ticket = models.CharField(max_length=10)
    marks = models.CharField(max_length=10)
    name = models.CharField(max_length=255)
    backlogs = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.hall_ticket}"
