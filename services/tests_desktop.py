from services.service import Service
from utils import TestSuite

class DesktopServiceTests(TestSuite):

    def test_service_initialized(self):
        service = Service(events=[])
        self.assertTrue(hasattr(service, 'event_registry'))
        self.assertTrue(service.event_registry.name == 'Service.EventRegistry')