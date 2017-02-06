"""Customer-level meta services"""

from his.api.handlers import AdminService

__all__ = ['Logo']


class Logo(AdminService):
    """Handles service permissions"""

    def post(self):
        """Allows services"""
        pass
