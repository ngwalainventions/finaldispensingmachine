from django.db import models, transaction
import secrets
import string
import datetime
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, FileExtensionValidator
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import F

TITLE = [
    ('', 'Select title'),
    ('mr', 'Mr.'),
    ('mrs', 'Mrs.'),
    ('Miss', 'Miss.'),
    ('dr', 'Dr.'),
    ('eng', 'Eng.'),
    ('scientist', 'Scientist'),
    ('researcher', 'Researcher'),
]


GENDERS = [
    ('', 'Select Gender'),
    ('MALE', 'Male'),
    ('FEMALE', 'Female')
]


RECEIPT = [
    ('general appliance', 'GENERAL APPLIANCE'),
    ('it applications','IT APPLICATIONS'),
    ('electronics applications', 'ELECTRONICS APPLICATIONS'),
    ('others', 'OTHERS')
    ]


CONDITION = [
        ('new', 'NEW'),
        ('good','GOOD'),
        ('fair', 'FAIR'),
        ('poor', 'POOR')
    ]


STATUS = [
    ('on', 'ON'),
    ('off', 'OFF')
]


CROP_TYPES = [
    ('Mahindi', 'Mahindi'),
    ('Maharage', 'Maharage'),
    ('Alizeti', 'Alizeti'),
    ('Mbaazi', 'Mbaazi'),
    ('Mpunga', 'Mpunga'),
    ('Ngano', 'Ngano'),
    ('Uwele', 'Uwele'),
    ('Korosho', 'Korosho'),
    ('Mihogo', 'Mihogo'),
]


def generate_ref_number():
    return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for i in range(12))


def generate_machine_location_identifier():
    return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for i in range(12))


class Farmer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='farmer')
    title = models.CharField(verbose_name='title', max_length=10, choices=TITLE, default='Mr.')
    first_name = models.CharField(verbose_name=_('first name'), max_length=256, null=True)
    last_name = models.CharField(verbose_name=_('last name'), max_length=256, null=True)
    gender = models.CharField(verbose_name='gender', max_length=100, choices=GENDERS, null=True)
    d_o_b = models.DateField(verbose_name='date of birth', blank=True, null=True)
    email = models.EmailField(verbose_name=_('Email'), max_length=255, null=True, blank=True, help_text="Example: kamau@gmail.com")
    uid = models.CharField(verbose_name=_('registed cards'), max_length=256, default=None, unique=True, null=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))
    expire_date = models.DateTimeField( null=True,  blank=True,  verbose_name=_('expire date') )
    address = models.CharField(verbose_name='Address', max_length=10, blank=True, null=True, help_text="Example: P.O Box 123")
    phone_no1 = models.CharField(verbose_name='Call:', max_length=16, null=True, help_text="Namba ya simu")
    phone_no2 = models.CharField(verbose_name='Tel:', max_length=16, null=True, blank=True, help_text="Namba ya simu")
    postal_code  = models.IntegerField(verbose_name='Postal code', null=True, blank=True, help_text="Note*: Not neccessary")
    nation = models.CharField(verbose_name='Nation/Nchi', max_length=30, null=True, help_text="Nation/Nchi")
    region = models.CharField(verbose_name='Jiji/Mkoa', max_length=30, null=True, help_text="Mkoa")
    district = models.CharField(verbose_name='Wilaya', max_length=30, null=True, help_text="Wilaya")
    ward = models.CharField(verbose_name='Kata', max_length=30, null=True, help_text="Kata")
    village = models.CharField(verbose_name='Kijiji/Mtaa', max_length=30, null=True, help_text="Kijiji au Mtaa")
    crop_type1 = models.CharField(blank=True, null=True, help_text='Aina ya zao', max_length=100, choices=CROP_TYPES)
    crop_type2 = models.CharField(blank=True, null=True, help_text='Aina ya zao', max_length=100, choices=CROP_TYPES)
    crop_type3 = models.CharField(blank=True, null=True, help_text='Aina ya zao', max_length=100, choices=CROP_TYPES)
    farm_size = models.FloatField(blank=True, null=True, help_text='ukubwa wa shamba', max_length=9)
    other_occ = models.CharField(verbose_name='extra activities', max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True, help_text="Make a little summary here")
    profile_photo = models.ImageField(upload_to='Farmer_profile_photos/',  validators=[FileExtensionValidator(['png','jpg'])]) 
    send_notification = models.BooleanField(default=False, verbose_name='send me notifications')
    send_newslaters = models.BooleanField(default=False, verbose_name='send me newslaters')
    
    def save(self, *args, **kwargs):
        # Ensure phone numbers are stored in E.164 format before saving
        self.phone_no1 = self.format_phone_number(self.phone_no1)
        self.phone_no2 = self.format_phone_number(self.phone_no2)
        super().save(*args, **kwargs)

    @staticmethod
    def format_phone_number(phone_number):
        if phone_number and not phone_number.startswith('+'):
            return '+255' + phone_number[1:] if phone_number.startswith('0') else phone_number
        return phone_number

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Farmer'
        verbose_name_plural = 'Farmers'
    
    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)


