from django.contrib import admin
from .models import Transaction, Machine, Farmer, Equipment, Subcomponent, Receipt, UserMessage, Post, RegisteredCard, FertilizerAddition, UserProfile, ReceivedSMS, TeamMember
from django.utils.html import format_html
from .models import *


class RegisteredCardAdmin(admin.ModelAdmin):
    list_display = ('card_number', 'user', 'phone','card_balance')
    search_fields = ('card_number', 'user__username', 'user__email')
admin.site.register(RegisteredCard, RegisteredCardAdmin)

class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('teammember_name', 'position', 'bio')
admin.site.register(TeamMember, TeamMemberAdmin)

admin.site.register(Subcomponent)

class TransactionsAdmin(admin.ModelAdmin):
    model = Transaction
    list_display = ('ref_number', 'uid', 'fertilizer_taken','fertilizer_cost', 'machine','get_machine_region')
    search_fields = ('uid','machine','get_machine_region',)
    
    def get_machine_region(self, obj):
        return obj.machine.region if obj.machine else None

    get_machine_region.short_description = 'Machine Region'
admin.site.register(Transaction, TransactionsAdmin)

class FertilizerAdditionAdmin(admin.ModelAdmin):
    list_display = ('machine', 'amount_of_fertilizer', 'date_added')
admin.site.register(FertilizerAddition, FertilizerAdditionAdmin)

@admin.register(Machine)
class MachinesAdmin(admin.ModelAdmin):
    model = Machine
    list_display = ['name', 'machine_model','region','district','ward','village', 'tank_volume', 'refill_date', 'status', 'tank_cap','volume_left']
    # list_display = ['name', 'machine_model', 'location', 'tank_volume', 'refill_date', 'status', 'tank_cap', 'inst_date']
    
@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['serial', 'name', 'models_no', 'category', 'color', 'location']

@admin.register(Farmer)
class FarmerAdmin(admin.ModelAdmin):  
    list_display = ['user','first_name', 'last_name', 'gender', 'phone_no1', 'farm_size','display_crop_types','nation', 'region', 'district', 'ward', 'village']
    list_filter = ['region', 'ward', 'gender']
    
    def display_crop_types(self, obj):
        crop_types = [getattr(obj, f'crop_type{i}') for i in range(1, 4) if getattr(obj, f'crop_type{i}')]
        return ', '.join(crop_types)

    display_crop_types.short_description = 'Crop Types'

    fieldsets = [
        (None, {
            'fields': (('first_name', 'last_name'), 'email', 'phone_no1', 'farm_size','crop_type1','crop_type2','crop_type3','nation', 'region', 'gender')
        }),
        
        ('Advanced options', {
            'classes': ('wide', 'extrapretty'),
            'fields': ('address', 'postal_code', 'village', 'district', 'ward', 'profile_photo', 'other_occ', 'notes'),
        }),
        
        ('others', {
            'classes': ('collapse'),
            'fields': ('send_notification', 'send_newslaters', 'expire_date'),
        }),
    ]
    
    # add_fieldsets = (
    #     (None, {
    #         'classes': ('collapse',),
    #         'fields': ('first_name', 'last_name', 'email', 'phone_no', 'created')
    #     }),
    # )
    search_fields = ('first_name', 'last_name', 'email', 'phone_no')
    ordering = ()
    filter_horizontal = ()
    
    def profile_photo(self, obj):
        return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>')
 
@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ['number', 'serial', 'supplier', 'date', 'item']

class UserMessageAdmin(admin.ModelAdmin):
    list_display = ('name','email', 'message',)
    list_filter = ('name','email','message')
    search_fields = ('name', 'email', 'message')
admin.site.register(UserMessage, UserMessageAdmin)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'image', 'author',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_image')

@admin.register(ReceivedSMS)
class ReceivedSMSAdmin(admin.ModelAdmin):
    list_display = ('amount_received', 'phone_number', 'sender_name', 'muamala_number')
    

admin.site.register(Faqs)
admin.site.register(News)
admin.site.register(Portfolio)
admin.site.register(IntroVideo)
admin.site.register(Review)
admin.site.register(Service)
admin.site.register(FrontPage)
admin.site.register(WhyUseAgki)



admin.site.register(Purpose)
admin.site.register(Success)
admin.site.register(PurposeTop)

admin.site.register(FooterContact)
admin.site.register(FeaturedPage)
admin.site.register(FooterLink)
admin.site.register(Team)
admin.site.register(TopLogo)
admin.site.register(WhyUseBg)
admin.site.register(ContactUsModel)