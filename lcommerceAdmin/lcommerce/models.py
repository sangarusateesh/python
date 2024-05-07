from django.db import models

# Create your models here.
class users(models.Model):
    user_id = models.CharField(max_length=124)
    user_name = models.CharField(max_length=124)
    user_email = models.EmailField(unique=True)
    userPhone = models.CharField(max_length=10, unique=True)
    passCode = models.CharField(max_length=8)

    class Meta:
        managed = False  # Set managed to False to indicate that Django should not manage the table
        db_table = 'users'  # Set the actual table name
    