class Machine(models.Model):
    name = models.CharField(max_length=50, editable=False, default=generate_machine_location_identifier, verbose_name=('Machine Identifier'))
    machine_model = models.CharField(max_length=30, null=True, verbose_name='model')
    region = models.CharField(max_length=30 ,verbose_name='mkoa', null=False, blank=False)
    district = models.CharField(max_length=30 ,verbose_name='wilaya', null=False, blank=False)
    ward = models.CharField(max_length=30 ,verbose_name='kata', null=False, blank=False)
    village = models.CharField(max_length=30 ,verbose_name='kijiji', null=False, blank=False)
    tank_volume = models.DecimalField(verbose_name='tank volume', max_digits=20, decimal_places = 2, null=True)
    refill_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Refilled at'))
    status = models.CharField(max_length=250,verbose_name='Status', blank=True, null=True)
    tank_cap = models.CharField(verbose_name='default', default='10L', max_length=40, blank=True, null=True)
    inst_date = models.DateTimeField(auto_now_add=True, verbose_name=_('date ocurred'))
    volume_left = models.DecimalField(verbose_name='Volume Left', max_digits=20, decimal_places=2, default=None, blank=True, null=True)    

    # Calculate the amount of litres based on the money entered (Assuming 1 litre = 10000 TZS)
    def withdraw_fertilizer_and_litres(self, money_entered):
        if self.volume_left is not None and self.volume_left > 0:
            litres_drawn = money_entered / 10000
            if self.tank_volume is not None and litres_drawn is not None:
                self.volume_left -= litres_drawn
                # ensure volume_left does not go below zero
                self.volume_left = max(0, self.volume_left)
                self.save()
                return litres_drawn
        return 0  # Return 0 if volume_left is 0

    def add_fertilizer(self, litres):
        if self.tank_volume is not None:
            # Add fertilizer and update volume_left
            litres_added = litres/2
            self.tank_volume += litres_added
            self.volume_left += litres_added
            self.save()
        
    def save(self, *args, **kwargs):
        #ensure that volume_left is initialized with tank_volume when first created
        if self.pk is None:
            self.volume_left = self.tank_volume
        super().save(*args, **kwargs)
        
    @property
    def volume_taken(self):
        if self.tank_volume is not None and self.volume_left is not None:
            return self.tank_volume - self.volume_left
        return None
    
    def __str__(self):
        return self.name


class FertilizerAddition(models.Model):
    machine = models.ForeignKey('Machine', on_delete=models.CASCADE)
    amount_of_fertilizer = models.DecimalField(verbose_name='Fertilizer Amount', max_digits=20, decimal_places=2)
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Date Added')

    def save(self, *args, **kwargs):
        # Update the machine's tank_volume and volume_left when adding fertilizer
        self.machine.add_fertilizer(self.amount_of_fertilizer)
        super().save(*args, **kwargs)


