from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, phoneNumber, fullName, password=None):
        if not email and not phoneNumber:
            raise ValueError('Users must have either an email address or phone number')
        user = self.model(email=email, phoneNumber=phoneNumber, fullName=fullName)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phoneNumber, fullName, password=None):
        user = self.create_user(email=email, phoneNumber=phoneNumber, fullName=fullName, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(unique=True, null=True, blank=True)
    phoneNumber = models.CharField(max_length=15, unique=True, null=True, blank=True)
    fullName = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phoneNumber', 'fullName']

    def __str__(self):
        return self.email if self.email else self.phoneNumber

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
