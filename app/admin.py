from django.contrib import admin
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse

from app.models import DuesPayment, ContactRequest, DonationPayment, Profile, TeamDate, OldProfile, OfTheYear, OldHighlight, ProfileNote, ProfileImage, AccountRequest, SavedSearch, Gallery, GalleryImage, EventRegistration, ProfileUpdate

class ProfileImageInline(admin.StackedInline):
    model = ProfileImage
    extra = 0

class TeamDateInline(admin.TabularInline):
    model = TeamDate
    extra = 0

class OldHighlightInline(admin.StackedInline):
    model = OldHighlight
    extra = 0

class ProfileNoteInline(admin.StackedInline):
    model = ProfileNote
    extra = 0

class ProfileUpdateAdmin(admin.ModelAdmin):
    list_display = ('profile','action','date')

class OldProfileAdmin(admin.ModelAdmin):
    list_display = ('last_name','first_name')
    search_fields = ['first_name','last_name','nickname','aka']

class ProfileAdmin(admin.ModelAdmin):
    fields = (
        'type',
        'rank','first_name','middle_name','last_name',
        'nickname','aka',
        'home_city','home_state',
        'mos','gkas_year','d_number',
        'deceased_year','deceased_date',
        'admin_cleaned',
        'comments',
        'search_field'
        )

    list_display = ('last_name','first_name','type')
    search_fields = ['first_name','last_name','nickname','aka']
    readonly_fields = ('member_id','user','old_id')
    list_filter = ('type','admin_cleaned')
    inlines = [TeamDateInline,OldHighlightInline, ProfileNoteInline,ProfileImageInline]

    # thing to do when we update a profile
    def response_change(self,request, obj):

        if "_view_profile" in request.POST:
            return HttpResponseRedirect(reverse('website:profile', args=(obj.short_code,)))

        return super().response_change(request, obj)

class DuesPaymentAdmin(admin.ModelAdmin):
    list_display = ('name','email','date','donation','total')
    search_fields = ['name','email']
    readonly_fields = ('uuid',)

class OfTheYearAdmin(admin.ModelAdmin):
    list_display = ('profile','type','year')
    list_filter = ('type',)
    search_fields = ['profile__first_name','profile__last_name']

class AccountRequestAdmin(admin.ModelAdmin):
    list_display = ('name','email_address','date')

class SavedSearchAdmin(admin.ModelAdmin):
    list_display = ('term','date')

class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('name','email','event','type')
    search_fields = ['email','name']

class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ('name','email_address','date')

# Register your models here.
admin.site.register(EventRegistration, EventRegistrationAdmin)
admin.site.register(AccountRequest,AccountRequestAdmin)
admin.site.register(DuesPayment, DuesPaymentAdmin)
admin.site.register(DonationPayment)
admin.site.register(ContactRequest, ContactRequestAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(OldProfile, OldProfileAdmin)
admin.site.register(OfTheYear,OfTheYearAdmin)
admin.site.register(SavedSearch, SavedSearchAdmin)
admin.site.register(GalleryImage)
admin.site.register(ProfileUpdate,ProfileUpdateAdmin)
