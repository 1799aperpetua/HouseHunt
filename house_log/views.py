from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import UserLoginForm, RegisterUserForm, CreateHouseForm, UpdateProfileForm, UpdateStatusForm, UpdateNotesForm
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from .services import Calc_Neighborhood_Scores, QueryDistance, CaptureCoordinates
from .models import Profile, House
from django.urls import reverse
from django.db.models import Q

# Basic Home Page #
def Index(request):

    return render(request, 'index.html')


# Login #
def MyLogin(request):

    form = UserLoginForm()

    # If someone submits something to this MyLogin URL
    if request.method == "POST":
        print("POST Submitted on MyLogin")

        # fill out a form with the data provided in the POST request
        form = UserLoginForm(request, data=request.POST)

        if form.is_valid():
            
            print("Form is valid!")
            user_name = request.POST.get('username')
            pw = request.POST.get('password')

            user = authenticate(request, username=user_name, password=pw)

            if user is not None:

                auth.login(request, user)

                return redirect('user-home')

    # If someone just accesses this page (not submitting), we'll grab a blank form to show them
    context = {'form': form}

    return render(request, 'mylogin.html', context=context)

# Register | User Creation #
def Register(request):

    form = RegisterUserForm()

    if request.method == 'POST':

        form = RegisterUserForm(request.POST)

        if form.is_valid():

            form.save()
            
            return redirect('mylogin')

    context = {'form': form}

    return render(request, 'register.html', context=context)


# User Homepage
@login_required(login_url='mylogin')
def UserHome(request):

    return render(request, 'profile/user-home.html')

# Logout
def Logout(request):

    return redirect('')


# Add house
@login_required(login_url='mylogin')
def Add_House(request):

    form = CreateHouseForm()

    if request.method == "POST":

        form = CreateHouseForm(request.POST)

        # If our form is not valid, this will display what went wrong
        print(form.errors)
        if form.is_valid():

            house = form.save(commit=False)

            house.user = request.user

            # You could put logic in here to add the commute times

            # Calculate food, errand, shopping, and nightlife scores based on neighborhood
            #print("Address: ", house.address)
            #print("Neighborhood: ", house.get_neighborhood_display())
            scores = Calc_Neighborhood_Scores(house.get_neighborhood_display())

            house.food_score = scores[0]
            house.errand_stores_score = scores[1]
            house.shopping_score = scores[2]
            house.nightlife_score = scores[3]

            house_coordinates = CaptureCoordinates(house.address)
            house.latitude = house_coordinates["lat"]
            house.longitude = house_coordinates["long"]

            house.save()

            return redirect('user-home') # can redirect to view houses later
        else:
            print("Error, Form is not valid!!!!")

    context = {'form': form}

    return render(request, 'profile/add-house.html', context=context)


# View Houses
@login_required(login_url='mylogin')
def View_Houses(request):

    houses = House.objects.all()

    return render(request, 'profile/view-houses.html', context = {'houses': houses})

# View Profile
@login_required(login_url='mylogin')
def View_Profile(request):

    profile = request.user.profile

    return render(request, 'profile/user-profile.html', {'profile': profile})

# Update Profile
@login_required(login_url='mylogin')
def Update_Profile(request):

    user_profile = get_object_or_404(Profile, user=request.user)

    form = UpdateProfileForm(instance=user_profile)

    if request.method == 'POST':

        form = UpdateProfileForm(request.POST, instance=user_profile)
        
        if form.is_valid():

            form.save()

            return redirect('user-profile')

    context = {'form': form}

    return render(request, 'profile/update-profile.html', context=context)

class user_coords():
    work_lat = None
    work_long = None

# Drill in on a house
@login_required(login_url='mylogin')
def House_View(request, pk): # pk comes from the string passed in the url

    # Grab the instance of the house we're accessing
    house = House.objects.get(id=pk)

    # Determine coordinates to be passed into the google maps static api
    house_coordinates = CaptureCoordinates(house.address)
    house.latitude = house_coordinates["lat"]
    house.longitude = house_coordinates["long"]
    house.save()
    
    user = request.user
    if user.profile.work_address is not None:
        work_coordinates = CaptureCoordinates(user.profile.work_address)
        uc = user_coords()
        uc.work_lat = work_coordinates["lat"]
        uc.work_long = work_coordinates["long"]
        
    # Put the house into a context dictionary so that it can be accessed in our html
    context = {'house': house, "uc": uc}

    return render(request, 'profile/house-view.html', context=context)

