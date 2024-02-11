from django.views import generic

from ..models import Project


class ProjectListView(generic.ListView):
    model = Project
    queryset = Project.active_objs.order_by('-datetime_updated')
    context_object_name = 'projects'
    template_name = 'portfolio/project/project_list.html'
    paginate_by = 1


class ProjectDetailView(generic.DetailView):
    model = Project
    queryset = Project.active_objs
    context_object_name = 'project'
    template_name = 'portfolio/project/project_detail.html'
