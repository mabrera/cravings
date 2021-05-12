from .models import DineList, Restaurant, User


# Input: [string] category name (settings, cuisines, price ranges, dinelists, or a given user's dinelists), [string] username
# Action: Queries database for all restaurants, organizes them in category's subcategories, sorts them by mean rating, tags them with whether they're craved by user or not
# Output: [(subcategory, [(restaurant, is_craved)])]
#   i.e. returns a [list] of [tuples], whose first element is a [string] of the subcategory name and second element is a [list] of [tuples], whose 
#   first element is a restaurant [object] and second element is a [boolean] for whether said restaurant is in the session's user's cravings
def subcategorized_restaurants(category_name, username):
    # Initialize outer list [(subcategory, [(restaurant, is_craved)])]
    subcategorized_restaurants = []
    # Query database for category's subcategories
    if category_name == 'dinelist':
        subcategories = DineList.objects.all()
    elif category_name == 'prof_dinelist':
        subcategories = DineList.objects.filter(user=User.objects.get(username=username))
    else :
        subcategories = sorted(Restaurant.objects.values_list(category_name, flat=True).distinct())
    # Query database for subcategories' restaurants
    for subcategory in subcategories:
        if category_name in ['dinelist', 'prof_dinelist']:
            subcategory_restaurants_raw = subcategory.restaurants.all()
        else:
            subcategory_restaurants_raw = Restaurant.objects.filter(**{category_name+'__in':[subcategory]}).all()
        # Sort subcategory's restaurants by mean rating
        sort_helper = []
        for restaurant in subcategory_restaurants_raw:
            sort_helper.append((restaurant, restaurant.mean_rating))
        sort_helper = sorted(sort_helper, key=lambda item:item[1], reverse=True)
        # Initialize inner list [(restaurant, is_craved)] for current subcategory
        subcategory_restaurants = []
        # Populate inner list with tuples (restaurant, is_craved) by checking if there's an active session,
        # and if so, querying the database for whether each restaurant is in the session's user's cravings
        for item in sort_helper:
            if username == '':
                subcategory_restaurants.append((item[0], False))
            else:
                subcategory_restaurants.append((item[0], {'is_craved': item[0] in User.objects.get(username=username).cravings.all()}))
        # Populate outer list with tuples [(subcategory, inner_list)]
        subcategorized_restaurants.append((subcategory, subcategory_restaurants))
    return subcategorized_restaurants


# Input: [string] category name (settings, cuisines, price ranges, dinelists, or a given user's cravings,), [string] subcategory name (of said category), [string] username
# Action: Queries database for all restaurants within subcategory and sorts them by mean rating
# Output: [(restaurant, is_craved)]
#   i.e. returns a [list] of [tuples] whose first element is a restaurant [object] and second element is a [boolean] for whether said restaurant is in the session's user's cravings
def subcategory_restaurants(category_name, subcategory_name, username):
    # Query database for subcategory's restaurants
    if category_name == 'dinelist':
        subcategory_restaurants_raw = DineList.objects.get(name=subcategory_name).restaurants.all()
    elif category_name == 'cravings':
        subcategory_restaurants_raw = User.objects.get(username=username).cravings.all()
    else:
        subcategory_restaurants_raw = Restaurant.objects.filter(**{category_name+'__in':[subcategory_name]}).all()
    # Sort restaurants by mean rating
    sort_helper = []
    for restaurant in subcategory_restaurants_raw:
        sort_helper.append((restaurant, restaurant.mean_rating))
    sort_helper = sorted(sort_helper, key=lambda item:item[1], reverse=True)
    # Initialize subcategory's list [(restaurant, is_craved)]
    subcategory_restaurants = []
    # Populate list with tuples (restaurant, is_craved) by checking if there's an active session,
    # and if so, querying the database for whether each restaurant is in the session's user's cravings
    for item in sort_helper:
        if username == '':
            subcategory_restaurants.append((item[0], False))
        else:
            subcategory_restaurants.append((item[0], {'is_craved': item[0] in User.objects.get(username=username).cravings.all()}))
    return subcategory_restaurants    


