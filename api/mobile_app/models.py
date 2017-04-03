from django.db import models


class Teacher(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    upna_id = models.IntegerField(min_value=0)
    name = models.CharField(max_length=100, blank=True, default='')
    email = models.CharField(max_length=100, blank=True, default='')  # TODO: Hay un campo especial para emails.
    telephone = models.CharField(max_length=20, blank=True, default='')

    class Meta:
        ordering = ('created',)