class RegisteredCard(models.Model):
    phone = models.CharField(verbose_name='Namba ya Simu:', max_length=16, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='registered_card')
    card_number = models.CharField(max_length=10, unique=True)
    card_balance = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
        
    def __str__(self):
        return self.card_number


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions', null=True, blank=True)
    ref_number = models.CharField(max_length=50, editable=False, default=generate_ref_number, verbose_name=('Trans reference number'))
    uid = models.CharField(max_length=10, null=True, verbose_name='Card')
    fertilizer_cost = models.DecimalField(default=0.00, max_digits=10, decimal_places=2, verbose_name='fertilizer cost')
    fertilizer_taken = models.DecimalField(default=0.00, max_digits=10, decimal_places=2, null=True)  #fertilizer taken
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    volume_updated = models.DateTimeField(null=True, blank= True, help_text="last time volume was added", verbose_name="Date Volume Update")
    amount_version = models.PositiveIntegerField(default=1, editable = False, null=True, verbose_name='version', help_text="Do not touch this field")
    volume_version = models.PositiveIntegerField(default=0, null=True, help_text="Do not touch this field")
    location = models.CharField(max_length=30, verbose_name="location", blank=True, null=True, editable=False)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='transactions', verbose_name='machine number')
    version = models.PositiveIntegerField(default=0, verbose_name='Version', help_text="Transaction version")
    # New field to store card_balance at the time of the transaction
    card_balance_at_transaction = models.DecimalField(default=0.00, max_digits=10, decimal_places=2, editable=False)
    # transaction_datetime = models.DateTimeField(auto_now_add=True, verbose_name='Transaction Datetime')
    transaction_datetime = models.CharField(max_length=15, null=True, verbose_name='TR time')
    
    def save(self, *args, **kwargs):
        if self.uid:
            with transaction.atomic():  # Use atomic transaction for consistency
                # Retrieve the associated card
                registered_card = RegisteredCard.objects.filter(card_number=self.uid).first()

                if registered_card:
                    # Get the last transaction version for this card
                    last_version_for_card = Transaction.objects.filter(uid=self.uid).order_by('-version').first()

                    if last_version_for_card:
                        self.version = last_version_for_card.version + 1
                    else:
                        self.version = 1  # Start the versioning for this card from 1
                else:
                    raise ValidationError(f"No registered card found with the card number: {self.uid}")
                
                if registered_card:
                    # Set card_balance_at_transaction to the current card_balance
                    self.card_balance_at_transaction = registered_card.card_balance - self.fertilizer_cost

                # Handle None values for self.fertilizer_cost and registered_card.card_balance
                if self.fertilizer_cost is None:
                    self.fertilizer_cost = 0.00  # Set a default value

                if registered_card.card_balance is None:
                    registered_card.card_balance = 0.00  # Set a default value

                if self.fertilizer_cost > registered_card.card_balance:
                    raise ValidationError('The amount entered exceeds, your current account balance.')

                if self.pk is not None:
                    transactions = Transaction.objects.get(pk=self.pk)
                    if self.fertilizer_cost != transactions.fertilizer_cost:
                        self.amount_version += 1
                        self.amount_add = timezone.now()

                    # Update the version field using F() expression
                    Transaction.objects.filter(pk=self.pk).update(version=F('version') + 1)

                registered_card.card_balance -= self.fertilizer_cost
                litres_drawn = self.machine.withdraw_fertilizer_and_litres(self.fertilizer_cost)
                if litres_drawn == 0:
                    self.machine.add_fertilizer(self.fertilizer_cost)
                self.volume_left = self.machine.volume_left

                # Update the card_balance in RegisteredCard
                registered_card.save()

                if self.pk is not None:
                    super(Transaction, self).save(
                        update_fields=['volume_left', 'amount_version', 'amount_add', 'version'], *args, **kwargs
                    )
                else:
                    super(Transaction, self).save(*args, **kwargs)

    def __str__(self):
        return self.ref_number

  
class Subcomponent(models.Model):
    city = models.CharField(verbose_name='Jiji/Mkoa', max_length=15, null=True, help_text="Mkoa")
    name = models.CharField(max_length=20, null=True)
    date = models.DateField()
    price = models.DecimalField(max_digits=9, decimal_places=2, null=True)
    stock = models.IntegerField()
    status = models.CharField(max_length=30, blank=True,  null=True,  verbose_name='status')
    description = models.TextField(max_length=250, blank=True, null=True, verbose_name='Description')
        
    def __str__(self):
        return self.name


