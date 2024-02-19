from django import forms
from django.forms.models import BaseInlineFormSet
from django.utils.translation import gettext_lazy as _

from ..models import PostComment


class PostImageTabuFormSetAdmin(BaseInlineFormSet):
    def clean(self):
        main_count = 0

        for form in self.forms:
            if form.cleaned_data.get('is_main'):
                main_count += 1

        if main_count != 1:
            raise forms.ValidationError(_('Exactly one image should be marked as main.'))

        return super().clean()


class PostSearchForm(forms.Form):
    q = forms.CharField()


class PostCommentForm(forms.ModelForm):
    parent = forms.ModelChoiceField(queryset=PostComment.objects.filter(confirmation=True), widget=forms.HiddenInput,
                                    required=False)

    class Meta:
        model = PostComment
        fields = ('parent', 'text',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget = forms.Textarea(
            attrs={'rows': 5, 'placeholder': _('Enter your comment')})
