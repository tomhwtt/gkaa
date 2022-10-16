from django.urls import path

from . import views

app_name = 'app'

urlpatterns = [

    path('', views.app_index, name='app-index'),

    path('accountrequests/', views.accountrequest_list, name='accountrequest-list'),

    path('accountrequest/<int:pk>/',
        views.accountrequest_detail, name='accountrequest-detail'),

    path('accountrequest/<int:pk>/delete/',
        views.accountrequest_delete, name='accountrequest-delete'),

    path('accountrequest/<int:pk>/set-pending/',
        views.accountrequest_set_pending, name='accountrequest-set-pending'),

    path('accountrequest/<int:pk>/set-later/',
        views.accountrequest_set_later, name='accountrequest-set-later'),

    path('accountrequest/<int:pk>/complete/',
        views.accountrequest_complete, name='accountrequest-complete'),

    path('armydate/<int:pk>/delete/', views.armydate_delete, name='armydate-delete'),

    path('user/new/<int:pk>/', views.customuser_new, name='customuser-new'),

    path('user/<int:pk>/', views.customuser_detail, name='customuser-detail'),

    path('users/', views.customuser_list, name='customuser-list'),

    path('dues/', views.duespayment_list, name='duespayment-list'),

    # Events
    path('events/', views.event_list, name='event-list'),
    path('events/<int:pk>/', views.event_detail, name='event-detail'),
    path('events/<int:pk>/email/', views.event_email, name='event-email'),

    path('events/<int:pk>/registration/',
        views.eventregistration_new, name='eventregistration-new'),

    path('registration/<int:pk>/',
        views.eventregistration_detail, name='eventregistration-detail'),

    # Gallery
    path('gallery/', views.gallery_list, name='gallery-list'),
    path('gallery/<int:pk>/', views.gallery_detail, name='gallery-detail'),
    path('galleryimage/<int:pk>/', views.galleryimage_detail, name='galleryimage-detail'),

    path('search/', views.app_search, name='search'),

    path('profile/<int:pk>/', views.profile_detail, name='profile-detail'),

    path('profile/<int:pk>/edit/', views.profile_edit_view, name='profile-edit'),

    path('profile/<int:pk>/dates/', views.profile_dates, name='profile-dates'),

    path('profile/<int:pk>/entries/<int:type>/',
        views.profile_entries, name='profile-entries'),

    path('profile/new/', views.profile_new, name='profile-new'),

    path('profile/<int:pk>/split/',
        views.profile_split_entry_view, name='profile-split-entry'),

    path('profile/<int:pk>/set-user/<int:id>/',
        views.profile_set_user, name='profile-set-user'),

    # ProfileUpdate List
    path('profileupdates/',
        views.profileupdate_list, name='profileupdate-list'),

    # ProfileImage List
    path('profile/<int:pk>/images/',
        views.profileimage_list, name='profileimage-list'),

    # ProfileImage New
    path('profile/<int:pk>/images/new/',
        views.profileimage_new, name='profileimage-new'),

    # ProfileImage Detail
    path('profile/<int:pk>/images/<int:id>/',
        views.profileimage_detail, name='profileimage-detail'),

    # ProfileImage Edit
    path('profile/<int:pk>/images/<int:id>/edit/',
        views.profileimage_edit, name='profileimage-edit'),

    # ProfileImage Delete
    path('profile/<int:pk>/images/<int:id>/delete/',
        views.profileimage_delete, name='profileimage-delete'),

    # ProfileImage Set as Profile Image
    path('profile/<int:pk>/images/<int:id>/profile/',
        views.profileimage_profile_image, name='profileimage-profile-image'),

    # ProfileImage Set as Profile Image
    path('profile/<int:pk>/images/<int:id>/roster/',
        views.profileimage_roster_image, name='profileimage-roster-image'),


    path('teamdate/<int:pk>/delete/', views.teamdate_delete, name='teamdate-delete'),

    path('entry/<int:pk>/', views.entry_detail, name='entry-detail'),

    path('entry/<int:pk>/delete/', views.entry_delete, name='entry-delete'),

    path('subevents/<int:pk>/', views.subevent_detail, name='subevent-detail'),

    # Emails
    path('user/<int:pk>/send-account-email/',
        views.send_user_account_email, name='send-user-account-email'),

    # ProfileStory List
    path('profile/<int:pk>/stories/',
        views.profilestory_list, name='profilestory-list'),

     # ProfileStory New
    path('profile/<int:pk>/stories/new/',
        views.profilestory_new, name='profilestory-new'),

    # ProfileStory Detail
    path('profile/<int:pk>/stories/<int:id>/',
        views.profilestory_detail, name='profilestory-detail'),

    # ProfileStory Edit
    path('profile/<int:pk>/stories/<int:id>/edit/',
        views.profilestory_edit, name='profilestory-edit'),

    # ProfileStory Delete
    path('profile/<int:pk>/stories/<int:id>/delete/',
        views.profilestory_delete, name='profilestory-delete'),


    # TEMPORARY VIEWS # TEMPORARY VIEWS
    # ProfileStory Delete
    path('temp/', views.temp_index, name='temp-index'),


    ### Clean Up Below Here

    # Profile Update Priority List
    path('profiles/priority/', views.profile_priority_list, name='profile-priority'),

    # Go To Profile
    path('profiles/<int:pk>/go/', views.profile_go_action, name='profile-go'),

    # sandbox
    path('sandbox/', views.sandbox, name='sandbox'),
    path('sandbox/registration/name/', views.sandbox_registration_name, name='registration-name'),
    path('sandbox/searchfield/', views.sandbox_search_field, name='sandbox-searchfield'),
    path('sandbox/stripnames/', views.sandbox_strip_names, name='sandbox-stripnames'),
    path('sandbox/highlight/sortorder/', views.sandbox_highlight_sort_order, name='sandbox-sortorder'),
    path('sandbox/gallery/transfer/', views.sandbox_gallery_transfer, name='sandbox-gallery-transfer'),
    path('sandbox/galleryimage/exists/', views.sandbox_galleryimage_exists, name='sandbox-galleryimage-exists'),
]
