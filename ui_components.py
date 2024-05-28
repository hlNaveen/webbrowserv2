from PyQt5.QtWidgets import QAction, QToolBar, QLineEdit, QMenuBar, QToolButton, QMenu
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

def create_nav_toolbar(browser):
    toolbar = QToolBar()
    toolbar.setIconSize(QSize(24, 24))
    toolbar.setFixedHeight(50)
    toolbar.setMovable(False)
    toolbar.setStyleSheet("""
        QToolBar {
            background-color: #ffffff;
            border: 1px solid #dcdcdc;
            border-radius: 15px;
            padding: 5px;
            margin: 5px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
        }
        QToolButton {
            background-color: #ffffff;
            border: 1px solid #dcdcdc;
            border-radius: 15px;
            padding: 8px;
            margin: 3px;
        }
        QToolButton:hover {
            background-color: #f0f0f0;
        }
    """)

    back_action = QAction(QIcon('icons/back.png'), "Back", browser)
    back_action.triggered.connect(browser.navigate_back)
    toolbar.addAction(back_action)

    forward_action = QAction(QIcon('icons/forward.png'), "Forward", browser)
    forward_action.triggered.connect(browser.navigate_forward)
    toolbar.addAction(forward_action)

    reload_action = QAction(QIcon('icons/reload.png'), "Reload", browser)
    reload_action.triggered.connect(browser.reload_page)
    toolbar.addAction(reload_action)

    home_action = QAction(QIcon('icons/home.png'), "Home", browser)
    home_action.triggered.connect(browser.navigate_home)
    toolbar.addAction(home_action)

    return toolbar

def create_url_toolbar(browser):
    toolbar = QToolBar()
    toolbar.setIconSize(QSize(24, 24))
    toolbar.setFixedHeight(50)
    toolbar.setMovable(False)
    toolbar.setStyleSheet("""
        QToolBar {
            background-color: #ffffff;
            border: 1px solid #dcdcdc;
            border-radius: 15px;
            padding: 5px;
            margin: 5px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
        }
    """)

    browser.url_bar.setFixedWidth(800)
    toolbar.addWidget(browser.url_bar)

    menu_button = QToolButton()
    menu_button.setIcon(QIcon('icons/menu.png'))
    menu_button.setStyleSheet("padding: 8px; border-radius: 15px;")
    menu = QMenu()
    menu_button.setMenu(menu)
    menu_button.setPopupMode(QToolButton.InstantPopup)

    # Menu actions
    menu.addAction("Zoom In", browser.zoom_in)
    menu.addAction("Zoom Out", browser.zoom_out)
    menu.addAction("Toggle Dark Mode", browser.toggle_dark_mode)
    menu.addAction("Print", browser.print_page)

    toolbar.addWidget(menu_button)

    return toolbar

def create_menu(browser):
    menubar = QMenuBar()

    file_menu = menubar.addMenu("File")

    new_tab_action = QAction("New Tab", browser)
    new_tab_action.triggered.connect(lambda: browser.add_new_tab())
    file_menu.addAction(new_tab_action)

    print_action = QAction("Print", browser)
    print_action.triggered.connect(browser.print_page)
    file_menu.addAction(print_action)

    view_menu = menubar.addMenu("View")

    zoom_in_action = QAction("Zoom In", browser)
    zoom_in_action.triggered.connect(browser.zoom_in)
    view_menu.addAction(zoom_in_action)

    zoom_out_action = QAction("Zoom Out", browser)
    zoom_out_action.triggered.connect(browser.zoom_out)
    view_menu.addAction(zoom_out_action)

    dark_mode_action = QAction("Toggle Dark Mode", browser)
    dark_mode_action.triggered.connect(browser.toggle_dark_mode)
    view_menu.addAction(dark_mode_action)

    return menubar
