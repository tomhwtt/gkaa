from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Q
import operator
from functools import reduce
import datetime
import stripe
from django.conf import settings
import json
from django.http import JsonResponse
from random import randrange, shuffle
import math

from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from app.models import DuesPayment, DonationPayment, Registration, Attendee, Profile, TeamDate, SavedSearch, Gallery, GalleryImage, GalleryImageSearch, GalleryImageHolder, OfTheYear, ProfileEntry, Event, EventRegistration, ProfileFilter

from website.forms import DuesPaymentForm, DonationPaymentForm, ContactRequestForm

from utils.postmark import send_contactrequest_email
from utils.utils import create_safe_email, set_profile_show_link
from utils.spam import form_spam


@login_required
def sandbox(request):

    profile_list = Profile.objects.all()

    for p in profile_list:
        set_profile_show_link(p)

    return HttpResponse('sandbox')

@login_required
def sandbox_gallery(request):

    image_list = GalleryImage.objects.all()

    for image in image_list:

        name = image.image.split('/')[1]

        image.old_name = name.strip()
        image.save()


    return HttpResponse('sandbox')

@login_required
def sandbox_validate_email(request):

    try:
        validate_email('joe.jones.jimbobarmy.mail.mil')
        email_is_valid = True
    except:
        email_is_valid = False

    return HttpResponse(email_is_valid)

def index(request):

    image_list = [
        'ramp_jump.jpg',
        'double.jpg',
        'usa_pow.jpg',
        'baton_pass.jpg',
        'freefall.jpg',
        'aviation.jpg',
        'eight_way.jpg',
        'lineup.jpg'
    ]

    gallery_list = [
        'freefall.jpg',
        'chuck.jpg',
        'triangle.jpg',
        'tri_by_side.jpg'
    ]

    slideshow = []

    for index, image in enumerate(image_list):

        if index == 0:
            active = 'active'
        else:
            active = ''

        slide_obj = {
            'name': image,
            'index': index,
            'active': active
        }

        slideshow.append(slide_obj)

    if request.GET.get('p'):
        page = 'website/index_' + request.GET.get('p') + '.html'
    else:
        page = 'website/index_two.html'

    context = {
        'slideshow': slideshow,
        'gallery_list': gallery_list
    }

    return render(request, page, context)

# gallery home/index view
def gallery_index(request):

    gallery = get_object_or_404(Gallery,slug='eighties')

    # create a more images list
    holder_set = gallery.galleryimageholder_set.all().select_related(
        'galleryimage',
        'gallery'
    )[:24]

    image_list = []

    for h in holder_set:

        image_obj = {
            'uuid': h.galleryimage.uuid,
            'slug': h.gallery.slug,
            'src': h.galleryimage.grid_src()
        }

        image_list.append(image_obj)

    context = {
        'image_list': image_list
    }

    if request.GET.get('p'):
        page = 'website/gallery_' + request.GET.get('p') + '.html'
    else:
        page = 'website/galleryindex.html'

    return render(request, page, context )

def gallery_detail(request,slug):

    gallery = get_object_or_404(Gallery,slug=slug)

    # create a more images list
    holder_set = gallery.galleryimageholder_set.all().select_related(
        'galleryimage',
        'gallery'
    ).order_by('id')[:24]

    image_list = []

    for h in holder_set:

        image_obj = {
            'uuid': h.galleryimage.uuid,
            'slug': h.gallery.slug,
            'src': h.galleryimage.grid_src()
        }

        image_list.append(image_obj)


    context = {
        'gallery': gallery,
        'image_list': image_list
    }

    return render(request, 'website/gallery_detail.html', context)

