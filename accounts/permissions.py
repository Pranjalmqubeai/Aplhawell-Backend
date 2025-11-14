# Use on any view: permission_classes = [IsInvestor]
from rest_framework.permissions import BasePermission
class IsInvestor(BasePermission):
    """Allow access only to users with the INVESTOR role."""
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == "INVESTOR"
        )

class IsOperator(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == "OPERATOR")
class IsAnalyst(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == "ANALYST")