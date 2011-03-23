from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory
from django.forms.formsets import formset_factory

from cv.forms import *
from cv.models import *

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
    """ Create a form view for the Distribution of Effort """

    # get this user's Summary or else create a new one
    try:
        summaryData = Summary.objects.get(user=request.user)
    except Summary.DoesNotExist:
        summaryData = Summary()

    # get this user's DoEs or else create a new one
    try:
        doeData = DistributionOfEffort.objects.filter(user=request.user).order_by('year')
    except DistributionOfEffort.DoesNotExist:
        doeData = DistributionOfEffort()

    if request.method == 'POST':
        summaryFormset = ExecutiveSummaryForm(request.POST, request.FILES,
                instance=summaryData, prefix="summary")
        doeFormset = modelformset_factory(DistributionOfEffort,
                form=DistributionOfEffortForm, extra=1)(request.POST,
                        request.FILES, queryset=doeData)

        if summaryFormset.is_valid() and doeFormset.is_valid():
            # Save the form data, ensure they are updating as themselves
            summary = summaryFormset.save(commit=False)
            summary.user = request.user
            summary.save()
            summaryFormset.save_m2m()

            
            doe = doeFormset.save(commit=False)
            # add user to each table row
            for d in doe:
                d.user = request.user
            doeFormset.save()
            doeFormset.save_m2m()
            return HttpResponseRedirect('/executive/')
    else:
        # Show the Executive Summary form
        summaryFormset = ExecutiveSummaryForm(instance=summaryData, prefix="summary")
        doeFormset = modelformset_factory(DistributionOfEffort,
                form=DistributionOfEffortForm, extra=1)(queryset=doeData)

    # Set up widget HTML properties
    # TODO: not sure if this should be here or in forms.py

    for form in doeFormset.forms:
        form.fields['year'].widget.attrs['class'] = 'datepicker'

    summaryFormset.fields['executive'].widget.attrs['rows'] = '50'
    summaryFormset.fields['executive'].widget.attrs['cols'] = '40'

    return direct_to_template(request, 'executive.html', {'summaryFormset': summaryFormset, 'doeFormset': doeFormset})

@login_required
def biographical(request):
    return direct_to_template(request, 'biographical.html', {})

@login_required
def offCampusRecognition(request):
    return direct_to_template(request, 'OffCampusRecognition.html', {})

@login_required
def ServiceAndAdmin(request):
    return direct_to_template(request, 'ServiceAndAdministrativeContributions.html', {})

@login_required
def ReportOnTeaching(request):
    return direct_to_template(request, 'ReportOnTeaching.html', {})

@login_required
def ResearchGrants(request):
    return direct_to_template(request, 'ResearchGrants.html', {})

@login_required
def Courses(request):
    return direct_to_template(request, 'Courses.html', {})

@login_required
def ResearchActivity(request):
    return direct_to_template(request, 'ResearchActivity.html', {})

@login_required
def distribution_of_effort(request):
    """ Create a form view for the Distribution of Effort """

    # get this user's DoE or else create a new one
    try:
        data = DistributionOfEffort.objects.get(user=request.user)
    except:
        data = DistributionOfEffort()

    if request.method == 'POST':
        formset = DistributionOfEffortForm(request.POST, request.FILES, instance=data)
        if formset.is_valid():
            # Save the form data, ensure they are updating as themselves
            doe = formset.save(commit=False)
            doe.user = request.user
            doe.save()
            formset.save_m2m()
    else:
        # Show the DoE form
        formset = DistributionOfEffortForm(instance=data)
    return direct_to_template(request, 'doe.html', {'formset': formset})
