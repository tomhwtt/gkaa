from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'website'
urlpatterns = [

    # index pages

    path('robots.txt', TemplateView.as_view(template_name='website/robots.txt', content_type="text/plain"), name="robots"),

    path('', views.index, name='index'),

    path('contact/', views.contact_us_view, name='contact'),

    # Event Detail (Event Description)
    path('event/<str:event_code>/', views.event_detail, name='event-detail'),

    # Event Detail Register View
    path('event/<str:event_code>/register/', views.event_register, name='event-register'),

    # Create the New Event Registration (AJAX)
    path('event/registration/new/', views.event_register_new),

    # Event Payment View Page
    path('event/registration/<str:short_code>/payment/',
        views.event_registration_payment, name='eventregistration-payment'),

    # Event Charge Action
    path('event/registration/<str:short_code>/charge/',
        views.event_registration_charge, name='eventregistration-charge'),

    # Event Complete (no balance due)
    path('event/registration/<str:short_code>/complete/',
        views.event_registration_complete, name='eventregistration-complete'),

    # Registration Detail
    path('event/registration/<str:short_code>/',
        views.event_registration_detail, name='eventregistration-detail'),

    # gallery
    path('gallery/', views.gallery_index, name='gallery-index'),
    path('gallery/<slug:slug>/', views.gallery_detail, name='gallery-detail'),
    path('gallery/<slug:slug>/<uuid:uuid>/', views.galleryimage_detail, name='galleryimage-detail'),


    path('history/', views.history_view, name='history'),

    path('roster/', views.roster_list, name='roster'),
    path('roster/menu/', views.roster_menu, name='roster-menu'),

    # Profile
    path('profile/<str:url_code>/', views.profile_view, name='profile'),
    path('profile/<str:url_code>/ext/', views.extended_profile_view, name='extended-profile'),


    # Pay Dues
    path('pay-dues/', views.pay_dues_view, name='pay-dues'),
    path('pay-dues/<uuid:uuid>/', views.pay_dues_charge_view, name='pay-dues-charge'),
    path('pay-dues/<uuid:uuid>/confirm/', views.pay_dues_confirm_view, name='pay-dues-confirm'),

    # Stripe
    path('api/stripe/charge/new/', views.stripe_charge_new, name='stripe-charge-new'),

    # Global Charge Success Page
    path('<str:type>/<uuid:id>/success/', views.charge_success_view, name='charge-success'),

    # Validate Email
    path('api/validate/email/', views.validate_email_action, name='validate-email'),


    # Donations
    path('donate/', views.donate_view, name='donate'),

    path('sandbox/', views.sandbox, name='sandbox'),


    # Non Login, Event Check In
    path('checkin/<slug:slug>/',
        views.checkin_event_detail, name='checkin-event-detail'),

    path('checkin/<slug:slug>/<int:pk>/',
        views.checkin_subevent_detail, name='checkin-subevent-detail'),

    path('registration/<int:pk>/',
        views.checkin_subeventregistration_detail, name='checkin-subeventregistration-detail'),

    path('registration/<int:pk>/checkin/',
        views.checkin_subeventregistration_checkin, name='checkin-subeventregistration-checkin'),






]
