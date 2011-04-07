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
    try:
        pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)
    except RuntimeError:
        # Is is a runtime error because the maximum recursion depth has been
        # exceeded. Raising the recursion limit is a bad idea in this case
        # This happens when the DOM of the document is seriously nested or
        # otherwise screwed up. This shouldn't normally happen, but happened in
        # our stress testing
        return HttpResponse("Your document is too long to convert to a PDF. "
                            "Please try reducing the content in the free-form "
                            "fields.")
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

    # We need to build up the information for the export
    out = {}
    out['user'] = request.user

    doeData = DistributionOfEffort.objects.filter(user=request.user).order_by('year')
    out['doe'] = doeData

    out['summary'] = get_table_or_dict(Summary, user=request.user)

    out['faculty_info'] = request.user.get_profile()
    out['faculty_info'].departments = out['faculty_info'].departments.split(",")

    out['degree_info'] = Accred.objects.filter(user=request.user).order_by("date")
    out['honors_info'] = Honor.objects.filter(user=request.user)
    out['position_held_info'] = PositionHeld.objects.filter(
            user=request.user).order_by("start_date")
    out['position_prior_info'] = PositionPriorTable.objects.filter(
            user=request.user).order_by("StartDate")
    out['position_elsewhere_info'] = PositionElsewhereTable.objects.filter(
            user=request.user).order_by("StartDate")

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

