from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Farmer, Transaction, Equipment, Receipt, Machine, Subcomponent, Post, RegisteredCard, FertilizerAddition, UserProfile, ReceivedSMS, TeamMember #, RechargeCard
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, HttpResponse
from . forms import FarmerForm, EquipmentForm, SubcomponentForm, ReceiptForm, TransactionForm, MachineRegistrationForm, PostForm, RegisteredCardForm, FertilizerAdditionForm, UserProfileForm #, RechargeCardForm, DepositForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from .forms import UserMessageForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, F, DecimalField
from django.db.models.functions import Coalesce
from decimal import Decimal, ROUND_DOWN
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from twilio.rest import Client
from rest_framework import viewsets
from .serializers import TransactionSerializer, RegisteredCardSerializer, ReceivedSMSSerializer #, TransactionCreateSerializer
from rest_framework.response import Response
from rest_framework import viewsets, status
from collections import defaultdict
import json
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .serializers import MachinePostSerializer
from django.views.decorators.csrf import csrf_exempt
from django.views import View
import logging
from .models import *




def machine_create_view(request):
    if request.method == 'POST':
        form = MachineRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('machine-list')
    else:
        form = MachineRegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'machine_create.html', context)

class MachineListView(ListView):
    model = Machine
    template_name = 'machine_list.html'
    context_object_name = 'machines'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Machine.objects.all().order_by('-id')
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        machines = self.get_queryset()
        paginator = Paginator(machines, self.paginate_by)
        page = self.request.GET.get('page')
        equipment_page = paginator.get_page(page)
        context['machines'] = equipment_page
        return context

class MachineDetailView(DetailView):
    model = Machine
    template_name = 'machine_detail.html'
    context_object_name = 'machine'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Calculate total purchased price for the machine
        total_purchased_price = self.object.transactions.aggregate(total=Sum('fertilizer_cost'))['total']
        context['total_purchased_price'] = total_purchased_price

        # Calculate total volume of fertilizer in litres for the machine
        total_volume_litres = self.object.transactions.aggregate(total=Sum('fertilizer_taken'))['total']
        context['total_volume_litres'] = total_volume_litres
        
        # Include volume taken
        context['volume_taken'] = self.object.volume_taken

        return context


def machine_update_view(request, pk):
    machine = get_object_or_404(Machine, pk=pk)
    if request.method == 'POST':
        form = MachineRegistrationForm(request.POST, instance=machine)
        if form.is_valid():
            form.save()
            return redirect('machine-list')
    else:
        form = MachineRegistrationForm(instance=machine)
    context = {
        'form': form,
        'machine': machine,
    }
    return render(request, 'machine_update.html', context)


def machine_delete_view(request, pk):
    machine = get_object_or_404(Machine, pk=pk)
    if request.method == 'POST':
        machine.delete()
        return redirect('machine-list')
    context = {
        'machine': machine,
    }
    return render(request, 'machine_delete.html', context)

def add_fertilizer(request, machine_id):
    machine = get_object_or_404(Machine, pk=machine_id)
    if request.method == 'POST':
        form = FertilizerAdditionForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount_of_fertilizer']
            FertilizerAddition.objects.create(machine=machine, amount_of_fertilizer=amount)
            machine.add_fertilizer(amount)  # Update machine's volume_left
            return redirect('machine-detail', pk=machine_id)
    else:
        form = FertilizerAdditionForm()
    return render(request, 'add_fertilizer.html', {'form': form, 'machine': machine})

@login_required
def farmer_registration(request):
    if request.method == 'POST':
        form = FarmerForm(request.POST)
        if form.is_valid():
            form.instance.first_name = form.instance.first_name.upper()
            form.instance.last_name = form.instance.last_name.upper()
            
            # Get the currently logged-in user
            current_user = request.user

            # Create a new Farmer instance and associate it with the current user
            farmer_instance = form.save(commit=False)
            farmer_instance.user = current_user  # Set the user field
            
            farmer_instance.save()
            
            send_sms_to_farmer(farmer_instance.phone_no1, farmer_instance.first_name, farmer_instance.last_name)
            return redirect('thank-you')
    else:
        form = FarmerForm()
    context = {
        'form': form
    }
    return render(request, 'farmer_registration.html', context)

def thank_you(request):
    return render(request, 'thank_you.html')

def send_sms_to_farmer(phone_number, first_name, last_name):
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    twilio_phone_number = settings.TWILIO_PHONE_NUMBER
    # Create Twilio client
    client = Client(account_sid, auth_token)
    login_url = "https://www.ngwalainventions.co.tz/"  # Replace with your actual login URL login_url = "http://127.0.0.1:8000/accounts/login/" 
    message_body = f"Thank you {first_name} {last_name} for trusting and registering at Ngwala Inventions. You can now log in here {login_url} for more info. We value our Farmers and you can ask anything here in Chatbot about our company and We, will answer your questions. Fore more help contact this number 0754689034"
    message = client.messages.create(
        body=message_body,
        from_=twilio_phone_number,
        to=phone_number
    )

class FarmerListView(ListView):
    model = Farmer
    template_name = 'farmer_list.html'
    context_object_name = 'farmers'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Farmer.objects.all().order_by('-id')
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        farmers = self.get_queryset()
        paginator = Paginator(farmers, self.paginate_by)
        page = self.request.GET.get('page')
        equipment_page = paginator.get_page(page)
        context['farmers'] = equipment_page
        return context

