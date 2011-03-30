# -*- coding: utf-8 -*-
from django.forms import ModelForm
from cv.models import *
from django import forms
from django.forms.models import BaseModelFormSet
import datetime

class DoEForm(ModelForm):
    """ This form is based on the DoE model and shows the
        year, research, teaching, and service """
        
    Year = forms.DateField(initial=datetime.date.today, widget=forms.TextInput(attrs={'class': 'datepicker'}))
    
    class Meta:
        fields = ('Year', 'Research', 'Teaching', 'Service')
        model = DoETable

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
        
class FacultyNameDeptForm(ModelForm):
    Faculty_GName = forms.CharField(label='Given Name')
    Faculty_SName = forms.CharField(label='Surname')

    class Meta:
        fields = ('Faculty_GName', 'Faculty_SName', 'Department')
        model = FacultyTable
        
class AccredForm(ModelForm):
    Date = forms.DateField(initial=datetime.date.today, widget=forms.TextInput(attrs={'class': 'datepicker'}))

    class Meta:
        model = AccredTable
        fields = ('Degree', 'Discipline', 'Institution', 'Date')
        widgets = {
            'Degree': forms.Textarea(attrs={'class': 'mceNoEditor'}),
            'Discipline': forms.Textarea(attrs={'class': 'mceNoEditor'}),
            'Institution': forms.Textarea(attrs={'class': 'mceNoEditor'}),
        }

class HonorForm(ModelForm):
    Honor_desc = forms.CharField(label='Description', widget=forms.Textarea(attrs={'class': 'mceNoEditor'}))
    
    class Meta:
        model = HonorTable
        fields = ('Honor_desc',)
    
class FacultyStartForm(ModelForm):
    Faculty_Start = forms.DateField(initial=datetime.date.today, widget=forms.TextInput(attrs={'class': 'datepicker'}))
    class Meta:
        fields = ('Faculty_Start',)
        model = FacultyTable

class ExecutiveSummaryForm(ModelForm):
    class Meta:
        fields = ('Executive',)
        model = SummaryTable
        widgets = {
            'Executive': forms.Textarea(attrs={'rows': '50', 'cols': '40',})
        }
        
class PositionForm(ModelForm):
    StartDate = forms.DateField(initial=datetime.date.today, widget=forms.TextInput(attrs={'class': 'datepicker'}))
    EndDate = forms.DateField(initial=datetime.date.today, widget=forms.TextInput(attrs={'class': 'datepicker'}))
    class Meta:
        fields = ('Rank', 'StartDate', 'EndDate', 'Location')


class OffCampusRecognitionForm(ModelForm):
    class Meta:
        fields = ('OffCampus',)
        model = SummaryTable 

class ResearchActivityForm(ModelForm):
    class Meta:
        fields = ('Research',)
        model = SummaryTable       