# Input: [string] restaurant name, [string] username
# Action: Queries database for all dinelists that include input restaurant, finds these dinelists' restaurants, sorts them by mean rating, 
#   tags them with whether they're craved by user or not
# Output: [(dinelist, [(restaurant, is_craved)])]
#   i.e. returns a [list] of [tuples], whose first element is a [string] of the dinelist name and second element is a [list] of [tuples], whose 
#   first element is a restaurant [object] and second element is a [boolean] for whether said restaurant is in the session's user's cravings
# In a sense, this is equivalent to subcategorized_restaurants(), except it doesn't get all the resaurants in the database but only those
#   in the dinelists that feature the input restaurant
def restaurant_dinelists(restaurant_name, username):
    # Query database for restaurant
    restaurant = Restaurant.objects.get(name=restaurant_name)
    # Initialize dinelists list [(dinelist, [(restaurant, is_craved)])]
    dinelists = []
    # Check which dinelists include input restaurant, call subcategory_restaurants() to find their restaurants and add them to output list
    for dinelist in DineList.objects.all():
        if restaurant in dinelist.restaurants.all():
            dinelists.append((dinelist, subcategory_restaurants('dinelist', dinelist.name, username)))
    return dinelists


# Input: [string] querystring
# Action: parses querystring and separates queries and filters of settings, cuisines, and price ranges
# Output: ([queries], [filtered settings], [filtered cuisines], [filtered price ranges])
#   i.e. [tuple] whose elements are a [list] of [string] queries and [list]s of [string] settings, cuisine, and price range filters
#   called a "parsed search request"
def parse_search_request(request):
    queries = request.GET['q'].split()
    settings_filters = request.GET.getlist('setting[]')
    cuisines_filters = request.GET.getlist('cuisine[]')
    price_ranges_filters = request.GET.getlist('price_range[]')
    return (queries, settings_filters, cuisines_filters, price_ranges_filters)


# Input: [int] n, [string] character, [string] string
# Action: finds the index of the n-th instance of character in string
# Output: [int] index
def nth_occurrence(n, character, string):
    count = 0
    index = 0
    while index < len(string):
        if string[index] == character:
            count += 1
        if count == n:
            return index
        index += 1
    return None


# Input: parsed search query [string] (stringified output from parse_search_request())
# Action: re-constructs [list]s of queries and filters from [string] '([queries], [filtered settings], [filtered cuisines], [filtered price ranges])'
# Output: ([queries], [filtered settings], [filtered cuisines], [filtered price ranges])
#   i.e. [tuple] whose elements are a [list] of [string] queries and [list]s of [string] settings, cuisine, and price range filters
#   called a "parsed search request"
def parse_parsed_search_request_string(parsed_search_request_string):
    queries = parsed_search_request_string[nth_occurrence(1,'[',parsed_search_request_string)+1:nth_occurrence(1,']',parsed_search_request_string)].replace('\'','').split(', ')
    settings_filters = parsed_search_request_string[nth_occurrence(2,'[',parsed_search_request_string)+1:nth_occurrence(2,']',parsed_search_request_string)].replace('\'','').split(', ')
    cuisines_filters = parsed_search_request_string[nth_occurrence(3,'[',parsed_search_request_string)+1:nth_occurrence(3,']',parsed_search_request_string)].replace('\'','').split(', ')
    price_ranges_filters = parsed_search_request_string[nth_occurrence(4,'[',parsed_search_request_string)+1:nth_occurrence(4,']',parsed_search_request_string)].replace('\'','').split(', ')
    if queries == ['']:
        queries = []
    if settings_filters == ['']:
        settings_filters = []
    if cuisines_filters == ['']:
        cuisines_filters = []
    if price_ranges_filters == ['']:
        price_ranges_filters = []
    return (queries, settings_filters, cuisines_filters, price_ranges_filters)


