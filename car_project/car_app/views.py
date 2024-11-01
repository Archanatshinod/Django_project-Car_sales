from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *

# Create your views here.

from django.contrib import messages
from django.contrib.auth import get_user


# -----------------------------------------------------LOGIN------------------------------------------
# views.py

from django.shortcuts import render, redirect
from .models import Login  # Assuming Login is your custom user model

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # Query the Login model to authenticate the user
            user = Login.objects.get(Username=username, Password=password)
            
            # Set user information in the session
            request.session['user_id'] = user.id
            request.session['username'] = user.Username

            # Redirect to the home page after setting session data
            return redirect('home_page')
        
        except Login.DoesNotExist:
            return render(request, 'login.html', {'error': 'Invalid username or password'})

    return render(request, 'login.html')



# ---------------------------------USER REGISTRATION-------------------------------------------------

def user_registration(request):
    if request.method == 'POST':
        name = request.POST['Name']
        email = request.POST['Email']
        phone = request.POST['Phone']
        whatsapp_number = request.POST['Whatsapp_number']
        profile_photo = request.FILES.get('Profile_photo')
        password = request.POST['Password']
        my_location_link=request.POST['my_location_link']
        confirm_password = request.POST['Confirm_password']

        if not name:
            return render(request, 'user_registration.html', {'x': 'Name field is required!'})
        
        if Login.objects.filter(Username=name).exists():
            return render(request, 'user_registration.html', {'x': 'Username already exists!'})

        if password != confirm_password:
            return render(request, 'user_registration.html', {'x': 'Passwords do not match!'})

        login_entry = Login.objects.create(Username=name, Password=password)
        User.objects.create(
            login=login_entry,
            Name=name,
            Email=email,
            Phone=phone,
            my_location_link=my_location_link,
            whatsapp_number=whatsapp_number,
            profile_picture=profile_photo
        )

        return redirect('Login')  

    return render(request, 'user_registration.html')

# ------------------------------------------HOME PAGE------------------------------------------------------

def home_page(request):
    username = request.session.get('username')

    if not username:
        return redirect('Login')
    
    return render(request, 'User_home.html', {'username': username})


# -------------------------------------LOGOUT-------------------------------------------------------------

def logout(request):
    request.session.flush()  
    messages.success(request, "You have been logged out successfully!") 
    return redirect('Login')

#--------------------------------------ADD CAR FOR SALE---------------------------------------------------

def add_car_for_sale(request):
    # Check if the user is logged in
    user_id = request.session.get('user_id')
    if not user_id:
        return HttpResponse('''<script>alert("You are not logged in!"); window.location="/car_project/Login/"</script>''')

    user_instance = User.objects.filter(id=user_id).first()
    if not user_instance:
        return HttpResponse('''<script>alert("User does not exist!"); window.location="/car_project/Login/"</script>''')

    if request.method == 'POST':
        # Extract form data
        name = request.POST.get('name')
        model_year = request.POST.get('model_year')
        km_driven = request.POST.get('km_driven')
        brand_name = request.POST.get('brand')  # Get brand name from input
        oil_type_name = request.POST.get('oil_type')  # Get the selected oil type
        accidental_background = request.POST.get('accidental_background') == 'True'
        description = request.POST.get('description')
        price = request.POST.get('price')
        mileage = request.POST.get('mileage')
        front_image = request.FILES.get('front_image')
        leftside_img = request.FILES.get('leftside_img')
        rightside_img = request.FILES.get('rightside_img')
        back_image = request.FILES.get('back_image')
        registration_number = request.POST.get('registration_number')
        insurance_end_date = request.POST.get('insurance_end_date')
        ownership_type = request.POST.get('ownership_type')

        # Create or get the brand
        brand, created = Brand.objects.get_or_create(name=brand_name)

        # Check if the oil type already exists
        oil_type, created = OilType.objects.get_or_create(oil_type=oil_type_name)

        # Create a new CarForSale instance
        car = CarForSale(
            user=user_instance,
            name=name,
            model_year=model_year,
            km_driven=km_driven,
            brand=brand,  # Assign the brand object
            oil_type=oil_type,  # Use the oil_type object to link to OilType
            accidental_background=accidental_background,
            description=description,
            price=price,
            mileage=mileage,
            front_image=front_image,
            leftside_img=leftside_img,
            rightside_img=rightside_img,
            back_image=back_image,
            registration_number=registration_number,
            insurance_end_date=insurance_end_date,
            ownership_type=ownership_type
        )
        car.save()
        return redirect('home_page')  # Redirect to the appropriate page

    return render(request, 'add_car_for_sale.html')

#---------------------------LIST OF CARS FOR SALES ----------------------------------------

def list_cars_for_sale(request):
    cars = CarForSale.objects.order_by('?')[:10]
    return render(request, 'list_cars_for_sale.html', {'cars': cars})

#------------------------------LIST OF MY CARS ----------------------------------------

def list_my_cars(request):
    user_id = request.session.get('user_id')  # Retrieve the user ID from the session

    if not user_id:
        return redirect('login')  # Redirect to login page if user is not logged in

    my_cars = CarForSale.objects.filter(user_id=user_id)
    return render(request, 'list_my_cars.html', {'my_cars': my_cars})



# ------------------------- ADD CAR FOR RENT-------------------------------------------------

def add_car_for_rent(request):
    # Check if the user is logged in
    user_id = request.session.get('user_id')
    if not user_id:
        return HttpResponse('''<script>alert("You are not logged in!"); window.location="/car_project/Login/"</script>''')

    user_instance = User.objects.filter(id=user_id).first()
    if not user_instance:
        return HttpResponse('''<script>alert("User does not exist!"); window.location="/car_project/Login/"</script>''')

    if request.method == 'POST':
        # Extract form data
        name = request.POST.get('name')
        brand_name = request.POST.get('brand')  # Get brand name from input
        oil_type_name = request.POST.get('oil_type')  # Get the selected oil type
        description = request.POST.get('description')
        price_per_day = request.POST.get('price_per_day')
        mileage = request.POST.get('mileage')
        rent_car_image = request.FILES.get('rent_car_image')

        # Create or get the brand
        brand, created = Brand.objects.get_or_create(name=brand_name)

        # Check if the oil type already exists
        oil_type, created = OilType.objects.get_or_create(oil_type=oil_type_name)

        # Create a new CarForSale instance
        car = CarForRent(
            user=user_instance,
            name=name,
            brand=brand,  # Assign the brand object
            oil_type=oil_type,  # Use the oil_type object to link to OilType
            description=description,
            price_per_day=price_per_day,
            mileage=mileage,
            rent_car_image=rent_car_image,
        )
        car.save()
        return redirect('home_page')  # Redirect to the appropriate page

    return render(request, 'add_car_for_rent.html')


#---------------------------LIST OF CARS FOR RENT ----------------------------------------

def list_cars_for_rent(request):
    cars = CarForRent.objects.order_by('?')[:10]
    return render(request, 'list_cars_for_rent.html', {'cars': cars})

#------------------------------LIST OF MY CARS FOR RENT ----------------------------------------

def list_my_cars_for_rent(request):
    user_id = request.session.get('user_id')  # Retrieve the user ID from the session

    if not user_id:
        return redirect('login')  # Redirect to login page if user is not logged in

    my_cars = CarForRent.objects.filter(user_id=user_id)
    return render(request, 'list_my_cars_for_rent.html', {'my_cars': my_cars})
