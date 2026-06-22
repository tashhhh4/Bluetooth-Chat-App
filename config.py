from uuid import UUID
from kivy.utils import platform

# Determine execution environment
if platform == 'android':
    ENVIRONMENT = 'debug'
else:
    ENVIRONMENT = 'local'

# Hard-coded Service UUID
SERVICE_UUID = UUID('10002e1f-3d7b-4200-a112-bdc54faf6f23')
