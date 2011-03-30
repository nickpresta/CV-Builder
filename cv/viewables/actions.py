# -*- coding: utf-8 -*-
import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template
from django.template.loader import get_template
from django.template import Context
import ho.pisa as pisa
import cStringIO as StringIO

from cv.forms import *
from cv.models import *
from common import *

def write_pdf(template_src, context_dict, request):
    """ This writes the PDF using pisa and makes the PDF available for download """
    template = get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context)
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)
    if not pdf.err:
        response = HttpResponse(mimetype='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=cv_%s_%s.pdf' % (
                request.user.username, datetime.datetime.now().strftime("%Y-%m-%d"))
        response.write(result.getvalue())
        return response
    return HttpResponse("Bad stuff happened. Oops!")

@login_required
def export_download(request, download):
    """ Return the response, either a PDF, or some error text """

    faculty = getFaculty(request.user)

    # We need to build up the information for the export
    out = {}
    out['user'] = request.user

    doeData = DoETable.objects.filter(Faculty_ID=faculty).order_by('Year')
    out['doe'] = doeData

    out['summary'] = get_table_or_dict(SummaryTable, Faculty_ID=faculty)

    out['faculty_info'] = get_table_or_dict(FacultyTable, Faculty_ID=faculty.Faculty_ID)
    out['faculty_info'].Department = out['faculty_info'].Department.split(",")

    out['degree_info'] = AccredTable.objects.filter(Faculty_ID=faculty).order_by("Date")
    out['honors_info'] = HonorTable.objects.filter(Faculty_ID=faculty)
    out['position_held_info'] = PositionHeldTable.objects.filter(
            Faculty_ID=faculty).order_by("StartDate")
    out['position_prior_info'] = PositionPriorTable.objects.filter(
            Faculty_ID=faculty).order_by("StartDate")
    out['position_elsewhere_info'] = PositionElsewhereTable.objects.filter(
            Faculty_ID=faculty).order_by("StartDate")

    if download:
        return write_pdf('export.html', out, request)
    else:
        return direct_to_template(request, 'export.html', out)


# Helper Func
def get_table_or_dict(table, *args, **kwargs):
    table = table._default_manager.all()
    try:
        data = table.get(*args, **kwargs)
        return data
    except table.model.DoesNotExist:
        return {}

