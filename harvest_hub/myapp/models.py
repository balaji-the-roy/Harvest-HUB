from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image

# -------------------------------------------------------
# CROP MANAGEMENT MODELS
# -------------------------------------------------------
class Crop(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    planting_date = models.DateField()
    harvest_date = models.DateField()
    quantity = models.IntegerField()
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Inventory(models.Model):
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    stored_quantity = models.IntegerField()
    storage_location = models.CharField(max_length=100)
    date_stored = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.crop.name} in {self.storage_location}"


class Sale(models.Model):
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    quantity_sold = models.IntegerField()
    sale_date = models.DateField(default=timezone.now)
    buyer_name = models.CharField(max_length=100)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Sale of {self.crop.name} to {self.buyer_name}"


# -------------------------------------------------------
# USER PROFILE MODEL
# -------------------------------------------------------
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

    category = models.CharField(
        max_length=10,
        choices=[('Farmer', 'Farmer'), ('Buyer', 'Buyer')],
        default='Buyer',  # SAFE DEFAULT
        blank=True
    )

    image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    # Resize profile image on save
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)
            max_size = (300, 300)
            img.thumbnail(max_size)  # keeps aspect ratio
            img.save(self.image.path)


# -------------------------------------------------------
# PRODUCT MODEL
# -------------------------------------------------------
class Product(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='products'
    )
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    category = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    about = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

    # Resize product image on save
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)
            max_size = (300, 300)  # set your desired size
            img.thumbnail(max_size)  # keeps aspect ratio
            img.save(self.image.path)
