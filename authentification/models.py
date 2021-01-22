from django.contrib.auth.models import AbstractBaseUser, Group, BaseUserManager, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.db import models


# Create Manager

class UserManager(BaseUserManager):

    def create_user(self, username, password):
        if not username:
            raise TypeError('Username must not be empty')
        if not password:
            raise TypeError('Password must not be empty')
        user = self.model(username=username)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password):
        user = self.create_user(username, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


# Create your models here.

def dni_validation(value):
    control_letter = "TRWAGMYFPDXBNJZSQVHLCKE"
    dig_ext = "XYZ"
    reemp_dig_ext = {'X':'0', 'Y':'1', 'Z':'2'}
    range_values = "1234567890"
    dni = value.upper()
    if len(dni) == 9:
        dig_control = dni[8]
        dni = dni[:8]
        if dni[0] in dig_ext:
            dni = dni.replace(dni[0], reemp_dig_ext[dni[0]])
        return len(dni) == len([n for n in dni if n in range_values]) \
            and control_letter[int(dni)%23] == dig_control
    return False


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        max_length=150,
        unique=True,
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        validators=[username_validator],
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    image = models.ImageField(upload_to='avatar/', null=True)
    legal_id = models.CharField(max_length=9, validators=[])
    organization = models.ForeignKey(Group, related_name='status', null=True, on_delete=models.CASCADE, )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    blocked = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['password']
    objects = UserManager()

    @property
    def total_strikes(self):
        return self.strikes.count()

    def __str__(self):
        return self.username


class UserStrike(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, related_name="strikes", null=True)
    reason = models.ForeignKey('StrikeReason', on_delete=models.CASCADE)
    value = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.reason.label


class StrikeReason(models.Model):
    label = models.CharField(max_length=255)

    def __str__(self):
        return self.label