class Equipment(models.Model):
    serial = models.CharField(verbose_name=_('Equipment Serial Number'), max_length=50, null=True,  help_text="If the equipment has a serial number, record it in this field.")
    name = models.CharField(max_length=20, null=True, verbose_name='Equipment Name')
    models_no = models.CharField(max_length=20, null=True, verbose_name='Equipment Modal Number')
    category = models.CharField(max_length=30, blank=True, null=True, verbose_name='Classfication', choices=RECEIPT)
    status = models.CharField(max_length=30, blank=True, null=True, verbose_name='equipment status', help_text="This list field provides several values for documenting how an equipment item is currently being used--is it in storage, being repaired, salvaged, or in use?")
    color = models.SlugField(max_length=30, verbose_name='equipment color',  blank=True, null=True)
    use = models.CharField(max_length=256,verbose_name='Use Case',help_text='Use this field to document how the equipment item is used', blank=True, null=True)
    condition = models.CharField(max_length=30, verbose_name='Condition', help_text='Equipment Condition', blank=True, null=True,   choices=CONDITION)
    location = models.CharField(max_length=30, verbose_name="Equipment's location", blank=True, null=True)
    subcomponent  = models.ManyToManyField(Subcomponent)
    date_of_manufact = models.DateField(verbose_name="Date of Manufucture", blank=True, null=True, editable=False, auto_created=False)
    last_surve_update = models.CharField(max_length=200, blank=True, null=True, verbose_name="Last Survey Update")
    insured = models.BooleanField(verbose_name='Insurance?', help_text="Equipment insured?", null=True)
        
    def __str__(self):
        return self.name  


class Receipt(models.Model):
    number = models.CharField(max_length=10, null=True, help_text="Unique receipt number", verbose_name="Receipt Number")
    serial = models.CharField(verbose_name=_('Serial Number'), max_length=50,blank=True, null=True, help_text="If the receipt has a serial number, record it in this field.")
    supplier = models.CharField(max_length=50,   verbose_name="Supplier name", null=True)
    price = models.DecimalField(max_digits=20, decimal_places=2, default= 0.0, verbose_name=_('Cost'), help_text="This field holds the cost of the Item mentioned in Tsh", validators=[MinValueValidator(0.00)], null=True)
    category = models.CharField(max_length=30, verbose_name="Category", choices=RECEIPT, help_text="Fill in the Item category according to application of the Item")
    date = models.DateTimeField(auto_now_add=True, verbose_name=_('date ocurred'))
    item = models.CharField(verbose_name=_('Item name'), max_length=256, null=True)
    picture = models.ImageField(upload_to='receipt_images/',  validators=[FileExtensionValidator(['png','jpg'])])

    def __str__(self):
        return self.number    


class UserRegistration(models.Model):
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)
    # user = models.OneToOneField(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, default='')
    last_name = models.CharField(max_length=30)
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )
    gender = models.CharField(max_length=7, choices=GENDER_CHOICES)
    address = models.CharField(max_length=50)
    nationality = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=12, default='')
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    confirm_password = models.CharField(max_length=128, default='')  # Confirm Password
    profile_picture = models.ImageField(upload_to='user_profile_pictures/', default='default/logo.png', validators=[FileExtensionValidator(['png','jpg'])])

    def __str__(self):
        return self.first_name + " " + self.last_name


class UserMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to="profile_images/", blank=True, null=True)
    
    def __str__(self):
        return self.user.username


class Post(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=300)
    content = models.TextField()
    image = models.ImageField(upload_to="post_images/")
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)
    likes_users = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    
    def increment_likes(self):
        self.likes += 1
        self.save()
        
    def __str__(self):
        return self.title


class ReceivedSMS(models.Model):
    amount_received = models.CharField(max_length=50)
    sender_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    muamala_number = models.CharField(max_length=255)
    received_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"SMS from {self.sender_name}"



