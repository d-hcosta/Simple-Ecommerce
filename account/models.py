from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
import re


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField()
    street_adress = models.CharField(max_length=50)
    city = models.CharField(max_length=30)
    zipcode = models.CharField(max_length=8)
    state = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.user}'

    def clean(self):
        error_messages  = {}

        if re.search(r'[^0-9]', self.zipcode) or len(self.zipcode) < 8:
            error_messages['zipcode'] = 'Invalid Zip Code, enter 8 numbers only.'

        if error_messages:
            raise ValidationError(error_messages)
