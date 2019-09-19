from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
"""-------------------------------------------------------------------------"""
# Create your models here.
class Daily_log(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, unique_for_date="date")
    date = models.DateField()
    session_hours = models.DecimalField(max_digits=4, decimal_places=2)
    observed_hours = models.DecimalField(max_digits=4, decimal_places=2)
    supervisor = models.CharField(max_length=256)

class Monthly_log(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    year = models.IntegerField(
        validators = [
            MaxValueValidator(5000),
            MinValueValidator(1900)            
        ]
    )
    month = models.IntegerField(
        validators = [
            MaxValueValidator(12),
            MinValueValidator(1)
        ]
    )
    session_hours = models.DecimalField(max_digits=5, decimal_places=2)
    observed_hours = models.DecimalField(max_digits=5, decimal_places=2)
    mutable = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user_id", "year", "month"],
                name="unique_weekly_logs"
            )
        ]