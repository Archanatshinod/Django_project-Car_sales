from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from django import forms

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

            # Check if there's a 'next' parameter in the request
            next_url = request.GET.get('next', 'home_page')  # Default to home_page if not set
            print(next_url)
            return redirect(next_url)  # Redirect to the target page
            
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
    # Check if the user is authenticated

    return render(request, 'User_home.html')



# -------------------------------------LOGOUT-------------------------------------------------------------

def logout(request):
    request.session.flush()  
    messages.success(request, "You have been logged out successfully!") 
    return redirect('home_page')

#--------------------------------------ADD CAR FOR SALE---------------------------------------------------

def add_car_for_sale(request):

    user_id = request.session.get('user_id')
    if not user_id:
        return HttpResponse('''<script>alert("You are not logged in!"); window.location="/car_project/Login/"</script>''')

    user_instance = User.objects.filter(id=user_id).first()
    if not user_instance:
        return HttpResponse('''<script>alert("User does not exist!"); window.location="/car_project/Login/"</script>''')

    if request.method == 'POST':
        
        name = request.POST.get('name')
        model_year = request.POST.get('model_year')
        km_driven = request.POST.get('km_driven')
        brand_name = request.POST.get('brand') 
        oil_type_name = request.POST.get('oil_type') 
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

       
        brand, created = Brand.objects.get_or_create(name=brand_name)

        
        oil_type, created = OilType.objects.get_or_create(oil_type=oil_type_name)

        
        car = CarForSale(
            user=user_instance,
            name=name,
            model_year=model_year,
            km_driven=km_driven,
            brand=brand,  
            oil_type=oil_type, 
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
        return redirect('home_page')  

    return render(request, 'add_car_for_sale.html')

#---------------------------LIST OF CARS FOR SALES ----------------------------------------

# def list_cars_for_sale(request):
#     cars = CarForSale.objects.order_by('?')[:10]
#     return render(request, 'list_cars_for_sale.html', {'cars': cars})

#------------------------------LIST OF MY CARS ----------------------------------------

def list_my_cars(request):
    user_id = request.session.get('user_id')  # Retrieve the user ID from the session

    if not user_id:
        return redirect('login')  # Redirect to login page if user is not logged in

    my_cars = CarForSale.objects.filter(user_id=user_id)
    return render(request, 'list_my_cars.html', {'my_cars': my_cars})



# ------------------------- ADD CAR FOR RENT-------------------------------------------------

def add_car_for_rent(request):
    
    user_id = request.session.get('user_id')
    if not user_id:
        return HttpResponse('''<script>alert("You are not logged in!"); window.location="/car_project/Login/"</script>''')

    user_instance = User.objects.filter(id=user_id).first()
    if not user_instance:
        return HttpResponse('''<script>alert("User does not exist!"); window.location="/car_project/Login/"</script>''')

    if request.method == 'POST':
        name = request.POST.get('name')
        brand_name = request.POST.get('brand')  
        oil_type_name = request.POST.get('oil_type') 
        description = request.POST.get('description')
        price_per_day = request.POST.get('price_per_day')
        mileage = request.POST.get('mileage')
        rent_car_image = request.FILES.get('rent_car_image')

        brand, created = Brand.objects.get_or_create(name=brand_name)

        oil_type, created = OilType.objects.get_or_create(oil_type=oil_type_name)

        car = CarForRent(
            user=user_instance,
            name=name,
            brand=brand,  
            oil_type=oil_type,  
            description=description,
            price_per_day=price_per_day,
            mileage=mileage,
            rent_car_image=rent_car_image,
        )
        car.save()
        return redirect('home_page') 

    return render(request, 'add_car_for_rent.html')


#---------------------------LIST OF CARS FOR RENT ----------------------------------------

# def list_cars_for_rent(request):
#     user_id = request.session.get('user_id')  # Retrieve the user ID from the session

#     if not user_id:
#         return redirect('login')  # Redirect to login page if user is not logged in

#     my_cars = CarForRent.objects.filter(user_id=user_id)
#     return render(request, 'list_cars_for_rent.html', {'cars': my_cars})

#------------------------------LIST OF MY CARS FOR RENT ----------------------------------------

def list_my_cars_for_rent(request):
    user_id = request.session.get('user_id')  # Retrieve the user ID from the session

    if not user_id:
        return redirect('login')  # Redirect to login page if user is not logged in

    my_cars = CarForRent.objects.filter(user_id=user_id)
    return render(request, 'list_my_cars_for_rent.html', {'my_cars': my_cars})


#---------------------------------EDIT MY CARS FOR SALE-------------------------------------------



from django.http import HttpResponseNotFound,HttpResponseBadRequest


def edit_my_cars(request, car_id):
    try:
        car = CarForSale.objects.get(id=car_id)
        print("Editing car with ID:", car)
        print(car.front_image)
    except CarForSale.DoesNotExist:
        return HttpResponseNotFound("Car not found")

    if request.method == 'POST':
        car.name = request.POST.get('name')
        car.model_year = request.POST.get('model_year')
        car.km_driven = request.POST.get('km_driven')

        # Get brand and oil type by ID
        brand_id = request.POST.get('brand')
        oil_type_id = request.POST.get('oil_type')
        car.brand = Brand.objects.get(id=brand_id) if brand_id else car.brand
        car.oil_type = OilType.objects.get(id=oil_type_id) if oil_type_id else car.oil_type

        car.accidental_background = request.POST.get('accidental_background') == 'True'
        car.description = request.POST.get('description')
        car.price = request.POST.get('price')
        car.mileage = request.POST.get('mileage')

        car.front_image = request.FILES.get('front_image', car.front_image)
        car.leftside_img = request.FILES.get('leftside_img', car.leftside_img)
        car.rightside_img = request.FILES.get('rightside_img', car.rightside_img)
        car.back_image = request.FILES.get('back_image', car.back_image)


        car.registration_number = request.POST.get('registration_number')
        car.insurance_end_date = request.POST.get('insurance_end_date')
        car.ownership_type = request.POST.get('ownership_type')
        car.save()

        
        return redirect('list_of_my_cars')  # Or redirect to a specific success page

    # Populate the form with existing car data for editing
    brands = Brand.objects.all()
    oil_types = OilType.objects.all()
    context = {
        'car': car,
        'brands': brands,
        'oil_types': oil_types,
    }

    # print("Front Image URL:", car.front_image.url if car.front_image else "No Image")
    # print("Left Side Image URL:", car.leftside_img.url if car.leftside_img else "No Image")
    # print("Right Side Image URL:", car.rightside_img.url if car.rightside_img else "No Image")
    # print("Back Image URL:", car.back_image.url if car.back_image else "No Image")
    return render(request, 'edit_my_cars.html', context)

       

   

#---------------------------------EDIT MY CARS FOR RENT -------------------------------------------

def edit_my_rent_cars(request,car_id):
    try:
        car = CarForRent.objects.get(id=car_id)

    except CarForSale.DoesNotExist:
        return HttpResponseNotFound("Car not found")
    
    if request.method == 'POST':
        car.name = request.POST.get('name')
        brand_id = request.POST.get('brand')
        oil_type_id = request.POST.get('oil_type')
        car.brand = Brand.objects.get(id=brand_id) if brand_id else car.brand
        car.oil_type = OilType.objects.get(id=oil_type_id) if oil_type_id else car.oil_type
        car.description = request.POST.get('description')
        car.price_per_day = request.POST.get('price_per_day')
        car.mileage = request.POST.get('mileage')
        car.rent_car_image = request.FILES.get('rent_car_image',car.rent_car_image)
        car.save()
        return redirect('list_of_my_cars_for_rent')  # Or redirect to a specific success page

        # Populate the form with existing car data for editing
    brands = Brand.objects.all()
    oil_types = OilType.objects.all()
    context = {
        'car': car,
        'brands': brands,
        'oil_types': oil_types,
    }
    
    return render(request,'edit_my_rent_cars.html',context)


#-------------------------------FILTER------------------------------------------------------------

from django.utils import timezone

def list_cars_for_sale(request):
    # Retrieve all cars initially
    cars = CarForSale.objects.all()

    # Get the current year for filtering by year range
    current_year = timezone.now().year

    # Filters from GET parameters
    brand_filter = request.GET.get('brand')
    year_filter = request.GET.get('year')
    km_filter = request.GET.get('km')
    oil_type_filter = request.GET.get('oil_type')
    price_filter = request.GET.get('price')
    search_filter = request.GET.get('search')

    # Apply filters
    if brand_filter:
        print("Brand Filter:", brand_filter)
        cars = cars.filter(brand__name__iexact=brand_filter)

    if year_filter:
        if year_filter == 'below_3_years':
            cars = cars.filter(model_year__gte=current_year - 3)
        elif year_filter == '3_to_5_years':
            cars = cars.filter(model_year__range=(current_year - 5, current_year - 3))
        elif year_filter == '5_to_10_years':
            cars = cars.filter(model_year__range=(current_year - 10, current_year - 5))
        elif year_filter == 'above_10_years':
            cars = cars.filter(model_year__lt=current_year - 10)

    if km_filter:
        if km_filter == 'below_10k':
            cars = cars.filter(km_driven__lt=10000)
        elif km_filter == '10k_to_20k':
            cars = cars.filter(km_driven__range=(10000, 20000))
        elif km_filter == '20k_to_40k':
            cars = cars.filter(km_driven__range=(20000, 40000))
        elif km_filter == 'above_40k':
            cars = cars.filter(km_driven__gt=40000)

    if oil_type_filter:
        cars = cars.filter(oil_type__oil_type=oil_type_filter)

    if price_filter:
        if price_filter == 'below_50k':
            cars = cars.filter(price__lt=50000)
        elif price_filter == '1L_to_3L':
            cars = cars.filter(price__range=(100000, 300000))
        elif price_filter == '3L_to_5L':
            cars = cars.filter(price__range=(300000, 500000))
        elif price_filter == '5L_to_10L':
            cars = cars.filter(price__range=(500000, 1000000))
        elif price_filter == 'above_10L':
            cars = cars.filter(price__gt=1000000)

    if search_filter:
        cars = cars.filter(name__icontains=search_filter)

    # Limit to 10 random cars
    cars = cars.order_by('?')[:10]

    # Get all brands and oil types for filters in the template
    brands = Brand.objects.all()
    oil_types = OilType.objects.all()
    user_id = request.session.get('user_id')
    
    # Fetch user information if the user is logged in
    user_profile = None
    if user_id:
        try:
            user_profile = User.objects.get(login_id=user_id)  # Assuming login_id is the foreign key
        except User.DoesNotExist:
            user_profile = None

    return render(request, 'list_cars_for_sale.html', {
        'cars': cars,
        'brands': brands,
        'oil_types': oil_types,
        'user_profile': user_profile,
    })


#---------------DELETE METHOD FOR SALE CARS-------------------------------------

def delete_car_for_sale(request, car_id):
    try:
        car = CarForSale.objects.get(id=car_id)
        car.delete()
        # messages.success(request, "Car deleted successfully!")
        return redirect('list_of_my_cars')  
    except CarForRent.DoesNotExist:
        # messages.error(request, "Car not found!")
        return redirect('list_of_my_cars')  
    

#---------------DELETE METHOD FOR RENT CARS-------------------------------------

def delete_car_for_rent(request, car_id):
    try:
        car = CarForRent.objects.get(id=car_id)
        car.delete()
        messages.success(request, "Car deleted successfully!")
        return redirect('list_of_my_cars_for_rent')  # Updated with the correct URL name
    except CarForRent.DoesNotExist:
        messages.error(request, "Car not found!")
        return redirect('list_of_my_cars_for_rent')  # Updated with the correct URL name
    
    
#-------------------LIST OF CAR FOR RENT--------------------------------------------
def list_cars_for_rent(request):
    
    cars = CarForRent.objects.all()
    
    
    brand_filter = request.GET.get('brand')
    oil_type_filter = request.GET.get('oil_type')
    price_filter = request.GET.get('price')
    search_filter = request.GET.get('search')  

    
    if brand_filter:
        print("Brand Filter:", brand_filter)  
        cars = cars.filter(brand__name__iexact=brand_filter)
        

    if oil_type_filter:
        cars = cars.filter(oil_type__oil_type=oil_type_filter)

    if price_filter:
        if price_filter == 'below_5k':
            cars = cars.filter(price_per_day__lt=5000)
        elif price_filter == '5k_to_10k':
            cars = cars.filter(price_per_day__range=(5000, 10000))
        elif price_filter == 'above_10k':
            cars = cars.filter(price_per_day__gt=10000)

    cars = cars.order_by('?')[:10]

    brands = Brand.objects.all()
    oil_types = OilType.objects.all()

    if search_filter:
        cars = cars.filter(name__icontains=search_filter)  
    
    user_id = request.session.get('user_id')
    
    # Fetch user information if the user is logged in
    user_profile = None
    if user_id:
        try:
            user_profile = User.objects.get(login_id=user_id)  # Assuming login_id is the foreign key
        except User.DoesNotExist:
            user_profile = None


    return render(request, 'list_cars_for_rent.html', {
        'cars': cars,
        'brands': brands,
        'oil_types': oil_types,
       'user_profile': user_profile, # Pa
    })

# ==========================================================================

def car_detail(request, car_id):
    try:
        car = CarForSale.objects.get(id=car_id)
    except CarForSale.DoesNotExist:
        car = None

    return render(request, 'car_detail.html', {'car': car})

def rent_car_detail(request, car_id):
    try:
        car = CarForRent.objects.get(id=car_id)
    except CarForRent.DoesNotExist:
        car = None

    return render(request, 'rent_car_detail.html', {'car': car})





def view_profile(request):
    # Get the user ID from the session
    user_id = request.session.get('user_id')
    user_profile = None

    # Check if the user is logged in
    if user_id:
        try:
            # Fetch the user's profile based on the user ID
            user_profile = User.objects.get(login_id=user_id)  # Assuming login_id is the foreign key
        except User.DoesNotExist:
            user_profile = None
    
    # Render the profile page with user profile data
    return render(request, 'my_profile.html', {
        'user_profile': user_profile,  # Pass the user profile to the template
    })


#----------------------------SALE PAGE-------------------------------------------------------------


def sale_page(request,car_id):
    try:
        car = CarForSale.objects.get(id=car_id)
    except CarForSale.DoesNotExist:
        car = None

    return render(request, 'sale.html', {'car': car})

#----------------------------SALE PAGE-------------------------------------------------------------


def rent_page(request,car_id):
    try:
        car = CarForRent.objects.get(id=car_id)
    except CarForRent.DoesNotExist:
        car = None
    
    return render(request, 'rent.html', {'car': car})
