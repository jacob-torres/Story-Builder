# Context Processors

def user_context(request):
    """Context processor for passing a user object to a template context."""

    if request.user.is_authenticated:
        user = request.user
    else:
        user = None

    return {'user': user}
