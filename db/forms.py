from django import forms
from . models import Farmer, Equipment, Subcomponent, Receipt, Transaction, Machine,UserMessage, Post
from .models import RegisteredCard, FertilizerAddition, UserProfile #, RechargeCard
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

class FarmerForm(forms.ModelForm):
    class Meta:
        model = Farmer
        fields = ['title', 'first_name', 'last_name', 'gender', 'd_o_b', 'email', 'address', 'phone_no1', 'farm_size', 'crop_type1', 'crop_type2', 'crop_type3', 'nation', 'region', 'district', 'ward', 'village']
        labels = {
            # 'user': 'User',
            'title': 'Title',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'gender': 'Gender',
            'd_o_b': 'Date of Birth',
            'email': 'Email',
            'address': 'Address',
            'phone_no1': 'Phone Number',
            'farm_size': 'Farm Size (Hekari)',
            'crop_type1': 'Crop Type 1',
            'crop_type2': 'Crop Type 2 (Option)',
            'crop_type3': 'Crop Type 3 (Option)',
            'nation': 'Nation/ Nchi',
            'region': 'Region/Mkoa',
            'district': 'District/Wilaya',
            'ward': 'Ward/ Kata',
            'village': 'Village or Street/Mtaa au kijiji',
        }
        # Add this field definition to override the default crop_types field
        

        # django representation of HTML is Widget
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.Select(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'd_o_b': forms.DateInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_no1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'eg. 0757900133'}),
            'farm_size': forms.NumberInput(attrs={'class': 'form-control'}),
            'crop_type1': forms.Select(attrs={'class': 'form-control'}),
            'crop_type2': forms.Select(attrs={'class': 'form-control'}),
            'crop_type3': forms.Select(attrs={'class': 'form-control'}),
            'nation': forms.TextInput(attrs={'class': 'form-control'}),
            'region': forms.TextInput(attrs={'class': 'form-control'}),
            'district': forms.TextInput(attrs={'class': 'form-control'}),
            'ward': forms.TextInput(attrs={'class': 'form-control'}),
            'village': forms.TextInput(attrs={'class': 'form-control'})
        }

class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['serial', 'name', 'models_no', 'category', 'color','condition', 'location']
        labels = {
            'serial': 'Serial Number',
            'name': 'Equipment Name',
            'models_no': 'Equipment Model Number',
            'category': 'Category',
            'color': 'Equipment Color',
            'condition': 'Equipment condition',
            'location': 'Equipment Location',
        }
        widgets = {
            'serial': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'models_no': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'condition': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            # 'location': forms.Select(attrs={'class': 'select2'}),
        }
        
class SubcomponentForm(forms.ModelForm):
    class Meta:
        model = Subcomponent
        fields = ['name', 'price', 'stock', 'status', 'date', 'description']
        labels = {
            'name': 'Component Name',
            'price': 'Price',
            'stock': 'Stock',
            'status': 'Status',
            'date': 'Date',
            'description': 'Description',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class ReceiptForm(forms.ModelForm):
    class Meta:
        model = Receipt
        exclude = ['date']  # Exclude the 'date' field from the form. It adds the data automatic
        labels = {
            'number': 'Receipt Number',
            'serial': 'Serial Number',
            'supplier': 'Supplier Name',
            'price': 'Cost',
            'category': 'Category',
            'item': 'Item Name',
            'picture': 'Receipt Picture',
        }
        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'serial': forms.TextInput(attrs={'class': 'form-control'}),
            'supplier': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'item': forms.TextInput(attrs={'class': 'form-control'}),
            'picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class RegisteredCardForm(forms.ModelForm):
    class Meta:
        model = RegisteredCard
        fields = ['user', 'card_number', 'phone', 'card_balance']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control col-md-12'}),
            'card_number': forms.NumberInput(attrs={'class': 'form-control col-md-12'}),
            'phone': forms.TextInput(attrs={'class': 'form-control col-md-12'}),
            'card_balance': forms.NumberInput(attrs={'class': 'form-control col-md-12'}),
        }
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(RegisteredCardForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['user'].initial = user

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        # fields = ['ref_number','uid','amount','balance','volume','created_date','amount_add','volume_update','amount_version','volume_version','location',]
        exclude = ['ref_number']
        labels = {
            'uid': 'Card',
            'fertilizer_cost': 'Money Amount to withdraw fertilizer',
            'fertilizer_taken': 'Fertilizer taken',
            'created_date': 'Created Date',
            'amount_add': 'Date Amount Added',
            'volume_updated': 'Date Volume Update',
            'amount_version': 'Amount Version',
            'volume_version': 'Volume Version',
            'location': 'Location',
            'machine': 'Machine',
            'version': 'Version',
        }

        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'uid': forms.TextInput(attrs={'class': 'form-control'}),
            'fertilizer_cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'fertilizer_taken': forms.NumberInput(attrs={'class': 'form-control'}),
            'created_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'volume_updated': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'volume_version': forms.NumberInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'machine': forms.Select(attrs={'class': 'form-control'}),
            'version': forms.TextInput(attrs={'class': 'form-control'}),
        }

