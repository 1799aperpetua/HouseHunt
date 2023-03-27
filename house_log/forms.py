from django.forms import ModelForm

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User

from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput

from django import forms
from .models import House, Profile


# Register a User

class RegisterUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



# User Login

class UserLoginForm(AuthenticationForm):

    username = forms.CharField(widget=TextInput())

    password = forms.CharField(widget=PasswordInput())


# Create a House

class CreateHouseForm(ModelForm):

    class Meta: 
        model = House
        fields = ['address', 'web_address', 'type_of_home', 'price', 'sq_footage', 'beds', 'bathrooms', 'dog_permission', 'neighborhood',
        'room_notes', 'bathroom_notes', 'kitchen_notes', 'outdoor_bool', 'storage_bool', 'dog_notes',
        'distance_to_park_score', 'date_available', 'applied_status', 'next_steps']
        exclude = ['user', 'food_score', 'errand_stores_score', 'shopping_score', 'nightlife_score']

    # Figure out how to show/hide fields based on the value of other fields
    # Potentially through __init__(self): super()...


# Update a House
class UpdateHouseForm(ModelForm):
    # Define a list of choices for the user to select from
    field_choices = [
        ('address', 'Address'),
        ('price', 'Price'),
        ('sq_footage', 'Sq. Footage'),
        ('beds', 'Bedrooms'),
        ('bathrooms', 'Bathrooms'),
        ('type_of_home', 'Type of Home'),
        ('pet_permission', 'Pet Permission'),
        ('dog_notes', 'Dog Notes'),
        ('room_notes', 'Room Notes'),
        ('bathroom_notes', 'Bathroom Notes'),
        ('kitchen_notes', 'Kitchen Notes')
    ]
    field = forms.TypedChoiceField(choices=field_choices, widget=forms.RadioSelect)

    class Meta:
        model = House
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Dynamically add the selected field to the form fields
        if 'field' in self.data:
            field = self.data['field']
            print(f"Selected Field: {field}")
            print("Form Fields:", self.fields)
            if field:
                self.fields[field] = forms.CharField(max_length=100, widget=forms.TextInput())
                print("Form Fields after Update", self.fields)
                

    def save(self, commit=True):
        # Only save the selected field
        field = self.data.get('field')
        setattr(self.instance, field, self.cleaned_data[field])
        if commit:
            self.instance.save()
        return self.instance

# Update Profile
class UpdateProfileForm(ModelForm):

    class Meta:
        
        model = Profile
        fields = ['work_address', 'gym_address']
        exclude = ['user']

# Update House Status
class UpdateStatusForm(ModelForm):

    class Meta:
        model = House
        fields = ['date_available', 'next_steps', 'applied_status']
        exclude = ['user']

class UpdateNotesForm(ModelForm):

    class Meta:
        model = House
        fields = ['room_notes', 'bathroom_notes', 'kitchen_notes', 'dog_notes', 'parking_notes', 'storage_bool', 'outdoor_bool', 'outdoor_name', 'outdoor_notes']
        exclude = ['user']