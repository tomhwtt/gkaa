from django.urls import path
from django.conf.urls import url
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

from . import views

app_name = 'account'

urlpatterns = [

    # Account Home
    path('', views.account_index, name='index'),

    # Profile Index
    path('profile/<uuid:uuid>/', views.profile_index, name='profile-index'),

    # Profile Detail
    path('profile/<uuid:uuid>/detail/', views.profile_detail, name='profile-detail'),

    # Profile Edit
    path('profile/<uuid:uuid>/edit/', views.profile_edit, name='profile-edit'),

    # Profile Entries
    path('profile/<uuid:uuid>/entries/<int:type>/',
        views.profile_entries, name='profile-entries'),


    ## THIS PAGE IS WHERE THEY SET THEIR PROFILE AND ROSTER CARD IMAGE
    path('profile/<uuid:uuid>/image/', views.profile_image, name='profile-image'),


    ## THIS IS GOING TO BE PROFILE GALLERY IMAGES
    ## change this to a different name

    # ProfileImage List
    path('profile/<uuid:uuid>/images/',
        views.profileimage_list, name='profileimage-list'),

    # ProfileImage Detail
    path('profile/<uuid:uuid>/images/<int:id>/',
        views.profileimage_detail, name='profileimage-detail'),

    # ProfileImage Detail
    path('profile/<uuid:uuid>/images/<int:id>/edit/',
        views.profileimage_edit, name='profileimage-edit'),

    # ProfileImage New
    path('profile/<uuid:uuid>/images/new/',
        views.profileimage_new, name='profileimage-new'),

    # ProfileImage Delete
    path('profile/<uuid:uuid>/images/<int:id>/delete/',
        views.profileimage_delete, name='profileimage-delete'),

    # ProfileImage Set as Profile Image
    path('profile/<uuid:uuid>/images/<int:id>/profile/',
        views.profileimage_profile_image, name='profileimage-profile-image'),

    # ProfileImage Set as Roster Image
    path('profile/<uuid:uuid>/images/<int:id>/roster/',
        views.profileimage_roster_image, name='profileimage-roster-image'),

    # an How To and Profile Example
    path('profile/<uuid:uuid>/example/', views.profile_example, name='profile-example'),

    # Old Highlights
    path('profile/<uuid:uuid>/past/', views.oldhighlights, name='oldhighlights'),

    # Delete Old Highlight
    path('profile/<uuid:uuid>/oldhighlight/<int:id>/delete/',
        views.oldhighlight_delete, name='oldhighlight-delete'),

    # Profile Entry Detail
    path('profile/<uuid:uuid>/entry/<int:id>/',
        views.entry_detail, name='entry-detail'),

    # Profile Entry Delete
    path('profile/<uuid:uuid>/entry/<int:id>/delete/',
        views.entry_delete, name='entry-delete'),

    # Profile Dates
    path('profile/<uuid:uuid>/dates/',
        views.profile_dates, name='profile-dates'),

    # Delete TeamDate
    path('profile/<uuid:uuid>/teamdate/<int:id>/delete/',
        views.teamdate_delete, name='teamdate-delete'),

    # Delete ArmyDate
    path('profile/<uuid:uuid>/armydate/<int:id>/delete/',
        views.armydate_delete, name='armydate-delete'),

    # ProfileStory List
    path('profile/<uuid:uuid>/stories/',
        views.profilestory_list, name='profilestory-list'),

    # ProfileStory Detail
    path('profile/<uuid:uuid>/story/<int:id>/',
        views.profilestory_detail, name='profilestory-detail'),

    # ProfileStory New
    path('profile/<uuid:uuid>/story/new/',
        views.profilestory_new, name='profilestory-new'),

    # ProfileStory Edit
    path('profile/<uuid:uuid>/story/<int:id>/edit/',
        views.profilestory_edit, name='profilestory-edit'),

    # ProfileStory Delete
    path('profile/<uuid:uuid>/story/<int:id>/delete/',
        views.profilestory_delete, name='profilestory-delete'),


    # Profile Public Comment
    path('profile/<uuid:uuid>/comments/',
        views.profile_comments, name='profile-comments'),

    # Profile Current Status
    path('profile/<uuid:uuid>/status/',
        views.profile_current_status, name='profile-current-status'),

    # Account Request
    path('new/request/', views.accountrequest_new, name='accountrequest-new'),

    path('new/request/<uuid:uuid>/',
        views.accountrequest_confirmed, name='accountrequest-confirmed'),


    ## LOGIN | AUTH INFO | LOGIN | AUTH INFO
    ## LOGIN | AUTH INFO | LOGIN | AUTH INFO

    # login info
    path('login/', auth_views.LoginView.as_view(
        redirect_authenticated_user=True), name='login'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # password reset
    path('password-reset/',
        auth_views.PasswordResetView.as_view(
        success_url='/account/password-reset/done/'),
        name="password-reset"
        ),

    # url after you submit your email address
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(),
        name='password-reset-done'),

    # url that confirms the link you clicked in your email
    path('password-reset/confirm/<str:uidb64>/<str:token>/',
        auth_views.PasswordResetConfirmView.as_view(
            success_url='/account/password-reset/complete/'),
            name = "password-reset-confirm"
        ),

    # url that confirms you are done and offers link to login
    path('password-reset/complete/',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password-reset-complete'
        ),

    # sandbox
    path('sandbox/', views.sandbox, name='sandbox'),
    path('sandbox/user/connect/', views.sandbox_connect_user, name='sandbox-connect-user'),
    path('sandbox/originaluser/type/', views.sandbox_originaluser_type, name='originaluser-type'),


]
