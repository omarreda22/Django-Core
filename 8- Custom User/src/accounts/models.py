from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.core.validators import RegexValidator
from django.conf import settings
from django.db.models.signals import post_save


User = settings.AUTH_USER_MODEL

######## This in CMD ############


class NewUserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        if not username:
            raise ValueError('Users must have an username address')

        if len(password) < 8:
            raise ValueError('Password must be bigger than 8 Char')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        if len(password) < 8:
            raise ValueError('Password must be bigger than 8 Char')

        user = self.create_user(
            email,
            username,
            first_name,
            last_name,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


USERNAME_REGEX = '^[a-zA-Z0-9.@+-]*$'


class NewUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    username = models.CharField(
        max_length=225,
        validators=[
            RegexValidator(
                regex=USERNAME_REGEX,
                message='Username must be alpahnumeric or contain any of the following: ". @ + -" ',
                code='invalid_username'
            ),
        ],
        unique=True
    )
    first_name = models.CharField(max_length=225)
    last_name = models.CharField(max_length=225)
    city = models.CharField(max_length=225)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = NewUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    # @property
    # def is_staff(self):
    #     "Is the user a member of staff?"
    #     # Simplest possible answer: All admins are staff
    #     return self.is_admin

###################################################################################################
###################################################################################################
###################################################################################################

########## Add Group and Permissions

# from models.py
# add PermissionsMixin
# remove has_perm and has_module_perms

# from admin.py
# fieldsets -> Permissions -> add ('groups', 'user_permissions')
# remove filter_horizontal


###################################################################################################
###################################################################################################
###################################################################################################



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=125, null=True, blank=True)

    def __str__(self):
        return self.user.username


def post_save_create_profile(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        pass


post_save.connect(post_save_create_profile, sender=User)