class FertilizerAdditionForm(forms.ModelForm):
    class Meta:
        model = FertilizerAddition
        fields = ['machine', 'amount_of_fertilizer']
        
        widgets = {
            'machine': forms.Select(attrs={'class': 'form-control col-md-4'}),
            'amount_of_fertilizer': forms.NumberInput(attrs={'class': 'form-control col-md-4'}),
        }

class MachineRegistrationForm(forms.ModelForm):
    class Meta:
        model = Machine
        fields = ['machine_model','region','district','ward','village', 'tank_volume', 'status', 'tank_cap']
        exclude = ['name']
        # fields = ['name', 'machine_model', 'location', 'tank_volume', 'status', 'tank_cap']

        # Adding labels and widgets for each form field
        labels = {
            # 'name': 'Machine Name',
            'machine_model': 'Machine Model',
            # 'location': 'Machine Location',
            'region': 'Mkoa',
            'district': 'Wilaya',
            'ward': 'Kata',
            'village': 'Mtaa au Kijiji',
            'tank_volume': 'Tank Volume',
            'status': 'Machine Status',
            'tank_cap': 'Volume Left',
        }
        widgets = {
            # 'name': forms.TextInput(attrs={'class': 'form-control'}),
            'machine_model': forms.TextInput(attrs={'class': 'form-control col-md-4'}),
            # 'location': forms.Select(attrs={'class': 'form-control col-md-4'}),
            'region': forms.TextInput(attrs={'class': 'form-control col-md-4'}),
            'district': forms.TextInput(attrs={'class': 'form-control col-md-4'}),
            'ward': forms.TextInput(attrs={'class': 'form-control col-md-4'}),
            'village': forms.TextInput(attrs={'class': 'form-control col-md-4'}),
            'tank_volume': forms.NumberInput(attrs={'class': 'form-control col-md-4'}),
            'status': forms.Textarea(attrs={'class': 'form-control col-md-4', 'rows': 1}),
            'tank_cap': forms.TextInput(attrs={'class': 'form-control col-md-4'}),
        }

class UserMessageForm(forms.ModelForm):
    class Meta:
        model = UserMessage
        fields = ['name', 'email', 'message']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image','author']
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
        }
      
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_image']  # Include other fields as needed


################################
################################
################################
################################
################################
################################
################################
################################
from .models import *


class FaqsForm(forms.ModelForm):
    class Meta:
        model = Faqs
        fields = ['question','answer']

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['header','body','image']

class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['image1','image2','image3','image4','image5','image6']

class IntroVideoForm(forms.ModelForm):
    class Meta:
        model = IntroVideo
        fields = ['title','video_file']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['name','username','image','body','time_posted',
                  'views','likes','comments','share','link']

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['header','body']

class FrontPageForm(forms.ModelForm):
    class Meta:
        model = FrontPage
        fields = ['header','body','image']

class WhyUseAgkiForm(forms.ModelForm):
    class Meta:
        model = WhyUseAgki
        fields = ['header','body','image']


# purpose forms
class PurposeVideoForm(forms.ModelForm):
    class Meta:
        model = PurposeTop
        fields = ['video_file']

class PurposeFirstForm(forms.ModelForm):
    class Meta:
        model = PurposeTop
        fields = ['header','subheader','description']

class PurposeSecondForm(forms.ModelForm):
    class Meta:
        model = PurposeTop
        fields = ['descriptionSecond']

class PurposeProblemForm(forms.ModelForm):
    class Meta:
        model = PurposeTop
        fields = ['problem']

class PurposeSolutionForm(forms.ModelForm):
    class Meta:
        model = PurposeTop
        fields = ['solution']

class PurposeForm(forms.ModelForm):
    class Meta:
        model = Purpose
        fields = ['description']

class SuccessForm(forms.ModelForm):
    class Meta:
        model = Success
        fields = ['description']


class FooterContactForm(forms.ModelForm):
    class Meta:
        model = FooterContact
        fields = ['phonenumber','email','address']

class FeaturedPageForm(forms.ModelForm):
    class Meta:
        model = FeaturedPage
        fields = ['title','image']

class FooterLinkForm(forms.ModelForm):
    class Meta:
        model = FooterLink
        fields = ['logo','title','instagramLink','facebookLink','linkedinLink','twitterLink']


class ContactUsModelForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name','role','image']

class TopLogoForm(forms.ModelForm):
    class Meta:
        model = TopLogo
        fields = ['logo']

class WhyUseBgForm(forms.ModelForm):
    class Meta:
        model = WhyUseBg
        fields = ['image']

class ContactUsModelForm(forms.ModelForm):
    class Meta:
        model = ContactUsModel
        fields = ['firstname','lastname','subject','message']
        
class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'role', 'image']

    def clean_image(self):
        image = self.cleaned_data.get('image')

        # You can add validation for the image field if needed

        return image

######################################
######################################
######################################
######################################
######################################
######################################
######################################
######################################