class FarmerDetailView(DetailView):
    model =Farmer
    template_name = 'farmer_detail.html'
    context_object_name = 'farmer'

@login_required
def farmer_edit_info(request, farmer_id):
    farmer = get_object_or_404(Farmer, id=farmer_id)
    if request.method == 'POST':
        form = FarmerForm(request.POST, instance=farmer)
        if form.is_valid():
            form.save()
            # return redirect('farmer-detail', pk=farmer.pk)
            return redirect('farmer-list')
    else:
        form = FarmerForm(instance=farmer)
        
    context = {
        'form':form,
        'farmer':farmer,
    }
    return render(request, 'farmer_edit_info.html', context)

@login_required
def farmer_deletion(request, farmer_id):
    farmer = get_object_or_404(Farmer, id=farmer_id)
    if request.method == 'POST':
        farmer.delete()
        return redirect('farmer-list')
    context = {
        'farmer':farmer
    }
    return render(request, 'farmer_deletion.html', context)

@login_required
def create_receipt(request):
    if request.method == 'POST':
        form = ReceiptForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('receipt-list')
    else:
        form = ReceiptForm()
    return render(request, 'receipt_creation.html', {'form': form})

class ReceiptListView(ListView):
    model = Receipt
    template_name = 'receipt_list.html'
    context_object_name = 'receipts'
    paginate_by = 2
    
    def get_queryset(self):
        queryset = Receipt.objects.all().order_by('-id')
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        receipts = self.get_queryset()
        paginator = Paginator(receipts, self.paginate_by)
        page = self.request.GET.get('page')
        equipment_page = paginator.get_page(page)
        context['receipts'] = equipment_page
        return context

class ReceiptDetailView(DetailView):
    model = Receipt
    template_name = 'receipt_detail.html'
    context_object_name = 'receipt'

@login_required
def receipt_list(request):
    receipts = Receipt.objects.all()
    return render(request, 'receipt_list.html', {'receipts': receipts})

@login_required
def update_receipt(request, receipt_id):
    receipt = get_object_or_404(Receipt, id=receipt_id)
    if request.method == 'POST':
        form = ReceiptForm(request.POST, request.FILES, instance=receipt)
        if form.is_valid():
            form.save()
            return redirect('receipt-list')
    else:
        form = ReceiptForm(instance=receipt)
    return render(request, 'receipt_update.html', {'form': form, 'receipt': receipt})

@login_required
def delete_receipt(request, receipt_id):
    receipt = get_object_or_404(Receipt, id=receipt_id)
    if request.method == 'POST':
        receipt.delete()
        return redirect('receipt-list')
    return render(request, 'receipt_delete.html', {'receipt': receipt})

@login_required
def register_equipment(request):
    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('equipment-list')  # Redirect to the equipment list page after successful registration
    else:
        form = EquipmentForm()
    
    context = {
        'form': form,
    }
    return render(request, 'equipment_registration.html', context)

class EquipmentListView(ListView):
    model = Equipment
    template_name = 'equipment_list.html'
    context_object_name = 'equipment_items'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Equipment.objects.all().order_by('-id')
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        equipment_items = self.get_queryset()
        paginator = Paginator(equipment_items, self.paginate_by)
        page = self.request.GET.get('page')
        equipment_page = paginator.get_page(page)
        context['equipment_items'] = equipment_page
        return context

class EquipmentDetailView(DetailView):
    model = Equipment
    template_name = 'equipment_detail.html'
    context_object_name = 'equipment_item'

@login_required
def equipment_update_info(request, equipment_id):
    equipment = get_object_or_404(Equipment, id=equipment_id)
    if request.method == 'POST':
        form = EquipmentForm(request.POST, instance=equipment)
        if form.is_valid():
            form.save()
            # return redirect('equipment-detail', equipment_id=equipment_id)
            return redirect('equipment-list')
    else:
        form = EquipmentForm(instance=equipment)
    context = {
        'form':form,
        'equipment':equipment,
    }
    return render(request, 'equipment_update_info.html', context)

@login_required
def equipment_deletion(request, equipment_id):
    equipment = get_object_or_404(Equipment, id=equipment_id)
    if request.method =='POST':
        equipment.delete()
        return redirect('equipment-list')
    context = {
        'equipment':equipment
    }
    return render(request, 'equipment_deletion.html', context)

@login_required
def subcomponent_registration(request):
    if request.method =='POST':
        form = SubcomponentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subcomponent-list')
    else:
        form = SubcomponentForm()
    context = {
        'form':form
    }
    return render(request, 'subcomponent_registration.html', context)

class SubcomponentListView(ListView):
    model = Subcomponent
    template_name = 'subcomponent_list.html'
    context_object_name = 'subcomponents'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Subcomponent.objects.all().order_by('-id')
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subcomponents = self.get_queryset()
        paginator = Paginator(subcomponents, self.paginate_by)
        page = self.request.GET.get('page')
        equipment_page = paginator.get_page(page)
        context['subcomponents'] = equipment_page
        return context

class SubcomponentDetailView(DetailView):
    model = Subcomponent
    template_name = 'subcomponent_detail.html'
    context_object_name = 'subcomponent'

def subcomponent_update(request, subcomponent_id):
    subcomponent = get_object_or_404(Subcomponent, id=subcomponent_id)
    if request.method == 'POST':
        form = SubcomponentForm(request.POST, instance=subcomponent)
        if form.is_valid():
            form.save()
            return redirect('subcomponent-list')  # Redirect to the subcomponent list view upon successful update
    else:
        form = SubcomponentForm(instance=subcomponent)
    context = {
        'form': form,
        'subcomponent': subcomponent,
    }
    return render(request, 'subcomponent_update.html', context)