# view for a specific gallery by slug
def gallery_view(request,slug):

    # if this is a post, save the search and
    # redirect back to the page with search term
    if request.method == 'POST':

        search = request.POST['search'].strip()

        galleryimagesearch = GalleryImageSearch(term=search)
        galleryimagesearch.save()

        return HttpResponseRedirect(reverse('website:gallery', args=('search',))+ '?q=' + search)


    # if a page is passed in for pagination
    if request.GET.get('page') and request.GET.get('page').isnumeric():
        current_page = int(request.GET.get('page'))
    else:
        current_page = 1

    # try to find a gallery that matches the slug
    try:
        gallery = Gallery.objects.get(slug=slug)

        galleryimage_all = GalleryImage.objects.filter(
            gallery = gallery,
            image_exists = True
        )

    # if there is no gallery, we search the whole table
    except:
        gallery = None

        galleryimage_all = GalleryImage.objects.filter(
            image_exists = True
        )


    # if a search term was passed in, filter the list even more
    if request.GET.get('q'):

        search = request.GET.get('q')

        # create an OR query using all the terms in the search block
        multiple_lookups = reduce(operator.or_, (
            Q(caption__icontains=term) for term in search.split()
            )
        )

        # filter the search
        galleryimage_all = galleryimage_all.filter(multiple_lookups)

    else:
        search = None

    # set the pagination number
    paginate_by = 12

    # set up pagination
    paginator = Paginator(galleryimage_all,paginate_by)
    page = request.GET.get('page')

    galleryimage_list = paginator.get_page(page)

    if galleryimage_list.has_next() and not search:

        next_page = '?page=' + str(galleryimage_list.next_page_number())

    elif galleryimage_list.has_next() and search:

        next_page = '?page=' + str(galleryimage_list.next_page_number()) + '&q=' + search

    else:
        next_page = None

    if galleryimage_list.has_previous() and not search:
        previous_page = '?page=' + str(galleryimage_list.previous_page_number())
    elif galleryimage_list.has_previous() and search:
        previous_page = '?page=' + str(galleryimage_list.previous_page_number()) + '&q=' + search
    else:
        previous_page = None

    # set the total number of pages
    num_pages = galleryimage_list.paginator.num_pages

    # create the first and last link
    if not search:
        first_link = '?page=1'
        last_link = '?page=' + str(num_pages)
    else:
        first_link = '?page=1&q=' + search
        last_link = '?page=' + str(num_pages) + '&q=' + search

    # create a pagination array
    pagination_array = []

    # create a start page
    if num_pages - current_page < 3:
        start_page = num_pages - 4
    elif num_pages >= 3:
        start_page = current_page - 2

    # since the splice is zero based, subtract one from the start page
    start_page = start_page - 1

    #lastly, if the start page is less than 1, make it one
    if start_page < 0:
        start_page = 0

    # set the end page
    end_page = start_page + 5

    # loop through the pages to create pagination
    for page in galleryimage_list.paginator.page_range[start_page:end_page]:

        if page == current_page:
            status = 'active'
        else:
            status = None

        if not search:
            query_string = '?page=' + str(page)
        else:
            query_string = '?page=' + str(page) + '&q=' + search.strip()

        pagination_array.append({
            'page_number': page,
            'query_string': query_string,
            'status': status
        })

    # create a first and last link:


    # show pagination only if there is more than one page
    if num_pages > 1:
        show_pagination = True
    else:
        show_pagination = False

    context = {
        'galleryimage_list': galleryimage_list,
        'gallery_slug': slug,
        'next_page': next_page,
        'previous_page': previous_page,
        'num_pages': num_pages,
        'pagination_array': pagination_array,
        'current_page': current_page,
        'start_page': start_page,
        'end_page': end_page,
        'show_pagination': show_pagination,
        'search': search,
        'first_link': first_link,
        'last_link': last_link
    }

    return render(request, 'website/gallery.html', context)

def galleryimage_detail(request,slug,uuid):

    gallery = get_object_or_404(Gallery, slug=slug)
    galleryimage = get_object_or_404(GalleryImage, uuid=uuid)


    # create a more images list
    holder_set = gallery.galleryimageholder_set.all().select_related(
        'galleryimage',
        'gallery'
    ).exclude(
        galleryimage = galleryimage
    )[:24]

    image_list = []

    for h in holder_set:

        image_obj = {
            'uuid': h.galleryimage.uuid,
            'slug': h.gallery.slug,
            'src': h.galleryimage.grid_src()
        }

        image_list.append(image_obj)

    context = {
        'gallery': gallery,
        'image': galleryimage,
        'image_list': image_list
    }

    return render(request, 'website/galleryimage_detail.html', context)


    return HttpResponse(uuid)

def contact_us_view(request):

    if request.method == 'POST':

        form = ContactRequestForm(request.POST)

        if form.is_valid():

            name = request.POST['name'].strip()
            message = request.POST['message'].strip()
            date = request.POST['date'].strip()

            # check for SPAM
            spam = form_spam(
                name = name,
                message = message,
                date_string = date
            )

            if not spam['is_spam']:

                # save the request
                contactrequest = form.save()

                # consider not sending the notice
                # these can be checked in the APP every morning.
                send_contactrequest_email(
                    contactrequest.id
                )

                # redirect with a success message
                return HttpResponseRedirect(
                    reverse('website:contact') + '?m=' + str(contactrequest.uuid) )

            # if it is SPAM, redirect to contact form
            else:
                return HttpResponseRedirect(reverse('website:contact') )


        else:
            return HttpResponseRedirect(reverse('website:contact') )

    else:

        if request.GET.get('m'):
            message_id = request.GET.get('m')
        else:
            message_id = ''

        date = datetime.datetime.now()
        date_text = date.strftime('%Y:%m:%d:%H:%M:%S:%f')

        context = {
            'message_id': message_id,
            'date_text': date_text
        }

        return render(request, 'website/contact_us.html', context)

def donate_view(request):

    if request.GET.get('e'):
        error_code = request.GET.get('e')
    else:
        error_code = ''

    # set the stripe key
    if settings.DEBUG:
        stripe_pk = settings.STRIPE_PUBLISHABLE_KEY_TEST
    else:
        stripe_pk = settings.STRIPE_PUBLISHABLE_KEY

    context = {
        'stripe_pk': stripe_pk,
        'error_code': error_code,
        'show_stripe': True
    }

    return render(request, 'website/donation_charge.html' ,context)

def history_view(request):

    return render(request, 'website/history.html')

def pay_dues_view(request):

    # if they entered a search field, find it
    if request.method == 'POST':

        search_string = request.POST['dues_search'].strip()

        # set the current year
        current_year = int(datetime.datetime.now().year)

        if len(search_string) > 2:

            profile_search = Profile.objects.filter(
                last_name__istartswith = search_string
            )

            context = {
                'year': datetime.datetime.now().year,
                'dues_search': profile_search
            }

            return render(request, 'website/pay_dues.html',context)

        # if the search string is less than 3 characters (aka. blank)
        else:
            return HttpResponseRedirect(reverse('website:pay-dues') + '?e=char')

    else:

        context = {
            'year': datetime.datetime.now().year
        }


        return render(request, 'website/pay_dues.html',context)

