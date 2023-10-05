from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

# Create your models here.

class Date_user(models.Model):
    row = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    line = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    date_user = models.ForeignKey(to=User, related_name='date', on_delete=models.CASCADE, null=True)
    def __str__(self):
        return str(self.id)
#约束条件
class Equation(models.Model):
    sign = models.CharField(max_length=2, choices=[('=', '='), ('<', '<'), ('>', '>')])
    constraint_value = models.FloatField()
    belong_to_user1 = models.ForeignKey(Date_user, related_name="this_user1", on_delete=models.CASCADE, null=True)
    def __str__(self):
        return str(self.id)

#系数组
class Coefficient(models.Model):
    belong_to_equation = models.ForeignKey(Equation, related_name='coefficients', on_delete=models.CASCADE, null=True)
    value = models.FloatField()
    belong_to_user2 = models.ForeignKey(Date_user, related_name="this_user2", on_delete=models.CASCADE, null=True)
    def __str__(self):
        return str(self.id)
    
#目标函数
class Zuizhi(models.Model):
    value = models.FloatField()
    belong_to_user3 = models.ForeignKey(Date_user, related_name="this_user3", on_delete=models.CASCADE, null=True)
    def __str__(self):
        return str(self.id)