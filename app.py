import sys
import os
import math
from PyQt5.QtCore import QUrl, Qt, QTimer, QSize, QPropertyAnimation, QTime, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QLineEdit, QToolBar, QSizePolicy, QLabel, QGraphicsOpacityEffect, QMenuBar, QMenu, QFileDialog, QProgressDialog, QMessageBox, QInputDialog
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineDownloadItem

# Import the transformers library
from transformers import pipeline

class DownloadThread(QThread):
    progress_signal = pyqtSignal(int, int, float)  # received, total, elapsed_time
    finished_signal = pyqtSignal(bool)

    def __init__(self, download_item):
        super().__init__()
        self.download_item = download_item
        self.download_time = QTime()
        self.download_time.start()

    def run(self):
        self.download_item.downloadProgress.connect(self.update_progress)
        self.download_item.finished.connect(self.download_finished)

    def update_progress(self, received, total):
        elapsed_time = self.download_time.elapsed() / 1000  # in seconds
        self.progress_signal.emit(received, total, elapsed_time)

    def download_finished(self):
        self.finished_signal.emit(self.download_item.state() == QWebEngineDownloadItem.DownloadCompleted)

class AIFunctions:
    def __init__(self):
        # Initialize the pipelines for different AI tasks
        self.summarizer = pipeline("summarization")
        self.sentiment_analyzer = pipeline("sentiment-analysis")
        self.qa_pipeline = pipeline("question-answering")

    def summarize_text(self, text):
        summary = self.summarizer(text, max_length=130, min_length=30, do_sample=False)
        return summary[0]['summary_text']

    def analyze_sentiment(self, text):
        sentiment = self.sentiment_analyzer(text)
        return sentiment[0]['label']

    def answer_question(self, context, question):
        answer = self.qa_pipeline(question=question, context=context)
        return answer['answer']

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.browser = QWebEngineView()
        home_page_path = os.path.abspath('homepage.html')
        self.browser.setUrl(QUrl.fromLocalFile(home_page_path))
        self.setCentralWidget(self.browser)
        self.showMaximized()

        # Initialize AI functions
        self.ai_functions = AIFunctions()

        # Enable/disable specific features for performance
        settings = self.browser.settings()
        settings.setAttribute(settings.JavascriptEnabled, True)
        settings.setAttribute(settings.PluginsEnabled, False)
        settings.setAttribute(settings.FullScreenSupportEnabled, False)

        # Navigation Bar
        navbar = QToolBar()
        navbar.setMovable(False)
        navbar.setStyleSheet("background-color: #F7F7F7; border: none;")
        self.addToolBar(Qt.TopToolBarArea, navbar)

        # Set icon size for toolbar
        icon_size = QSize(24, 24)
        navbar.setIconSize(icon_size)

        # Previous Button
        prev_btn = QAction(QIcon('icons/previous.png'), '', self)
        prev_btn.setToolTip('Go to the previous page')
        prev_btn.triggered.connect(self.browser.back)
        navbar.addAction(prev_btn)

        # Next Button
        next_btn = QAction(QIcon('icons/next.png'), '', self)
        next_btn.setToolTip('Go to the next page')
        next_btn.triggered.connect(self.browser.forward)
        navbar.addAction(next_btn)

        reload_btn = QAction(QIcon('icons/refresh.png'), '', self)
        reload_btn.setToolTip('Reload the current page')
        reload_btn.triggered.connect(self.browser.reload)
        navbar.addAction(reload_btn)

        home_btn = QAction(QIcon('icons/home.png'), '', self)
        home_btn.setToolTip('Go to the home page')
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        # New Page Button
        new_page_btn = QAction(QIcon('icons/new_page.png'), '', self)
        new_page_btn.setToolTip('Open a new page')
        new_page_btn.triggered.connect(self.navigate_new_page)
        navbar.addAction(new_page_btn)

        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText('Enter URL here...')
        self.url_bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.url_bar.setStyleSheet("border: 1px solid #CCCCCC; border-radius: 15px; padding: 6px;")
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        self.browser.urlChanged.connect(self.update_url)

        self.setWindowTitle("Enrco")
        self.setWindowIcon(QIcon('icons/browser.png'))

        # Show name with fade-in and fade-out effect
        QTimer.singleShot(0, self.show_name_with_fade)

        # Menu Bar
        menubar = self.menuBar()
        menubar.setStyleSheet("background-color: #F7F7F7; border: none;")
        self.setMenuBar(menubar)

        # Menu on the right
        right_menu = QMenu('Menu', self)
        right_menu.setIcon(QIcon('icons/menu.png'))  # Assuming you have an icon for the menu
        menubar.addMenu(right_menu)

        # Connect the downloadRequested signal to the download handler
        profile = QWebEngineProfile.defaultProfile()
        profile.downloadRequested.connect(self.handle_download)

        # AI Toolbar
        ai_toolbar = QToolBar("AI Tools")
        ai_toolbar.setMovable(False)
        ai_toolbar.setStyleSheet("background-color: #F7F7F7; border: none;")
        self.addToolBar(Qt.BottomToolBarArea, ai_toolbar)

        summarize_btn = QAction("Summarize", self)
        summarize_btn.setToolTip('Summarize the content of the current page')
        summarize_btn.triggered.connect(self.summarize_page)
        ai_toolbar.addAction(summarize_btn)

        sentiment_btn = QAction("Analyze Sentiment", self)
        sentiment_btn.setToolTip('Analyze the sentiment of the content of the current page')
        sentiment_btn.triggered.connect(self.analyze_page_sentiment)
        ai_toolbar.addAction(sentiment_btn)

        qa_btn = QAction("Ask Question", self)
        qa_btn.setToolTip('Ask a question about the content of the current page')
        qa_btn.triggered.connect(self.ask_question)
        ai_toolbar.addAction(qa_btn)

    def show_name_with_fade(self):
        self.label = QLabel('Enrco', self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont('Helvetica Neue', 50))
        self.label.setStyleSheet("color: black; background-color: white;")

        # Set the position and size of the label
        self.label.setGeometry(self.width() // 2 - 150, self.height() // 2 - 50, 300, 100)

        # Create an opacity effect and apply it to the label
        self.opacity_effect = QGraphicsOpacityEffect()
        self.label.setGraphicsEffect(self.opacity_effect)

        # Create an animation for the opacity effect
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(2000)
        self.animation.setStartValue(0.0)
        self.animation.setKeyValueAt(0.25, 1.0)
        self.animation.setKeyValueAt(0.75, 1.0)
        self.animation.setEndValue(0.0)
        self.animation.finished.connect(self.label.deleteLater)
        self.animation.start()

    def navigate_home(self):
        home_page_path = os.path.abspath('homepage.html')
        self.browser.setUrl(QUrl.fromLocalFile(home_page_path))

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        self.browser.setUrl(QUrl(url))

    def update_url(self, q):
        self.url_bar.setText(q.toString())

    def navigate_new_page(self):
        new_page_path = os.path.abspath('newpage.html')
        self.browser.setUrl(QUrl.fromLocalFile(new_page_path))

    def handle_download(self, download_item):
        # Show a file dialog to select download location
        path, _ = QFileDialog.getSaveFileName(self, "Save File", download_item.path())
        if path:
            download_item.setPath(path)
            download_item.accept()

            # Create a progress dialog
            progress_dialog = QProgressDialog("Downloading...", "Cancel", 0, 100, self)
            progress_dialog.setWindowTitle("Download")
            progress_dialog.setWindowModality(Qt.WindowModal)
            progress_dialog.setMinimumDuration(0)
            progress_dialog.setValue(0)
            progress_dialog.setAutoClose(False)
            progress_dialog.setAutoReset(False)
            progress_dialog.canceled.connect(download_item.cancel)
            progress_dialog.show()

            # Create a download thread to track the progress
            self.download_thread = DownloadThread(download_item)
            self.download_thread.progress_signal.connect(lambda received, total, elapsed: self.update_progress(progress_dialog, received, total, elapsed))
            self.download_thread.finished_signal.connect(lambda success: self.finish_download(progress_dialog, success))
            self.download_thread.start()

            download_item.finished.connect(self.download_thread.download_finished)
        else:
            download_item.cancel()

    def update_progress(self, progress_dialog, received, total, elapsed_time):
        if total > 0:
            progress_dialog.setMaximum(total)
            progress_dialog.setValue(received)

            # Calculate download speed and remaining time
            download_speed = received / (elapsed_time * 1024)  # in KB/s
            remaining_time = (total - received) / (download_speed * 1024)  # in seconds

            # Update the progress dialog label
            speed_text = f"Speed: {download_speed:.2f} KB/s"
            time_text = f"Time left: {math.ceil(remaining_time)} s"
            size_text = f"Size: {received / 1024:.2f} KB / {total / 1024:.2f} KB"
            progress_dialog.setLabelText(f"Downloading... {size_text}\n{speed_text}\n{time_text}")

    def finish_download(self, progress_dialog, success):
        progress_dialog.close()
        if success:
            QMessageBox.information(self, "Download Completed", "The file has been downloaded successfully.")
        else:
            QMessageBox.warning(self, "Download Failed", "The file could not be downloaded.")

    def summarize_page(self):
        self.browser.page().toPlainText(self.process_summary)

    def process_summary(self, page_text):
        try:
            summary = self.ai_functions.summarize_text(page_text)
            QMessageBox.information(self, "Page Summary", summary)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to summarize the page: {str(e)}")

    def analyze_page_sentiment(self):
        self.browser.page().toPlainText(self.process_sentiment)

    def process_sentiment(self, page_text):
        try:
            sentiment = self.ai_functions.analyze_sentiment(page_text)
            QMessageBox.information(self, "Sentiment Analysis", f"Sentiment: {sentiment}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to analyze sentiment: {str(e)}")

    def ask_question(self):
        question, ok = QInputDialog.getText(self, "Ask a Question", "Enter your question:")
        if ok and question:
            self.browser.page().toPlainText(lambda page_text: self.process_question(page_text, question))

    def process_question(self, page_text, question):
        try:
            answer = self.ai_functions.answer_question(page_text, question)
            QMessageBox.information(self, "Answer", answer)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to get the answer: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName('Enrco')

    # Set the font and style
    font = QFont('Helvetica Neue', 12)
    app.setFont(font)
    app.setStyle('Fusion')

    # Use Chromium backend for QtWebEngine
    from PyQt5.QtWebEngineWidgets import QWebEngineSettings
    QWebEngineSettings.defaultSettings().setAttribute(QWebEngineSettings.PluginsEnabled, True)


    window = Browser()
    app.exec_()
