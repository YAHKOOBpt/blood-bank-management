from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
import os
from django.shortcuts import render, get_object_or_404
# Create your views here.

def home(request):
    return render(request,'index.html')

########################## donor panel #######################

############### donor home page ################
def index(request):
    user=request.user
    view=BloodRequest.objects.filter(donor_id=user)
    context={
        'view':view
    }
    return render(request,'donor/index.html',context)

##################donor registeration ################

def donor_register(request):
    if request.method == "POST":
        uname = request.POST.get("username")
        passw1 = request.POST.get("password")
        passw2= request.POST.get("password1")
        email= request.POST.get("email")
        if passw1 ==passw2:
            if User.objects.filter(username=uname).exists():
                messages.error(request, 'Username already exists.')
                return render(request, 'donor/register.html')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'email id already exists.')
                return render(request, 'donor/register.html')
            else:
                user = User.objects.create_user(
                    username=uname,
                    password=passw1,
                    email=email,
                    is_donor=True,
                )
                user.save()
                # Add a success message
                messages.success(request, 'Registration successful. You can now log in.')
                return redirect('donor_login')
        else:
            messages.error(request, 'password not matching.')
            return redirect('donor_register')
        
    else:
        return render(request, "donor/register.html")
    
#############login #########################
def donor_login(request):  
    if request.method == 'POST':
        uname = request.POST.get('username')
        passw = request.POST.get('password')

        user = User.objects.filter(username=uname).first()
        
        if user is not None and user.check_password(passw) and user.is_donor:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid login credentials.')
    return render(request, "donor/login.html")

################ add Donor details #################
def add_donor(request):
    if request.method == "POST":
        # Retrieve form data from request.POST
        name = request.POST.get("name")
        age = request.POST.get("age")
        address = request.POST.get("address")
        mobile = request.POST.get("phone")
        email = request.POST.get("email")
       
        district = request.POST.get("district")
        gender = request.POST.get("gender")
        image=request.FILES.get('img')

      
        # Create a new user or retrieve the current user (assuming the donor is logged in)
        if request.user.is_authenticated:
            current_user = request.user
        else:
            current_user = User.objects.create_user(username="a_random_username", password="a_random_password", is_donor=True)
         # Update the user's details with the form data
        current_user.name = name
        current_user.age = age
        current_user.address = address
        current_user.mobile = mobile
        current_user.email = email
        current_user.district = district
        current_user.gender = gender
        current_user.photo = image

        # Save the user object with the updated details
        current_user.save()
        return redirect('view_donor',pk=current_user.pk)  # Redirect to the donor's dashboard or a success page
    

    return render(request,'donor/add_donor.html')

################view donor details #############

def view_donor(request,pk):
    view=User.objects.filter(pk=pk)
    context={
        'view':view
    }
    return render(request,'donor/view_donor.html',context)

############ Update donor details #############3

def update_donor(request,pk):
    update=User.objects.get(pk=pk)
    if request.method == 'POST':
        if 'img' in request.FILES:
            if len(update.photo) > 0:
                os.remove(update.photo.path)
            update.photo = request.FILES['img']
        update.name=request.POST.get('name')
        update.age=request.POST.get('age')
        update.address=request.POST.get('address')
        update.mobile=request.POST.get('phone')
        update.email=request.POST.get('email')
        
        update.district=request.POST.get('district')
        update.gender=request.POST.get('gender')
        update.save()  
        return redirect('view_donor', pk=pk)    
    context={
        'update':update
    }
    return render(request,'donor/update_donor.html',context)

############add blood details ###############

def donate(request,pk):
    
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        # Retrieve form data from request.POST
        blood = request.POST.get("blood")
        unit = request.POST.get("unit")
        disease = request.POST.get("disease")
        # Update the User model fields
        user.blood_grou = blood
        user.unit = unit
        user.disease = disease
        user.save()
        return redirect('index')

    context={
        'user':user
    }
        

    return render(request,'donor/donate_blood.html',context)

##########view Blood Details##########


def view_donate(request,pk):
    
    user = get_object_or_404(User, pk=pk)    
    context={
        'user':user
    }
    return render(request,'donor/view_blood.html',context)

################# update blood details ##################
def update_donate(request,pk):
    
    update = get_object_or_404(User, pk=pk)    
    if request.method == 'POST':
        
        update.blood_grou=request.POST.get('blood')
        update.unit=request.POST.get('unit')
        update.disease=request.POST.get('disease')
        update.age=request.POST.get('age')
        update.save()  
        return redirect('view_donate', pk=pk) 
        
        
    context={
        'update':update
    }
    return render(request,'donor/update_blood.html',context)

############# delete blood details ###############
def delete_donate(request,pk):
    user = get_object_or_404(User, id=pk)
    
    # Delete specific fields
    user.blood_grou = None
    user.unit = None
    user.disease = None
    user.age = None
    # Save the changes
    user.save()
    return redirect('view_donate',pk=pk)

############# VIEW blood request #################
def patient_request(request):
    user=request.user
    view=BloodRequest.objects.filter(donor_id=user)
    context={
        'view':view
    }
    return render(request,'donor/view_request.html',context)


###########approved blood request ################