def pay_dues_confirm_view(request,uuid):

    # get the profile
    profile = get_object_or_404(Profile,uuid=uuid)

    context = {
        'profile': profile
    }

    return render(request, 'website/pay_dues_confirm.html',context)

def pay_dues_charge_view(request,uuid):

    # get the profile
    profile = get_object_or_404(Profile,uuid=uuid)

    # set the stripe key
    if settings.DEBUG:
        stripe_pk = settings.STRIPE_PUBLISHABLE_KEY_TEST
    else:
        stripe_pk = settings.STRIPE_PUBLISHABLE_KEY

    if request.GET.get('e'):
        error_code = request.GET.get('e')
    else:
        error_code = None

    if profile.dues_paid():
        dues_paid = 'true'
        payment_amount = 0
    else:
        dues_paid = ''
        payment_amount = 50

    context = {
        'profile': profile,
        'stripe_pk': stripe_pk,
        'error_code': error_code,
        'show_stripe': True,
        'dues_paid': dues_paid,
        'payment_amount': payment_amount
    }

    return render(request, 'website/pay_dues_charge.html',context)

def charge_success_view(request,type,id):

    # set some default information
    charge_heading = 'Paid!'
    charge_subheading = 'Check your email for a paid receipt.'

    # if type == dues
    # for now, they can only pay one year at a time
    if type == 'dues':

        # get and add the DuesPayment
        payment = get_object_or_404(DuesPayment,uuid=id)

        # set current year
        current_year = int(datetime.datetime.now().year)

        # set some payment information
        name = payment.name
        email = create_safe_email(payment.email)
        date = payment.date
        total = payment.amount + payment.donation

        # set a blank lineitem array
        lineitem_array = []

        if payment.amount:

            dues_obj = {
                'name': str(current_year) + ' Annual Dues',
                'amount': str(payment.amount)
            }

            lineitem_array.append(dues_obj)

        if payment.donation:

            donation_obj = {
                'name': str(current_year) + ' Donation',
                'amount': str(payment.donation)
            }

            lineitem_array.append(donation_obj)

    elif type == 'donation':

        # get the DonationPayment
        donation = get_object_or_404(DonationPayment,uuid=id)

        # create new heading info
        charge_heading = 'Thank You!'
        charge_subheading = 'Your donation is greatly appreciated.<br>Please check your email for a receipt.'

        # set current year
        # should this be a util?
        current_year = int(datetime.datetime.now().year)

        # set some payment information
        name = donation.name
        email = create_safe_email(donation.email)
        date = donation.date
        total = donation.amount

        lineitem_array = [
            {
                'name': 'GKAA Donation (' + str(current_year) + ')',
                'amount': donation.amount
            }
        ]

    else:
        name = ''
        email = ''
        date = ''
        total = ''
        lineitem_array = ''


    context = {
        'name': name,
        'email': email,
        'date': date,
        'total': total,
        'lineitem_array': lineitem_array,
        'charge_heading': charge_heading,
        'charge_subheading': charge_subheading
    }


    return render(request, 'website/charge_success.html', context)

