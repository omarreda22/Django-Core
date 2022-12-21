from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL  # auth.User

# One user have many cars, but car have only 1 user
# ManytoOneField

# ManytoOneField


class Car(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="car_rel")  # user.car_rel.all() not user.car_set.all()
    name = models.CharField(max_length=125)

    def __str__(self):
        return self.name


################
"""
    using get_user_model to get all users
    then get user and get all car with this user
"""
# from django.contrib.auth import get_user_model
# User = get_user_model()
# User.objects.all()
# u = User.objects.all()
# u = u.first()
# u.car_set.all()
###################

###############################
# from django.contrib.auth import get_user_model
# cl = get_user_model()
# cl.objects.all

# >> Equal

# u = car.user
# cl = u.__class__
# cl.objects.all
###############################

# Example
# >>> from cars.models import Car
# >>> car_obj = Car.objects.all().first()
# >>> car_obj.user
# <User: omar>
# >>> users = car_obj.user.__class__
# >>> users
# <class 'django.contrib.auth.models.User'>
# >>> users.objects.all()
# <QuerySet [<User: omar>, <User: user>]>
# >>> a = users.objects.all()
# >>> a.last()
# <User: user>
# >>> a.last()
# >>> new_user
# <User: user>
# >>> car_obj
# <Car: new>
# >>> car_obj.user
# <User: omar>
# >>> car_obj.user = new_user
# >>> car_obj.save()
##############################


############################################################################################################
############################################################################################################
############################################################################################################

# One to One Field
# one car for one user
# can;'t user have 2 cars -> unique user

class OneCar(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=125)

    def __str__(self):
        return self.name


############################################################################################################
############################################################################################################
############################################################################################################

# Many to Many Field

class Driver(models.Model):
    drivers = models.ManyToManyField(
        User)  # user.car_set.all()
    name = models.CharField(max_length=125)

    def __str__(self):
        return self.name

# obj.drivers.all()
# obj.drivers.first()
# obj.drivers.last()
# obj.drivers.filter()

# 3

# >>> d = Driver.objects.all()
# >>> d
# <QuerySet [<Driver: car 1>, <Driver: car2>]>
# >>> f_d = d.first()
# >>> f_d
# <Driver: car 1>
# >>> f_d.drivers.all()
# <QuerySet [<User: omar>, <User: user>]>

# >>> Driver.objects.filter(drivers=omar)
# <QuerySet [<Driver: car 1>, <Driver: car2>]>

# queryset.distinct() -> For Remove doplicate


############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################

# on_delete
"""
    CASCADE     -> when delete user delete obj
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    PROTECT     -> when delete user will get error
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    SET_NULL    -> when delete user will set null
    user = models.ForeignKey(User, on_delete=models.SET_NULL, NULL=TRUE)
    
    SET_DEFAULT -> when delete user will set default vaLUE
    user = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1)
"""
