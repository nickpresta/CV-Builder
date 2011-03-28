# -*- coding: utf-8 -*-
from django.forms import ModelForm
from cv.models import *
from django import forms
from django.forms.models import BaseModelFormSet
import datetime

class DoEForm(ModelForm):
    """ This form is based on the DoE model and shows the
        year, research, teaching, and service """
        
    Year = forms.DateField(initial=datetime.date.today)
    
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

class ExecutiveSummaryForm(ModelForm):
    class Meta:
        fields = ('Executive',)
        model = SummaryTable
