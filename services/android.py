from android.permissions import check_permission, request_permissions
from services.service import Service

class AndroidService(Service):

    def __init__(self):

        super().__init__(events=['PERMISSION_GRANTED'])

    def run_with_permissions(self, permissions, callback, on_deny=None):
        """ If all the needed permissions are already granted, immediately run callback().
            Otherwise, initiate a permission request and pass in callback() to be run when done.
            The optional on_deny() handler can be run if the user does not grant the permissions.
        """
        if all(check_permission(p) for p in permissions):
            callback()
            return

        def _handle_permission_result(permissions, grants):
            for i, permission in enumerate(permissions):
                if grants[i]:
                    self.event_registry.emit_event('PERMISSION_GRANTED', permission)
            if all(grants):
                callback()
            else:
                if on_deny:
                    on_deny()

        request_permissions(permissions, _handle_permission_result)
