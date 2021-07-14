from django.db import models
import re	# regex
from datetime import datetime, date


class UserManager(models.Manager):
    def user_validator(self, postData):    
        errors = {}
        now = datetime.now()
        EMAIL_REGEX = re.compile(r'^[a-z0-9.+_-]+@[a-z0-9._-]+\.[a-z]+$')
        CHAR_REGEX = re.compile(r'^[a-zA-ZÀ-ÿ\u00f1\u00d1]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d1]*)*[a-zA-ZÀ-ÿ\u00f1\u00d1]+$')
        if len(postData['first_name'])<2:
            errors['first_name'] = "First Name must be at least 2 characters long"
        if len(postData['last_name'])<2:
            errors['last_name'] = "Last Name must be at least 2 characters long"
        if not CHAR_REGEX.match(postData['first_name']):
            errors['first_name'] = "First Name accepts only letters without a space at the beginning"
        if not CHAR_REGEX.match(postData['last_name']):
            errors['last_name'] = "Last Name accepts only letters without a space at the beginning"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Incorrect email format!"
        if len(postData['password'])<8:
            errors['password'] = "Password must have at least 8 characters!"
        if postData['password'] != postData['reppassword']:
            errors['password'] = "Passwords are not identical!"
        return errors


class User (models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __repr__(self):
        return (f"Id #{self.id} First name: {self.name} Last name : {self.last_name} Email: {self.email}")
    def __str__(self):
        return (f"Id #{self.id} First name: {self.name} Last name : {self.last_name} Email: {self.email}")