def subcomponent_delete(request, subcomponent_id):
    subcomponent = get_object_or_404(Subcomponent, id=subcomponent_id)
    if request.method == 'POST':
        subcomponent.delete()
        return redirect('subcomponent-list')
    context = {
        'subcomponent': subcomponent
    }
    return render(request, 'subcomponent_delete.html', context)

def send_withdrawal_sms(user, reference_number, card_number, amount_taken, cost, account_balance):
    # Your Twilio credentials from settings
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    twilio_phone_number = settings.TWILIO_PHONE_NUMBER
    
    # Create Twilio client
    client = Client(account_sid, auth_token)

    # Assuming phone number is stored in the 'phone_no1' field of the Farmer model
    phone_number = getattr(user.farmer, 'phone_no1', None)

    if phone_number:
        # Compose your personalized SMS message
        message_body = (
            f"Hello {user.farmer.first_name}, "
            f"Thank you for using our products. Your transaction {reference_number} with reference to card number {card_number} "
            f"takes {amount_taken} Litres of fertilizer which costs {cost} and your current account balance is {account_balance}."
        )

        # Send SMS
        message = client.messages.create(
            body=message_body,
            from_=twilio_phone_number,
            to=phone_number
        )
    else:
        # Handle the case where the phone number is not available
        print(f"Phone number not found for user: {user.username}")