def roster_list(request):

    # if POST, redirect back to the page with search term
    if request.method == 'POST':

        search = request.POST['q']

        return HttpResponseRedirect(
            reverse('website:roster') + '?q=' + search)

    # if a search term was entered, look for the term
    # set a safe return number. start with 24
    elif request.GET.get('q'):

        q = request.GET.get('q')

        profile_set = Profile.objects.filter(
            Q(first_name__istartswith = q)|
            Q(last_name__istartswith = q)|
            Q(nickname__icontains = q)|
            Q(aka__icontains = q)
        )[:24]

        # if this returns no results, shorten the request
        if not profile_set:

            # cut the search in half
            splice = int(len(q)/2)

            q = q[:splice]

            profile_set = Profile.objects.filter(
                Q(first_name__istartswith = q)|
                Q(last_name__istartswith = q)|
                Q(nickname__icontains = q)|
                Q(aka__icontains = q)
            )[:24]


        type = 'search'
        filter = None


    # if a ProfileFilter was clicked
    else:

        type = 'filter'

        # try to get the ProfileFilter
        try:

            filter = ProfileFilter.objects.get(
                slug = request.GET.get('f').strip()
            )

        # if the ProfileFilter does not exist, default to the Original Team
        except:

            filter = ProfileFilter.objects.get(slug='original')


        # get and the filtered sets by year and last name
        profile_set = filter.profilefilterholder_set.all().order_by(
            'year','profile__last_name'
        ).select_related(
            'profile'
        )

        # if we are using the ProfileFilterHolder date and no date exists
        # do not include in the list
        if filter.use_filter_date:
            profile_set = profile_set.exclude(
                year = 0
            )


    # simple pagination and default buttons
    paginate_by = 24
    prev_button = 0
    next_button = 0
    profile_count = profile_set.count()

    if profile_count > paginate_by:

        # if a page was added and it's greater than 1
        if request.GET.get('p') and int(request.GET.get('p')) > 1:

            page = int(request.GET.get('p'))

            # I do not need to add one because it is zero based
            start_record = (page-1)*paginate_by

            end_record = start_record + paginate_by

            # there will always be a back button because we are
            # on a page greater than 1
            prev_button = page - 1
            next_button = page + 1

        # if no page passed in, we are on page 1
        else:
            page = 1
            start_record = 0
            end_record = paginate_by
            next_button = 2

        # if the end record is greater than the profile_count
        # reset it to the profile_count and remove the next_button
        if end_record >= profile_count:
            end_record = profile_count
            next_button = 0

        # splice the profile_set
        profile_set = profile_set[start_record:end_record]

    # build the next and prev button strings
    next_button_string = ''
    prev_button_string = ''

    if filter:
        next_button_string += '?f=' + filter.slug + '&p=' + str(next_button)
        prev_button_string += '?f=' + filter.slug + '&p=' + str(prev_button)
    else:
        next_button_string += '?p=' + str(next_button)
        prev_button_string += '?p=' + str(prev_button)

    # convert the profile_list to an array
    profile_array = []
    num_profiles = 0

    # I am using record here instead of profile because
    # it might be a ProfileFilter holder vs a Profile
    for record in profile_set:

        # increment the number of profiles
        num_profiles += 1

        # I have to set the date shown before I call the record a profile
        if type == 'filter' and record.profilefilter.use_filter_date:

            # use the date shown in the ProfileFilterHolder
            teamdate_string = record.year
            teamdate_title = record.profilefilter.roster_card_title

        # if filter, but we do not want to use the filter date
        elif type == 'filter':

            # use the date shown in the ProfileFilterHolder
            teamdate_string = record.profile.teamdate_string
            teamdate_title = ''

        # if not filter,  use the profile.teamdate_string
        else:
            teamdate_string = record.teamdate_string
            teamdate_title = ''

        # Set the Profile

        # if filter it is teh profilefilterholder.profile
        if type == 'filter':
            roster_title = record.profilefilter.name
            profile = record.profile

        # if it is not a filter, it is the record itself
        else:
            roster_title = ''
            profile = record

        # if Honorary, prepend the date
        # this is crappy code
        if type == 'search' and profile.type == 3 and teamdate_string:
            teamdate_string = 'Honorary GK: ' + str(teamdate_string)

        elif type == 'search' and profile.type == 3 and not teamdate_string:
            teamdate_string = 'Honorary GK'

        if profile.home_city and profile.home_state:
            home_origin = profile.home_city + ', ' + profile.home_state
        elif profile.hometown:
            home_origin = profile.hometown
        else:
            home_origin = ''

        if profile.deceased_date:
            deceased_date = profile.deceased_date.strftime('%b %-d, %Y')
        elif profile.deceased_year:
            deceased_date = profile.deceased_year
        else:
            deceased_date = ''

        profile_obj = {
            'name': profile.last_name + ', ' + profile.first_name,
            'home_origin': home_origin,
            'deceased_date': deceased_date,
            'profile_code': profile.url_code,
            'roster_image': profile.roster_image_src(),
            'teamdate_title': teamdate_title,
            'teamdate_string': teamdate_string,
            'filter_text': 'filter_text',
            'show_link': profile.show_link
        }

        profile_array.append(profile_obj)

    # create a filter set
    filter_set = ProfileFilter.objects.all()

    # temp fix
    try:
        roster_title = roster_title
    except:
        roster_title = ''

    # is there a search query?
    if request.GET.get('q'):
        search = request.GET.get('q')
    else:
        search = ''


    context = {
        'profile_array': profile_array,
        'num_profiles': num_profiles,
        'filter_set': filter_set,
        'roster_title': roster_title,
        'prev_button': prev_button,
        'prev_button_string': prev_button_string,
        'next_button': next_button,
        'next_button_string': next_button_string,
        'search': search
    }



    page = 'website/roster_list_two.html'

    return render(request, page, context)

def roster_menu(request):

    # if POST, redirect back to the page with search term
    if request.method == 'POST':

        search = request.POST['q']

        return HttpResponseRedirect(reverse('website:roster') + '?q=' + search)

    else:

        filter_list = []

        filter_set = ProfileFilter.objects.all()

        for filter in filter_set:
            filter_list.append(filter)

        context = {
            'filter_list': filter_list
        }

        return render(request, 'website/roster_menu.html', context)

