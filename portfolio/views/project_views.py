from django.views import generic

from ..models import Project


class ProjectListView(generic.ListView):
    model = Project
    queryset = Project.active_objs.prefetch_related('images').order_by('-datetime_updated')
    context_object_name = 'projects'
    template_name = 'portfolio/project/project_list.html'
    paginate_by = 1


class ProjectDetailView(generic.DetailView):
    model = Project
    queryset = Project.active_objs
    context_object_name = 'project'
    template_name = 'portfolio/project/project_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        project_slug_list = list(self.queryset.values_list('slug', flat=True).order_by('-datetime_updated'))
        index_obj = project_slug_list.index(self.object.slug)

        try:
            context['previous_project_slug'] = project_slug_list[index_obj + 1]
        except IndexError:
            context['previous_project_slug'] = None

        try:
            if index_obj != 0:
                context['next_project_slug'] = project_slug_list[index_obj - 1]
            else:
                context['next_project_slug'] = None

        except IndexError:
            context['next_project_slug'] = None

        return context
