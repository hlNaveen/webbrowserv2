from PyQt5.QtWidgets import QToolBar, QAction, QMenuBar, QMenu, QLineEdit
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QSize

def create_toolbar(browser):
    toolbar = QToolBar()
    toolbar.setIconSize(QSize(24, 24))

    back_btn = QAction('◀', browser)
    back_btn.setFont(QFont("Arial", 16))
    back_btn.triggered.connect(browser.navigate_back)
    toolbar.addAction(back_btn)

    forward_btn = QAction('▶', browser)
    forward_btn.setFont(QFont("Arial", 16))
    forward_btn.triggered.connect(browser.navigate_forward)
    toolbar.addAction(forward_btn)

    reload_btn = QAction('↻', browser)
    reload_btn.setFont(QFont("Arial", 16))
    reload_btn.triggered.connect(browser.reload_page)
    toolbar.addAction(reload_btn)

    home_btn = QAction('⌂', browser)
    home_btn.setFont(QFont("Arial", 16))
    home_btn.triggered.connect(browser.navigate_home)
    toolbar.addAction(home_btn)

    bookmark_btn = QAction('★', browser)
    bookmark_btn.setFont(QFont("Arial", 16))
    bookmark_btn.triggered.connect(browser.add_bookmark)
    toolbar.addAction(bookmark_btn)

    find_btn = QAction('🔍', browser)
    find_btn.setFont(QFont("Arial", 16))
    find_btn.triggered.connect(lambda: browser.find_toolbar.setVisible(not browser.find_toolbar.isVisible()))
    toolbar.addAction(find_btn)

    zoom_in_btn = QAction('A+', browser)
    zoom_in_btn.setFont(QFont("Arial", 16))
    zoom_in_btn.triggered.connect(browser.zoom_in)
    toolbar.addAction(zoom_in_btn)

    zoom_out_btn = QAction('A-', browser)
    zoom_out_btn.setFont(QFont("Arial", 16))
    zoom_out_btn.triggered.connect(browser.zoom_out)
    toolbar.addAction(zoom_out_btn)

    dark_mode_btn = QAction('🌙', browser)
    dark_mode_btn.setFont(QFont("Arial", 16))
    dark_mode_btn.triggered.connect(browser.toggle_dark_mode)
    toolbar.addAction(dark_mode_btn)

    print_btn = QAction('🖨', browser)
    print_btn.setFont(QFont("Arial", 16))
    print_btn.triggered.connect(browser.print_page)
    toolbar.addAction(print_btn)

    toolbar.addSeparator()
    toolbar.addWidget(browser.url_bar)

    return toolbar

def create_menu(browser):
    menubar = QMenuBar()

    file_menu = menubar.addMenu('File')

    new_tab_action = QAction('New Tab', browser)
    new_tab_action.triggered.connect(lambda: browser.add_new_tab())
    file_menu.addAction(new_tab_action)

    bookmarks_menu = menubar.addMenu('Bookmarks')

    show_bookmarks_action = QAction('Show Bookmarks', browser)
    show_bookmarks_action.triggered.connect(browser.show_bookmarks)
    bookmarks_menu.addAction(show_bookmarks_action)

    history_menu = menubar.addMenu('History')

    show_history_action = QAction('Show History', browser)
    show_history_action.triggered.connect(browser.show_history)
    history_menu.addAction(show_history_action)

    return menubar

def create_download_manager(browser):
    pass

def create_find_toolbar(browser):
    toolbar = QToolBar()
    toolbar.setIconSize(QSize(16, 16))

    find_text_box = QLineEdit()
    find_text_box.setPlaceholderText("Find text...")
    toolbar.addWidget(find_text_box)

    find_btn = QAction('🔍', browser)
    find_btn.setFont(QFont("Arial", 16))
    find_btn.triggered.connect(lambda: browser.find_text(find_text_box.text()))
    toolbar.addAction(find_btn)

    toolbar.setVisible(False)
    browser.addToolBar(toolbar)
    return toolbar
