from __future__ import annotations
from typing import Any

from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone

class UserManager(BaseUserManager["User"]):
    def create_user(self, email: str, password: str | None=None, ** extra_fields: Any) -> "User":
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email).lower()
        
        user = self.model(email=email, **extra_fields)
        
        if password is None:
            raise ValueError("Password is required")
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email: str, password: str, **extra_fields: Any) -> "User":
        #extra_fields.setdefault("is staff", True)
        #extra_fields.setdefault("is_superuser", True)
        #extra_fields.setdefault("is_active", True)
        
        #if extra_fields.get("is_staff") is not True:
        #    raise ValueError("Superuser must have is_staff=True")
        #if extra_fields.get("is_superuser") is not True:
        #    raise ValueError("Superuser must have is_superuser=True")
        
        #return self.create_user(email=email, password=password, **extra_fields)
        extra_fields["is_staff"] = True
        extra_fields["is_superuser"] = True
        extra_fields["is_active"] = True
        
        return self.create_user(email=email, password=password, **extra_fields)
    
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    date_joined = models.DateTimeField(default=timezone.now)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = ["first_name", "last_name"]
    
    def __str__(self) -> str:
        return self.email