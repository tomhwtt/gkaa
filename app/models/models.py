from django.db import models
from django.db.models import Sum, Q
import uuid
import datetime

from decimal import Decimal

from users.models import CustomUser

class Profile(models.Model):
    member_id = models.PositiveIntegerField(default=0)
    rank = models.CharField(max_length=5,blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    nickname = models.CharField(max_length=50,blank=True)
    aka = models.CharField(max_length=50,blank=True,verbose_name='AKA')
    hometown = models.CharField(max_length=100, blank=True)
    home_city = models.CharField(max_length=50, blank=True)
    home_state = models.CharField(max_length=2, blank=True)
    mos = models.CharField(max_length=3, blank=True)
    old_id = models.PositiveSmallIntegerField(default=0)
    alumnus_choice = 1
    current_choice = 2
    honorary_choice = 3
    strac_team = 4
    other_choice = 5
    type_choices = (
        (alumnus_choice, 'Alumnus/Alumnae'),
        (current_choice, 'Current Team Member'),
        (honorary_choice, 'Honorary GK'),
        (other_choice, 'Other')
    )
    type = models.IntegerField(choices=type_choices, default=alumnus_choice)
    team_highlights_old = models.TextField(blank=True)
    army_highlights_old = models.TextField(blank=True)
    civilian_highlights_old = models.TextField(blank=True)
    current_status = models.TextField(blank=True)
    current_status_old = models.TextField(blank=True)
    comments = models.TextField(blank=True)
    deceased_date = models.DateField(blank=True, null=True)
    deceased_year = models.PositiveIntegerField(blank=True, null=True)
    army_start_date = models.PositiveIntegerField(default=0,blank=True, null=True)
    army_end_date = models.PositiveIntegerField(default=0, blank=True, null=True)
    gkas_year = models.CharField(max_length=4, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    uuid = models.UUIDField(default=uuid.uuid4,editable=False)
    short_code = models.CharField(max_length=12)
    skip_state = models.BooleanField(default=False)
    admin_cleaned = models.BooleanField(default=False)
    do_not_display = models.BooleanField(default=False)
    search_field = models.TextField(blank=True)
    temp_user_id = models.PositiveIntegerField(default=0)
    has_thumbnail = models.BooleanField(default=False)
    thumbnail_checked = models.BooleanField(default=False)
    d_number = models.CharField(max_length=10, blank=True)
    old_highlights = models.BooleanField(default=False)
    url_code = models.CharField(max_length=15)
    update_priority = models.PositiveIntegerField(default=0)
    update_complete = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    teamdate_string = models.CharField(max_length=150,blank=True)
    show_link = models.BooleanField(default=False)

    def dues_paid(self):

        # set the current year
        current_year = int(datetime.datetime.now().year)

        dues_search = self.duespayment_set.filter(
                amount__gt=0,
                year__gte = current_year
            )

        if dues_search:
            are_dues_paid = True
        else:
            are_dues_paid = False

        return are_dues_paid

    def show_home_origin(self):

        if self.home_city and self.home_state:
            return self.home_city + ', ' + self.home_state
        elif not self.home_city and self.home_state:
            return self.home_state
        else:
            return None

    def show_deceased_date(self):

        if self.deceased_date:
            return self.deceased_date
        elif self.deceased_year:
            return self.deceased_year
        else:
            return None

    def start_year(self):

        if self.teamdate_set.count():
            start_year = self.teamdate_set.first().start_year
        else:
            start_year = None

        return start_year

    def end_year(self):

        if self.teamdate_set.count():

            if self.teamdate_set.first().end_year:
                end_year = self.teamdate_set.first().end_year
            else:
                end_year = None
        else:
            end_year = None

        return end_year

    # show the Extended Profile page?
    def extended_profile(self):

        if self.profileentry_set.count() > 2:
            extended = True
        else:
            extended = False

        return extended

    # show (3 highlights on Main Profile Page)
    def home_highlights(self):

        return self.profileentry_set.filter(
            show_on_home = True,
            date_delete__isnull = True,

        )[:3]

    # does the Profile have a Profile Image set up?
    def profile_image_src(self):

        image = self.profileimage_set.filter(profile_image=True).first()

        if image:

            imgix = (
                'https://gkaa.imgix.net/images/profiles/' + image.name +
                '?fit=fill&fill=solid&fill-color=ffffff&w=600&h=600'
            )

        elif self.has_thumbnail and self.thumbnail_checked:

            imgix = (
                'https://gkaa.imgix.net/images/roster/' +
                str(self.member_id) + '-detail-hero.jpg'
            )


        else:

            imgix = 'https://gkaa.imgix.net/images/assets/roster-owls-head-sm.jpg?fit=crop&w=300&h=300'

        return imgix

    def roster_image_src(self):

        roster_image = self.profileimage_set.filter(roster_image=True).first()
        profile_image = self.profileimage_set.filter(profile_image=True).first()

        if roster_image:
            image = roster_image
        elif profile_image:
            image = profile_image
        else:
            image = None

        # if there is an image, use it
        if image:

            imgix = (
                'https://gkaa.imgix.net/images/profiles/' + image.name +
                '?fit=fill&fill=solid&fill-color=ffffff&w=200&h=260'
            )

        # are we still using the old image (member_id)
        elif self.has_thumbnail and self.thumbnail_checked:

            imgix = (
                'https://gkaa.imgix.net/images/roster/' +
                str(self.member_id) + '-detail-hero.jpg' +
                '?fit=crop&w=200&h=260'
            )

        # if no other image, use the Owl's head
        else:

            imgix = 'https://gkaa.imgix.net/images/assets/roster-owls-head-sm.jpg?fit=crop&w=200&h=260'

        return imgix

    def note_list(self):
        return self.profileentry_set.filter(
            type=8,
            date_delete__isnull = True
            )

    def story_list(self):
        return self.profilestory_set.all()

    def oldhighlight_list(self):
        return self.oldhighlight_set.filter(
            date_delete__isnull=True
        )

    def oldhighlights(self):

        return self.oldhighlight_set.filter(
            date_delete__isnull = True
        )

    def image_list(self):
        return self.profileimage_set.filter(
            date_delete__isnull=True
        )

    def entry_list(self):

        # get all EntryTypes except Highlights & Admin Notes
        type_set = EntryType.objects.exclude(
            Q(slug = 'admin-notes')|
            Q(slug = 'entries')|
            Q(slug = 'links')|
            Q(slug = 'stories')|
            Q(slug = 'highlights')
        )

        the_list = []

        for type in type_set:

            entries = self.profileentry_set.filter(
                entrytype = type
            )

            type_obj = {
                'id': type.id,
                'title': type.title,
                'singular': type.singular,
                'entries': entries,
                'count': entries.count()
            }

            the_list.append(type_obj)

        return the_list

    def __str__(self):
        return self.last_name + str(', ') + self.first_name

class ProfileUpdate(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=250)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return str(self.profile)

class ProfileFilter(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField()
    active = models.BooleanField(default=False)
    use_filter_date = models.BooleanField(default=False)
    roster_card_title = models.CharField(max_length=20,blank=True)

    def __str__(self):
        return self.name

class ProfileFilterHolder(models.Model):
    profilefilter = models.ForeignKey(ProfileFilter,on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    sort_order = models.PositiveIntegerField(default=0)
    year = models.PositiveIntegerField(default=0)

class AccountRequest(models.Model):
    name = models.CharField(max_length=150)
    email_address = models.EmailField()
    info = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField(default=uuid.uuid4,editable=False)
    pending_verification = models.BooleanField(default=False)
    pending_date = models.DateTimeField(null=True,blank=True)
    later = models.BooleanField(default=False)
    complete = models.DateTimeField(null=True,blank=True)

    def text_date(self):
        return self.date.strftime('%b %-d, %Y @ %-I:%M%p')

    def has_account(self):

        try:
            account = CustomUser.objects.get(email=self.email_address)
        except:
            account = None

        return account

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return self.name

class AccountRequestNote(models.Model):
    accountrequest = models.ForeignKey(AccountRequest,on_delete=models.CASCADE)
    note = models.CharField(max_length=250)
    date = models.DateTimeField(auto_now_add=True)
    reminder_date = models.DateField(null=True)
    user = models.ForeignKey(CustomUser,on_delete=models.SET_NULL,null=True)

    def text_date(self):
        return self.date.strftime('%b %-d, %Y @ %-I:%M%p')

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return self.note

class RecentProfile(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def date_text(self):
        return self.date.strftime('%a %b %-m @ %-I:%M %p')

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return str(self.profile)

class ProfileImage(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=150,blank=True)
    caption = models.TextField(blank=True)
    credit = models.CharField(max_length=150,blank=True)
    year = models.CharField(max_length=4,blank=True)
    image = models.CharField(max_length=150,blank=True)
    name = models.CharField(max_length=20)
    uuid = models.UUIDField(default=uuid.uuid4,editable=False)
    thumb = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    sort_order = models.PositiveIntegerField(default=0)
    date_delete = models.DateTimeField(blank=True, null=True)
    size = models.PositiveIntegerField(default=0)
    profile_image = models.BooleanField(default=False)
    roster_image = models.BooleanField(default=False)

    def profile_src(self):

        imgix = (
            'https://gkaa.imgix.net/images/profiles/' +
            self.name +
            '?fit=fillmax&fill=solid&fill-color=ffffff' +
            '&w=300&h=300'
        )

        return imgix

    def src(self):

        aws = 'https://gkaa-assets.s3.amazonaws.com/tmpimages/'

        return aws + self.name

    # create a short caption for the image list
    def short_caption(self):

        if len(self.caption) > 15:
            return self.caption[:15] + '...'
        else:
            return self.caption

    # show the edit image link in the ProfileImage list
    def show_edit_text(self):
        if (
            not self.title and not
            self.caption and not
            self.credit and not
            self.year
            ):
            return True
        else:
            return False

    # is this the profile image (hero shot)
    def is_profile_image(self):

        if self.profile_image:
            return 'text-success'
        else:
            return 'text-black-50'

    class Meta:
        ordering = ('-profile_image','sort_order')

    def __str__(self):
        return str(self.profile)

class EntryType(models.Model):
    title = models.CharField(max_length=50)
    singular = models.CharField(max_length=50)
    slug = models.SlugField()
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('sort_order',)

    def __str__(self):
        return self.title

class ProfileEntry(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    entrytype = models.ForeignKey(EntryType,on_delete=models.CASCADE)
    text = models.CharField(max_length=250)
    details = models.TextField(blank=True)
    link = models.URLField(max_length=250, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    date_delete = models.DateTimeField(blank=True, null=True)
    teamjob_choice = 1
    armyjob_choice = 2
    award_choice = 3
    license_choice = 4
    highlight_choice = 5
    comment_choice = 6
    link_choice = 7
    note_choice = 8
    type_choices = (
        (teamjob_choice, 'Team Job'),
        (armyjob_choice, 'Army Job'),
        (award_choice, 'Award or Badge'),
        (license_choice, 'License or Rating'),
        (highlight_choice, 'Highlight'),
        (comment_choice, 'Comment or Story'),
        (link_choice, 'External Link'),
        (note_choice, 'Admin Note')
    )
    type = models.IntegerField(choices=type_choices, default=teamjob_choice)
    highlight = models.BooleanField(default=False)
    show_on_home = models.BooleanField(default=False)

    class Meta:
        ordering = ('sort_order',)

    def __str__(self):
        return self.text

class EntryExample(models.Model):
    entrytype = models.ForeignKey(EntryType,on_delete=models.CASCADE)
    example = models.CharField(max_length=150)

    def __str__(self):
        return self.example

class ProfileActivity(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    activity = models.CharField(max_length=150)
    type = models.SlugField()
    type_id = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.activity

class Section(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()

    def __str__(self):
        return self.name

class TeamDate(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    start_year = models.PositiveIntegerField(blank=True, null=True)
    end_year = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        ordering = ('start_year',)

    def __str__(self):
        return str(self.start_year) + '-' + str(self.end_year)

class ArmyDate(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    start_year = models.PositiveIntegerField(blank=True, null=True)
    end_year = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        ordering = ('start_year',)

    def __str__(self):
        return str(self.start_year) + '-' + str(self.end_year)

class ProfileStory(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=150,blank=True)
    text = models.TextField()

    def the_title(self):
        if self.title:
            return self.title
        else:
            return 'Untitled Comment'

    def date_text(self):
        return self.date.strftime('%b %d, %Y @ %-H:%M %p')

    class Meta:
        ordering = ('date',)

    def __str__(self):
        return self.title

class ProfileNote(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    in_house_choice = 1
    public_choice = 2
    type_choices = (
        (in_house_choice, 'In House'),
        (public_choice, 'Public/Website'),

    )
    type = models.IntegerField(choices=type_choices,default=in_house_choice)

class OldHighlight(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    text = models.TextField()
    slug = models.SlugField()
    date_delete = models.DateTimeField(blank=True,null=True)

class DuesPayment(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=250)
    email = models.EmailField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    donation = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stripe_charge_id = models.CharField(max_length=32)
    uuid = models.UUIDField(default=uuid.uuid4,editable=False)
    year = models.PositiveIntegerField()

    def text_date(self):
        return self.date.strftime('%b %-d, %Y @ %-I:%M%p')

    def total(self):
        return self.amount + self.donation

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return self.email

class DonationPayment(models.Model):
    name = models.CharField(max_length=250)
    email = models.EmailField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_charge_id = models.CharField(max_length=32)
    note = models.TextField(blank=True)
    uuid = models.UUIDField(default=uuid.uuid4,editable=False)

    def total(self):
        return self.amount

    def __str__(self):
        return self.email

class ContactRequest(models.Model):
    name = models.CharField(max_length=150)
    email_address = models.EmailField()
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField(default=uuid.uuid4,editable=False)
    url = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.name

class OfTheYear(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT)
    year = models.PositiveIntegerField(blank=True, null=True)
    goldenknight_choice = 1
    aviator_choice = 2
    photographer_choice = 3
    civilian_choice = 4
    type_choices = (
        (goldenknight_choice, 'Golden Knight'),
        (aviator_choice, 'Aviator'),
        (photographer_choice, 'Photographer'),
        (civilian_choice, 'Civilian')
    )
    type = models.IntegerField(choices=type_choices, default=goldenknight_choice)

    def roster_card_text(self):

        if self.type == 1:
            text = 'Golden Knight / Year: ' + str(self.year)
        elif self.type == 2:
            text = 'Aviator / Year: ' + str(self.year)
        elif self.type == 3:
            text = 'Photographer / Year: ' + str(self.year)
        elif self.type == 4:
            text = 'Civilian / Year: ' + str(self.year)
        elif self.type == 5:
            text = 'Honorary GK: ' + str(self.year)
        elif self.type == 6:
            text = 'Original USAPT'
        else:
            text = None

        return text

    def __str__(self):
        return str(self.profile)

class ShipState(models.Model):
    long_name = models.CharField(max_length=15)
    short_name = models.CharField(max_length=2)
    def __str__(self):
        return self.long_name

class SavedSearch(models.Model):
    term = models.CharField(max_length=250)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.term

# TEMP MODELS TO TRANSFER INFO
class OldProfile(models.Model):
    old_id = models.PositiveIntegerField()
    member_id = models.PositiveIntegerField()
    last_name = models.CharField(max_length=150,blank=True)
    first_name = models.CharField(max_length=150,blank=True)
    middle_name = models.CharField(max_length=150,blank=True)
    nickname = models.CharField(max_length=150,blank=True)
    aka = models.CharField(max_length=150,blank=True)
    rank = models.CharField(max_length=50,blank=True)
    hometown = models.CharField(max_length=50,blank=True)
    email_address = models.EmailField(max_length=250,blank=True)
    deceased = models.CharField(max_length=50,blank=True)
    status = models.CharField(max_length=50,blank=True)
    type = models.CharField(max_length=50,blank=True)
    army_start_date = models.CharField(max_length=50,blank=True)
    army_end_date = models.CharField(max_length=50,blank=True)
    team_start_one = models.CharField(max_length=50,blank=True)
    team_start_two = models.CharField(max_length=50,blank=True)
    team_end_one = models.CharField(max_length=50,blank=True)
    team_end_two = models.CharField(max_length=50,blank=True)
    goy1 = models.CharField(max_length=50,blank=True)
    goy2 = models.CharField(max_length=50,blank=True)
    aoy1 = models.CharField(max_length=50,blank=True)
    aoy2 = models.CharField(max_length=50,blank=True)
    army_jobs = models.TextField(blank=True)
    team_jobs = models.TextField(blank=True)
    army_beats = models.TextField(blank=True)
    team_beats = models.TextField(blank=True)
    civilian_beats = models.TextField(blank=True)
    awards = models.TextField(blank=True)
    comments = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    license = models.TextField(blank=True)
    current_status = models.TextField(blank=True)
    coy1 = models.CharField(max_length=50,blank=True)
    coy2 = models.CharField(max_length=50,blank=True)
    poy1 = models.CharField(max_length=50,blank=True)
    poy2 = models.CharField(max_length=50,blank=True)
    hgk = models.CharField(max_length=50,blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return self.last_name + str(' ') + self.first_name

class OriginalUser(models.Model):
    email_address = models.CharField(max_length=250)
    name = models.CharField(max_length=250)
    member_id = models.CharField(max_length=15)
    notes = models.TextField()
    type = models.PositiveIntegerField(default=0)

class TeamDateOld(models.Model):
    old_id = models.PositiveIntegerField(default=0)
    team_start_one = models.CharField(max_length=4)
    team_end_one = models.CharField(max_length=4)
    team_start_two = models.CharField(max_length=4)
    team_end_two = models.CharField(max_length=4)
    done = models.BooleanField(default=False)


# The first iteration of Event was Registration
# This can be removed after saving the records. IF we even want to
class Registration(models.Model):
    name = models.CharField(max_length=150)
    first_name = models.CharField(max_length=100,blank=True)
    last_name = models.CharField(max_length=100,blank=True)
    email_address = models.EmailField(max_length=150)
    uuid = models.UUIDField(default=uuid.uuid4,editable=False)
    alumnus_choice = 1
    current_choice = 2
    honorary_choice = 3
    other_choice = 4
    type_choices = (
        (alumnus_choice, 'Alumnus'),
        (current_choice, 'Current'),
        (honorary_choice, 'Honorary'),
        (other_choice, 'Other')
    )
    type = models.IntegerField(choices=type_choices, default=alumnus_choice)
    num_sponsor = models.PositiveIntegerField(default=0)
    num_veggie = models.PositiveIntegerField(default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stripe_charge_id = models.CharField(max_length=32, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    email_sent = models.DateTimeField(blank=True, null=True)

    def dues_paid(self):
        try:
            duespayment = DuesPayment.objects.filter(email=self.email_address)
        except:
            duespayment = ''

        if duespayment:
            return True
        else:
            return False

    def friday_attendees(self):
        return self.attendee_set.filter(event=1)

    def saturday_attendees(self):
        return self.attendee_set.filter(event=2)

    def num_friday_attendees(self):
        return self.attendee_set.filter(event=1).count()

    def num_saturday_attendees(self):
        return self.attendee_set.filter(event=2).count()


    def __str__(self):
        return self.email_address

class Attendee(models.Model):
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE)
    name = models.CharField(max_length=150,blank=True)
    fri_choice = 1
    sat_choice = 2
    event_choices = (
        (fri_choice, 'Friday Night'),
        (sat_choice, 'Saturday Night'),
    )
    event = models.IntegerField(choices=event_choices,default=fri_choice)
    uuid = models.UUIDField(default=uuid.uuid4,editable=False)

    def __str__(self):
        return self.name


class Gallery(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField()

    def __str__(self):
        return str(self.name)

class GalleryImage(models.Model):
    caption = models.TextField(blank=True)
    credit = models.CharField(max_length=150,blank=True)
    year = models.PositiveIntegerField(blank=True,null=True)
    image = models.CharField(max_length=250)
    old_name = models.CharField(max_length=150,blank=True)
    uuid = models.UUIDField(default=uuid.uuid4,editable=False)
    old_id = models.CharField(max_length=32)
    date_added = models.DateTimeField(auto_now_add=True)
    image_exists = models.BooleanField(default=False)

    def detail_src(self):

        imgix = (
            'https://gkaa.imgix.net/images/ogallery/' +
            self.old_name +
            '?w=800&h=800'
        )

        return imgix

    def grid_src(self):

        imgix = (
            'https://gkaa.imgix.net/images/ogallery/' +
            self.old_name +
            '?fit=crop&w=500&h=500'
        )

        return imgix

    def url(self):

        imgix = (
            'https://gkaa.imgix.net/images/ogallery/' +
            self.old_name +
            '?w=500&h=500'
        )

        return imgix + self.old_name

    def caption_text(self):

        if len(self.caption) > 100:
            return self.caption[:100]
        else:
            return self.caption

    def long_caption(self):

        if len(self.caption) > 100:
            return True
        else:
            return False

    def __str__(self):
        return str(self.gallery)

class GalleryImageHolder(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE)
    galleryimage = models.ForeignKey(GalleryImage, on_delete=models.CASCADE)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('id',)

class GalleryImageSearch(models.Model):
    term = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.term

class OldGalleryImage(models.Model):
    title = models.CharField(max_length=150, blank=True)
    caption = models.TextField(blank=True)
    credit = models.CharField(max_length=150,blank=True)
    year = models.CharField(max_length=150,blank=True)
    old_id = models.CharField(max_length=32)
    gallery = models.PositiveIntegerField(default=0)
    transferred = models.BooleanField(default=False)
