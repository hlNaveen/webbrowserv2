from PyQt5.QtCore import QUrl, QSize
from PyQt5.QtWidgets import QMainWindow, QTabWidget, QStatusBar, QVBoxLayout, QWidget, QLineEdit, QToolBar, QMenuBar, QAction, QLabel, QLineEdit, QToolButton, QHBoxLayout, QDialog
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings, QWebEnginePage
from PyQt5.QtGui import QIcon
from ui_components import create_toolbar, create_menu, create_find_toolbar

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

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        self.menu_bar = create_menu(self)
        self.setMenuBar(self.menu_bar)

        self.toolbar = create_toolbar(self)
        self.addToolBar(self.toolbar)

        self.find_toolbar = create_find_toolbar(self)
        self.addToolBar(self.find_toolbar)

        self.add_new_tab(QUrl("http://www.google.com"), 'Homepage')

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
        printer = QPrinter()
        print_dialog = QPrintDialog(printer)
        if print_dialog.exec_() == QDialog.Accepted:
            self.tab_widget.currentWidget().page().print(printer, lambda success: self.status.showMessage("Printing succeeded" if success else "Printing failed", 5000))

    def zoom_in(self):
        self.tab_widget.currentWidget().setZoomFactor(self.tab_widget.currentWidget().zoomFactor() + 0.1)

    def zoom_out(self):
        self.tab_widget.currentWidget().setZoomFactor(self.tab_widget.currentWidget().zoomFactor() - 0.1)

    def toggle_dark_mode(self):
        settings = self.tab_widget.currentWidget().settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.DnsPrefetchEnabled, not settings.testAttribute(QWebEngineSettings.WebAttribute.DnsPrefetchEnabled))

    def add_bookmark(self):
        pass  # Placeholder for add bookmark functionality

    def show_bookmarks(self):
        pass  # Placeholder for show bookmarks functionality

    def show_history(self):
        pass  # Placeholder for show history functionality

    def find_text(self, text):
        self.tab_widget.currentWidget().findText(text)
