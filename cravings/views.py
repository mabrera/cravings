from django.contrib.auth.backends import AllowAllUsersModelBackend
from django.http.response import JsonResponse

from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError

from django.views.generic import View
from .models import DineList, Restaurant, User, Review
from .util import parse_parsed_search_request_string, restaurant_dinelists, search_dinelist_results, search_restaurant_results, subcategorized_restaurants, subcategory_restaurants, parse_search_request, user_dinelists

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

import json

#----------------------------------------------------------------#
#-------------------------- Page Views --------------------------#
#----------------------------------------------------------------#

# Get - Redirects to category=settings view
def index(request):
    return HttpResponseRedirect(reverse('category', args=('setting',)))

class CategoryView(View):

    # For a given category (settings, cuisines, price ranges, or dinelists), shows all its subcategories in a vertical-scrollable format
    # whithin each subcategory, shows all its restaurants as small cards in a horizontal-scrollable format
    def get(self, request, category_name):
        return render(request, 'category.html', {
            'category': category_name.replace('_',' ').capitalize()+'s',
            'subcategorized_restaurants': subcategorized_restaurants(category_name, request.user.username),
            'category_link_attribute': category_name,
            'is_dinelist': category_name == 'dinelist',
            'user_dinelists': user_dinelists(request.user.username),
        })


class SubcategoryView(View):

    # For a given subcategory (within settings, cuisines, price ranges) or dinelist (within dinelists), 
    # shows all its restaurants as large cards in a vertical-scrollable format
    def get(self, request, category_name, subcategory_name):
        # If in a specific dinelist, find author
        dinelist_user = ''
        if category_name == 'dinelist':
            dinelist_user = DineList.objects.get(name=subcategory_name).user
        return render(request, 'subcategory.html', {
            'subcategory': subcategory_name,
            'subcategory_restaurants': subcategory_restaurants(category_name, subcategory_name, request.user.username),
            'is_dinelist': category_name == 'dinelist',
            'dinelist_user': dinelist_user,
            'user_dinelists': user_dinelists(request.user.username),
        })


class RestaurantView(View):

    # For a given restaurant, shows a header with pictures and info, dinelists it's featured in, and reviews
    def get(self, request, restaurant_name):
        # Query database for restaurant
        restaurant = Restaurant.objects.get(name=restaurant_name)
        # If there's an active session, figure out if restaurant is craved by session's user
        is_craved = False
        if request.user.is_authenticated:
            is_craved = restaurant in User.objects.get(username=request.user.username).cravings.all()
        return render(request, 'restaurant.html', {
            'restaurant': restaurant,
            'banner_images': restaurant.images.all(),
            'dinelists': restaurant_dinelists(restaurant_name, request.user.username)[:3],
            'reviews': restaurant.reviews.all()[:3],
            'num_reviews': len(restaurant.reviews.all()),
            'is_restaurant': True,
            'is_craved': is_craved,
            'user_dinelists': user_dinelists(request.user.username),
        })


class RestaurantDinelistsView(View):

    # For a given restaurant, shows all the dinelists it's featured in (accessed from RestaurantView)
    def get(self, request, restaurant_name):
        return render(request, 'category.html', {
            'category': 'Dinelists featuring '+restaurant_name,
            'subcategorized_restaurants': restaurant_dinelists(restaurant_name, request.user.username),
            'category_link_attribute': 'dinelist',
            'is_dinelist': True,
            'user_dinelists': user_dinelists(request.user.username),
        })


class RestaurantReviewsView(View):

    # For a given restaurant, shows all its reviews (accessed from RestaurantView)
    def get(self, request, restaurant_name):
        # Query database for restaurant
        restaurant = Restaurant.objects.get(name=restaurant_name)
        # If there's an acive session, figure out if restaurant is craved by session's user
        is_craved = False
        if request.user.is_authenticated:
            is_craved = restaurant in User.objects.get(username=request.user.username).cravings.all()
        return render(request, 'restaurant.html', {
            'restaurant': restaurant,
            'banner_images': restaurant.images.all(),
            'reviews': restaurant.reviews.all(),
            'num_reviews': len(restaurant.reviews.all()),
            'is_reviews': True,
            'is_craved': is_craved,
        })


