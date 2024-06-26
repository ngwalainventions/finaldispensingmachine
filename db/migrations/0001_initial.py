# Generated by Django 5.0.2 on 2024-03-07 09:41

import db.models
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=db.models.generate_machine_location_identifier, editable=False, max_length=50, verbose_name='Machine Identifier')),
                ('machine_model', models.CharField(max_length=30, null=True, verbose_name='model')),
                ('region', models.CharField(max_length=30, verbose_name='mkoa')),
                ('district', models.CharField(max_length=30, verbose_name='wilaya')),
                ('ward', models.CharField(max_length=30, verbose_name='kata')),
                ('village', models.CharField(max_length=30, verbose_name='kijiji')),
                ('tank_volume', models.DecimalField(decimal_places=2, max_digits=20, null=True, verbose_name='tank volume')),
                ('refill_date', models.DateTimeField(auto_now_add=True, verbose_name='Refilled at')),
                ('status', models.CharField(blank=True, max_length=250, null=True, verbose_name='Status')),
                ('tank_cap', models.CharField(blank=True, default='10L', max_length=40, null=True, verbose_name='default')),
                ('inst_date', models.DateTimeField(auto_now_add=True, verbose_name='date ocurred')),
                ('volume_left', models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=20, null=True, verbose_name='Volume Left')),
            ],
        ),
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(help_text='Unique receipt number', max_length=10, null=True, verbose_name='Receipt Number')),
                ('serial', models.CharField(blank=True, help_text='If the receipt has a serial number, record it in this field.', max_length=50, null=True, verbose_name='Serial Number')),
                ('supplier', models.CharField(max_length=50, null=True, verbose_name='Supplier name')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, help_text='This field holds the cost of the Item mentioned in Tsh', max_digits=20, null=True, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='Cost')),
                ('category', models.CharField(choices=[('general appliance', 'GENERAL APPLIANCE'), ('it applications', 'IT APPLICATIONS'), ('electronics applications', 'ELECTRONICS APPLICATIONS'), ('others', 'OTHERS')], help_text='Fill in the Item category according to application of the Item', max_length=30, verbose_name='Category')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='date ocurred')),
                ('item', models.CharField(max_length=256, null=True, verbose_name='Item name')),
                ('picture', models.ImageField(upload_to='receipt_images/', validators=[django.core.validators.FileExtensionValidator(['png', 'jpg'])])),
            ],
        ),
        migrations.CreateModel(
            name='ReceivedSMS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_received', models.CharField(max_length=50)),
                ('sender_name', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=15)),
                ('muamala_number', models.CharField(max_length=255)),
                ('received_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subcomponent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(help_text='Mkoa', max_length=15, null=True, verbose_name='Jiji/Mkoa')),
                ('name', models.CharField(max_length=20, null=True)),
                ('date', models.DateField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=9, null=True)),
                ('stock', models.IntegerField()),
                ('status', models.CharField(blank=True, max_length=30, null=True, verbose_name='status')),
                ('description', models.TextField(blank=True, max_length=250, null=True, verbose_name='Description')),
            ],
        ),
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teammember_name', models.CharField(max_length=255)),
                ('position', models.CharField(max_length=255)),
                ('bio', models.TextField()),
                ('image', models.ImageField(upload_to='team_images/')),
            ],
        ),
        migrations.CreateModel(
            name='UserMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Farmer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(choices=[('', 'Select title'), ('mr', 'Mr.'), ('mrs', 'Mrs.'), ('Miss', 'Miss.'), ('dr', 'Dr.'), ('eng', 'Eng.'), ('scientist', 'Scientist'), ('researcher', 'Researcher')], default='Mr.', max_length=10, verbose_name='title')),
                ('first_name', models.CharField(max_length=256, null=True, verbose_name='first name')),
                ('last_name', models.CharField(max_length=256, null=True, verbose_name='last name')),
                ('gender', models.CharField(choices=[('', 'Select Gender'), ('MALE', 'Male'), ('FEMALE', 'Female')], max_length=100, null=True, verbose_name='gender')),
                ('d_o_b', models.DateField(blank=True, null=True, verbose_name='date of birth')),
                ('email', models.EmailField(blank=True, help_text='Example: kamau@gmail.com', max_length=255, null=True, verbose_name='Email')),
                ('uid', models.CharField(default=None, max_length=256, null=True, unique=True, verbose_name='registed cards')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('expire_date', models.DateTimeField(blank=True, null=True, verbose_name='expire date')),
                ('address', models.CharField(blank=True, help_text='Example: P.O Box 123', max_length=10, null=True, verbose_name='Address')),
                ('phone_no1', models.CharField(help_text='Namba ya simu', max_length=16, null=True, verbose_name='Call:')),
                ('phone_no2', models.CharField(blank=True, help_text='Namba ya simu', max_length=16, null=True, verbose_name='Tel:')),
                ('postal_code', models.IntegerField(blank=True, help_text='Note*: Not neccessary', null=True, verbose_name='Postal code')),
                ('nation', models.CharField(help_text='Nation/Nchi', max_length=30, null=True, verbose_name='Nation/Nchi')),
                ('region', models.CharField(help_text='Mkoa', max_length=30, null=True, verbose_name='Jiji/Mkoa')),
                ('district', models.CharField(help_text='Wilaya', max_length=30, null=True, verbose_name='Wilaya')),
                ('ward', models.CharField(help_text='Kata', max_length=30, null=True, verbose_name='Kata')),
                ('village', models.CharField(help_text='Kijiji au Mtaa', max_length=30, null=True, verbose_name='Kijiji/Mtaa')),
                ('crop_type1', models.CharField(blank=True, choices=[('Mahindi', 'Mahindi'), ('Maharage', 'Maharage'), ('Alizeti', 'Alizeti'), ('Mbaazi', 'Mbaazi'), ('Mpunga', 'Mpunga'), ('Ngano', 'Ngano'), ('Uwele', 'Uwele'), ('Korosho', 'Korosho'), ('Mihogo', 'Mihogo')], help_text='Aina ya zao', max_length=100, null=True)),
                ('crop_type2', models.CharField(blank=True, choices=[('Mahindi', 'Mahindi'), ('Maharage', 'Maharage'), ('Alizeti', 'Alizeti'), ('Mbaazi', 'Mbaazi'), ('Mpunga', 'Mpunga'), ('Ngano', 'Ngano'), ('Uwele', 'Uwele'), ('Korosho', 'Korosho'), ('Mihogo', 'Mihogo')], help_text='Aina ya zao', max_length=100, null=True)),
                ('crop_type3', models.CharField(blank=True, choices=[('Mahindi', 'Mahindi'), ('Maharage', 'Maharage'), ('Alizeti', 'Alizeti'), ('Mbaazi', 'Mbaazi'), ('Mpunga', 'Mpunga'), ('Ngano', 'Ngano'), ('Uwele', 'Uwele'), ('Korosho', 'Korosho'), ('Mihogo', 'Mihogo')], help_text='Aina ya zao', max_length=100, null=True)),
                ('farm_size', models.FloatField(blank=True, help_text='ukubwa wa shamba', max_length=9, null=True)),
                ('other_occ', models.CharField(blank=True, max_length=100, null=True, verbose_name='extra activities')),
                ('notes', models.TextField(blank=True, help_text='Make a little summary here', null=True)),
                ('profile_photo', models.ImageField(upload_to='Farmer_profile_photos/', validators=[django.core.validators.FileExtensionValidator(['png', 'jpg'])])),
                ('send_notification', models.BooleanField(default=False, verbose_name='send me notifications')),
                ('send_newslaters', models.BooleanField(default=False, verbose_name='send me newslaters')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='farmer', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Farmer',
                'verbose_name_plural': 'Farmers',
                'db_table': '',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='FertilizerAddition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_of_fertilizer', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Fertilizer Amount')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='Date Added')),
                ('machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.machine')),
            ],
        ),
        migrations.CreateModel(
            name='RegisteredCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=16, null=True, verbose_name='Namba ya Simu:')),
                ('card_number', models.CharField(max_length=10, unique=True)),
                ('card_balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registered_card', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial', models.CharField(help_text='If the equipment has a serial number, record it in this field.', max_length=50, null=True, verbose_name='Equipment Serial Number')),
                ('name', models.CharField(max_length=20, null=True, verbose_name='Equipment Name')),
                ('models_no', models.CharField(max_length=20, null=True, verbose_name='Equipment Modal Number')),
                ('category', models.CharField(blank=True, choices=[('general appliance', 'GENERAL APPLIANCE'), ('it applications', 'IT APPLICATIONS'), ('electronics applications', 'ELECTRONICS APPLICATIONS'), ('others', 'OTHERS')], max_length=30, null=True, verbose_name='Classfication')),
                ('status', models.CharField(blank=True, help_text='This list field provides several values for documenting how an equipment item is currently being used--is it in storage, being repaired, salvaged, or in use?', max_length=30, null=True, verbose_name='equipment status')),
                ('color', models.SlugField(blank=True, max_length=30, null=True, verbose_name='equipment color')),
                ('use', models.CharField(blank=True, help_text='Use this field to document how the equipment item is used', max_length=256, null=True, verbose_name='Use Case')),
                ('condition', models.CharField(blank=True, choices=[('new', 'NEW'), ('good', 'GOOD'), ('fair', 'FAIR'), ('poor', 'POOR')], help_text='Equipment Condition', max_length=30, null=True, verbose_name='Condition')),
                ('location', models.CharField(blank=True, max_length=30, null=True, verbose_name="Equipment's location")),
                ('date_of_manufact', models.DateField(blank=True, editable=False, null=True, verbose_name='Date of Manufucture')),
                ('last_surve_update', models.CharField(blank=True, max_length=200, null=True, verbose_name='Last Survey Update')),
                ('insured', models.BooleanField(help_text='Equipment insured?', null=True, verbose_name='Insurance?')),
                ('subcomponent', models.ManyToManyField(to='db.subcomponent')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref_number', models.CharField(default=db.models.generate_ref_number, editable=False, max_length=50, verbose_name='Trans reference number')),
                ('uid', models.CharField(max_length=10, null=True, verbose_name='Card')),
                ('fertilizer_cost', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='fertilizer cost')),
                ('fertilizer_taken', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('volume_updated', models.DateTimeField(blank=True, help_text='last time volume was added', null=True, verbose_name='Date Volume Update')),
                ('amount_version', models.PositiveIntegerField(default=1, editable=False, help_text='Do not touch this field', null=True, verbose_name='version')),
                ('volume_version', models.PositiveIntegerField(default=0, help_text='Do not touch this field', null=True)),
                ('location', models.CharField(blank=True, editable=False, max_length=30, null=True, verbose_name='location')),
                ('version', models.PositiveIntegerField(default=0, help_text='Transaction version', verbose_name='Version')),
                ('card_balance_at_transaction', models.DecimalField(decimal_places=2, default=0.0, editable=False, max_digits=10)),
                ('transaction_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Transaction Datetime')),
                ('machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='db.machine', verbose_name='machine number')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='profile_images/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('content', models.TextField()),
                ('image', models.ImageField(upload_to='post_images/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('likes', models.PositiveIntegerField(default=0)),
                ('likes_users', models.ManyToManyField(blank=True, related_name='liked_posts', to=settings.AUTH_USER_MODEL)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='db.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='UserRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('middle_name', models.CharField(default='', max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=7)),
                ('address', models.CharField(max_length=50)),
                ('nationality', models.CharField(max_length=50)),
                ('date_of_birth', models.DateField()),
                ('phone_number', models.CharField(default='', max_length=12)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('confirm_password', models.CharField(default='', max_length=128)),
                ('profile_picture', models.ImageField(default='default/logo.png', upload_to='user_profile_pictures/', validators=[django.core.validators.FileExtensionValidator(['png', 'jpg'])])),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
