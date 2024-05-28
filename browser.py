from PyQt5.QtWidgets import QMainWindow, QLineEdit, QTabWidget, QStatusBar, QVBoxLayout, QWidget, QAction, QToolBar, QDialog, QListWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, QSize, Qt
from PyQt5.QtGui import QIcon, QFont, QPalette, QColor
from PyQt5.QtPrintSupport import QPrintDialog
from ui_components import create_toolbar, create_menu, create_download_manager, create_find_toolbar

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Modern Web Browser")
        self.setGeometry(100, 100, 1200, 800)
        
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.tabs.currentChanged.connect(self.current_tab_changed)

        self.setCentralWidget(self.tabs)
        self.status = QStatusBar()
        self.setStatusBar(self.status)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.url_bar.setFont(QFont("Arial", 12))

        self.toolbar = create_toolbar(self)
        self.addToolBar(self.toolbar)

        menubar = create_menu(self)
        self.setMenuBar(menubar)

        self.download_manager = create_download_manager(self)
        self.find_toolbar = create_find_toolbar(self)

        self.add_new_tab(QUrl("http://www.google.com"), "Home")

    def add_new_tab(self, qurl=None, label="Blank"):
        if qurl is None:
            qurl = QUrl("")

        browser = QWebEngineView()
        browser.setUrl(qurl)
        browser.urlChanged.connect(lambda q: self.update_url_bar(q, browser))
        browser.loadFinished.connect(lambda _: self.tabs.setTabText(self.tabs.indexOf(browser), browser.page().title()))

        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)
        browser.page().urlChanged.connect(self.save_history)

    def close_current_tab(self, i):
        if self.tabs.count() < 2:
            return
        self.tabs.removeTab(i)

    def current_tab_changed(self, i):
        qurl = self.tabs.currentWidget().url()
        self.update_url_bar(qurl, self.tabs.currentWidget())

    def navigate_to_url(self):
        url = self.url_bar.text()
        self.tabs.currentWidget().setUrl(QUrl(url))

    def update_url_bar(self, q, browser=None):
        if browser != self.tabs.currentWidget():
            return
        self.url_bar.setText(q.toString())
        self.url_bar.setCursorPosition(0)

    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl("http://www.google.com"))

    def navigate_back(self):
        self.tabs.currentWidget().back()

    def navigate_forward(self):
        self.tabs.currentWidget().forward()

    def reload_page(self):
        self.tabs.currentWidget().reload()

    def add_bookmark(self):
        url = self.tabs.currentWidget().url().toString()
        with open("bookmarks.txt", "a") as f:
            f.write(url + "\n")

    def show_bookmarks(self):
        dialog = QDialog()
        dialog.setWindowTitle("Bookmarks")
        layout = QVBoxLayout()
        bookmark_list = QListWidget()
        layout.addWidget(bookmark_list)
        dialog.setLayout(layout)
        
        try:
            with open("bookmarks.txt", "r") as f:
                bookmarks = f.readlines()
            bookmarks = [x.strip() for x in bookmarks]
            for bookmark in bookmarks:
                bookmark_list.addItem(bookmark)
                bookmark_list.itemClicked.connect(lambda item: self.add_new_tab(QUrl(item.text()), item.text()))
        except FileNotFoundError:
            pass
        
        dialog.exec_()

    def show_history(self):
        dialog = QDialog()
        dialog.setWindowTitle("History")
        layout = QVBoxLayout()
        history_list = QListWidget()
        layout.addWidget(history_list)
        dialog.setLayout(layout)
        
        try:
            with open("history.txt", "r") as f:
                history = f.readlines()
            history = [x.strip() for x in history]
            for url in history:
                history_list.addItem(url)
                history_list.itemClicked.connect(lambda item: self.add_new_tab(QUrl(item.text()), item.text()))
        except FileNotFoundError:
            pass
        
        dialog.exec_()

    def save_history(self, qurl):
        with open("history.txt", "a") as f:
            f.write(qurl.toString() + "\n")

    def find_text(self, text):
        self.tabs.currentWidget().findText(text)

    def zoom_in(self):
        self.tabs.currentWidget().setZoomFactor(self.tabs.currentWidget().zoomFactor() + 0.1)

    def zoom_out(self):
        self.tabs.currentWidget().setZoomFactor(self.tabs.currentWidget().zoomFactor() - 0.1)

    def toggle_dark_mode(self):
        app.setStyle("Fusion")
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(15, 15, 15))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)
        app.setPalette(dark_palette)

    def print_page(self):
        dialog = QPrintDialog()
        if dialog.exec_() == QDialog.Accepted:
            self.tabs.currentWidget().page().print(dialog.printer(), lambda ok: None)
