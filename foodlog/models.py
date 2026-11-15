from django.db import models
from accounts.models import User

# Create your models here.
class Foodlog(models.Model):
    title=models.CharField(max_length=200)
    MEAL_TYPE_CHOICE=[
        ("breakfast","breakfast"),
        ("lunch","lunch"),
        ("tea","tea"),
        ("snack","snack"),
        ("dinner","dinner")
    ]
    meal_type=models.CharField(max_length=100,choices=MEAL_TYPE_CHOICE,default="tea")
    serving_size=models.CharField(max_length=100)
    owner=models.ForeignKey(User,on_delete=models.CASCADE)
    food_image=models.ImageField(upload_to="food_image",null=True)
    calorie=models.FloatField()
    created_at=models.DateTimeField(auto_now_add=True)
