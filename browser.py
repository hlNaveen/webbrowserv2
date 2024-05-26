from PyQt5.QtWidgets import QMainWindow, QLineEdit
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from ui_components import create_toolbar, create_menu

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enrco")
        self.setGeometry(100, 100, 1200, 800)

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://www.google.com"))

        self.setCentralWidget(self.browser)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.browser.urlChanged.connect(self.update_url)

        navbar = create_toolbar(self)
        self.addToolBar(navbar)

        menubar = create_menu(self)
        self.setMenuBar(menubar)

    def back(self):
        self.browser.back()

    def forward(self):
        self.browser.forward()

    def reload(self):
        self.browser.reload()

    def navigate_home(self):
        self.browser.setUrl(QUrl("http://www.google.com"))

    def navigate_new_page(self):
        self.browser.setUrl(QUrl("http://www.example.com"))

    def navigate_to_url(self):
        url = self.url_bar.text()
        self.browser.setUrl(QUrl(url))

    def update_url(self, q):
        self.url_bar.setText(q.toString())