def roster_list_old(request):

    # set a paginate default
    paginate = True

    # if this is a post, redirect back to the page with search term
    if request.method == 'POST':
        search = request.POST['search']
        return HttpResponseRedirect(reverse('website:roster') + '?q=' + search)

    # if there is a search term (q)
    elif request.GET.get('q'):

        search = request.GET.get('q').strip()

        # save the search so we can see what people are looking for
        savedsearch = SavedSearch(term=search)
        savedsearch.save()

        # if they entered a number, they are searching by year
        if search.isnumeric():
            year = int(search)

            if year == 0:
                year = 1959

            profile_list = Profile.objects.filter(
                teamdate__start_year__lte = year,
                teamdate__end_year__gte = year,
                do_not_display = False,
                type = 1 # alumnus
                )

        # if they typed in anything other than a number
        # they are looking for a name
        else:

            q = search

            profile_list = Profile.objects.filter(
                Q(first_name__icontains = q)|
                Q(last_name__icontains = q)|
                Q(nickname__icontains = q)|
                Q(aka__icontains = q)
            )

        type = 'profile'

        # set the query string
        query_string = '?q=' + search

    # if this is a filtered search
    elif request.GET.get('f'):

        filter = request.GET.get('f').strip()

        if filter == 'aoy':
            filter_type = 2
            filter_prefix = 'Aviator/Year: '

        elif filter == 'coy':
            filter_type = 4
            filter_prefix = 'Civilian/Year: '

        elif filter == 'goy':
            filter_type = 1
            filter_prefix = 'Golden Knight/Year: '

        elif filter == 'poy':
            filter_type = 3
            filter_prefix = 'Photographer/Year: '

        elif filter == 'hon':
            filter_type = 5
            filter_prefix = 'Honorary GK: '

        elif filter == 'usapt':
            filter_type = 6
            filter_prefix = 'Original USAPT: '

        # if url string (f) exists, but does not match any of the above
        # default to the original team
        else:
            filter_type = 6
            filter_prefix = 'Original USAPT: '

        profile_list = OfTheYear.objects.select_related('profile').filter(
            type = filter_type
        ).order_by('year')

        # if filter type is Original Team, order by last name
        # and do not paginate
        if filter_type == 6:

            profile_list = profile_list.order_by('profile__last_name')
            paginate = False

        type = 'filter'
        search = None
        query_string = '?f=' + filter

    # if this is not a post and there is no search term
    # show all of them
    else:
        profile_list = Profile.objects.filter(
            do_not_display = False,
            type = 1 # alumnus
            ).order_by('last_name')

        type = 'profile'
        search = None
        query_string = None


    # START PAGINATION

    # set the full profile list
    full_profile_list = profile_list

    # set the paginate by
    if paginate:
        paginate_by = 12
    else:
        paginate_by = full_profile_list.count()

    # turn off the paginate if less than paginate by
    if full_profile_list.count() < paginate_by:
        paginate = False

    # set the number of pages
    num_pages = math.ceil(full_profile_list.count() / paginate_by)

    # was a page passed in from the URL
    if request.GET.get('page') and request.GET.get('page').isnumeric():
        page = int(request.GET.get('page'))
    else:
        page = 1

    # do not let them exceed the total number of pages
    if page > num_pages:
        page = num_pages

    # set the start and end record
    # I do NOT add 1 because it is zero based
    start_record = ((page-1) * paginate_by)
    end_record = start_record + paginate_by

    # the start record cannot be less than 0
    if start_record < 0:
        start_record = 1

    # slice the profile list
    profile_list = full_profile_list[start_record:end_record]

    # is there a next_page
    if page < num_pages:
        next_page = page + 1
    else:
        next_page = None

    # is there a previous page
    if page > 2:
        prev_page = page - 1
    else:
        prev_page = None

    # create a mobile pagination array
    # I will build a bigger one later
    pagination_array = []

    if page > 1 and page < num_pages:
        pagination_start = page - 1
    elif page == num_pages and page < num_pages:
        pagination_start = page - 2
    else:
        pagination_start = 1

    # keep the pagination length to 3 for mobile
    if num_pages > 3:
        pagination_length = 3
    else:
        pagination_length = num_pages

    while len(pagination_array) < pagination_length:

        number = pagination_start

        if number == page:
            active = 'active'
        else:
            active = ''

        # set the query string
        if query_string:
            page_query_string = query_string + '&page=' + str(number)
        else:
            page_query_string = '?page=' + str(number)

        page_obj = {
            'number': number,
            'active': active,
            'query_string': page_query_string
        }

        pagination_array.append(page_obj)

        # advance the pagination number
        pagination_start += 1

    # convert the profile_list to an array
    profile_array = []

    for record in profile_list:

        # if this is a filtered search, set the profile
        # and the filter text
        if type == 'filter':
            profile = record.profile

            if filter_type <= 5:
                filter_text = filter_prefix + ' ' + str(record.year)
            elif filter_type == 6:
                filter_text = filter_prefix + profile.d_number
        else:
            profile = record
            filter_text = None

        # deceased date
        if profile.show_deceased_date:
            deceased_date = profile.show_deceased_date
        else:
            deceased_date = None

        # home origin
        if profile.show_home_origin:
            home_origin = profile.show_home_origin
        else:
            home_origin = None

        # profile link
        if profile.show_profile_link():
            profile_link = True
        else:
            profile_link = False

        # set the profile dates array
        teamdate_string = ''

        for d, date in enumerate(profile.teamdate_set.all()):

            # add the start year
            teamdate_string += str(date.start_year)

            # add the end year if there is one
            if date.end_year:
                teamdate_string += '-' + str(date.end_year)

            # if this is not the last record, add a comma
            if d != profile.teamdate_set.count()-1:
                teamdate_string += ','


        # create a roster image
        if profile.has_image():

            image = profile.has_image()

            imgix = (
                'https://gkaa.imgix.net/images/profiles/' + image.name +
                '?fit=fill&fill=solid&fill-color=ffffff&w=200&h=260'
            )

            imgix = (
                'https://gkaa.imgix.net/images/profiles/' + image.name +
                '?fit=crop&w=200&h=260'
            )

            roster_src = imgix


        elif profile.has_thumbnail and profile.thumbnail_checked:

            roster_src = (
                'https://gkaa-assets.s3.us-east-2.amazonaws.com/media/roster-card/' +
                str(profile.member_id) +
                '-detail-hero.jpg'
            )

        else:

            roster_src = (
                'https://gkaa-assets.s3.amazonaws.com/static/website/images/roster/auls_head.jpg'
            )


        profile_obj = {
            'name': profile.last_name + ', ' + profile.first_name,
            'deceased_date': deceased_date,
            'profile_code': profile.url_code,
            'home_origin': home_origin,
            'profile_link': profile_link,
            'roster_image': roster_src,
            'teamdate_string': teamdate_string,
            'filter_text': filter_text
        }

        profile_array.append(profile_obj)

    if profile_list.count() == 1:
        results_text = 'We found 1 result for: '
    else:
        results_text = (
            'We found ' +
            str(full_profile_list.count()) +
            ' results for: '
        )

    context = {
        'profile_array': profile_array,
        'paginate': paginate,
        'pagination_array': pagination_array,
        'num_pages': num_pages,
        'next_page': next_page,
        'prev_page': prev_page,
        'search': search,
        'results_text': results_text
    }

    try:
        page = 'website/roster_list_' + request.GET.get('p') + '.html'
        return render(request, page, context)
    except:
        page = 'website/roster_list.html'
        return render(request, page, context)

