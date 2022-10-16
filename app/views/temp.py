from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.db.models import Q

import datetime

from app.decorators import view_login_required, edit_login_required

from app.models import Event, EventRegistration


@view_login_required
def temp_index(request):

    event_list = Event.objects.all()

    context = {
        'event_list': event_list
    }

    return render(request, 'app/temp/event_list.html', context)

    return HttpResponse('Temp Index')