######################
######################
######################
def transaction_creation(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            try:
                transaction = form.save(commit=False)

                # Access the registered card and get the initial balance
                registered_card = RegisteredCard.objects.filter(card_number=transaction.uid).last()
                # registered_card = RegisteredCard.objects.filter(card_number=transaction.uid).first()
                
                if registered_card:
                    transaction.card_balance = registered_card.card_balance
                else:
                    raise ValidationError('No registered card found with the card number.')

                # Check if the tank has sufficient volume
                if transaction.fertilizer_cost > transaction.card_balance:
                    raise ValidationError(f'The amount entered exceeds your current account balance. Your current balance is {transaction.card_balance}.')
                
                if transaction.fertilizer_taken > transaction.machine.volume_left:
                    raise ValidationError(f'The volume entered exceeds, the available volume in the tank = {transaction.machine.volume_left}')

                transaction.save()

                # Send SMS to the user
                send_withdrawal_sms(
                    user=registered_card.user,  # Assuming a ForeignKey relationship between RegisteredCard and User
                    reference_number=transaction.ref_number,
                    card_number=transaction.uid,
                    amount_taken=transaction.fertilizer_taken,
                    cost=transaction.fertilizer_cost,
                    account_balance=transaction.card_balance
                )
                return redirect('transaction-list')
            except ValidationError as e:
                form.add_error(None, f'{e.message}')
    else:
        form = TransactionForm()
    return render(request, 'transaction_creation.html', {'form': form})

class TransactionListView(ListView):
    model = Transaction
    template_name = 'transaction_list.html'
    context_object_name = 'transactions'
    paginate_by = 20

    def get_queryset(self):
        return Transaction.objects.all().order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(context['transactions'], self.paginate_by)
        page = self.request.GET.get('page')

        try:
            equipment_page = paginator.page(page)
        except PageNotAnInteger:
            equipment_page = paginator.page(1)
        except EmptyPage:
            equipment_page = paginator.page(paginator.num_pages)

        context['transactions'] = equipment_page

        return context



class TransactionDetailView(DetailView):
    model = Transaction
    template_name = 'transaction_detail.html'
    context_object_name = 'transaction'

@login_required
def transaction_updation(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('transaction-list')
    else:
        form = TransactionForm(instance=transaction)
    context = {'form': form, 'transaction':transaction}
    return render(request, 'transaction_updation.html', context)

@login_required
def transaction_deletion(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    if request.method == 'POST':
        transaction.delete()
        return redirect('transaction-list')
    context = {'transaction': transaction}
    return render(request, 'transaction_deletion.html', context)
#####################
#####################
#####################


class AllMachineTransactionsView(ListView):
    model = Transaction
    template_name = 'all_machine_transactions.html'
    context_object_name = 'transactions'
    paginate_by = 10  # Adjust the number of items per page as needed

    def get_queryset(self):
        queryset = Transaction.objects.all().order_by('-created_date')
        
        # Filter by date range
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        if start_date and end_date:
            queryset = queryset.filter(created_date__range=[start_date, end_date])


        # Filter by machine name
        machine_name = self.request.GET.get('machine_name')
        if machine_name:
            queryset = queryset.filter(machine__name__icontains=machine_name)

        # Filter by machine region
        machine_region = self.request.GET.get('machine_region')
        if machine_region:
            queryset = queryset.filter(machine__region__icontains=machine_region)
            
        machine_district = self.request.GET.get('machine_district')
        if machine_district:
            queryset = queryset.filter(machine__district__icontains=machine_district)
            
        machine_ward = self.request.GET.get('machine_ward')
        if machine_ward:
            queryset = queryset.filter(machine__ward__icontains=machine_ward)
            
        machine_village = self.request.GET.get('machine_village')
        if machine_village:
            queryset = queryset.filter(machine__village__icontains=machine_village)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        transactions = self.get_queryset()
        paginator = Paginator(transactions, self.paginate_by)
        page = self.request.GET.get('page')
        transactions_page = paginator.get_page(page)
        # Retrieve start_date and end_date from the request
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        
        # Calculate total amount and total volume
        total_amount = self.get_queryset().aggregate(total_amount=Sum('fertilizer_cost'))['total_amount']
        total_volume = self.get_queryset().aggregate(total_volume=Sum('fertilizer_taken'))['total_volume']

        context['transactions'] = transactions_page
        context['total_amount'] = total_amount
        context['total_volume'] = total_volume
        
        # Calculate total amount for each region
        regions_totals = (
            Transaction.objects.filter(created_date__range=[start_date, end_date])
            .values('machine__region')
            .annotate(
                total_amount=Coalesce(Sum('fertilizer_cost', output_field=DecimalField()), Decimal(0)),
                total_volume=Coalesce(Sum('fertilizer_taken', output_field=DecimalField()), Decimal(0))
            )
            .order_by('-total_amount')
        )
        context['regions_totals'] = regions_totals

        return context

class UserTransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'user_transaction_list.html'  # Create this template for displaying user-specific transactions
    context_object_name = 'user_transactions'
    paginate_by = 20
    
    def get_queryset(self):
        # Filter transactions for the logged-in user
        return Transaction.objects.filter(user=self.request.user).order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_transactions = self.get_queryset()
        paginator = Paginator(user_transactions, self.paginate_by)
        page = self.request.GET.get('page')
        user_transactions_page = paginator.get_page(page)
        context['user_transactions'] = user_transactions_page
        return context

class UserTransactionDetailView(LoginRequiredMixin, DetailView):
    model = Transaction
    template_name = 'user_transaction_detail.html'
    context_object_name = 'user_transaction'

    def get_queryset(self):
        # Filter transactions based on the logged-in user
        return Transaction.objects.filter(user=self.request.user)

def efforts(request):
    return render(request, 'efforts.html')

def impacts(request):
    return render(request, 'impacts.html')

def about_us(request):
    return render(request, 'about_us.html')

def contact(request):
    return render(request, 'contact.html')

def welcome_page(request):
    team_members = TeamMember.objects.all()
    return render(request, 'welcome_page.html', {'team_members': team_members})

def contact_us(request):
    if request.method == 'POST':
        form = UserMessageForm(request.POST)
        if form.is_valid():
            # Save the form data to the database
            user_message = form.save()
            
            # # Send a confirmation email to the user
            # subject = 'Confirmation of Message Submission'
            # message = 'Thank you for contacting us. We have received your message.'
            # from_email = 'victoranthony.av@gmail.com'  # Update with your email
            # recipient_list = [user_message.email]
            
            # send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            return redirect('welcome')  # Redirect to a success page.
    else:
        form = UserMessageForm()
    return render(request, 'contact.html', {'form': form})

def research_and_development(request):
    return render(request, 'researchanddevelopment.html')

def social_feeds(request):
    posts = Post.objects.all()
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            return redirect('social-feeds')
    return render(request, 'social_feeds.html', {'posts':posts, 'form':form,})

def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('social-feeds')  # Redirect to the social feeds page after successful form submission
    else:
        form = PostForm()

    return render(request, 'add_post.html', {'form': form})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'post_detail.html', {'post': post})

@require_POST
def update_like(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        
        try:
            post = Post.objects.get(pk=post_id)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Post not found'}, status=404)

        # Check if the user has already liked the post
        if request.user.is_authenticated and post.likes_users.filter(pk=request.user.pk).exists():
            return JsonResponse({'error': 'You have already liked this post'}, status=400)

        # Increment the likes only if the user hasn't liked the post before
        post.increment_likes()

        # Add the user to the liked_users list
        if request.user.is_authenticated:
            post.likes_users.add(request.user)

        # Return the updated likes count in the JsonResponse
        data = {'likes': post.likes}
        return JsonResponse(data)
    else:
        # Handle other HTTP methods if needed
        return JsonResponse({'error': 'Invalid request method'}, status=405)

#########################
#########################
#########################
@login_required
def register_card(request):
    if request.method == 'POST':
        form = RegisteredCardForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('registered-card-list')
    else:
        form = RegisteredCardForm(user=request.user)
    context = {'form': form}
    return render(request, 'register_card.html', context)

@login_required
def registered_card_list(request):
    cards = RegisteredCard.objects.all().order_by('id')
    
    cards_per_page = 20
    paginator = Paginator(cards, cards_per_page)
    page = request.GET.get('page')
    
    try:
        cards_page = paginator.page(page)
    except PageNotAnInteger:
        cards_page = paginator.page(1)
    except EmptyPage:
        cards_page = paginator.page(paginator.num_pages)
    return render(request, 'registered_card_list.html', {'cards_with_balance': cards_page})

@login_required
def registered_card_detail(request, pk):
    card = get_object_or_404(RegisteredCard, pk=pk)
    return render(request, 'registered_card_detail.html', {'card': card})

@login_required
def registered_card_update(request, pk):
    card = get_object_or_404(RegisteredCard, pk=pk)
    # card = get_object_or_404(RegisteredCard, pk=pk, user=request.user)
    if request.method == 'POST':
        form = RegisteredCardForm(request.POST, instance=card)
        # form = RegisteredCardForm(request.POST, instance=card, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('registered-card-list')
    else:
        form = RegisteredCardForm(instance=card)
        # form = RegisteredCardForm(instance=card, user=request.user)  
    context = {'form': form, 'card': card}
    return render(request, 'registered_card_update.html', context)

@login_required
def registered_card_delete(request, pk):
    card = get_object_or_404(RegisteredCard, pk=pk)
    if request.method == 'POST':
        card.delete()
        return redirect('registered-card-list')
    return render(request, 'registered_card_delete.html', {'card': card})
#########################
#########################
#########################

def create_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('profile-view')
    else:
        form = UserProfileForm()
    return render(request, 'profile_creation.html', {'form': form})

def view_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'profile_view.html', {'user_profile': user_profile})

def update_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile-view')
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'profile_update.html', {'form': form})

def delete_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        # Handle profile deletion
        user_profile.delete()
        return redirect('profile-create')  # Redirect to the profile creation page after deletion
    return render(request, 'profile_delete.html')

###########API
class CardViewSet(viewsets.ModelViewSet):
    queryset = RegisteredCard.objects.all()
    serializer_class = RegisteredCardSerializer  
###########API
class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def list(self, request, *args, **kwargs):
        # Fetch all unique card numbers from the RegisteredCard model
        all_cards = RegisteredCard.objects.values_list('card_number', flat=True).distinct()

        # Construct a dictionary to store card balances and versions
        card_data = {card: {'card_balance': 0.0, 'version': 0} for card in all_cards}

        # Update the dictionary with transaction data
        transactions = Transaction.objects.all()
        for transaction in transactions:
            # Fetch the card_balance from RegisteredCard
            registered_card = RegisteredCard.objects.get(card_number=transaction.uid)
            card_data[transaction.uid]['card_balance'] = registered_card.card_balance
            card_data[transaction.uid]['version'] = transaction.version

        # Fetch initial balances for cards that haven't made transactions
        cards_with_transactions = Transaction.objects.values_list('uid', flat=True).distinct()
        cards_without_transactions = set(all_cards) - set(cards_with_transactions)
        card_balances = RegisteredCard.objects.filter(card_number__in=cards_without_transactions).values_list('card_number', 'card_balance')

        for card_number, card_balance in card_balances:
            card_data[card_number]['card_balance'] = card_balance

        # Reformat the data for the response
        user_balances = [{"user": [{uid: str(data['card_balance']), "ver": data['version']} for uid, data in card_data.items()]}]

        # Return the response
        return Response(user_balances[0])

# tank=level ya tank 
# level=kiasi alichochota
# amt=kiasi cha pesa
# bal=kiasi kilichobak kwenye card
from  datetime import datetime
@csrf_exempt
def getMethod(request):
    if request.method == 'GET':
        try:
            uid = request.GET.get("uid")
            api = request.GET.get("api")
            amt = request.GET.get("amt")
            level = request.GET.get("level")
            tank = request.GET.get("tank")
            bal = request.GET.get("bal")
            dt_str = request.GET.get("dt")

            machine = Machine.objects.get(name=api)
            
            user = request.user if request.user.is_authenticated else None
            
            # Save data to Transaction model
            transaction = Transaction(
                machine=machine,
                fertilizer_cost=amt,
                card_balance_at_transaction=bal,
                fertilizer_taken=level,
                uid=uid,
                user=user,
                transaction_datetime=dt_str
            )
            transaction.full_clean()
            transaction.save()

            # Save data to Machine model
            machine.volume_left = tank
            machine.save()

            # Save data to RegisteredCard model
            registered_card = RegisteredCard.objects.get(user=user)  # Replace with appropriate condition
            registered_card.card_balance = bal
            registered_card.save()
            
            return JsonResponse({"message": "success"})
        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except ObjectDoesNotExist:
            return JsonResponse({'error': "Machine does not exist"}, status=404)

    return JsonResponse({"message": "error"}, status=405)


#############
#############
# def getMethod(request):
#     if request.method == 'GET':
#         try:
#             bal = request.GET.get("bal")
#             api = request.GET.get("api")
#             amt = request.GET.get("amt")
#             level = request.GET.get("level")
#             uid = request.GET.get("uid")
            
#             machine = Machine.objects.get(name=api)
            
#             user = request.user if request.user.is_authenticated else None
            
#             transaction = Transaction(
#                 machine=machine,
#                 fertilizer_cost=amt,
#                 card_balance_at_transaction = bal,
#                 fertilizer_taken=level,
#                 uid=uid,
#                 user=user
#             )
#             transaction.full_clean()
#             transaction.save()
            
#             return JsonResponse({"message": "success"})
#         except ValidationError as e:
#             return JsonResponse({"error": str(e)}, status=400)
#         except ObjectDoesNotExist:
#             return JsonResponse({'error': "Machine does not exist"}, status=404)
#     return JsonResponse({"message": "error"}, status=405)

############
############

def transactiontocard_list(request):
    transactions = ReceivedSMS.objects.all().order_by('-received_time')
    return render(request, 'transactiontocard_list.html', {'transactions': transactions})

# from django.http import JsonResponse
logger = logging.getLogger(__name__)
@csrf_exempt
def received_sms_view(request):
    if request.method == 'POST':
        try:
            payload = json.loads(request.body.decode('utf-8'))
            
            # Check if the muamala_number already exists in ReceivedSMS
            existing_sms = ReceivedSMS.objects.filter(muamala_number=payload['muamala_number']).first()

            # Fetch the corresponding RegisteredCard
            registered_card = RegisteredCard.objects.filter(phone=payload['phone_number']).first()

            if not existing_sms and registered_card and payload['phone_number'] == registered_card.phone:
                # Create a new ReceivedSMS object
                received_sms = ReceivedSMS.objects.create(
                    amount_received=Decimal(payload['amount_received']),
                    sender_name=payload['sender_name'],
                    phone_number=payload['phone_number'],
                    muamala_number=payload['muamala_number']
                )

                # Update the card_balance for the corresponding RegisteredCard
                registered_card.card_balance = F('card_balance') + Decimal(payload['amount_received'])
                registered_card.save()

                return JsonResponse({'status': 'success'})
            elif existing_sms:
                # If the SMS already exists, you may choose to update the card or handle it differently
                return JsonResponse({'status': 'duplicate', 'message': 'Duplicate transaction. Bunned out'})
            elif not registered_card:
                # If the phone_number in the payload does not match any RegisteredCard
                return JsonResponse({'status': 'error', 'message': 'Phone number does not match any registered card'})
            else:
                # If phone numbers do not match
                return JsonResponse({'status': 'error', 'message': 'Phone numbers do not match'})

        except Exception as e:
            logger.error(f"Error processing received SMS: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def user_transaction_history_receivedamount(request):
    user = request.user
    registered_cards = RegisteredCard.objects.filter(user=user)

    transaction_history = []

    for card in registered_cards:
        # Get all top-up entries for each card
        topup_entries = ReceivedSMS.objects.filter(phone_number=card.phone).order_by('-received_time')

        previous_balance = card.card_balance  # Initialize with the current card balance
        
        # Create a transaction entry for each top-up
        for entry in topup_entries:
            current_balance = previous_balance - Decimal(entry.amount_received)

            transaction_history.append({
                'card_number': card.card_number,
                'previous_balance': previous_balance,
                'amount_received': entry.amount_received,
                'time_received': entry.received_time,
                'current_balance': current_balance,
            })

            # Update previous_balance for the next iteration
            previous_balance = current_balance

    return render(request, 'user_transaction_history_receivedamount.html', {'transaction_history': transaction_history})

#############################
#############################
#############################
#############################
#############################
#############################
#############################
#############################
#############################
#############################
#############################
from .forms import *

def purpose(request):
    x = PurposeTop.objects.all()
    purposes = Purpose.objects.all()
    success = Success.objects.all()
    top = TopLogo.objects.all()
    linksfooter = FooterLink.objects.all()
    footer = FooterContact.objects.all()


    context = {
        'x':x,
        'purposes':purposes,
        'success':success,
        'top':top,
        'linksfooter':linksfooter,
        'footer':footer
    }
    return render(request,'purpose.html',context)

def index(request):
    user = request.user
    faqs = Faqs.objects.all()
    news = News.objects.all()
    portfolios = Portfolio.objects.all()
    videos = IntroVideo.objects.all()
    reviews = Review.objects.all()
    services = Service.objects.all()
    frontpages = FrontPage.objects.all()
    whyuseagkis = WhyUseAgki.objects.all()
    footer = FooterContact.objects.all()
    featured = FeaturedPage.objects.all()
    linksfooter = FooterLink.objects.all()
    team = Team.objects.all()
    top = TopLogo.objects.all()
    whyuseimg = WhyUseBg.objects.all()

    form = ContactUsModelForm()
    if request.method=='POST':
        form = ContactUsModelForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"Message send successfully")
            
            return redirect('index')

    context = {
        'faqs':faqs,
        'user':user,
        'news':news,
        'portfolios':portfolios,
        'videos':videos,
        'reviews':reviews,
        'services':services,
        'frontpages':frontpages,
        'whyuseagkis':whyuseagkis,
        'footer':footer,
        'featured':featured,
        'linksfooter':linksfooter,
        'team':team,
        'top':top,
        'whyuseimg':whyuseimg,
        'form':form,

    }
    return render(request,'index.html',context)

def faqdelete(request,id):
    x = get_object_or_404(Faqs,id=id)
    x.delete()
    return redirect('index')

def faqedit(request,pk):
    s = Faqs.objects.get(pk=pk)
    form = FaqsForm(instance=s)
    if request.method=='POST':
        form = FaqsForm(request.POST,instance=s)
        if form.is_valid():
            form.save()
            return redirect('index')
    context = {
            'form':form,
            's':s
         }
    return render(request, 'faqedit.html',context)

def faqadd(request):
    if request.method=='POST':
        form = FaqsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = FaqsForm()
    
    return render(request, 'faqadd.html',{'form':form})

def news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)  # Include request.FILES
        if form.is_valid():
            form.save()
            messages.success(request,"you added hospital successfully")
            return redirect('news')
    else:
        form = NewsForm()
    context = {
        'form': form,
    }
    return render(request,'news.html',context)

