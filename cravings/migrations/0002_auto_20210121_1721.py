# Generated by Django 3.1.1 on 2021-01-21 23:21

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cravings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.CharField(blank=True, max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('location', models.TextField(blank=True, max_length=300)),
                ('business_hours', models.TextField(blank=True, max_length=300)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('email', models.CharField(blank=True, max_length=100)),
                ('website', models.CharField(blank=True, max_length=100)),
                ('mean_rating', models.FloatField(blank=True, null=True)),
                ('image', models.CharField(blank=True, max_length=1000, null=True)),
                ('category', models.CharField(choices=[('Fast Food', 'Fast Food'), ('Fast Casual', 'Fast Casual'), ('Sports Bar', 'Sports Bar'), ('Casual Dining', 'Casual Dining'), ('Fine Dining', 'Fine Dining'), ('Pop-Up', 'Pop Up'), ('Food Truck', 'Food Truck')], max_length=100)),
                ('cuisine', models.CharField(choices=[('Afghan', 'Afghan'), ('African_American', 'African American'), ('Albanian', 'Albanian'), ('Algerian', 'Algerian'), ('Amish_Mennonite', 'Amish Mennonite'), ('Angolan', 'Angolan'), ('Argentine', 'Argentine'), ('Armenian', 'Armenian'), ('Aruban', 'Aruban'), ('Australian', 'Australian'), ('Austrian', 'Austrian'), ('Azerbaijani', 'Azerbaijani'), ('Bahamian', 'Bahamian'), ('Barbadian', 'Barbadian'), ('Basque', 'Basque'), ('Belgian', 'Belgian'), ('Belizean', 'Belizean'), ('Belorussian', 'Belorussian'), ('Bolivian', 'Bolivian'), ('Bosnian', 'Bosnian'), ('Brazilian', 'Brazilian'), ('Bulgarian', 'Bulgarian'), ('Burmese', 'Burmese'), ('Cajun', 'Cajun'), ('Cambodian', 'Cambodian'), ('Cameroon', 'Cameroon'), ('Canadian', 'Canadian'), ('Cape_Verdean', 'Cape Verdean'), ('Chilean', 'Chilean'), ('Chinese', 'Chinese'), ('Colombian', 'Colombian'), ('Congolese', 'Congolese'), ('Cornish', 'Cornish'), ('Costa_Rican', 'Costa Rican'), ('Côte_dIvoire', 'Côte Divoire'), ('Creole', 'Creole'), ('Croatian', 'Croatian'), ('Cuban', 'Cuban'), ('Czech', 'Czech'), ('Danish', 'Danish'), ('Dominican', 'Dominican'), ('Dutch', 'Dutch'), ('Ecuadorian', 'Ecuadorian'), ('Egyptian', 'Egyptian'), ('English', 'English'), ('Ethiopian', 'Ethiopian'), ('Filipino', 'Filipino'), ('Finnish', 'Finnish'), ('French', 'French'), ('Gambian', 'Gambian'), ('Georgian', 'Georgian'), ('German', 'German'), ('Ghanaian', 'Ghanaian'), ('Greek', 'Greek'), ('Guam', 'Guam'), ('Guatemalan', 'Guatemalan'), ('Guyanese', 'Guyanese'), ('Haitian', 'Haitian'), ('Hawaiian', 'Hawaiian'), ('Honduran', 'Honduran'), ('Hungarian', 'Hungarian'), ('Icelandic', 'Icelandic'), ('Indian', 'Indian'), ('Indonesian', 'Indonesian'), ('Iraqi', 'Iraqi'), ('Irish', 'Irish'), ('Israeli', 'Israeli'), ('Italian', 'Italian'), ('Jamaican', 'Jamaican'), ('Japanese', 'Japanese'), ('Jewish', 'Jewish'), ('Jordanian', 'Jordanian'), ('Kazakh', 'Kazakh'), ('Kenyan', 'Kenyan'), ('Korean', 'Korean'), ('Laotian', 'Laotian'), ('Lebanese', 'Lebanese'), ('Liberian', 'Liberian'), ('Libyan', 'Libyan'), ('Luxembourgian', 'Luxembourgian'), ('Macedonian', 'Macedonian'), ('Malagasy', 'Malagasy'), ('Malaysian', 'Malaysian'), ('Malian', 'Malian'), ('Maltese', 'Maltese'), ('Mexican', 'Mexican'), ('Mongolian', 'Mongolian'), ('Moroccan', 'Moroccan'), ('Native_American', 'Native American'), ('Nepali', 'Nepali'), ('New_Zealander', 'New Zealander'), ('Nicaraguan', 'Nicaraguan'), ('Nigerian', 'Nigerian'), ('Norwegian', 'Norwegian'), ('Pakistani', 'Pakistani'), ('Palestinian', 'Palestinian'), ('Panamanian', 'Panamanian'), ('Paraguayan', 'Paraguayan'), ('Persian', 'Persian'), ('Peruvian', 'Peruvian'), ('Polish', 'Polish'), ('Portuguese', 'Portuguese'), ('Puerto_Rican', 'Puerto Rican'), ('Romanian', 'Romanian'), ('Russian', 'Russian'), ('Salvadoran', 'Salvadoran'), ('Saudi', 'Saudi'), ('Scottish', 'Scottish'), ('Senegalese', 'Senegalese'), ('Sierra_Leonean', 'Sierra Leonean'), ('Singaporean', 'Singaporean'), ('Slovakian', 'Slovakian'), ('Slovenian', 'Slovenian'), ('South_African', 'South African'), ('Southern_American', 'Southern American'), ('Spanish', 'Spanish'), ('Sri_Lankan', 'Sri Lankan'), ('Sudanese', 'Sudanese'), ('Surinamese', 'Surinamese'), ('Swedish', 'Swedish'), ('Swiss', 'Swiss'), ('Syrian', 'Syrian'), ('Tanzanian', 'Tanzanian'), ('Tatar', 'Tatar'), ('Thai', 'Thai'), ('Tibetan', 'Tibetan'), ('Tunisian', 'Tunisian'), ('Turkish', 'Turkish'), ('Turkmen', 'Turkmen'), ('Ukrainian', 'Ukrainian'), ('Uruguayan', 'Uruguayan'), ('Uzbek', 'Uzbek'), ('Venezuelan', 'Venezuelan'), ('Vietnamese', 'Vietnamese'), ('Welsh', 'Welsh'), ('Zimbabwean', 'Zimbabwean')], max_length=100)),
                ('price_range', models.CharField(choices=[('$', 'Very Low'), ('$$', 'Low'), ('$$$', 'Mid'), ('$$$$', 'High'), ('$$$$$', 'Very High')], max_length=5)),
                ('images', models.ManyToManyField(blank=True, to='cravings.Pic')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='follows',
            field=models.ManyToManyField(blank=True, related_name='followers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(10.0)])),
                ('comment', models.TextField()),
                ('visited', models.BooleanField()),
                ('visited_timestamp', models.DateField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='cravings.restaurant')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DineList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('followers', models.ManyToManyField(blank=True, related_name='follow_dinelists', to=settings.AUTH_USER_MODEL)),
                ('restaurants', models.ManyToManyField(blank=True, related_name='dinelists', to='cravings.Restaurant')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dinelists', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='cravings',
            field=models.ManyToManyField(blank=True, related_name='craved_by', to='cravings.Restaurant'),
        ),
        migrations.AddField(
            model_name='user',
            name='history',
            field=models.ManyToManyField(blank=True, related_name='customers', to='cravings.Restaurant'),
        ),
        migrations.AddField(
            model_name='user',
            name='recommendations',
            field=models.ManyToManyField(blank=True, related_name='recommended_for', to='cravings.Restaurant'),
        ),
    ]
