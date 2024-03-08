from rest_framework import serializers
from .models import Transaction, RegisteredCard, ReceivedSMS, Machine
from django.contrib.auth.models import User

      
class RegisteredCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisteredCard
        fields = ['user','card_number', 'card_balance']
        
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['uid', 'version']

class MachinePostSerializer(serializers.ModelSerializer):
    machine = serializers.CharField(source='machine.name', read_only=True)
    class Meta:
        model = Transaction
        fields = ['uid','fertilizer_cost','fertilizer_taken', 'machine']

class ReceivedSMSSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceivedSMS
        fields = ('amount_received', 'phone_number', 'sender_name', 'muamala_number')



# from rest_framework import serializers

# class MachineSerializer(serializers.ModelSerializer):
#     machine_api = serializers.CharField(source='name', read_only=True)
#     tank_volume = serializers.DecimalField(source='tank_volume', read_only=True)
#     volume_left = serializers.DecimalField(source='volume_left', read_only=True)
#     fertilizer_taken = serializers.DecimalField(source='volume_taken', read_only=True)

#     class Meta:
#         model = Machine
#         fields = ['machine_api', 'tank_volume', 'volume_left', 'fertilizer_taken']

# class RegisteredCardSerializer(serializers.ModelSerializer):
#     phone_number = serializers.CharField(source='phone')
#     card_number = serializers.CharField(source='uid')
#     card_balance = serializers.DecimalField(source='card_balance', read_only=True)

#     class Meta:
#         model = RegisteredCard
#         fields = ['phone_number', 'card_number', 'card_balance']

# class TransactionSerializer(serializers.ModelSerializer):
#     uid = serializers.CharField(source='machine.name', read_only=True)
#     fertilizer_cost = serializers.DecimalField(source='fertilizer_cost', read_only=True)
#     fertilizer_taken = serializers.DecimalField(source='fertilizer_taken', read_only=True)
#     card_balance = serializers.DecimalField(source='card_balance_at_transaction', read_only=True)
#     machine_api = serializers.CharField(source='machine.name', read_only=True)

#     class Meta:
#         model = Transaction
#         fields = ['uid', 'fertilizer_cost', 'fertilizer_taken', 'card_balance', 'machine_api']
