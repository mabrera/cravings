from django.db import models
from django.db.models.fields import BooleanField, CharField, FloatField, IntegerField, TextField
from django.db.models.fields.related import ForeignKey, ManyToManyField

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    cravings = ManyToManyField('Restaurant', blank=True, related_name='craved_by')
    recommendations = ManyToManyField('Restaurant', blank=True, related_name='recommended_for')
    history = ManyToManyField('Restaurant', blank=True, related_name='customers')
    follows = ManyToManyField('User', blank=True, related_name='followers')

    def serialize(self):
        return {
            "id": self.id,
            "cravings": self.cravings,
            "recommendations": self.recommendations,
            "history": self.history,
            "follows": self.follows
        }


class Pic(models.Model):
    image_url = CharField(max_length=1000, blank=True, null=True)


class Restaurant(models.Model):
    name = CharField(max_length=100)
    clean_name = CharField(max_length=100)
    location = TextField(max_length=300, blank=True)
    business_hours = TextField(max_length=300, blank=True)
    phone = CharField(max_length=20, blank=True)
    email = CharField(max_length=100, blank=True)
    website = CharField(max_length=100, blank=True)
    mean_rating = FloatField(null=True, blank=True)
    image = CharField(max_length=1000, blank=True, null=True)
    images = ManyToManyField('Pic', blank=True)

    class Setting(models.TextChoices):
        FAST_FOOD = 'Fast Food'
        FAST_CASUAL = 'Fast Casual'
        SPORTS_BAR = 'Sports Bar'
        CASUAL_DINING = 'Casual Dining'
        FINE_DINING = 'Fine Dining'
        POP_UP = 'Pop-Up'
        FOOD_TRUCK = 'Food Truck'

    setting = CharField(max_length=100, choices=Setting.choices)

    class Cuisine(models.TextChoices):
        AFGHAN = 'Afghan'
        AFRICAN_AMERICAN = 'African_American'
        ALBANIAN = 'Albanian'
        ALGERIAN = 'Algerian'
        AMERICAN = 'American'
        AMISH_MENNONITE = 'Amish_Mennonite'
        ANGOLAN = 'Angolan'
        ARGENTINE = 'Argentine'
        ARMENIAN = 'Armenian'
        ARUBAN = 'Aruban'
        AUSTRALIAN = 'Australian'
        AUSTRIAN = 'Austrian'
        AZERBAIJANI = 'Azerbaijani'
        BAHAMIAN = 'Bahamian'
        BARBADIAN = 'Barbadian'
        BASQUE = 'Basque'
        BELGIAN = 'Belgian'
        BELIZEAN = 'Belizean'
        BELORUSSIAN = 'Belorussian'
        BOLIVIAN = 'Bolivian'
        BOSNIAN = 'Bosnian'
        BRAZILIAN = 'Brazilian'
        BULGARIAN = 'Bulgarian'
        BURMESE = 'Burmese'
        CAJUN = 'Cajun'
        CAMBODIAN = 'Cambodian'
        CAMEROON = 'Cameroon'
        CANADIAN = 'Canadian'
        CAPE_VERDEAN = 'Cape_Verdean'
        CHILEAN = 'Chilean'
        CHINESE = 'Chinese'
        COLOMBIAN = 'Colombian'
        CONGOLESE = 'Congolese'
        CORNISH = 'Cornish'
        COSTA_RICAN = 'Costa_Rican'
        CÔTE_DIVOIRE = 'Côte_dIvoire'
        CREOLE = 'Creole'
        CROATIAN = 'Croatian'
        CUBAN = 'Cuban'
        CZECH = 'Czech'
        DANISH = 'Danish'
        DOMINICAN = 'Dominican'
        DUTCH = 'Dutch'
        ECUADORIAN = 'Ecuadorian'
        EGYPTIAN = 'Egyptian'
        ENGLISH = 'English'
        ETHIOPIAN = 'Ethiopian'
        FILIPINO = 'Filipino'
        FINNISH = 'Finnish'
        FRENCH = 'French'
        GAMBIAN = 'Gambian'
        GEORGIAN = 'Georgian'
        GERMAN = 'German'
        GHANAIAN = 'Ghanaian'
        GREEK = 'Greek'
        GUAM = 'Guam'
        GUATEMALAN = 'Guatemalan'
        GUYANESE = 'Guyanese'
        HAITIAN = 'Haitian'
        HAWAIIAN = 'Hawaiian'
        HONDURAN = 'Honduran'
        HUNGARIAN = 'Hungarian'
        ICELANDIC = 'Icelandic'
        INDIAN = 'Indian'
        INDONESIAN = 'Indonesian'
        IRAQI = 'Iraqi'
        IRISH = 'Irish'
        ISRAELI = 'Israeli'
        ITALIAN = 'Italian'
        JAMAICAN = 'Jamaican'
        JAPANESE = 'Japanese'
        JEWISH = 'Jewish'
        JORDANIAN = 'Jordanian'
        KAZAKH = 'Kazakh'
        KENYAN = 'Kenyan'
        KOREAN = 'Korean'
        LAOTIAN = 'Laotian'
        LEBANESE = 'Lebanese'
        LIBERIAN = 'Liberian'
        LIBYAN = 'Libyan'
        LUXEMBOURGIAN = 'Luxembourgian'
        MACEDONIAN = 'Macedonian'
        MALAGASY = 'Malagasy'
        MALAYSIAN = 'Malaysian'
        MALIAN = 'Malian'
        MALTESE = 'Maltese'
        MEXICAN = 'Mexican'
        MONGOLIAN = 'Mongolian'
        MOROCCAN = 'Moroccan'
        NATIVE_AMERICAN = 'Native_American'
        NEPALI = 'Nepali'
        NEW_ZEALANDER = 'New_Zealander'
        NICARAGUAN = 'Nicaraguan'
        NIGERIAN = 'Nigerian'
        NORWEGIAN = 'Norwegian'
        PAKISTANI = 'Pakistani'
        PALESTINIAN = 'Palestinian'
        PANAMANIAN = 'Panamanian'
        PARAGUAYAN = 'Paraguayan'
        PERSIAN = 'Persian'
        PERUVIAN = 'Peruvian'
        POLISH = 'Polish'
        PORTUGUESE = 'Portuguese'
        PUERTO_RICAN = 'Puerto_Rican'
        ROMANIAN = 'Romanian'
        RUSSIAN = 'Russian'
        SALVADORAN = 'Salvadoran'
        SAUDI = 'Saudi'
        SCOTTISH = 'Scottish'
        SENEGALESE = 'Senegalese'
        SIERRA_LEONEAN = 'Sierra_Leonean'
        SINGAPOREAN = 'Singaporean'
        SLOVAKIAN = 'Slovakian'
        SLOVENIAN = 'Slovenian'
        SOUTH_AFRICAN = 'South_African'
        SOUTHERN_AMERICAN = 'Southern_American'
        SPANISH = 'Spanish'
        SRI_LANKAN = 'Sri_Lankan'
        SUDANESE = 'Sudanese'
        SURINAMESE = 'Surinamese'
        SWEDISH = 'Swedish'
        SWISS = 'Swiss'
        SYRIAN = 'Syrian'
        TANZANIAN = 'Tanzanian'
        TATAR = 'Tatar'
        TEXMEX = 'TexMex'
        THAI = 'Thai'
        TIBETAN = 'Tibetan'
        TUNISIAN = 'Tunisian'
        TURKISH = 'Turkish'
        TURKMEN = 'Turkmen'
        UKRAINIAN = 'Ukrainian'
        URUGUAYAN = 'Uruguayan'
        UZBEK = 'Uzbek'
        VENEZUELAN = 'Venezuelan'
        VIETNAMESE = 'Vietnamese'
        WELSH = 'Welsh'
        ZIMBABWEAN = 'Zimbabwean'
    
    cuisine = CharField(max_length=100, choices=Cuisine.choices)

    class PriceRange(models.TextChoices):
        VERY_LOW = '$'          # $0-$10
        LOW = '$$'              # $10-$20
        MID = '$$$'             # $20-$40
        HIGH = '$$$$'           # $40-$80
        VERY_HIGH = '$$$$$'     # $80+

    price_range = CharField(max_length=5, choices=PriceRange.choices)

    def __str__(self):
        return f'{self.name}'

    def update_mean_rating(self):
        return ((len(self.reviews.all()) - 1) * self.mean_rating + self.reviews.all()[len(self.reviews.all())-1].rating) / (len(self.reviews.all()))

    def serialize(self):
        return {
            "name": self.name,
            "location": self.location,
            "business_hours": self.business_hours,
            "phone": self.phone,
            "email": self.email,
            "website": self.website,
            "mean_rating": self.mean_rating,
            "image": self.image,
            "setting": self.setting,
            "cuisine": self.cuisine,
            "price_range": self.price_range
        }


class Review(models.Model):
    user = ForeignKey('User', on_delete=models.CASCADE, related_name='reviews')
    restaurant = ForeignKey('Restaurant', on_delete=models.CASCADE, related_name='reviews')
    rating = FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])
    comment = TextField()
    visited = BooleanField()
    visited_timestamp = models.DateField()
    timestamp = models.DateTimeField(auto_now_add=True)


class DineList(models.Model):
    name = CharField(max_length=100)
    user = ForeignKey('User', on_delete=models.CASCADE, related_name='dinelists')
    restaurants = ManyToManyField('Restaurant', blank=True, related_name='dinelists')
    followers = ManyToManyField('User', blank=True, related_name='follow_dinelists')

    def serialize(self):
        return {
            "name": self.name,
            "user": self.user,
            "restaurants": self.restaurants,
            "followers": self.followers
        }

    def __str__(self):
        return f'{self.name}'