def newsedit(request,pk):
    s = News.objects.get(pk=pk)
    form = NewsForm(instance=s)
    if request.method=='POST':
        form = NewsForm(request.POST,instance=s)
        if form.is_valid():
            form.save()
            
            return redirect('index')
    context = {
            'form':form,
            's':s
         }

    return render(request,'newsedit.html',context)

def newsdelete(request,pk):
    x = get_object_or_404(News,pk=pk)
    x.delete()
    return redirect('index')

def portfolioedit(request,pk):
    s = Portfolio.objects.get(pk=pk)
    form = PortfolioForm(instance=s)
    if request.method == 'POST':
        form = PortfolioForm(request.POST, request.FILES,instance=s)  # Include request.FILES
        if form.is_valid():
            form.save()
            messages.success(request,"you added image successfully")
            return redirect('index')
    else:
        form = PortfolioForm()
    context = {
        'form': form,
        's': s,
    }
    return render(request,'portfolioedit.html',context)

def videoedit(request,pk):
    s = IntroVideo.objects.get(pk=pk)
    form = IntroVideoForm(instance=s)
    if request.method=='POST':
        form = IntroVideoForm(request.POST,request.FILES,instance=s)
        if form.is_valid():
            form.save()
            
            return redirect('index')
    context = {
            'form':form,
            's':s
         }

    return render(request,'videoedit.html',context)

