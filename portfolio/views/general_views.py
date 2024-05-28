from django.views import generic
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from meta.views import Meta

from ..models import ContactMe, Project
from ..forms import ContactMeForm
from ..mixins import JSONResponseMixin


class HomePageView(generic.ListView):
    model = Project
    context_object_name = 'projects'
    template_name = 'portfolio/general/home_page.html'

    def get_queryset(self):
        queryset = Project.active_objs.all().prefetch_related('images').order_by('-datetime_updated')[:6]
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['meta'] = Meta(title=_('Ali Sirjani - Freelance Website Developer with Django Expertise'),
                               description=_(
                                   'Discover the projects and expertise of a freelance website developer with Django passionate about delivering quality work.'
                               ),
                               )

        return context


class ContactMeView(JSONResponseMixin, generic.CreateView):
    model = ContactMe
    form_class = ContactMeForm
    http_method_names = ('post',)

    def form_valid(self, form):
        contact_obj = form.save(commit=False)
        if self.request.user.is_authenticated:
            contact_obj.user = self.request.user
        contact_obj.save()

        messages.success(self.request, _('Your message has been sent successfully. I will get back to you shortly.'))
        response_data = {'success': True, 'message': 'message created successfully.'}
        return self.render_to_json_response(response_data)

    def form_invalid(self, form):
        response_data = {'form': self.ajax_response_form(form)}
        return self.render_to_json_response(response_data, status=400)
