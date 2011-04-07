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
    user = request.user
    out = {}
    out['user'] = user

    doeData = DistributionOfEffort.objects.filter(user=user).order_by('year')
    out['doe'] = doeData

    out['summary'] = get_table_or_dict(Summary, user=user)

    out['faculty_info'] = user.get_profile()
    try:
        out['faculty_info'].departments = out['faculty_info'].departments.split(",")
    except AttributeError:
        # No departments yet
        out['faculty_info'].departments = []

    out['degree_info'] = Accred.objects.filter(user=user).order_by("date")
    out['honors_info'] = Honor.objects.filter(user=user)
    out['position_held_info'] = PositionHeld.objects.filter(
            user=user).order_by("start_date")
    out['position_prior_info'] = PositionPrior.objects.filter(
            user=user).order_by("start_date")
    out['position_elsewhere_info'] = PositionElsewhere.objects.filter(
            user=user).order_by("start_date")

    # build up our full grant info
    grants_held = Grant.objects.filter(user=user, held=True)
    for grant in grants_held:
        grant.year_info = GrantYear.objects.filter(grant=grant)
        grant.investigator_info = Investigator.objects.filter(grant=grant)
    out['grants_held_info'] = grants_held

    grants_applied = Grant.objects.filter(user=user, held=False)
    for grant in grants_applied:
        grant.year_info = GrantYear.objects.filter(grant=grant)
        grant.investigator_info = Investigator.objects.filter(grant=grant)
    out['grants_applied_info'] = grants_applied

    out['courses_info'] = FacultyCourseJoin.objects.filter(user=user)
    out['dept_service_contribution_info'] = Service.objects.filter(user=user,
            level="d")
    out['uni_service_contribution_info'] = Service.objects.filter(user=user,
            level="u")
    out['coll_service_contribution_info'] = Service.objects.filter(user=user,
            level="c")
    out['ext_service_contribution_info'] = Service.objects.filter(user=user,
            level="e")




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

