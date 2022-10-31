from django.contrib.auth import get_user_model
from products.model import Product

User = get_user_model()

j = User.objects.first()

Product.objects.create(title='first Title after user', user=j, price=12.2)
