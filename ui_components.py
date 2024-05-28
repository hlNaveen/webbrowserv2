from PyQt5.QtWidgets import QAction, QToolBar, QLineEdit, QLabel, QMenuBar
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

def create_toolbar(browser):
    toolbar = QToolBar()
    toolbar.setIconSize(QSize(16, 16))
    toolbar.setFixedHeight(40)

    back_action = QAction(QIcon.fromTheme("go-previous"), "Back", browser)
    back_action.triggered.connect(browser.navigate_back)
    toolbar.addAction(back_action)

    forward_action = QAction(QIcon.fromTheme("go-next"), "Forward", browser)
    forward_action.triggered.connect(browser.navigate_forward)
    toolbar.addAction(forward_action)

    reload_action = QAction(QIcon.fromTheme("view-refresh"), "Reload", browser)
    reload_action.triggered.connect(browser.reload_page)
    toolbar.addAction(reload_action)

    home_action = QAction(QIcon.fromTheme("go-home"), "Home", browser)
    home_action.triggered.connect(browser.navigate_home)
    toolbar.addAction(home_action)

    toolbar.addSeparator()

    browser.url_bar.setFixedWidth(600)
    toolbar.addWidget(browser.url_bar)

    toolbar.addSeparator()

    bookmark_action = QAction(QIcon.fromTheme("bookmark-new"), "Add Bookmark", browser)
    bookmark_action.triggered.connect(browser.add_bookmark)
    toolbar.addAction(bookmark_action)

    bookmarks_action = QAction(QIcon.fromTheme("document-open"), "Show Bookmarks", browser)
    bookmarks_action.triggered.connect(browser.show_bookmarks)
    toolbar.addAction(bookmarks_action)

    history_action = QAction(QIcon.fromTheme("document-open-recent"), "Show History", browser)
    history_action.triggered.connect(browser.show_history)
    toolbar.addAction(history_action)

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

    exit_action = QAction("Exit", browser)
    exit_action.triggered.connect(browser.close)
    file_menu.addAction(exit_action)

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

def create_find_toolbar(browser):
    find_toolbar = QToolBar("Find")
    find_toolbar.setIconSize(QSize(16, 16))
    find_toolbar.setFixedHeight(40)
    
    find_label = QLabel("Find:")
    find_toolbar.addWidget(find_label)
    
    browser.find_input = QLineEdit()
    browser.find_input.setFixedWidth(300)
    find_toolbar.addWidget(browser.find_input)
    
    find_action = QAction("Find", browser)
    find_action.triggered.connect(lambda: browser.find_text(browser.find_input.text()))
    find_toolbar.addAction(find_action)

    return find_toolbar
