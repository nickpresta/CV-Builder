from django.http import HttpResponse
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required

def index(request):
    """ Responsible for showing the index page """

    return direct_to_template(request, 'index.html', {'status': 'works!'})
    
def stylesheet(request):
    return direct_to_template(request, 'style.css', { })
    
def editcv(request):
    return direct_to_template(request, 'editcv.html', { })
