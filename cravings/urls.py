from django.urls import path

from . import views

urlpatterns = [
    # Page Views
    path("", views.index, name="index"),
    path("category/<str:category_name>", views.CategoryView.as_view(), name="category"),
    path("category/<str:category_name>/<str:subcategory_name>", views.SubcategoryView.as_view(), name="subcategory"),
    path("restaurant/<str:restaurant_name>", views.RestaurantView.as_view(), name="restaurant"),
    path("restaurant/<str:restaurant_name>/all_dinelists", views.RestaurantDinelistsView.as_view(), name="restaurant_dinelists"),
    path("restaurant/<str:restaurant_name>/all_reviews", views.RestaurantReviewsView.as_view(), name="restaurant_reviews"),
    path("restaurant/<str:restaurant_name>/add_review", views.AddReviewView.as_view(), name="add_review"),
    path("cravings/<str:username>", views.CravingsView.as_view(), name="cravings"),
    path("prof_dinelists/<str:username>", views.ProfDinelistsView.as_view(), name="prof_dinelists"),
    path("dinelist", views.DinelistView.as_view(), name="dinelist"),
    path("search", views.SearchView.as_view(), name="search"),
    path("search/<str:parsed_search_request_string>/all_restaurants", views.SearchRestaurantsView.as_view(), name="search_restaurants"),
    path("search/<str:parsed_search_request_string>/all_dinelists", views.SearchDinelistsView.as_view(), name="search_dinelists"),

    # Sessions
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
]
