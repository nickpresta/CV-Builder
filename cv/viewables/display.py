from django.http import HttpResponse
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required

# TODO: Checkout serving *.html pages instead of individual views per page

def index(request):
    """ Responsible for showing the index page """

    return direct_to_template(request, 'index.html', {'status': 'works!'})
    
def stylesheet(request):
    # TODO: serving style.css for any css request
    return direct_to_template(request, 'style.css', { })
    
def editcv(request):
    return direct_to_template(request, 'editcv.html', { })

# TODO: currently an example / test for form layout
def form1(request):
    return direct_to_template(request, 'form1.html', { })
