from .models import Category, Tag

def blog_globals(request):
    """
    Context processor to make categories and top tags available globally to all templates.
    """
    try:
        categories = Category.objects.all()
        tags = Tag.objects.all()[:15]
    except Exception:
        categories = []
        tags = []
        
    return {
        'global_categories': categories,
        'global_tags': tags,
    }
