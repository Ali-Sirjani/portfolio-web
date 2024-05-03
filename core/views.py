from django.views import generic
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.utils.translation import gettext_lazy as _
from django.db import transaction

from allauth.account.forms import ChangePasswordForm, SetPasswordForm

from portfolio.mixins import JSONResponseMixin
from .models import Profile
from .forms import ProfileForm, SetUsernameForm


class ProfileView(LoginRequiredMixin, JSONResponseMixin, generic.UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'core/profile.html'
    success_url = reverse_lazy('core:profile')
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        profile_user, create = Profile.objects.get_or_create(user=self.request.user)
        return profile_user

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, _('profile successfully updated'))
        response_data = {'success': True, 'message': 'Profile updated successfully.'}
        return self.render_to_json_response(response_data)

    def form_invalid(self, form):
        response_data = {'form': self.ajax_response_form(form)}
        return self.render_to_json_response(response_data, status=400)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.has_usable_password():
            context['change_pass_form'] = ChangePasswordForm()
        else:
            context['set_pass_form'] = SetPasswordForm()

        context['set_username_form'] = SetUsernameForm(initial={'username': self.request.user.username})

        return context


@login_required
@require_POST
def set_username_view(request):
    json_mixin_obj = JSONResponseMixin()

    form = SetUsernameForm(data=request.POST)
    if form.is_valid():
        user_model = get_user_model()
        username = form.cleaned_data.get('username')
        try:
            user_exist = get_user_model().objects.get(username=username)
            if request.user.username == user_exist.username:
                form.add_error('username', _('You are already using this username. Choose a different one.'))

        except user_model.DoesNotExist:
            with transaction.atomic():
                request.user.username = username
                request.user.save()

            messages.success(request, _('Username successfully changed.'))
            return json_mixin_obj.render_to_json_response({'message': 'success'})

    response_data = {'form': json_mixin_obj.ajax_response_form(form)}
    return json_mixin_obj.render_to_json_response(response_data, status=400)
