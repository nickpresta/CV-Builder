# -*- coding: utf-8 -*-
from django.forms import ModelForm
from cv.models import *
from django import forms
from django.forms.models import BaseModelFormSet
import datetime

class FormMixin(ModelForm):
    def __init__(self, *args, **kwargs):
        self.pk = kwargs.pop('pk', None)
        super(FormMixin, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        form = super(FormMixin, self).save(commit=False)

        if self.pk:
            form.setPK(self.pk)
        
        if commit:
            form.save()

        return form        
        
class FormsetMixin(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        self.pk = kwargs.pop('pk', None)
        super(FormsetMixin, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        forms = super(FormsetMixin, self).save(commit=False)
        for form in forms:
            if self.pk:
                form.setPK(self.pk)
            if commit:
                form.save()
        return forms

class DoEForm(FormMixin):
    """ This form is based on the DoE model and shows the
        year, research, teaching, and service """
        
    Year = forms.DateField(initial=datetime.date.today, widget=forms.TextInput(attrs={'class': 'datepicker'}))
    
    class Meta:
        fields = ('Year', 'Research', 'Teaching', 'Service')
        model = DoETable

    def setPK(self, form):
        form.Faculty_ID = self.pk

    def clean(self):
        """ Clean the form according to our custom rules """
        cleaned_data = self.cleaned_data
        research = cleaned_data.get("Research")
        teaching = cleaned_data.get("Teaching")
        service = cleaned_data.get("Service")

        # ensure that all 3 fields add up to 100
        if (research + teaching + service) != 100:
            msg = "Research, teaching and service must add up to 100"
            self._errors['Research'] = self.error_class([msg])
            self._errors['Teaching'] = self.error_class([msg])
            self._errors['Service'] = self.error_class([msg])

            # These fields are no longer valid
            del cleaned_data['Research']
            del cleaned_data['Teaching']
            del cleaned_data['Service']

        return cleaned_data
        
class FacultyNameDeptForm(FormMixin):
    Faculty_GName = forms.CharField(label='Given Name')
    Faculty_SName = forms.CharField(label='Surname')

    class Meta:
        fields = ('Faculty_GName', 'Faculty_SName', 'Department')
        model = FacultyTable
        
class AccredForm(FormMixin):
    Date = forms.DateField(initial=datetime.date.today, widget=forms.TextInput(attrs={'class': 'datepicker'}))

    class Meta:
        model = AccredTable
        fields = ('Degree', 'Discipline', 'Institution', 'Date')
        widgets = {
            'Degree': forms.Textarea(attrs={'class': 'mceNoEditor'}),
            'Discipline': forms.Textarea(attrs={'class': 'mceNoEditor'}),
            'Institution': forms.Textarea(attrs={'class': 'mceNoEditor'}),
        }

class HonorForm(FormMixin):
    Honor_desc = forms.CharField(label='Description', widget=forms.Textarea(attrs={'class': 'mceNoEditor'}))
    
    class Meta:
        model = HonorTable
        fields = ('Honor_desc',)
    
class FacultyStartForm(FormMixin):
    Faculty_Start = forms.DateField(initial=datetime.date.today, widget=forms.TextInput(attrs={'class': 'datepicker'}))
    class Meta:
        fields = ('Faculty_Start',)
        model = FacultyTable

class ExecutiveSummaryForm(FormMixin):
    class Meta:
        fields = ('Executive',)
        model = SummaryTable
        widgets = {
            'Executive': forms.Textarea(attrs={'rows': '50', 'cols': '40',})
        }
        
class PositionHeldForm(FormMixin):
    StartDate = forms.DateField(initial=datetime.date.today, widget=forms.TextInput(attrs={'class': 'datepicker'}))
    EndDate = forms.DateField(initial=datetime.date.today, widget=forms.TextInput(attrs={'class': 'datepicker'}))
    
    class Meta:
        fields = ('StartDate', 'EndDate', 'Location', 'Rank')
        model = PositionHeldTable

class PositionPriorForm(FormMixin):
    StartDate = forms.DateField(initial=datetime.date.today, widget=forms.TextInput(attrs={'class': 'datepicker'}))
    EndDate = forms.DateField(initial=datetime.date.today, widget=forms.TextInput(attrs={'class': 'datepicker'}))

    class Meta:
        fields = ('StartDate', 'EndDate', 'Location', 'Position')
        model = PositionPriorTable

class PositionElsewhereForm(FormMixin):
    StartDate = forms.DateField(initial=datetime.date.today, widget=forms.TextInput(attrs={'class': 'datepicker'}))
    EndDate = forms.DateField(initial=datetime.date.today, widget=forms.TextInput(attrs={'class': 'datepicker'}))

    class Meta:
        fields = ('StartDate', 'EndDate', 'Location', 'Position')
        model = PositionElsewhereTable


class OffCampusRecognitionForm(FormMixin):
    class Meta:
        fields = ('OffCampus',)
        model = SummaryTable 

class ResearchActivityForm(FormMixin):
    class Meta:
        model = SummaryTable 
        fields = ('Research',)
        widgets = {
            'Research': forms.Textarea(attrs={'rows': '50', 'cols': '40'})
        }

class ReportOnTeachingForm(FormMixin):
    class Meta:
        model = SummaryTable
        fields = ('Teaching',)
        widgets = {
            'Teaching': forms.Textarea(attrs={'rows': '50', 'cols': '40'})
        }

class InvestigatorForm(FormMixin):
    class Meta:
        model = InvestigatorTable
        fields = ('Name', 'Amount', 'Role')