def approve_request(request, request_id):
    # Get the BloodRequest object
    blood_request = get_object_or_404(BloodRequest, id=request_id)

    # Check if the donor is the requester
    if blood_request.donor == request.user:
        # Update the status to approved
        blood_request.status = True
        blood_request.save()

    return redirect('patient_request') 



############logout donor ####################

def SignOut(request):
     logout(request)
     return redirect('home')



#######################patient panel start ############################################

###########patient home ####################
def patient_home(request):
    
     # Query all donors
    donors = User.objects.filter(is_donor=True)
    
    context={
        
        'donors':donors
    }
    return render(request,'patient/index.html',context)


##################patient registeration ################

def patient_register(request):
    if request.method == "POST":
        uname = request.POST.get("username")
        passw1 = request.POST.get("password")
        passw2= request.POST.get("password1")
        email= request.POST.get("email")
        if passw1 ==passw2:
            if User.objects.filter(username=uname).exists():
                messages.error(request, 'Username already exists.')
                return render(request, 'patient/signup.html')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'email id already exists.')
                return render(request, 'patient/signup.html')
            else:
                user = User.objects.create_user(
                    username=uname,
                    password=passw1,
                    email=email,
                    is_patient=True,
                )
                user.save()
                # Add a success message
                messages.success(request, 'Registration successful. You can now log in.')
                return redirect('patient_login')
        else:
            messages.error(request, 'password not matching.')
            return redirect('patient_register')
        
    else:
        return render(request, "patient/signup.html")
    

############## patient login #################

def patient_login(request):  
    if request.method == 'POST':
        uname = request.POST.get('username')
        passw = request.POST.get('password')

        user = User.objects.filter(username=uname).first()
        
        if user is not None and user.check_password(passw) and user.is_patient:
            login(request, user)
            return redirect('patient_home')
        else:
            messages.error(request, 'Invalid login credentials.')
    return render(request, "patient/signin.html")

################ add Patient details #################
def add_patient(request):
    if request.method == "POST":
        # Retrieve form data from request.POST
        name = request.POST.get("name")
        age = request.POST.get("age")
        address = request.POST.get("address")
        mobile = request.POST.get("phone")
        email = request.POST.get("email")
       
        district = request.POST.get("district")
        gender = request.POST.get("gender")
        image=request.FILES.get('img')

      
        # Create a new user or retrieve the current user (assuming the donor is logged in)
        if request.user.is_authenticated:
            current_user = request.user
        else:
            current_user = User.objects.create_user(username="a_random_username", password="a_random_password", is_patient=True)
         # Update the user's details with the form data
        current_user.name = name
        current_user.age = age
        current_user.address = address
        current_user.mobile = mobile
        current_user.email = email
        current_user.district = district
        current_user.gender = gender
        current_user.photo = image

        # Save the user object with the updated details
        current_user.save()
        return redirect('view_patient',pk=current_user.pk)  # Redirect to the donor's dashboard or a success page
    

    return render(request,'patient/add_patient.html')


################view patient details #############

def view_patient(request,pk):
    view=User.objects.filter(pk=pk)
    context={
        'view':view
    }
    return render(request,'patient/view_patient.html',context)

############ Update patient details #############3

def update_patient(request,pk):
    update=User.objects.get(pk=pk)
    if request.method == 'POST':
        if 'img' in request.FILES:
            if len(update.photo) > 0:
                os.remove(update.photo.path)
            update.photo = request.FILES['img']
        update.name=request.POST.get('name')
        update.age=request.POST.get('age')
        update.address=request.POST.get('address')
        update.mobile=request.POST.get('phone')
        update.email=request.POST.get('email')
        
        update.district=request.POST.get('district')
        update.gender=request.POST.get('gender')
        update.save()  
        return redirect('view_patient', pk=pk)    
    context={
        'update':update
    }
    return render(request,'patient/update_patient.html',context)

############### view all blood details##############33

def view_blood(request):
    # Query all donors
    donors = User.objects.filter(is_donor=True)
    context ={
        'donors':donors
    }
    return render(request,'patient/view_all_blood.html',context)

################make blood request ##############

def make_request(request,pk):
    
    if request.method == 'POST':
        patient_name = request.POST.get('name')
        patient_age = request.POST.get('age')
        reason = request.POST.get('reason')
        blood_type = request.POST.get('blood')
        unit = request.POST.get('unit')
        doctor = request.POST.get('doctor')

        donor = User.objects.get(id=pk)
        
        

        # Create a new BloodRequest object
        BloodRequest.objects.create(
            
            donor=donor,
           
            patient_name=patient_name,
            patient_age=patient_age,
            reasen=reason,
            blood_type=blood_type,
            unit=unit,
            doctor=doctor
        )

        messages.success(request, 'Blood request sent successfully!')
        return redirect('view_blood')
    return render(request,'patient/make_request.html')


###############blood request history ################

def request_history(request):
    patient = request.user.name
    blood_requests = BloodRequest.objects.filter(patient_name=patient)
    context={
        'blood_requests':blood_requests
    }
    return render(request,'patient/request_history.html',context)


############logout patient ####################

def patient_SignOut(request):
     logout(request)
     return redirect('home')

