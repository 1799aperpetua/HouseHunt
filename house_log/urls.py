from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [

    # Index (Home) Page
    path('', views.Index, name=""),

    # Login Page
    path('login', views.MyLogin, name='mylogin'),

    # Register
    path('register', views.Register, name='register'),


    # User Homepage
    path('homepage', views.UserHome, name='user-home'),

    # Logout
    path('logout', views.Logout, name='user-logout'),

    # User Profile
    path('user-profile', views.View_Profile, name='user-profile'),

    # Update Profile
    path('update-profile', views.Update_Profile, name='update-profile'),


    # Add house
    path('add-house', views.Add_House, name='add-house'),

    # View Houses
    path('view-houses', views.View_Houses, name='view-houses'),

    # Drill in on a house
    path('house/<str:pk>/', views.House_View, name='read-house'),

    # Update a house
    path('update-house/<str:pk>/', views.Update_House, name='update-house'),

    # Update status for a house
    path('update-status/<str:pk>/', views.UpdateStatus, name='update-status'),

    # Update notes for a house
    path('update-notes/<str:pk>', views.UpdateNotes, name='update-notes'),

    # Compare two houses
    # click compare houses -> form -> redirect 

    path('compare/', views.Comparator, name='compare-houses'),
    path('compare-houses/', views.Display_Comparison, name='display_comparison'),

    path('test/comparison', views.TestCompare, name="test-compare"),

    # Archive a house


    # Calculate commutes
    path('update-commutes/<str:pk>/', views.Update_Commutes, name='update-commutes'),

    # Update Lat/Long for all houses
    path('updatelatlong', views.UpdateLatLong, name='update-lat-long'), # you left off here. 
    # make a view, apply the service (possibly create a service)
    
    ]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)