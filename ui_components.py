from PyQt5.QtWidgets import QToolBar, QAction, QMenuBar
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

def create_toolbar(browser):
    toolbar = QToolBar()
    toolbar.setIconSize(QSize(24, 24))

    back_btn = QAction(QIcon('icons/back.png'), 'Back', browser)
    back_btn.triggered.connect(browser.back)
    toolbar.addAction(back_btn)

    forward_btn = QAction(QIcon('icons/forward.png'), 'Forward', browser)
    forward_btn.triggered.connect(browser.forward)
    toolbar.addAction(forward_btn)

    reload_btn = QAction(QIcon('icons/reload.png'), 'Reload', browser)
    reload_btn.triggered.connect(browser.reload)
    toolbar.addAction(reload_btn)

    home_btn = QAction(QIcon('icons/home.png'), 'Home', browser)
    home_btn.triggered.connect(browser.navigate_home)
    toolbar.addAction(home_btn)

    toolbar.addSeparator()

    toolbar.addWidget(browser.url_bar)

    return toolbar

def create_menu(browser):
    menubar = QMenuBar()

    file_menu = menubar.addMenu('File')

    new_page_action = QAction('New Page', browser)
    new_page_action.triggered.connect(browser.navigate_new_page)
    file_menu.addAction(new_page_action)

    return menubar
