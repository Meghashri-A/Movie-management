from django.db import models
from db_connection import db

zapp_collection = db['user_dets'] #name of the collection/table
# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Image(models.Model):
    caption=models.CharField(max_length=100)
    image=models.ImageField(upload_to="zapp/")
    def __str__(self):
        return self.caption