# Update a house
@login_required(login_url='mylogin')
def Update_House(request, pk):

    house = House.objects.get(id=pk)

    if request.method == "POST":
        form = CreateHouseForm(request.POST, instance=house)

        if form.is_valid():
            form.save()
            return redirect('read-house', pk=pk)
        else:
            print("Form was not valid!")
            for error in form.errors:
                print(error)

    context = {'form': CreateHouseForm(instance=house)}

    return render(request, 'profile/update-house.html', context = context)

# Update a house's status section
@login_required(login_url='mylogin')
def UpdateStatus(request, pk):

    # Capture the house using the pk from our url's arguments
    house = House.objects.get(id=pk)

    # Check if our request is POST to see if the user is submitting information
    if request.method == 'POST':
        form = UpdateStatusForm(request.POST, instance=house)

        if form.is_valid():
            form.save()
            return redirect('read-house', pk=pk)
        else:
            print("Form was not valid!")
            for error in form.errors:
                print(error)

    context = {'form': UpdateStatusForm(instance=house)}

    return render(request, 'profile/update-status.html', context=context)

# Update A house's notes section
@login_required(login_url='mylogin')
def UpdateNotes(request, pk):

    # Capture the house using the pk from our url's arguments
    house = House.objects.get(id=pk)

    # Check if our request is POST to see if the user is submitting information
    if request.method == 'POST':
        form = UpdateNotesForm(request.POST, instance=house)

        if form.is_valid():
            form.save()
            return redirect('read-house', pk=pk)
        else:
            print("Form was not valid!")
            for error in form.errors:
                print(error)

    context = {'form': UpdateNotesForm(instance=house)}

    return render(request, 'profile/update-notes.html', context=context)


# Archive a house


# Update Commute Times for a house
@login_required(login_url='mylogin')
def Update_Commutes(request, pk):

    # Capture the house for our origin
    house = House.objects.get(id=pk)

    # Capture the user's addresses for destinations
    user = request.user

    data = QueryDistance(user, house)

    house.car_commute_work = data['work']['driving']['time']
    house.walk_commute_work = data['work']['walking']['time']
    house.walk_dist_commute_work = data['work']['walking']['distance']
    house.bus_commute_work = data['work']['bus']['time']

    house.car_commute_gym = data['gym']['driving']['time']
    house.walk_commute_gym = data['gym']['walking']['time']
    house.walk_dist_commute_gym = data['gym']['walking']['distance']
    house.bus_commute_gym = data['gym']['bus']['time']

    house.save()

    return redirect('read-house', pk=pk)

    # NEED TO ADD IT SO THAT IT AUTOMATICALLY UPDATES COMMUTES WHEN WE ADD A NEW HOUSE (IF THE PERSON HAS A WORK AND/OR GYM ADDRESS)


@login_required(login_url='mylogin')
def Comparator(request):
    if request.method == "POST":
        house_ids = request.POST.getlist('house_ids')
        if len(house_ids) < 2:
            return render(request, 'profile/compare-houses.html', {'error': 'Please select at least two listings to compare.'})
        url = reverse('display_comparison', args=house_ids)
        return redirect(url)
    else:
        houses = House.objects.all()
        return render(request, 'profile/compare-houses.html', {'houses': houses})

@login_required(login_url='mylogin')
def Display_Comparison(request):
    house1 = get_object_or_404(House, pk=request.GET.get('pk1'))
    house2 = get_object_or_404(House, pk=request.GET.get('pk2'))
    if request.GET.get('pk3'):
        house3 = get_object_or_404(House, pk=request.GET.get('pk3'))
        return render(request, 'profile/display_comparison.html', {'house1':house1, 'house2':house2, 'house3':house3})
    else:
        return render(request, 'profile/display_comparison.html', {'house1':house1, 'house2':house2})
    
@login_required(login_url='mylogin')
def UpdateLatLong(request):
    if request:
        # query houses who don't have a latitude or longitude
        houses = House.objects.filter(Q(latitude__isnull=True) | Q(longitude__isnull=True))
        # run capture coordinates on it
        for house in houses:
            print("House:", house.address)
            house_coordinates = CaptureCoordinates(house.address)
            house.latitude = house_coordinates["lat"]
            house.longitude = house_coordinates["long"]
            house.save()
            print("Coordinates updated!")

    return redirect('view-houses')

# = = = Testing = = = #
@login_required(login_url='mylogin')
def TestCompare(request):
    house1 = get_object_or_404(House, pk=4)
    house2 = get_object_or_404(House, pk=3)
    return render(request, 'profile/testcomparison.html', {'house1':house1, 'house2':house2})