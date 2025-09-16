from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from jsonschema import ValidationError
from rest_framework.utils.serializer_helpers import ReturnDict
from rest_framework.exceptions import APIException
from accounts.models import Provider, Social, User, UserProfile

def handle_update(data: ReturnDict, user):
    if "password" in data.keys():
           validate_password(data["password"], user=user) # type: ignore
    if "follows" in data.keys():
        follow_data = dict(data["follows"])
        follows = get_object_or_404(User, username=follow_data["username"])
        action = follow_data['action_type']
        instance = Social.objects.filter(user=User, follows=follows)
        exists = instance.exists()
        if action == 'follow':
            if exists:
               raise APIException(detail="You've already followed this person", code="duplicate_entry")
            Social.objects.create(user=user, follows=follows)
        else:
            if exists:
                   instance.delete()
            else:
                  raise APIException(detail="You can't unfollow what you haven't followed", code="missing_entry")   
        data.pop("follows")
        if "user_type" in data.keys():
           user_type = data['user_type']
           # print(user_type)
           up= get_object_or_404(UserProfile, user=user)
           arguments = {"user_profile":up, "location" : data["location"]}
           if user_type == "provider":
               try:
                   Provider.objects.create(**arguments)
               except IntegrityError:
                   # Provi
                   instance = Provider.objects.get(user_profile=up)
                   if not instance:
                       raise ValidationError("Cannot get your user info. What went wrong?")
                   instance.location = data["location"]
                   instance.save()
                   
           else:
               Provider.objects.filter(**arguments).delete()
           data.pop("user_type")
       
        for k, v in data.items():
           if hasattr(user, k):
               setattr(user, k, v)
           elif hasattr(user.profile, k): # type: ignore
               setattr(user.profile, k, v) # type: ignore
           user.save()