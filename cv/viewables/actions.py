# -*- coding: utf-8 -*-
from datetime import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.template import Context
import ho.pisa as pisa
import cStringIO as StringIO

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
                request.user.username, datetime.now().strftime("%Y-%m-%d"))
        response.write(result.getvalue())
        return response
    return HttpResponse("Bad stuff happened. Oops!")

@login_required
def export_download(request):
    """ Return the response, either a PDF, or some error text """
    return write_pdf('export.html', {}, request)