def profile_view(request, url_code):

    # get the current user so we can show the edit button if they are logged in
    current_user = request.user

    # get the profile
    profile = get_object_or_404(Profile, url_code=url_code)

    # set a blank more knights array to fill if they have team dates
    more_knights_array = []

    # if they have team dates
    # we can fill the more_knights_array with other teamates from that era
    '''
    if profile.teamdate_set.count():
        profile_start_year = profile.start_year() + 1

        # if they have an end year, use it
        if profile.end_year():
            profile_end_year = profile.end_year() - 1

        # else if they do not have an end year
        # add 5 years to the start date
        else:
            profile_end_year = profile_start_year + 5

        # find people whose:
        # start year is at least one year before you left
        # end year is at least one year after you started
        more_knights_list = TeamDate.objects.filter(
            end_year__gte=profile_start_year,
            start_year__lte=profile_end_year,
            profile__type=1).exclude(profile=profile)

        # I am not 100% sure why we do this
        if len(more_knights_list) < 30:
            random_number = randrange(2,6)
        else:
            random_number = randrange(2,8)

        more_knights_get_number = round(more_knights_list.count() / random_number)

        for k in more_knights_list:

            knight = {

                'profile_id': k.profile.id,
                'short_code': k.profile.short_code,
                'url_code': k.profile.url_code,
                'first_name': k.profile.first_name,
                'last_name': k.profile.last_name,
                'start_year': k.start_year,
                'end_year': k.end_year
            }

            more_knights_array.append(knight)

        # shuffle the array
        shuffle(more_knights_array)
    '''

    # ProfileImage(s)
    profileimage_list = profile.profileimage_set.filter(
        profile_image=False,
        date_delete__isnull=True
        )

    if profileimage_list.count() > 4:
        show_more_images = True
    else:
        show_more_images = False

    # show the edit profile button?
    if current_user == profile.user:
        show_edit_link = True
    else:
        show_edit_link = False

    # is there a search term passed in from the roster
    if request.GET.get('q'):
        search = request.GET.get('q')
    else:
        search = ''

    if len(profile.comments) > 300:
        profile_comments = profile.comments[:300]
        extended_comments = True
    else:
        profile_comments = profile.comments
        extended_comments = False

    context = {
        'profile': profile,
        'profile_comments': profile_comments,
        'extended_comments': extended_comments,
        'more_knights': more_knights_array[0:12], # just show 12 of them
        'profileimage_list': profileimage_list[:4],
        'show_edit_link': show_edit_link,
        'show_more_images': show_more_images,
        'search': search
    }

    return render(request, 'website/profile.html', context)

def extended_profile_view(request, url_code):

    # get the Profile
    profile = get_object_or_404(Profile, url_code=url_code)

    # show the edit profile button?
    if request.user == profile.user:
        show_edit_link = True
    else:
        show_edit_link = False

    # ProfileImage(s)
    profileimage_list = profile.profileimage_set.filter(
        date_delete__isnull=True
        )

    context = {
        'profile': profile,
        'show_edit_link': show_edit_link,
        'profileimage_list': profileimage_list,
        'entry_list': profile.entry_list()
    }

    return render(request, 'website/profile_extended.html', context)

# OLD Reunion Registration
# OLD Reunion Registration

def registration_view(request):

    if request.GET.get('e'):
        error = request.GET.get('e')
    else:
        error = ''

    context = {
        'year': 2019,
        'error': error
    }

    return render(request, 'website/register.html', context)


# test validators
def registration_start_view(request):

    if request.method == 'POST':

        # set the email address
        email_address = request.POST['email_address'].strip()

        # see if there is a regisration using this email address and
        # stripe_charge_id is not null (they have paid)
        registration = Registration.objects.filter(
        email_address=email_address
            ).exclude(stripe_charge_id='')

        # if there is an existing registration
        # redirect back to the register page with a duplicate error
        if registration:
            return HttpResponseRedirect(reverse('website:registration') + '?e=duplicate')

        # if there is not one, setup a new registration
        else:

            name = request.POST['name']
            type = request.POST['attendee_type']

            # split the name up into a list separated by spaces
            name_list = name.strip().split(' ')

            # get the length of the list
            num_names = len(name_list)

            # set the last one as the last_name
            # it's zero based, so I need to minus one
            last_name = name_list[num_names-1].strip()

            # if there is only one name, it is the first name
            if num_names == 1:

                first_name = name_list[0]

            # else if there is more than one
            # piece it back together
            else:

                # set a base first name
                first_name = ''

                # for each name in the list except the last one
                for n in name_list[:num_names-1]:

                    first_name += n + ' '

            # clean up the first name
            first_name = first_name.strip()

            # validate the email address
            try:
                validate_email(email_address)
            except ValidationError as e:
                return HttpResponseRedirect(reverse('website:registration') + '?e=email')
            else:

                registration = Registration(
                    name=name,
                    first_name = first_name,
                    last_name = last_name,
                    email_address=email_address,
                    type=type
                    )

                registration.save()

                return HttpResponseRedirect(reverse('website:registration-update',
                    args=(registration.uuid,)))

    # if this is not a POST, return a blank page
    else:

        return HttpResponse('')

