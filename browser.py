from PyQt5.QtCore import QUrl, QSize
from PyQt5.QtWidgets import QMainWindow, QTabWidget, QStatusBar, QVBoxLayout, QWidget, QLineEdit, QToolBar, QMenuBar, QAction, QLineEdit, QToolButton, QHBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings, QWebEnginePage
from PyQt5.QtGui import QIcon, QPalette, QColor
from ui_components import create_nav_toolbar, create_url_toolbar, create_menu

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Web Browser')
        self.setWindowIcon(QIcon('icons/browser.png'))
        self.setGeometry(100, 100, 1200, 800)

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://www.google.com"))
        self.setCentralWidget(self.browser)

        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_current_tab)
        self.setCentralWidget(self.tab_widget)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.url_bar.setStyleSheet("padding: 6px; border-radius: 15px;")

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        self.menu_bar = create_menu(self)
        self.setMenuBar(self.menu_bar)

        self.nav_toolbar = create_nav_toolbar(self)
        self.addToolBar(self.nav_toolbar)

        self.url_toolbar = create_url_toolbar(self)
        self.addToolBar(self.url_toolbar)

        self.add_new_tab(QUrl("http://www.google.com"), 'Homepage')

        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
            }
            QToolBar {
                background-color: #ffffff;
                border: none;
                padding: 8px;
            }
            QTabWidget::pane {
                border-top: 2px solid #C2C7CB;
                top: -1px;
                background-color: #f8f9fa;
                border-radius: 15px;
            }
            QTabBar::tab {
                background: #ffffff;
                border: 2px solid #C4C4C3;
                padding: 10px;
                border-radius: 15px;
            }
            QTabBar::tab:selected {
                background: #e1e1e1;
            }
            QStatusBar {
                background: #ffffff;
                border-top: 1px solid #C2C7CB;
                padding: 8px;
                border-radius: 15px;
            }
        """)

    def add_new_tab(self, qurl=None, label="Blank"):
        if qurl is None:
            qurl = QUrl('')

        browser = QWebEngineView()
        browser.setUrl(qurl)
        i = self.tab_widget.addTab(browser, label)
        self.tab_widget.setCurrentIndex(i)
        browser.urlChanged.connect(lambda qurl, browser=browser: self.update_urlbar(qurl, browser))
        browser.loadFinished.connect(lambda _, i=i, browser=browser: self.tab_widget.setTabText(i, browser.page().title()))

    def close_current_tab(self, i):
        if self.tab_widget.count() < 2:
            return
        self.tab_widget.removeTab(i)

    def navigate_to_url(self):
        qurl = QUrl(self.url_bar.text())
        self.tab_widget.currentWidget().setUrl(qurl)

    def update_urlbar(self, qurl, browser=None):
        if browser != self.tab_widget.currentWidget():
            return
        self.url_bar.setText(qurl.toString())
        self.url_bar.setCursorPosition(0)

    def navigate_home(self):
        self.tab_widget.currentWidget().setUrl(QUrl("http://www.google.com"))

    def navigate_back(self):
        self.tab_widget.currentWidget().back()

    def navigate_forward(self):
        self.tab_widget.currentWidget().forward()

    def reload_page(self):
        self.tab_widget.currentWidget().reload()

    def print_page(self):
        pass  # Removed the print functionality

    def zoom_in(self):
        pass  # Removed the zoom functionality

    def zoom_out(self):
        pass  # Removed the zoom functionality

    def toggle_dark_mode(self):
        pass  # Removed the dark mode functionality

    def add_bookmark(self):
        pass  # Removed the add bookmark functionality

    def show_bookmarks(self):
        pass  # Removed the show bookmarks functionality

    def show_history(self):
        pass  # Removed the show history functionality