def reviewadd(request):
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)  # Include request.FILES
        if form.is_valid():
            form.save()
            messages.success(request,"you added image successfully")
            return redirect('reviewadd')
    else:
        form = ReviewForm()
    context = {
        'form': form,
    }
    return render(request,'reviewadd.html',context)

def reviewedit(request,pk):
    s = Review.objects.get(pk=pk)
    form = ReviewForm(instance=s)
    if request.method=='POST':
        form = ReviewForm(request.POST,request.FILES,instance=s)
        if form.is_valid():
            form.save()
            return redirect('index')
    context = {
            'form':form,
            's':s
         }

    return render(request,'reviewedit.html',context)

def serviceadd(request):
    form = ServiceForm()
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)  # Include request.FILES
        if form.is_valid():
            form.save()
            messages.success(request,"you added image successfully")
            return redirect('serviceadd')
    else:
        form = ServiceForm()
    context = {
        'form': form,
    }
    return render(request,'serviceadd.html',context)

def serviceedit(request,pk):
    s = Service.objects.get(pk=pk)
    form = ServiceForm(instance=s)
    if request.method=='POST':
        form = ServiceForm(request.POST,request.FILES,instance=s)
        if form.is_valid():
            form.save()
            return redirect('index')
    context = {
            'form':form,
            's':s
         }

    return render(request,'serviceedit.html',context)

