from .models import Restaurant

def layout_context(request):
    settings = sorted(Restaurant.objects.values_list('setting', flat=True).distinct())
    cuisines = sorted(Restaurant.objects.values_list('cuisine', flat=True).distinct())
    price_ranges = sorted(Restaurant.objects.values_list('price_range', flat=True).distinct())

    return {
        'settings': settings,
        'cuisines': cuisines,
        'price_ranges': price_ranges
    }
