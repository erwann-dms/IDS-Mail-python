import pytest
from PyQt5.QtWidgets import QApplication
from src.gui import IDSMainWindow

@pytest.fixture(scope="module")
def app():
    return QApplication([])

def test_window_creation(app):
    window = IDSMainWindow()
    assert window.windowTitle() == "IDS-Mail-Professional"
    assert window.domain_input.placeholderText() == "Domaine (ex: example.com)"