def servicedelete(request,pk):
    x = get_object_or_404(Service,pk=pk)
    x.delete()
    return redirect('index')


def whyuseagkiadd(request):
    form = WhyUseAgkiForm()
    if request.method == 'POST':
        form = WhyUseAgkiForm(request.POST, request.FILES)  # Include request.FILES
        if form.is_valid():
            form.save()
            messages.success(request,"you added  successfully")
            return redirect('whyuseagkiadd')
    else:
        form = WhyUseAgkiForm()
    context = {
        'form': form,
    }
    return render(request,'whyuseagkiadd.html',context)

def whyuseagkiedit(request,pk):
    s = WhyUseAgki.objects.get(pk=pk)
    form = WhyUseAgkiForm(instance=s)
    if request.method=='POST':
        form = WhyUseAgkiForm(request.POST,request.FILES,instance=s)
        if form.is_valid():
            form.save()
            return redirect('index')
    context = {
            'form':form,
            's':s
         }

    return render(request,'whyuseagkiedit.html',context)

def whyuseagkidelete(request,pk):
    x = get_object_or_404(WhyUseAgki,pk=pk)
    x.delete()
    return redirect('index')


def frontPageedit(request,pk):
    s = FrontPage.objects.get(pk=pk)
    form = FrontPageForm(instance=s)
    if request.method=='POST':
        form = FrontPageForm(request.POST,request.FILES,instance=s)
        if form.is_valid():
            form.save()
            return redirect('index')
    context = {
            'form':form,
            's':s
         }

    return render(request,'frontPageedit.html',context)

def reviewdelete(request,pk):
    x = get_object_or_404(Review,pk=pk)
    x.delete()
    return redirect('index')




# purpose section ##########################################
def purposeFirst(request,id):
    s = PurposeTop.objects.get(id=id)
    form = PurposeFirstForm(instance=s)
    if request.method=='POST':
        form = PurposeFirstForm(request.POST,instance=s)
        if form.is_valid():
            form.save()
            return redirect('purpose')
    context = {
            'form':form,
            's':s
         }
    
    return render(request,'purposeFirst.html',context)

def purposeSecond(request,id):
    s = PurposeTop.objects.get(id=id)
    form = PurposeSecondForm(instance=s)
    if request.method=='POST':
        form = PurposeSecondForm(request.POST,instance=s)
        if form.is_valid():
            form.save()
            return redirect('purpose')
    context = {
            'form':form,
            's':s
         }
    
    return render(request,'purposeSecond.html',context)

def purposeProblem(request,id):
    s = PurposeTop.objects.get(id=id)
    form = PurposeProblemForm(instance=s)
    if request.method=='POST':
        form = PurposeProblemForm(request.POST,instance=s)
        if form.is_valid():
            form.save()
            return redirect('purpose')
    context = {
            'form':form,
            's':s
         }
    
    return render(request,'purposeProblem.html',context)

def purposeSolution(request,id):
    s = PurposeTop.objects.get(id=id)
    form = PurposeSolutionForm(instance=s)
    if request.method=='POST':
        form = PurposeSolutionForm(request.POST,instance=s)
        if form.is_valid():
            form.save()
            return redirect('purpose')
    context = {
            'form':form,
            's':s
         }
    
    return render(request,'purposeSolution.html',context)