class TeamMember(models.Model):
    teammember_name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    bio = models.TextField()
    image = models.ImageField(upload_to='team_images/')

    def __str__(self):
        return self.teammember_name



###########################
###########################
###########################
###########################
###########################


   
class ContactModel(models.Model):
    jina = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    ujumbe = models.CharField(max_length=200)

    def __str__(self):
        return self.jina






# for index as a home page
class Faqs(models.Model):
    question = models.CharField(max_length=500)
    answer = models.CharField(max_length=1000)
    
    def __self__(self):
        return self.question
    
class News(models.Model):
    header = models.CharField(max_length=50)
    body = models.CharField(max_length=500)
    image = models.ImageField(upload_to ='media/',blank=True,null=True)
    
    def __self__(self):
        return self.header

class Portfolio(models.Model):
    image1 = models.ImageField(upload_to ='media/',blank=True,null=True)
    image2 = models.ImageField(upload_to ='media/',blank=True,null=True)
    image3 = models.ImageField(upload_to ='media/',blank=True,null=True)
    image4 = models.ImageField(upload_to ='media/',blank=True,null=True)
    image5 = models.ImageField(upload_to ='media/',blank=True,null=True)
    image6 = models.ImageField(upload_to ='media/',blank=True,null=True)
    
class IntroVideo(models.Model):
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='videos/')
    def __str__(self):
        return self.title

class Review(models.Model):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    image = models.ImageField(upload_to ='media/',blank=True,null=True)
    body = models.CharField(max_length=500)
    time_posted = models.CharField(max_length=50)
    views = models.CharField(max_length=5,blank=True,null=True)
    likes = models.CharField(max_length=5,blank=True,null=True)
    comments = models.CharField(max_length=5,blank=True,null=True)
    share = models.CharField(max_length=5,blank=True,null=True)
    link = models.CharField(max_length=500,blank=True,null=True)
    
    def __self__(self):
        return self.name
    
class Service(models.Model):
    header = models.CharField(max_length=50)
    body = models.CharField(max_length=500)
    
    def __self__(self):
        return self.header
    
class FrontPage(models.Model):
    header = models.CharField(max_length=50)
    body = models.CharField(max_length=500)
    image = models.ImageField(upload_to ='media/',blank=True,null=True)
    
    def __self__(self):
        return self.header
    
class WhyUseAgki(models.Model):
    header = models.CharField(max_length=50)
    body = models.CharField(max_length=500)
    image = models.ImageField(upload_to ='media/',blank=True,null=True)
    
    def __self__(self):
        return self.header



    
# purpose section
class PurposeTop(models.Model):
    video_file = models.FileField(upload_to='media/',null=True, blank=True)
    header = models.CharField(max_length=500)
    subheader = models.CharField(max_length=500)
    description = models.TextField(max_length=5000)
    descriptionSecond = models.TextField(max_length=5000)
    problem = models.TextField(max_length=5000)
    solution = models.TextField(max_length=5000)

class Purpose(models.Model):
    description = models.TextField(max_length=5000)

class Success(models.Model):
    description = models.TextField(max_length=5000)

class FooterContact(models.Model):
    phonenumber = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    address = models.CharField(max_length=200)

class FeaturedPage(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to ='media/',blank=True,null=True)

class FooterLink(models.Model):
    logo = models.ImageField(upload_to ='media/',blank=True,null=True)
    title = models.CharField(max_length=1000)
    instagramLink = models.CharField(max_length=1000)
    facebookLink = models.CharField(max_length=1000)
    linkedinLink = models.CharField(max_length=1000)
    twitterLink = models.CharField(max_length=1000)

class Team(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    image = models.ImageField(upload_to ='media/',blank=True,null=True)
   
class TopLogo(models.Model):
    logo = models.ImageField(upload_to ='media/',blank=True,null=True)

class WhyUseBg(models.Model):
    image = models.ImageField(upload_to ='media/',blank=True,null=True)


class ContactUsModel(models.Model):
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    subject = models.CharField(max_length=200)
    message = models.CharField(max_length=1000)
    time_posted = models.DateTimeField(auto_now_add=True)


#########################
##########################
############################
###########################