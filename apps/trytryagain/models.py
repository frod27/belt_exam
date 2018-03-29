from __future__ import unicode_literals
from django.db import models
import re
from datetime import datetime
import bcrypt

class UserManager(models.Manager):
    def register(self, name, username, password, confirm):
        response = {
            "valid": True,
            "errors": [],
            "user": None
        }

        if len(name) < 1:
            response["errors"].append("Name is required")
        elif len(name) < 3:
            response["errors"].append("Name must be 3 characters or longer")

        if len(username) < 1:
            response["errors"].append("Username is required")
        elif len(username) < 3:
            response["errors"].append("Username must be 3 characters or longer")
        else:
            username_list = User.objects.filter(username = username.lower())
            if(len(username_list) > 0):
                response["errors"].append("Username is already in use")

        if len(password) < 1:
            response["errors"].append("Password is required")
        elif len(password) < 8:
            response["errors"].append("Password must be 8 characters or longer")

        if len(confirm) < 1:
            response["errors"].append("Confirm Password is required")
        elif confirm != password:
            response["errors"].append("Confirm Password must match Password")

        if len(response["errors"]) > 0:
            response["valid"] = False
        else:
            response["user"] = User.objects.create(
                name=name,
                username=username.lower(),
                password=bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            )

        return response

    def login(self, username, password):
        response = {
            "valid": True,
            "errors": [],
            "user": None
        }

        if len(username) < 1:
            response["errors"].append("Username is required")
        else:
            username_list = User.objects.filter(username=username.lower())
            if len(username_list) == 0:
                response["errors"].append("Username not found")

        if len(password) < 1:
            response["errors"].append("Password is required")
        elif len(password) < 8:
            response["errors"].append("Password must be 8 characters or longer")

        if len(response["errors"]) == 0:
            hashed_pw = username_list[0].password
            if bcrypt.checkpw(password.encode(), hashed_pw.encode()):
                response["user"] = username_list[0]
            else:
                response["errors"].append("Incorrect Password")

        if len(response["errors"]) > 0:
            response["valid"] = False
        return response

class ItemManager(models.Manager):
    def addItem(self, item, creator):
        response = {
            "valid": True,
            "errors": [],
            "item": None
        }

        if len(item) < 1:
            response["errors"].append("Item is required")
        
        if(len(response["errors"]) == 0):
            today = datetime.now()
            # if(today > datetime.strptime(created_at, "%Y-%m-%d")):
            #     response["errors"].append("the future")
            # if(datetime.strptime(from_date, "%Y-%m-%d") > datetime.strptime(to_date, "%Y-%m-%d")):
            #     response["errors"].append(" Date From")

        if len(response["errors"]) > 0:
            response["valid"] = False
        else:
            response["item"] = Item.objects.create(
                name=item,
                creator_id = creator,
            )
            # response["item"].creator = User.objects.get(id = creator)
            response["item"].wish_user.add(User.objects.get(id = creator))
        return response

    def joinItem(self, item_id, joiner_id):
        response = {
            "valid": True,
            "errors": [],
        }

        item = Item.objects.get(id = item_id)
        if len(item.wish_user.all().filter(id = joiner_id)) > 0:
            response["errors"].append("You have already added this item!")

        if len(response["errors"]) > 0:
            response["valid"] = False
        else:
            item.wish_user.add(User.objects.get(id = joiner_id))
        return response
    
    def removeItem(self, item_id, joiner_id):
        response = {
            "valid": True,
            "errors": [],
        }

        item = Item.objects.get(id = item_id)
        if len(item.wish_user.all().filter(id = joiner_id)) > 0:
            response["errors"].append("You have removed already!")

        if len(response["errors"]) > 0:
            response["valid"] = False
        else:
            item.wish_user.remove(User.objects.get(id = joiner_id))
        return response

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()
    def __repr__(self):
        return "<User object: {}>".format(self.username)

class Item(models.Model):
    name = models.CharField(max_length=255)
    creator = models.ForeignKey(User, related_name='users_item')
    wish_user = models.ManyToManyField(User, related_name='users_wishes')
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now_add= True)
    objects = ItemManager()
    def __repr__(self):
        return "<Item object: {}>".format(self.item)