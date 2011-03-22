from django.forms import ModelForm
from cv.models import *

class DistributionOfEffortForm(ModelForm):
    """ This form is based on the DoE model and shows the
        year, research, teaching, and service """
    class Meta:
        fields = ('year', 'research', 'teaching', 'service')
        model = DistributionOfEffort

    def clean(self):
        """ Clean the form according to our custom rules """
        cleaned_data = self.cleaned_data
        research = cleaned_data.get("research")
        teaching = cleaned_data.get("teaching")
        service = cleaned_data.get("service")

        # ensure that all 3 fields add up to 100
        if (research + teaching + service) != 100:
            msg = "Research, teaching and service must add up to 100"
            self._errors['research'] = self.error_class([msg])
            self._errors['teaching'] = self.error_class([msg])
            self._errors['service'] = self.error_class([msg])

            # These fields are no longer valid
            del cleaned_data['research']
            del cleaned_data['teaching']
            del cleaned_data['service']

        return cleaned_data
