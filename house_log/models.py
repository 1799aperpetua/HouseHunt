from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User  # default User model from Django

# Create your models here.

class House(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.pk) + " | " + str(self.address)

    # = = = = = = Status = = = = = = #
    # ============================== #
    
    date_available = models.DateField(blank=True, null=True)

    next_steps = models.CharField(max_length=1000, blank=True, null=True) # next steps/last contact/resolution

    applied_status = models.BooleanField(blank=True, null=True)

    archive = models.BooleanField(default=False)

    # = = = House Information = = = #
    # ============================= #

    address = models.CharField(max_length=100)

    web_address = models.CharField(max_length=1000)

    # Type of home
    HOUSE=1
    SPLIT_HOUSE=2
    APARTMENT=3
    HOME_CHOICES = (
        (HOUSE, 'House'),
        (SPLIT_HOUSE, 'Split House'),
        (APARTMENT, 'Apartment')
    )
    type_of_home = models.IntegerField(choices=HOME_CHOICES, blank=True, null=True)

    price = models.IntegerField()
    sq_footage = models.IntegerField(blank=True, null=True)

    beds = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], blank=True, null=True)
    bathrooms = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(8)], blank=True, null=True)

    # Dog Permission
    YES = 1
    NO = 2
    MAYBE = 3
    PERMISSION_CHOICES = (
        (YES, 'yes'),
        (NO, 'no'),
        (MAYBE, 'maybe'),
    )
    dog_permission = models.IntegerField(choices=PERMISSION_CHOICES, blank=True, null=True)

    # Neighborhood 
    POINT_BREEZE = 1
    NEWBOLD = 2
    PASSYUNK_SQUARE = 3
    GRAD_HOSPITAL = 4
    HAWTHORNE = 5
    BELLA_VISTA = 6
    QUEEN_VILLAGE = 7
    UNIV_CITY = 8
    FITLER_SQUARE = 9
    RITTENHOUSE_SQUARE = 10
    WASHINGTON_SQUARE = 11
    SOCIETY_HILL = 12
    OLD_CITY = 13
    CHINATOWN = 14
    WEST_PASSYUNK = 15
    CENTRALSOUTH_PHILLY = 16
    FAIRMOUNT = 17
    GRAYS_FERRY = 18
    NEIGHBORHOOD_CHOICES = (
        (POINT_BREEZE, 'Point Breeze'),
        (NEWBOLD, 'Newbold'),
        (PASSYUNK_SQUARE, 'Passyunk Square'),
        (GRAD_HOSPITAL, 'Graduate Hospital'),
        (HAWTHORNE, 'Hawthorne'),
        (BELLA_VISTA, 'Bella Vista'),
        (QUEEN_VILLAGE, 'Queen Village'),
        (UNIV_CITY, 'University City'),
        (FITLER_SQUARE, 'Fitler Square'),
        (RITTENHOUSE_SQUARE, 'Rittenhouse Square'),
        (WASHINGTON_SQUARE, 'Washington Square'),
        (SOCIETY_HILL, 'Society Hill'),
        (OLD_CITY, 'Old City'),
        (CHINATOWN, 'Chinatown'),
        (WEST_PASSYUNK, 'West Passyunk'),
        (CENTRALSOUTH_PHILLY, 'CentralSouth Philly'),
        (FAIRMOUNT, 'Fairmount'),
        (GRAYS_FERRY, 'Grays Ferry'),
    )
    neighborhood = models.IntegerField(choices=NEIGHBORHOOD_CHOICES, blank=True, null=True)


    # = = = = = = Notes = = = = = = #
    # ============================= #

    # This includes the bedroom as-well as other rooms
    room_notes = models.CharField(max_length=1000, blank=True, null=True) # office potential/large primary bedroom/etc.

    bathroom_notes = models.CharField(max_length=1000, blank=True, null=True) # double sink/old/etc.

    kitchen_notes = models.CharField(max_length=1000, blank=True, null=True) # small or big/cabinets/stovetop/water dispensar fridge

    dog_notes = models.CharField(max_length=1000, blank=True, null=True) # park, neighborhood, house thoughts.  Windows, his stuff etc.

    parking_notes = models.CharField(max_length=1000, blank=True, null=True)

    storage_bool = models.BooleanField(blank=True, null=True)

    # Outdoor area
    outdoor_bool = models.BooleanField(blank=True, null=True)
    outdoor_name = models.CharField(max_length=100, null=True, blank=True) # patio, deck, rooftop, front porch, etc.
    outdoor_notes = models.CharField(max_length=1000, blank=True, null=True) # rooftop, backyard, balcony, etc.

    # = = = = = = Scores = = = = = = #
    # ============================== #

    # weight the below items based on importance.  Potentially come up with a model to calculate score?  
    # Would need to look into a scientific (the best) way to calculate that score

    distance_to_park_score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], blank=True, null=True)

    # - Food - #
    food_score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], blank=True, null=True)
    
    # - Stores - #
    errand_stores_score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], blank=True, null=True)
    shopping_score = models.IntegerField(blank=True, null=True)

    # - Fun - #
    nightlife_score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], blank=True, null=True)
    #sports_complex_score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], blank=True, null=True)
    #distance_to_friends_score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], blank=True, null=True)

    # = = = = = = Commutes = = = = = = #
    # ================================ #
    car_commute_work = models.CharField(max_length=100, blank=True, null=True)
    bus_commute_work = models.CharField(max_length=100, blank=True, null=True)
    walk_commute_work = models.CharField(max_length=100, blank=True, null=True)
    walk_dist_commute_work = models.CharField(max_length=100, blank=True, null=True)

    car_commute_gym = models.CharField(max_length=100, blank=True, null=True)
    bus_commute_gym = models.CharField(max_length=100, blank=True, null=True)
    walk_commute_gym = models.CharField(max_length=100, blank=True, null=True)
    walk_dist_commute_gym = models.CharField(max_length=100, blank=True, null=True)

    # When we go to save the house, if the user has a work/gym address calc it.  If not , they'll have 
    # to do it from the update button on the view house page

    # = = = = = Coordinates = = = = = #
    # =============================== #
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

class Profile(models.Model):

    def __str__(self):
        return self.user.username

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    work_address = models.CharField(max_length=1000, blank=True, null=True)

    gym_address = models.CharField(max_length=1000, blank=True, null=True)

    #friend_addresses = models.ManyToManyField('Friend_Address', blank=True, null=True)

'''
class Friend_Address(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    address = models.CharField(max_length=400, null=True)







"At a glance" table with 3 KPIs


- - Pricing - -
a | b | c

- - Ratings - -
1 - a | b
2 - a | b
3 - a | b
4 - a | b
5 - a | b

- - Features - -
Commute ...
1 - a | b
2 - a | b
3 - a | b
4 - a | b

Neighborhood Info ...
1 - a | b
2 - a | b
3 - a | b

High Level ...
1 - a | b
2 - a | b
3 - a | b
4 - a | b
5 - a | b

High Level ...
1 - a | b
2 - a | b

- - Categories - - 
Shared Categories - a | b
Unique Categories - a | b | c

Pictures?

Map that adjusts based on location?

'''