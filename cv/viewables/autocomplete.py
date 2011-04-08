# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template
from django.template.loader import get_template
from django.template import Context
from django.core import serializers

from cv.models import *
from common import *

import json

@login_required
def autocomplete(request):
    # This isn't used yet!
    table = request.GET['table']
    # it should be "departments":
    result = UserProfile.objects.filter(departments__icontains = request.GET['term']).values_list("departments", flat=True).distinct().order_by("departments")
    #result = DepartmentChoice.objects.filter(name__icontains = request.GET['term']).values_list("name", flat=True).distinct().order_by("name")
    rv = []
    for item in result:
        rv += item.split(',')

    return HttpResponse(repr(map(str,rv)).replace("'",'"'))