# view where enter numbers for each night
def registration_update_view(request,uuid):

    registration = get_object_or_404(Registration,uuid=uuid)

    if registration.type == 2: # current team member
        saturday_price = 50
    else:
        saturday_price = 100

    context = {
        'registration': registration,
        'saturday_price': saturday_price
    }

    return render(request, 'website/register_update.html', context)


def registration_update_form_view(request,uuid):

    registration = get_object_or_404(Registration,uuid=uuid)

    if request.method == 'POST':
        num_party_field = request.POST['num_party']

        if num_party_field.isdigit():
            num_party = int(num_party_field)
        else:
            num_party = 0

        num_event_field = request.POST['num_event']

        if num_event_field.isdigit():
            num_event = int(num_event_field)
        else:
            num_event = 0

        # sponsor info
        num_sponsor_field = request.POST['num_sponsor']
        if num_sponsor_field.isdigit():
            num_sponsor = int(num_sponsor_field)
            if num_sponsor > 0:
                registration.num_sponsor = num_sponsor
                registration.save()


        # enter the Fiday Night Party Attendees
        p = 0
        while p < num_party:

            # enter the registrant as the first attendee
            if p == 0:
                name = registration.name
            else:
                name = ''

            attendee = Attendee(registration=registration, name=name,event=1)
            attendee.save()
            p += 1


        # enter the Saturday Night Event attendees
        e = 0
        while e < num_event:

            if e == 0:
                name = registration.name
            else:
                name = ''

            attendee = Attendee(registration=registration, name=name,event=2)
            attendee.save()
            e += 1

        return HttpResponseRedirect(reverse('website:registration-attendees', args=(registration.uuid,)))

def registration_update_veggie_view(request,uuid):

    registration = get_object_or_404(Registration,uuid=uuid)

    if request.method == 'POST':
        num_veggie_field = request.POST['num_veggie']

        if num_veggie_field.isdigit():
            num_veggie = int(num_veggie_field)
            registration.num_veggie = num_veggie
            registration.save()

        return HttpResponseRedirect(reverse('website:registration-checkout', args=(registration.uuid,)))

    else:
        return HttpResponse('')


def registration_checkout_view(request,uuid):

    registration = get_object_or_404(Registration,uuid=uuid)

    # they cannot be on this page if they have already paid
    if registration.stripe_charge_id != '':
        return HttpResponseRedirect(reverse('website:registration-success', args=(registration.uuid,)))


    friday_night = registration.attendee_set.filter(event=1)
    saturday_night = registration.attendee_set.filter(event=2)
    leftover_friday = friday_night.count() - 2
    leftover_saturday = saturday_night.count() - 2

    # attendee lists
    friday_attendees = registration.attendee_set.filter(event=1)
    saturday_attendees = registration.attendee_set.filter(event=2)

    # calculate Friday Night:
    if registration.type < 3:

        if friday_night.count() > 2:
            free_friday_num = 2
            paid_friday_num = leftover_friday
            paid_friday_total = paid_friday_num * 35
        else:
            free_friday_num = friday_night.count()
            paid_friday_num = 0
            paid_friday_total = 0
    else:
        free_friday_num = 0
        paid_friday_num = friday_night.count()
        paid_friday_total = friday_night.count() * 35

    # Lastly, if Friday Night Total ends up being negative, make it zero
    if paid_friday_total < 0:
        paid_friday_total = 0


    # do they owe dues?
    if registration.type == 1 and registration.dues_paid() == False:
        dues_owed = 50
    else:
        dues_owed = 0


    # calculate Saturday Night
    if registration.type == 2:

        # if there are more than 2
        if saturday_night.count() > 2:

            half_saturday_num = 2
            full_saturday_num = leftover_saturday

            half_saturday_total = 100
            full_saturday_total = leftover_saturday * 100

        # if there are only 2, they are $50 each
        else:

            half_saturday_num = saturday_night.count()
            full_saturday_num = 0

            half_saturday_total = saturday_night.count() * 50
            full_saturday_total = 0

    # if they are not current team members, they are $100 each
    else:

        half_saturday_num = 0
        full_saturday_num = saturday_night.count()

        half_saturday_total = 0
        full_saturday_total = saturday_night.count() * 100


    if saturday_night.count() > 9:
        table_fee = 100
    else:
        table_fee = 0

    sponsor_total = registration.num_sponsor * 50

    checkout_total = (
        dues_owed +
        paid_friday_total +
        half_saturday_total +
        full_saturday_total +
        sponsor_total +
        table_fee
        )


    # set the type view
    if registration.type == 1:
        type_view = 'GK Alumnus/Alumnae'
    elif registration.type == 2:
        type_view = 'Current Team Member'
    elif registration.type == 3:
        type_view = 'Honorary GK'
    else:
        type_view = 'Friend of the Team'

    # just so we do not have to recalculate for stripe, create a registration_total
    registration.total = checkout_total
    registration.save()


    # if they were redirected back here for charge error
    if request.GET.get('e'):
        charge_error = request.GET.get('e')
    else:
        charge_error = ''

    # set the stripe key
    if settings.DEBUG:
        stripe_pk = settings.STRIPE_PUBLISHABLE_KEY_TEST
    else:
        stripe_pk = settings.STRIPE_PUBLISHABLE_KEY

    context = {
        'registration': registration,
        'dues_owed': dues_owed,

        'num_friday': friday_night.count(),
        'free_friday_num': free_friday_num,
        'paid_friday_num': paid_friday_num,
        'paid_friday_total': paid_friday_total,

        'num_saturday': saturday_night.count(),
        'half_saturday_num': half_saturday_num,
        'full_saturday_num': full_saturday_num,
        'half_saturday_total': half_saturday_total,
        'full_saturday_total': full_saturday_total,

        'sponsor_total': sponsor_total,
        'table_fee': table_fee,
        'checkout_total': checkout_total,
        'type_view': type_view,
        'stripe_pk': stripe_pk,
        'charge_error': charge_error,
        'friday_attendees': friday_attendees,
        'saturday_attendees': saturday_attendees,
        'debug': settings.DEBUG
    }

    return render(request, 'website/register_checkout.html', context)


