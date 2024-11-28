import sys
import unittest
from PyQt5.QtWidgets import QApplication
from ai_assistant.modules.visual_detection import VisualDetectionWidget
from ai_assistant.modules.audio_detection import AudioDetectionWidget
from ai_assistant.modules.device_monitoring import DeviceMonitoringWidget
from ai_assistant.modules.internet_search import InternetSearchWidget
from ai_assistant.modules.osint_tools import OSINTWidget

app = QApplication(sys.argv)

class TestModules(unittest.TestCase):
    def setUp(self):
        self.modules = {
            'visual': VisualDetectionWidget(),
            'audio': AudioDetectionWidget(),
            'device': DeviceMonitoringWidget(),
            'search': InternetSearchWidget(),
            'osint': OSINTWidget()
        }

    def test_visual_detection(self):
        widget = self.modules['visual']
        self.assertIsNotNone(widget.image_label)
        self.assertIsNotNone(widget.mode_combo)
        self.assertIsNotNone(widget.start_button)

    def test_audio_detection(self):
        widget = self.modules['audio']
        self.assertIsNotNone(widget.device_combo)
        self.assertIsNotNone(widget.level_bar)
        self.assertIsNotNone(widget.start_button)

    def test_device_monitoring(self):
        widget = self.modules['device']
        # Verify tabs exist
        tabs = widget.findChildren(QTabWidget)
        self.assertTrue(len(tabs) > 0)

    def test_internet_search(self):
        widget = self.modules['search']
        self.assertIsNotNone(widget.search_input)
        self.assertIsNotNone(widget.search_button)
        self.assertIsNotNone(widget.results_display)

    def test_osint_tools(self):
        widget = self.modules['osint']
        self.assertIsNotNone(widget.target_input)
        self.assertIsNotNone(widget.scan_button)
        self.assertIsNotNone(widget.results_display)

if __name__ == '__main__':
    unittest.main()
