# Description: This file contains the context processor for the application.
# The context processor is used to add additional context to the template context.
def theme(request):
    if 'is_dark_theme' in request.session:
        is_dark_theme = request.session.get('is_dark_theme')
        return {'is_dark_theme': is_dark_theme}
    return {'is_dark_theme': False}