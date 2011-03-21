from django.http import HttpResponse
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required

def index(request):
    """ Responsible for showing the index page """

    return direct_to_template(request, 'index.html', {'status': 'works!'})

@login_required
def editcv(request):
    return direct_to_template(request, 'editcv.html', {})

@login_required
def form1(request):
    return direct_to_template(request, 'form1.html', {})

@login_required
def executive(request):
    return direct_to_template(request, 'executive.html', {})
    
@login_required
def biographical(request):
    return direct_to_template(request, 'biographical.html', {})
