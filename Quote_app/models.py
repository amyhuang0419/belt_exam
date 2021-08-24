from django.db import models
import re

# Create your models here.
class UserManager(models.Manager):
    def register_validation(self,post_data):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        FIRST_NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
        LAST_NAME_REGEX = re.compile(r'^[a-zA-Z]+$')

        #validate first name
        if post_data['first_name'] == '':
            errors['first_name_empty'] = "First name is required!!"
        elif len(post_data['first_name']) < 2 :
            errors['first_name_length'] = "First name has at least 2 characters."
        elif not FIRST_NAME_REGEX.match(post_data['first_name']):
            errors['first_name'] = "First name must be letters!"

        #validate last name
        if post_data['last_name'] == '':
            errors['last_name_empty'] = "Last name is required!!"
        elif len(post_data['last_name'])< 2:
            errors['last_name_length'] = "Last name has at least 2 characters."
        elif not LAST_NAME_REGEX.match(post_data['last_name']):
            errors['last_name'] = "Last name must be letters!"

        #validate email
        users = User.objects.filter(email = post_data['email'])
        if post_data['email'] == '':
            errors['email_empty'] = "Email is required!!"
        elif not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = "Invalid email address!"
        elif users:
            errors['email_used'] = "This emaill address has registered by someone else."

        #validate password
        if post_data['password'] == '':
            errors['password_empty'] = "Password is required!!"
        elif len(post_data['password']) < 8:
            errors['password_length'] = "Password has at least 8 characters."

        if post_data['password'] != post_data['confirm_password']:
            errors['password_not_match'] = "Password Not Match!!!"

        return errors
        
    def login_validation(self,post_data):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if post_data['email'] == '':
            errors['email_empty'] = "Please enter your Login Email!!"
        elif not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = "Invalid email address!"

        elif post_data['password'] == '':
            errors['password_empty'] = "Password is required!"

        return errors


class QuoteManager(models.Manager):
    def quote_validation(self, post_data):
        errors = {}

        # quote validation
        if post_data['quoted_by'] == '':
            errors['quoted_by_empty'] = "Please tell me who make this Quotation!!!"
        elif len(post_data['quoted_by']) <2 :
            errors['quoted_by_length'] = "Quotor has at least 2 characters."

        if post_data['message'] == '':
            errors['message_empty'] = "What is the Quotation??"
        elif len(post_data['message']) < 10 :
            errors['message_length'] = "Message has at least 10 characters."

        return errors



class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Quote(models.Model):
    quoted_by = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    posted_by = models.ForeignKey(User, related_name = "quotes_posted", on_delete=models.CASCADE)
    users_who_like = models.ManyToManyField(User, related_name = "liked_quotes")
    objects = QuoteManager()