def registration_attendees_view(request,uuid):

    registration = get_object_or_404(Registration,uuid=uuid)

    # they cannot be on this page if they have already paid
    if registration.stripe_charge_id != '':
        return HttpResponseRedirect(reverse('website:registration-success', args=(registration.uuid,)))

    # attendee lists
    friday_attendees = registration.attendee_set.filter(event=1)
    saturday_attendees = registration.attendee_set.filter(event=2)


    context = {
        'registration': registration,
        'friday_attendees': friday_attendees,
        'saturday_attendees': saturday_attendees
    }

    return render(request, 'website/register_attendees.html', context)


def registration_charge_view(request,uuid):

    if request.method == 'POST':

        # set the stripe key
        if settings.DEBUG:
            stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
        else:
            stripe.api_key = settings.STRIPE_SECRET_KEY

        stripe_token = request.POST['stripeToken']

        registration = Registration.objects.get(uuid=uuid)
        receipt_email = registration.email_address
        charge_amount = int(registration.total * 100)

        try:
            charge = stripe.Charge.create(amount=charge_amount,currency="usd",source=stripe_token,description="60th GKAA Reunion",receipt_email=receipt_email)

            registration.stripe_charge_id = charge.id
            registration.save()

            # if they are alumni and are also paying dues
            if registration.type == 1 and registration.dues_paid() == False:
                duespayment = DuesPayment(name=registration.name, email=registration.email_address,amount=50,stripe_charge_id=charge.id)
                duespayment.save()

            # create sponsorship records
            if registration.num_sponsor > 0:

                s = 0

                while s < registration.num_sponsor:
                    sponsorship = Sponsorship(registration=registration)
                    sponsorship.save()

                    s += 1


            return HttpResponseRedirect(reverse('website:registration-success', args=(registration.uuid,)))

        except stripe.error.CardError as e:
            err = e.json_body['error']

            return HttpResponseRedirect(reverse('website:registration-checkout', args=(registration.uuid,)) + '?e=' + err.get('code') )

    else:
        return HttpResponse('')


def registration_success_view(request,uuid):

    registration = get_object_or_404(Registration,uuid=uuid)

    if registration.stripe_charge_id != '':

        context = {
            'registration': registration
        }

        return render(request, 'website/registration_success.html', context)

    else:
        return HttpResponseRedirect(reverse('website:registration-checkout', args=(registration.uuid,)))


# hard coded reunion (temp hard coded)
def reunion_info_view(request):

    context = {
        'year': 2019
    }

    return render(request, 'website/reunion.html', context)

# ACTIONS ACTIONS
def registration_attendee_remove_view(request,uuid):

    # get the attendee
    attendee = Attendee.objects.get(uuid=uuid)

    # get the registration uuid
    registration = attendee.registration

    # delete the attendee
    attendee.delete()

    # go back to registration page
    return HttpResponseRedirect(reverse('website:registration-attendees', args=(registration.uuid,)))


def registration_attendee_add_view(request,uuid,event):

    registration = Registration.objects.get(uuid=uuid)

    attendee = Attendee(registration=registration, event=event)
    attendee.save()

    # go back to registration page
    return HttpResponseRedirect(reverse('website:registration-attendees', args=(registration.uuid,)))


def action_confirm_registration(request,uuid):

    registration = get_object_or_404(Registration,uuid=uuid)

    # if they are alumnus or current team member
    # and there are no more than two Friday night guests
    # and there are no saturday night guests
    if (
        registration.type < 3 and
        registration.num_friday_attendees() < 3 and not
        registration.num_saturday_attendees()
        ):

        registration.stripe_charge_id = 'registration-confirmed'
        registration.save()

        return HttpResponseRedirect(
            reverse('website:registration-success', args=(registration.uuid,)))

    # else if they do not meet the above criteria
    # send them to a blank page
    else:

        return HttpResponseRedirect(
            reverse('website:registration-checkout', args=(registration.uuid,)))

# AJAX Calls
def registration_update_attendees_view(request):

    if request.is_ajax():

        attendee_string = request.POST['attendees_string']
        attendee_array = json.loads(attendee_string)

        for a in attendee_array:
            attendee = Attendee.objects.get(uuid=a['attendee_id'])
            attendee.name = a['attendee_name']
            attendee.save()

        return JsonResponse({'success':'success'})
    else:
        return HttpResponse('is HTTP')
