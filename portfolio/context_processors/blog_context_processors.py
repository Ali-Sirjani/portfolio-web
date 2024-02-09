from ..models import Post


def recent_posts(request):
    recent_posts_query = Post.active_objs.all().order_by('-datetime_updated')[:3]
    context = {'recent_posts': recent_posts_query}
    return context
