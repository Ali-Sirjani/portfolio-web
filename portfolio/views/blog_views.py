from django.views import generic
from django.db.models import Q, Count
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _

from ..models import Post, PostComment
from ..forms import PostSearchForm, PostCommentForm
from ..utils import top_category_query


class PostListView(generic.ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'portfolio/blog/post_list.html'
    paginate_by = 6

    def get_queryset(self):
        category_slug = self.kwargs.get('slug')
        if category_slug:
            queryset = Post.active_objs.filter(category__slug=category_slug)

        else:
            queryset = Post.active_objs.all()

        queryset = queryset.select_related('category').prefetch_related('images').order_by('-datetime_updated')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['top_categories'] = top_category_query()

        return context


class PostSearchView(generic.ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'portfolio/blog/search_page.html'
    paginate_by = 6

    def get_queryset(self):
        queryset = []
        request_get = self.request.GET

        if 'q' in request_get:
            form = PostSearchForm(request_get)
            if form.is_valid():
                q = form.cleaned_data['q']
                queryset = Post.active_objs.filter(
                    Q(title__icontains=q) | Q(category__name__icontains=q)).order_by('-datetime_updated').distinct()
                queryset = queryset.select_related('category').prefetch_related('images').order_by('-datetime_updated')

                self.q = q

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['q'] = self.q
        except AttributeError:
            context['q'] = None

        context['top_categories'] = top_category_query()

        return context

    def dispatch(self, request, *args, **kwargs):
        q = request.GET.get('q')
        if not q or q.isspace():
            return render(self.request, 'portfolio/blog/search_q_none.html', {'top_categories': top_category_query()})
        return super().dispatch(request, *args, **kwargs)


@method_decorator(login_required, name='post')
class PostDetailView(generic.edit.FormMixin, generic.DetailView):
    model = Post
    form_class = PostCommentForm
    template_name = 'portfolio/blog/post_detail.html'
    context_object_name = 'post'
    queryset = Post.active_objs.select_related('category').prefetch_related('images')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.object

        is_related_posts_empty = True
        if obj.category:
            context['related_posts'] = Post.active_objs.filter(category=obj.category).exclude(pk=obj.pk).order_by(
                '?').distinct()[0:3]

            if context['related_posts'].exists():
                is_related_posts_empty = False

        if is_related_posts_empty:
            context['related_posts'] = Post.active_objs.all().exclude(pk=obj.pk).order_by('?').distinct()[0:3]

        context['comments'] = PostComment.objects.filter(confirmation=True, post_id=obj.pk).select_related(
            'author__profile').order_by('-tree_id', 'level', 'datetime_created')

        return context

    def post(self, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        request = self.request

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.author = request.user
            messages.success(request, _('You comment after confirmation will show in comments.'))
            comment.save()
            return redirect(self.object.get_absolute_url())
        else:
            messages.error(request, _('Your comment have problem please try again!'))
            return super().form_invalid(form)
