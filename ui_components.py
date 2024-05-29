from PyQt5.QtWidgets import QAction, QToolBar, QLineEdit, QMenu, QToolButton, QSizePolicy
from PyQt5.QtCore import Qt

def create_toolbar(browser):
    toolbar = QToolBar("Main Toolbar")
    toolbar.setMovable(False)  # Disable moving

    back_button = QToolButton()
    back_button.setText("Back")
    back_button.setObjectName("navButton")
    back_button.clicked.connect(browser.navigate_back)
    toolbar.addWidget(back_button)

    forward_button = QToolButton()
    forward_button.setText("Forward")
    forward_button.setObjectName("navButton")
    forward_button.clicked.connect(browser.navigate_forward)
    toolbar.addWidget(forward_button)

    reload_button = QToolButton()
    reload_button.setText("Reload")
    reload_button.setObjectName("navButton")
    reload_button.clicked.connect(browser.reload_page)
    toolbar.addWidget(reload_button)

    home_button = QToolButton()
    home_button.setText("Home")
    home_button.setObjectName("navButton")
    home_button.clicked.connect(browser.navigate_home)
    toolbar.addWidget(home_button)

    browser.url_bar = QLineEdit()
    browser.url_bar.setObjectName("urlBar")
    browser.url_bar.returnPressed.connect(browser.navigate_to_url)
    toolbar.addWidget(browser.url_bar)

    menu_button = QToolButton()
    menu_button.setText("Menu")
    menu_button.setObjectName("menuButton")

    menu = QMenu(menu_button)

    new_tab_action = QAction("New Tab", browser)
    new_tab_action.triggered.connect(browser.add_new_tab)
    menu.addAction(new_tab_action)

    zoom_action = menu.addMenu("Zoom")
    zoom_in_action = QAction("Zoom In", browser)
    zoom_in_action.triggered.connect(browser.zoom_in)
    zoom_action.addAction(zoom_in_action)
    zoom_out_action = QAction("Zoom Out", browser)
    zoom_out_action.triggered.connect(browser.zoom_out)
    zoom_action.addAction(zoom_out_action)

    downloads_action = QAction("Downloads", browser)
    downloads_action.triggered.connect(browser.show_downloads)
    menu.addAction(downloads_action)

    history_action = QAction("History", browser)
    history_action.triggered.connect(browser.show_history)
    menu.addAction(history_action)

    settings_action = QAction("Settings", browser)
    settings_action.triggered.connect(browser.show_settings)
    menu.addAction(settings_action)

    about_action = QAction("About", browser)
    about_action.triggered.connect(browser.show_about)
    menu.addAction(about_action)

    menu_button.setMenu(menu)
    menu_button.setPopupMode(QToolButton.InstantPopup)
    menu_button.setStyleSheet("QToolButton::menu-indicator { image: none; }")  # Remove the arrow down icon
    toolbar.addWidget(menu_button)

    return toolbar