def purposeEdit(request,id):
    s = Purpose.objects.get(id=id)
    form = PurposeForm(instance=s)
    if request.method=='POST':
        form = PurposeForm(request.POST,instance=s)
        if form.is_valid():
            form.save()
            return redirect('purpose')
    context = {
            'form':form,
            's':s
         }
    
    return render(request,'purposeEdit.html',context)

def purposeAdd(request):
    form = PurposeForm()
    if request.method=='POST':
        form = PurposeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"purpose added successfully")
            return redirect('purposeAdd')
    context = {
            'form':form
        }
    return render(request,'purposeAdd.html',context)

def purposeDelete(request,id):
    x = get_object_or_404(Purpose,id=id)
    x.delete()
    return redirect('purpose')

def purposeSuccessAdd(request):
    form = SuccessForm()
    if request.method=='POST':
        form = SuccessForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"SuccessForm added successfully")
            return redirect('purposeAdd')
    context = {
            'form':form
        }
    return render(request,'purposeSuccessAdd.html',context)

def purposeSuccessEdit(request,id):
    s = Success.objects.get(id=id)
    form = SuccessForm(instance=s)
    if request.method=='POST':
        form = SuccessForm(request.POST,instance=s)
        if form.is_valid():
            form.save()
            return redirect('purpose')
    context = {
            'form':form,
            's':s
         }
    
    return render(request,'purposeSuccessEdit.html',context)

def purposeSuccessDelete(request,id):
    x = get_object_or_404(Success,id=id)
    x.delete()
    return redirect('purpose')

def purposeVideoEdit(request,id):
    s = PurposeTop.objects.get(id=id)
    form = PurposeVideoForm(instance=s)
    if request.method=='POST':
        form = PurposeVideoForm(request.POST,request.FILES,instance=s)
        if form.is_valid():
            form.save()
            
            return redirect('purpose')
    context = {
            'form':form,
            's':s
         }

    return render(request,'purposeVideoEdit.html',context)




def footerContact(request,id):
    s = FooterContact.objects.get(id=id)
    form = FooterContactForm(instance=s)
    if request.method=='POST':
        form = FooterContactForm(request.POST,request.FILES,instance=s)
        if form.is_valid():
            form.save()
            
            return redirect('index')
    context = {
            'form':form,
            's':s
         }

    return render(request,'footerContact.html',context)



def featuredEdit(request,id):
    s = FeaturedPage.objects.get(id=id)
    form = FeaturedPageForm(instance=s)
    if request.method=='POST':
        form = FeaturedPageForm(request.POST,request.FILES,instance=s)
        if form.is_valid():
            form.save()
            
            return redirect('index')
    context = {
            'form':form,
            's':s
         }

    return render(request,'featuredEdit.html',context)

def featuredAdd(request):
    form = FeaturedPageForm()
    if request.method=='POST':
        form = FeaturedPageForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"Sponsor added successfully")
            
            return redirect('featuredAdd')
    context = {
            'form':form,
         }

    return render(request,'featuredAdd.html',context)

def featuredDelete(request,id):
    x = get_object_or_404(FeaturedPage,id=id)
    x.delete()
    return redirect('index')


def footerLink(request,id):
    s = FooterLink.objects.get(id=id)
    form = FooterLinkForm(instance=s)
    if request.method=='POST':
        form = FooterLinkForm(request.POST,request.FILES,instance=s)
        if form.is_valid():
            form.save()
            
            return redirect('index')
    context = {
            'form':form,
            's':s
         }

    return render(request,'footerLink.html',context)



def teamAdd(request):
    form = TeamForm()
    if request.method=='POST':
        form = TeamForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"Team member added successfully")
            
            return redirect('teamAdd')
    context = {
            'form':form,
         }

    return render(request,'teamAdd.html',context)

def teamEdit(request,id):
    s = Team.objects.get(id=id)
    form = TeamForm(instance=s)
    if request.method=='POST':
        form = TeamForm(request.POST,request.FILES,instance=s)
        if form.is_valid():
            form.save()
            
            return redirect('index')
    context = {
            'form':form,
            's':s
         }

    return render(request,'teamEdit.html',context)

def teamDelete(request,id):
    x = get_object_or_404(Team,id=id)
    x.delete()
    return redirect('index')


def topLogo(request,id):
    s = TopLogo.objects.get(id=id)
    form = TopLogoForm(instance=s)
    if request.method=='POST':
        form = TopLogoForm(request.POST,request.FILES,instance=s)
        if form.is_valid():
            form.save()
            
            return redirect('index')
    context = {
            'form':form,
            's':s
         }

    return render(request,'topLogo.html',context)

def whyUseBg(request,id):
    s = WhyUseBg.objects.get(id=id)
    form = WhyUseBgForm(instance=s)
    if request.method=='POST':
        form = WhyUseBgForm(request.POST,request.FILES,instance=s)
        if form.is_valid():
            form.save()
            
            return redirect('index')
    context = {
            'form':form,
            's':s
         }

    return render(request,'whyUseBg.html',context)


def receivedSms(request):
    s = ContactUsModel.objects.all()
    top = TopLogo.objects.all()
    linksfooter = FooterLink.objects.all()
    footer = FooterContact.objects.all()



    context = {
                's':s,
                'top':top,
                'linksfooter':linksfooter,
                'footer':footer
         }

    return render(request,'receivedSms.html',context)

def receivedSmsDelete(request,id):
    x = get_object_or_404(ContactUsModel,id=id)
    x.delete()
    return redirect('receivedSms')

##########################
##########################
##########################
##########################
##########################
