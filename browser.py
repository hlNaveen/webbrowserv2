from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QApplication, QMenuBar
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
from PyQt5.QtCore import QUrl
from ui_components import create_toolbar
from download_manager import DownloadManager  # Import the DownloadManager
import sys

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Modern Browser")
        self.setGeometry(100, 100, 1200, 800)

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://www.google.com"))

        main_layout = QVBoxLayout()

        self.toolbar = create_toolbar(self)
        main_layout.addWidget(self.toolbar)
        main_layout.addWidget(self.browser)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Setup download manager
        self.download_manager = DownloadManager(self)
        profile = self.browser.page().profile()
        profile.downloadRequested.connect(self.download_manager.handle_download_requested)

        # Apply QSS styling
        self.setStyleSheet(self.load_stylesheet())

    def load_stylesheet(self):
        return """
        QMainWindow {
            background-color: #f0f0f0;
        }

        QToolBar {
            background-color: #ffffff;
            border: none;
            padding: 10px;
            border-radius: 10px;
            margin: 5px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }

        QToolButton#navButton {
            background-color: #e0e0e0;
            border: none;
            padding: 8px;
            border-radius: 8px;
            margin-right: 5px;
        }

        QToolButton#navButton:hover {
            background-color: #d0d0d0;
        }

        QLineEdit#urlBar {
            background-color: #ffffff;
            border: 1px solid #d0d0d0;
            padding: 8px;
            border-radius: 10px;
            margin: 5px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            flex: 1;
        }

        QToolButton#menuButton {
            background-color: #e0e0e0;
            border: none;
            padding: 8px;
            border-radius: 8px;
            margin-left: 5px;
        }

        QToolButton#menuButton:hover {
            background-color: #d0d0d0;
        }

        QMenu {
            background-color: #ffffff;
            border: 1px solid #d0d0d0;
            padding: 10px;
            border-radius: 10px;
            margin: 5px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }

        QMenu::item {
            background-color: transparent;
            padding: 8px 16px;
        }

        QMenu::item:selected {
            background-color: #e0e0e0;
        }
        """

    def navigate_to_url(self):
        url = self.url_bar.text()
        self.browser.setUrl(QUrl(url))

    def update_url_bar(self, q):
        self.url_bar.setText(q.toString())

    def navigate_back(self):
        self.browser.back()

    def navigate_forward(self):
        self.browser.forward()

    def reload_page(self):
        self.browser.reload()

    def navigate_home(self):
        self.browser.setUrl(QUrl("http://www.google.com"))

    def add_new_tab(self):
        from menu_actions import new_tab
        new_tab.add_new_tab(self)

    def zoom_in(self):
        from menu_actions import zoom_in
        zoom_in.zoom_in(self)

    def zoom_out(self):
        from menu_actions import zoom_out
        zoom_out.zoom_out(self)

    def show_downloads(self):
        from menu_actions import show_downloads
        show_downloads.show_downloads(self)

    def show_history(self):
        from menu_actions import show_history
        show_history.show_history(self)

    def show_settings(self):
        from menu_actions import show_settings
        show_settings.show_settings(self)

    def show_about(self):
        from menu_actions import show_about
        show_about.show_about(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Browser()
    window.show()
    sys.exit(app.exec_())
