from django.db import models

# Create your models here.

class Login(models.Model):
    Username=models.CharField(max_length=50)
    Password=models.CharField(max_length=50)


class User(models.Model):
    login=models.ForeignKey(Login,on_delete=models.CASCADE)
    Name=models.CharField(max_length=50)
    Email=models.CharField(max_length=50)
    Phone=models.CharField(max_length=10)  
    my_location_link=models.URLField(max_length=200,blank=True, null=True)
    profile_picture= models.ImageField(upload_to='profile_pictures/', blank=True, null=True, help_text="Upload a profile picture")
    whatsapp_number = models.CharField(max_length=10)

class OilType(models.Model):
    oil_choice = [
        ('Petrol', 'Petrol'),
        ('Diesel', 'Diesel'),
        ('Electric', 'Electric'),
    ]
    oil_type = models.CharField(max_length=20, choices=oil_choice, unique=True)

    def __str__(self):
        return self.oil_type


class Brand(models.Model):
    name = models.CharField(max_length=50, unique=True)

class CarForSale(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    model_year = models.IntegerField()
    km_driven = models.IntegerField()  
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)
    oil_type = models.ForeignKey('OilType', on_delete=models.CASCADE)
    accidental_background = models.BooleanField(default=False)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    mileage = models.DecimalField(max_digits=5, decimal_places=2)  
    front_image = models.ImageField(upload_to='car_images/front/', blank=True, null=True)
    leftside_img = models.ImageField(upload_to='car_images/leftside/', blank=True, null=True)
    rightside_img = models.ImageField(upload_to='car_images/rightside/', blank=True, null=True)
    back_image = models.ImageField(upload_to='car_images/back/', blank=True, null=True)
    registration_number = models.CharField(max_length=20, unique=True) 
    insurance_end_date = models.DateField()
    
    ownership_choice = [
        ('1st', '1st Owner'),
        ('2nd', '2nd Owner'),
        ('3rd', '3rd Owner'),
        ('4th+', '4th or more Owners'),
    ]
    ownership_type = models.CharField(max_length=4, choices=ownership_choice)
    
    created_date = models.DateField(auto_now_add=True)
    created_time = models.TimeField(auto_now_add=True)


class CarForRent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)
    oil_type = models.ForeignKey('OilType', on_delete=models.CASCADE)
    description = models.TextField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    mileage = models.DecimalField(max_digits=5, decimal_places=2) 
    rent_car_image = models.ImageField(upload_to='car_images/rent/', blank=True, null=True)
    created_date = models.DateField(auto_now_add=True)
    created_time = models.TimeField(auto_now_add=True)