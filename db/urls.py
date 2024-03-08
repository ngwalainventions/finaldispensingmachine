from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
# from rest_framework import routers
from . views import TransactionViewSet, CardViewSet #, ReceivedSMSViewSet #, MachinePostViewSet #, MachineDataView
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'transactions', TransactionViewSet)
# router.register(r'machineapi', MachinePostViewSet)
router.register(r'cards', CardViewSet)
# router.register(r'received-sms', ReceivedSMSViewSet)



urlpatterns = [
    #########################
    path('welcome/', views.welcome_page, name='welcome'),
    path('farmers/', views.FarmerListView.as_view(), name='farmer-list'),
    path('farmers/<int:pk>/', views.FarmerDetailView.as_view(), name='farmer-detail'),
    path('register/farmer/', views.farmer_registration, name='farmer-registration'),
    path('thank-you/', views.thank_you, name='thank-you'),
    path('edit_farmer_info/<int:farmer_id>/', views.farmer_edit_info, name='farmer-edit-info'),
    path('delete_farmer/<int:farmer_id>/', views.farmer_deletion, name='farmer-deletion'),
    #########################
    path('machines/', views.MachineListView.as_view(), name='machine-list'),
    path('machines/list/number/<int:pk>/', views.MachineDetailView.as_view(), name='machine-detail'),
    path('machine/create/', views.machine_create_view, name='machine-create'),
    path('machine/update/<int:pk>/', views.machine_update_view, name='machine-update'),
    path('machine/delete/<int:pk>/', views.machine_delete_view, name='machine-delete'),
    path('machine/<int:machine_id>/add_fertilizer/', views.add_fertilizer, name='add-fertilizer'),
    #########################
    path('equipment/', views.EquipmentListView.as_view(), name='equipment-list'),
    path('equipment/<int:pk>/', views.EquipmentDetailView.as_view(), name='equipment-detail'),
    path('register/equipment/', views.register_equipment, name='equipment-registration'),
    path('equipment/update/<int:equipment_id>/', views.equipment_update_info, name='equipment-update-info'),
    path('equipment/<int:equipment_id>/delete/', views.equipment_deletion, name='equipment-deletion'),
    #########################
    path('subcomponents/', views.SubcomponentListView.as_view(), name='subcomponent-list'),
    path('subcomponents/<int:pk>/', views.SubcomponentDetailView.as_view(), name='subcomponent-detail'),
    path('register/subcomponent/', views.subcomponent_registration, name='subcomponent-registration'),
    path('update/subcomponent/<int:subcomponent_id>/', views.subcomponent_update, name='subcomponent-update'),
    path('subcomponents/delete/<int:subcomponent_id>/', views.subcomponent_delete, name='subcomponent-delete'),
    #########################
    path('receipts/', views.ReceiptListView.as_view(), name='receipt-list'),
    path('receipts/<int:pk>/', views.ReceiptDetailView.as_view(), name='receipt-detail'),
    path('receipts/', views.receipt_list, name='receipt-list'),
    path('receipts/create/', views.create_receipt, name='create-receipt'),
    path('receipts/update/<int:receipt_id>/', views.update_receipt, name='receipt-update'),
    path('receipts/delete/<int:receipt_id>/', views.delete_receipt, name='receipt-delete'),
    #########################
    path('transactions/create/', views.transaction_creation, name='transaction-creation'),
    path('transaction-lists/', views.TransactionListView.as_view(), name='transaction-lists'),
    path('transactions/<int:pk>/', views.TransactionDetailView.as_view(), name='transaction-detail'),
    path('transactions/update/<int:transaction_id>/', views.transaction_updation, name='transaction-updation'),
    path('transactions/delete/<int:transaction_id>/', views.transaction_deletion, name='transaction-deletion'),
    path('all-machine-transactions/', views.AllMachineTransactionsView.as_view(), name='all-machine-transactions'),
    #########################
    path('user/message/', views.contact_us, name='user-message'),
    path('rnd/', views.research_and_development, name='research-and-development'),
    path('about/', views.about_us, name='about-us'),
    path('efforts/', views.efforts, name='efforts'),
    path('impacts/', views.impacts, name='impacts'),
    #########################
    path('social-feeds/', views.social_feeds, name='social-feeds'),
    path('add-post/', views.add_post, name='add-post'),
    path('post/<int:pk>/', views.post_detail, name='post-detail'),
    path('update_like/', views.update_like, name='update_like'),
    #########################
    path('user-transaction-list/', views.UserTransactionListView.as_view(), name='user-transaction-list'),
    path('user-transaction-detail/<int:pk>/', views.UserTransactionDetailView.as_view(), name='user-transaction-detail'),
    #########################
    path('register-card/', views.register_card, name='register-card'),
    path('registered-card-list/', views.registered_card_list, name='registered-card-list'),
    path('registered-cards/<int:pk>/', views.registered_card_detail, name='registered-card-detail'),
    path('registered-cards/<int:pk>/update/', views.registered_card_update, name='registered-card-update'),
    path('registered-cards/<int:pk>/delete/', views.registered_card_delete, name='registered-card-delete'),
    ########################
    path('create/', views.create_profile, name='profile-create'),
    path('view/', views.view_profile, name='profile-view'),
    path('update/', views.update_profile, name='profile-update'),
    path('delete/', views.delete_profile, name='profile-delete'),
    ########################
    # path('api/machine-data/', views.create, name='machine-data'),
    # path('api/machine-data-sent/', views.process_machine_data, name='machine-data-sent'),
    path('api/machine-data-getmethod/', views.getMethod, name='machine-data-getmethod'),
    path('api/', include(router.urls)),
    path('api/received-sms-to-card/', views.received_sms_view, name='received_sms'),
    ########################
    path('transactiontocard/', views.transactiontocard_list, name='transactiontocard'),
    path('user-transaction-history/', views.user_transaction_history_receivedamount, name='user-transaction-history'),
    
    
    
    
    ##################################
    ##################################
    ##################################
    ##################################
    ##################################
    ##################################
    ##################################
    ##################################
    path('purpose/', views.purpose,name='purpose'),
    path('', views.index,name='index'),
    path('faqdelete/<int:id>/', views.faqdelete,name='faqdelete'),
    path('faqedit/<str:pk>/', views.faqedit,name='faqedit'),
    path('faqadd/', views.faqadd,name='faqadd'),
    path('news/', views.news,name='news'),
    path('newsedit/<str:pk>/', views.newsedit,name='newsedit'),
    path('newsdelete/<str:pk>/', views.newsdelete,name='newsdelete'),
    path('portfolioedit/<str:pk>/', views.portfolioedit,name='portfolioedit'),
    path('videoedit/<str:pk>/', views.videoedit,name='videoedit'),
    path('reviewadd/', views.reviewadd,name='reviewadd'),
    path('reviewedit/<str:pk>/', views.reviewedit,name='reviewedit'),
    path('reviewdelete/<str:pk>/', views.reviewdelete,name='reviewdelete'),
    path('serviceadd/', views.serviceadd,name='serviceadd'),
    path('serviceedit/<str:pk>/', views.serviceedit,name='serviceedit'),
    path('servicedelete/<str:pk>/', views.servicedelete,name='servicedelete'),
    path('whyuseagkiadd/', views.whyuseagkiadd,name='whyuseagkiadd'),
    path('whyuseagkiedit/<str:pk>/', views.whyuseagkiedit,name='whyuseagkiedit'),
    path('whyuseagkidelete/<str:pk>/', views.whyuseagkidelete,name='whyuseagkidelete'),
    path('frontPageedit/<str:pk>/', views.frontPageedit,name='frontPageedit'),


    path('purposeFirst/<int:id>/', views.purposeFirst, name='purposeFirst'),
    path('purposeSecond/<int:id>/', views.purposeSecond, name='purposeSecond'),
    path('purposeProblem/<int:id>/', views.purposeProblem, name='purposeProblem'),
    path('purposeSolution/<int:id>/', views.purposeSolution, name='purposeSolution'),
    path('purposeEdit/<int:id>/', views.purposeEdit, name='purposeEdit'),
    path('purposeSuccessEdit/<int:id>/', views.purposeSuccessEdit, name='purposeSuccessEdit'),
    path('purposeDelete/<int:id>/', views.purposeDelete, name='purposeDelete'),
    path('purposeAdd/', views.purposeAdd, name='purposeAdd'),
    path('purposeSuccessAdd/', views.purposeSuccessAdd, name='purposeSuccessAdd'),
    path('purposeDelete/<int:id>/', views.purposeDelete, name='purposeDelete'),
    path('purposeSuccessDelete/<int:id>/', views.purposeSuccessDelete, name='purposeSuccessDelete'),
    path('purposeVideoEdit/<int:id>/', views.purposeVideoEdit, name='purposeVideoEdit'),
   
   
    path('featuredAdd/', views.featuredAdd, name='featuredAdd'),
    path('featuredEdit/<int:id>/', views.featuredEdit, name='featuredEdit'),
    path('featuredDelete/<int:id>/', views.featuredDelete, name='featuredDelete'),
    path('footerContact/<int:id>/', views.footerContact, name='footerContact'),
    path('footerLink/<int:id>/', views.footerLink, name='footerLink'),
    path('teamAdd/', views.teamAdd, name='teamAdd'),
    path('teamEdit/<int:id>/', views.teamEdit, name='teamEdit'),
    path('teamDelete/<int:id>/', views.teamDelete, name='teamDelete'),
    path('topLogo/<int:id>/', views.topLogo, name='topLogo'),
    path('whyUseBg/<int:id>/', views.whyUseBg, name='whyUseBg'),
    path('receivedSmsDelete/<int:id>/', views.receivedSmsDelete, name='receivedSmsDelete'),
    path('receivedSms/', views.receivedSms, name='receivedSms'),
   
    ##################################
    ##################################
    ##################################
    ##################################
    ##################################
    ##################################
    ##################################
    ##################################
    ]