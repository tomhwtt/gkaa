import uuid
import datetime

from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from app.models import DuesPayment, RecentProfile, ProfileUpdate

# clean up the trix html for a snippet
def clean_trix_html(html):

    # set the snippet
    snippet = html

    # replace all of the html
    snippet = snippet.replace('<div>','')
    snippet = snippet.replace('</div>','')

    snippet = snippet.replace('<h1>','')
    snippet = snippet.replace('</h1>','')

    snippet = snippet.replace('<strong>','')
    snippet = snippet.replace('</strong>','')

    snippet = snippet.replace('<ul>','')
    snippet = snippet.replace('</ul>','')

    snippet = snippet.replace('<ol>','')
    snippet = snippet.replace('</ol>','')

    snippet = snippet.replace('<li>',' --')
    snippet = snippet.replace('</li>',' ')

    snippet = snippet.replace('<em>','')
    snippet = snippet.replace('</em>','')

    snippet = snippet.replace('<del>','')
    snippet = snippet.replace('</del>','')

    snippet = snippet.replace('&nbsp;',' ')
    snippet = snippet.replace('<br>',' ')

    # shorten the snippet
    if len(snippet) > 200:
        snippet = snippet[:200]

    return snippet.strip()

# create a short code
def create_short_code():

    # create a uuid
    unique_id = uuid.uuid4()

    # convert it to text
    text = str(unique_id)

    # split it up by the dashes
    words = text.split('-')

    # return the first index of words
    code = words[0]

    return code

# create a short code
def create_url_code():

    # create a uuid
    unique_id = uuid.uuid4()

    # convert it to text
    text = str(unique_id)

    # split it up by the dashes
    words = text.split('-')

    # add the first and second set of words for 12 characters total
    code = words[0] + words[1]

    return code

# create a 12 character image name
def create_image_name():

    # create a uuid
    unique_id = uuid.uuid4()

    # convert it to text
    text = str(unique_id)

    # split it up by the dashes
    words = text.split('-')

    # return the first and second sections of the uuid
    code = words[0] + words[1]

    return code

def create_safe_email(email):

    #split the email address
    username = email.split('@')[0]
    domain_name = email.split('@')[1]

    try:

        if len(username) > 5:
            username = username[:2] + '***' + username[4:]

        safe_email = username + '@' + domain_name

    except:

        safe_email = email

    return safe_email

def check_dues_by_email(email):

    # set the current year
    this_year = datetime.datetime.today().year

    # find a dues payment for this email address and year
    dues = DuesPayment.objects.filter(
        email = email,
        year = this_year
    )

    if dues:
        return True
    else:
        return False

def calculate_event_total(registration):

    subevent_set = registration.subeventregistration_set.all()

    for sub in subevent_set:

        # get the SubEventPricing
        pricing = SubEventPricing.objects.get(
            subevent = sub.subevent,
            type = registration.type
        )

        if sub.quantity <= pricing.quantity:
            total = pricing.amount

        elif sub.quantity > pricing.quantity:
            add_ons = sub.quantity - pricing.quantity
            total = pricing.amount + (add_ons * pricing.add_on_pricing)

        # if they have paid dues, we can remove
        if registration.type == 1 and pricing.free_with_dues and dues_paid:
            total -= 50

        cart_total += total

    return cart_total

def set_recentprofile(profile):

    # get the last 5 RecentProfiles
    recent_set = RecentProfile.objects.all()[:5]

    # set to False by default
    is_recent = False

    # if this profile is in the last 5, set to True
    for recent in recent_set:
        if profile == recent.profile:
            is_recent = True

    # if this Profile is not in the last 5, create a record
    if not is_recent:
        # update the recent profile table
        recent = RecentProfile(
            profile = profile
        )

        recent.save()

def entry_type_title(type):

    if type == 1:
        title = 'Team Jobs'
        singular = 'Team Job'
    elif type == 2:
        title = 'Army Jobs'
        singular = 'Army Job'
    elif type == 3:
        title = 'Awards & Badges'
        singular = 'Award or Badge'
    elif type == 4:
        title = 'Licenses & Ratings'
        singular = 'License or Rating'
    elif type == 5:
        title = 'Highlights'
        singular = 'Highlight'
    elif type == 6:
        title = 'Comments and Stories'
        singular = 'Comment or Story'
    elif type == 7:
        title = 'External Links'
        singular = 'External Link'
    else:
        title = 'Entries'
        singular = 'Entry'

    return_obj = {
        'title': title,
        'singular': singular
    }

    return return_obj

def update_teamdate_string(profile):

    # set the updated team dates
    teamdate_set = profile.teamdate_set.all()

    # update the teamdate_string
    teamdate_string = ''

    if not teamdate_set:
        profile.teamdate_string = ''
        profile.save()

    else:

        for index, date in enumerate(teamdate_set):

            date_string = str(date.start_year)

            if date.end_year:
                date_string += '-' + str(date.end_year)

            teamdate_string += date_string.strip()

            if index + 1 < teamdate_set.count():
                teamdate_string += ', '

        profile.teamdate_string = teamdate_string
        profile.save()

def set_profile_show_link(profile):

    show_link = False

    if profile.profileentry_set.count():
        show_link = True

    if profile.comments:
        show_link = True

    profile.show_link = show_link
    profile.save()

def create_profileupdate(p,u,a):

    # log the update
    update = ProfileUpdate(
        profile = p,
        user = u,
        action = a
    )

    update.save()

# clean up the trix html for a snippet
def clean_trix_text(html):

    # set the snippet
    snippet = html

    # replace all of the html
    snippet = snippet.replace('<div>','')
    snippet = snippet.replace('</div>','')

    snippet = snippet.replace('<h1>','')
    snippet = snippet.replace('</h1>','')

    snippet = snippet.replace('<ul>','')
    snippet = snippet.replace('</ul>','')

    snippet = snippet.replace('<ol>','')
    snippet = snippet.replace('</ol>','')

    snippet = snippet.replace('<li>',' --')
    snippet = snippet.replace('</li>',' ')

    snippet = snippet.replace('<em>','')
    snippet = snippet.replace('</em>','')

    snippet = snippet.replace('<del>','')
    snippet = snippet.replace('</del>','')

    snippet = snippet.replace('&nbsp;',' ')

    # Trix adds a <br> at the end of the text for some reason
    # this removes it (if it exists)
    if snippet[len(snippet)-4:] == '<br>':
        snippet = snippet[:len(snippet)-4:]

    return snippet.strip()
