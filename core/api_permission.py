from rest_framework.permissions import BasePermission

from core.encryption import crypto_decode, jwt_decode_handler
from account.models import User


class UserAuthentication(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        try:
            user_id = crypto_decode(
                jwt_decode_handler(
                    request.META['HTTP_AUTHORIZATION']
                )['ai']
            )
            pwd = crypto_decode(
                jwt_decode_handler(
                    request.META['HTTP_AUTHORIZATION']
                )['bi']
            )
            request.user = User.objects.get(id=user_id, password=pwd, is_active=True)
            return True
        except:
            return False

