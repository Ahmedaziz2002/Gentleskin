from .selectors import get_navigation_categories


def site_context(request):
    return {"categories": get_navigation_categories()}