class AddReviewView(View):

    # For a given restaurant, shows form to add a review
    def get(self, request, restaurant_name):
        restaurant = Restaurant.objects.get(name=restaurant_name)
        return render(request, 'restaurant.html', {
            'restaurant': restaurant,
            'banner_images': restaurant.images.all(),
            'is_add_review': True,
        })

    # Processes post request from submitting above review, updates restaurant's mean rating, stores data in database
    def post(self, request, restaurant_name):
        restaurant = Restaurant.objects.get(name=restaurant_name)
        visited = False
        if request.POST['visit_date'] != '':
            visited = True
        new_review = Review(
            user = request.user,
            restaurant = restaurant,
            rating = request.POST['star'],
            comment = request.POST['content'],
            visited = visited,
            visited_timestamp = request.POST['visit_date'],
        )
        new_review.save()
        restaurant.mean_rating = restaurant.update_mean_rating()
        restaurant.save()
        return HttpResponseRedirect(reverse('restaurant', args=(restaurant_name,)))


@method_decorator(csrf_exempt, name='dispatch')
class CravingsView(View):

    # For a given user (session's), shows all user's craved restaurants as large cards in a vertical-scrollable format
    def get(self, request, username):
        return render(request, 'subcategory.html', {
            'subcategory': username.replace('_',' ').capitalize()+'\'s Cravings',
            'subcategory_restaurants': subcategory_restaurants('cravings', '', username),
            'is_dinelist': False,
            'dinelist_user': '',
            'user_dinelists': user_dinelists(request.user.username),
        })

    # For a given restaurant, change its crave status for session's user
    def put(self, request, username):
        # Get data from put request (contains restaurant's name)
        data = json.loads(request.body)
        # If craved, uncrave; viceversa
        if data.get('crave') == True:
            request.user.cravings.add(Restaurant.objects.get(name=data.get('restaurant_name')))
        else:
            request.user.cravings.remove(Restaurant.objects.get(name=data.get('restaurant_name')))
        return HttpResponse(status=204)


class ProfDinelistsView(View):
    
    # For a category=a given user's own dinelists, shows all said user's dinelists in a vertical-scrollable format
    # whithin each dinelist, shows all its restaurants as small cards in a horizontal-scrollable format
    def get(self, request, username):
        return render(request, 'category.html', {
            'category': username,
            'subcategorized_restaurants': subcategorized_restaurants('prof_dinelist', username),
            'category_link_attribute': 'dinelist',
            'is_prof_dinelist': True,
            'user_dinelists': user_dinelists(request.user.username),
        })


@method_decorator(csrf_exempt, name='dispatch')
class DinelistView(View):

    # Creates a new dinelist
    def post(self, request):
        dinelist_name = request.POST['dinelist_name']
        new_dinelist = DineList(
            name = dinelist_name,
            user = request.user
        )
        new_dinelist.save()
        return HttpResponseRedirect(reverse('subcategory', args=('dinelist', dinelist_name)))

    # Processes adding/subtracting a given restaurant to/from a given dinelist
    def put(self, request):
        data = json.loads(request.body)
        dinelist = DineList.objects.get(name=data.get('dinelist_name'))
        restaurant = Restaurant.objects.get(name=data.get('restaurant_name'))
        if data.get('action') == 'add':
            dinelist.restaurants.add(restaurant)
        elif data.get('action') == 'remove':
            dinelist.restaurants.remove(restaurant)
        return HttpResponse(status=204)


class SearchView(View):

    # Displays restaurants and dinelists that best fit querystring
    def get(self, request):
        return render(request, 'search.html', {
            'parsed_request': str(parse_search_request(request)),
            'subcategory_restaurants': search_restaurant_results(parse_search_request(request), request.user.username)[:6],
            'subcategorized_restaurants': search_dinelist_results(parse_search_request(request), request.user.username)[:6],
            'category_link_attribute': 'dinelist',
            'is_dinelist': True,
            'user_dinelists': user_dinelists(request.user.username),
        })


class SearchRestaurantsView(View):

    # Displays restaurants that best fit querystring (accessed from SearchView)
    def get(self, request, parsed_search_request_string):
        return render(request, 'subcategory.html', {
            'subcategory': 'Search Results',
            'subcategory_restaurants': search_restaurant_results(parse_parsed_search_request_string(parsed_search_request_string), request.user.username),
            'user_dinelists': user_dinelists(request.user.username),
        })


class SearchDinelistsView(View):

    # Displays dinelists that best fit querystring (accessed from SearchView)
    def get(self, request, parsed_search_request_string):
        return render(request, 'category.html', {
            'category': 'Search Results',
            'subcategorized_restaurants': search_dinelist_results(parse_parsed_search_request_string(parsed_search_request_string), request.user.username),
            'category_link_attribute': 'dinelist',
            'is_dinelist': True,
            'user_dinelists': user_dinelists(request.user.username),
        })
        

#----------------------------------------------------------------#
#--------------------------- Sessions ---------------------------#
#----------------------------------------------------------------#

# Get - login
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "login.html")


# Get - logout
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


# Get - register
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html")
