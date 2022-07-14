from django.db import models

# Create your models here.

class Budget(models.Model):

    currency_option = [('NGN', 'NGN'), ('USD', 'USD'), ('EUR', 'EUR')]
    duration_option = [('DAILY', 'DAILY'), ('WEEKLY', 'WEEKLY'), ('MONTHLY', 'MONTHLY'), ('YEARLY', 'YEARLY')]

    CATEGORY_OPTIONS=[
        ('FOOD', 'FOOD'),
        ('SHOPPING', 'SHOPPING'),
        ('HEALTH', 'HEALTH'),
        ('BOOKS', 'BOOKS'),
        ('OTHERS', 'OTHERS'),
    ]

    title = models.CharField(max_length = 255)
    the_currency = models.CharField(choices = currency_option, max_length=255)
    the_duration = models.CharField(choices = duration_option, max_length=255)
    category = models.CharField(choices =CATEGORY_OPTIONS, max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2, max_length=255)
    start_date =models.DateField(null=False, blank=False)
    end_date =models.DateField(null=False, blank=False)
    #owner = models.ForeignKey(to=User, on_delete = models.CASCADE) #remember to check up this line
    #for the above code to function properly  it needs the authentication app

