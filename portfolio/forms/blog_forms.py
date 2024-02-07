from django import forms
from django.forms.models import BaseInlineFormSet
from django.utils.translation import gettext_lazy as _


class PostImageTabuFormSetAdmin(BaseInlineFormSet):
    def clean(self):
        main_count = 0

        for form in self.forms:
            if form.cleaned_data.get('is_main'):
                main_count += 1

        if main_count != 1:
            raise forms.ValidationError(_('Exactly one image should be marked as main.'))

        return super().clean()
