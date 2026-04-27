from django.core.exceptions import PermissionDenied
from django.contrib.auth.views import redirect_to_login
from functools import wraps


def role_required(required_role):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect_to_login(request.get_full_path())

            if not hasattr(request.user, 'profile') or request.user.profile.role != required_role:
                raise PermissionDenied(
                    "You do not have the required role to access this page.")

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
