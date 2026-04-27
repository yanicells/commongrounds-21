from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import AccessMixin


class RoleRequiredMixin(AccessMixin):
    required_role = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        if not hasattr(request.user, 'profile') or request.user.profile.role != self.required_role:
            raise PermissionDenied(
                "You do not have the required role to access this page.")

        return super().dispatch(request, *args, **kwargs)