# Input: [parsed search request], [string] username
# Action: Queries database for all restaurants that match queries, then sorts them by filter match count, query match count, mean rating, in that priority
# Output: [(restaurant, is_craved)]
#   i.e. returns a [list] of [tuples] whose first element is a restaurant [object] and second element is a [boolean] for whether said restaurant is in the session's user's cravings
def search_restaurant_results(parsed_search_request, username):
    # Get queries and filters
    queries = parsed_search_request[0]
    settings_filters = parsed_search_request[1]
    cuisines_filters = parsed_search_request[2]
    price_ranges_filters = parsed_search_request[3]
    # Initialize [dictionary] of restaurants that match queries
    results_raw = {}
    # Query database for all restaurants matching at least one of the queries
    for query in queries:
        query_restaurants = Restaurant.objects.filter(name__contains=query)
        # For each such matching restaurant, initialize at 1 an [int] count of how many queries it matches and at 0 an [int] count of how many filters it matches
        for restaurant in query_restaurants:
            query_matches = 1
            filter_matches = 0
            # If restaurant already in [dictionary] of restaurants that match queries, increase its [int] count of query matches by 1
            if restaurant.name in results_raw:
                query_matches = results_raw[restaurant.name][2] + 1
            # If there's any filters at all, check whether restaurant matches said filters and increase its [int] count of filter matches accordingly
            if len(settings_filters) + len(cuisines_filters) + len(price_ranges_filters) > 0:
                if restaurant.setting in settings_filters:
                    filter_matches += 1
                if restaurant.cuisine in cuisines_filters:
                    filter_matches += 1
                if restaurant.price_range in price_ranges_filters:
                    filter_matches += 1
            # Update restaurant's entry in [dictionary] of restaurants that match queries with freshly computed filter match count, query match count, and mean rating
            results_raw[restaurant.name] = (restaurant, filter_matches, query_matches, restaurant.mean_rating)
    # From [dictionary] of restaurants that match queries generate [list] of restaurants and sort them by filter match count, query match count, and mean rating, in that priority
    sort_helper = sorted(results_raw.items(), key=lambda item:(item[1][1], item[1][2], item[1][3]), reverse=True)
    # Initialize list of restaurant search results [(restaurant, is_craved)]
    results = []
    for item in sort_helper:
        # Populate list with tuples (restaurant, is_craved) by checking if there's an active session,
        # and if so, querying the database for whether each restaurant is in the session's user's cravings
        if username == '':
            results.append((item[1][0], False))
        else:
            results.append((item[1][0], {'is_craved': item[1][0] in User.objects.get(username=username).cravings.all()}))
    return results


# Input: [parsed search request], [string] username
# Action: Queries database for all dinelists that match queries, then sorts them by query match count
# Output: [(dinelist, [(restaurant, is_craved)])]
#   i.e. returns a [list] of [tuples], whose first element is a [string] of the dinelist name and second element is a [list] of [tuples], whose 
#   first element is a restaurant [object] and second element is a [boolean] for whether said restaurant is in the session's user's cravings
def search_dinelist_results(parsed_search_request, username):
    # Get queries (and ignore filters, since those are only relevant for restaurants)
    queries = parsed_search_request[0]
    # Initialize [dictionary] of dinelists that match queries
    results_raw = {}
    # Initialize list of dinelist search results [(dinelist, [(restaurant, is_craved)])]
    results = []
    # Query database for all dinelists matching at least one of the queries
    for query in queries:
        query_dinelists = DineList.objects.filter(name__contains=query)
        # For each such matching dinelist, initialize at 1 an [int] count of how many queries it matches
        for dinelist in query_dinelists:
            query_matches = 1
            # If dinelist already in [dictionary] of dinelists that match queries, increase its [int] count of query matches by 1
            if  dinelist.name in results_raw:
                query_matches = results_raw[dinelist.name][1] + 1
            # Update restaurant's entry in [dictionary] of dinelists that match queries with freshly computed query match count
            results_raw[dinelist.name] = (dinelist, query_matches)
    # From [dictionary] of dinelists that match queries generate [list] of dinelists and sort them by query match count
    dinelists_sort_helper = sorted(results_raw.items(), key=lambda item:item[1][1], reverse=True)
    # For each dinelist in [dictionary] of dinelists that match queries, find all its restaurants, sort them by mean rating
    # (analogous to subcategorized_restaurants('dinelist', username)) except only for those dinelists matching search queries
    for dinelist in dinelists_sort_helper:
        dinelist_restaurants_raw = dinelist[1][0].restaurants.all()
        restaurants_sort_helper = []
        for restaurant in dinelist_restaurants_raw:
            restaurants_sort_helper.append((restaurant, restaurant.mean_rating))
        restaurants_sort_helper = sorted(restaurants_sort_helper, key=lambda item:item[1], reverse=True)
        dinelist_restaurants = []
        for item in restaurants_sort_helper:
            if username == '':
                dinelist_restaurants.append((item[0], False))
            else:
                dinelist_restaurants.append((item[0], {'is_craved': item[0] in User.objects.get(username=username).cravings.all()}))
        results.append((dinelist[1][0], dinelist_restaurants))
    return results


# Input: [string] username
# Action: If there's an active session, get session's user's dinelists
# Output: [list] of user's dinelists
def user_dinelists(username):
    if username != '':
        return DineList.objects.filter(user=User.objects.get(username=username))
    return None
