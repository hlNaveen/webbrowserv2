import asyncio
import aiohttp
import time
import logging
import json
import xml.etree.ElementTree as ET
from PIL import Image
import io
import torch
import torchvision.transforms as transforms
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
from PyQt5.QtCore import QThread, pyqtSignal, QRunnable, QThreadPool, QMutex, QMutexLocker, QWaitCondition, QUrl, Qt, QPropertyAnimation, pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QLineEdit, QAction, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QDialog, QLabel, QComboBox, QInputDialog, QMessageBox, QListWidget, QMenu, QToolButton, QFileDialog, QProgressDialog
from PyQt5.QtWebEngineWidgets import QWebEngineView
from functools import lru_cache
from concurrent.futures import ProcessPoolExecutor
import sys

# Custom Exceptions
class CustomException(Exception):
    pass

class NetworkException(CustomException):
    pass

class AIProcessingException(CustomException):
    pass

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class DownloadThread(QRunnable):
    progress = pyqtSignal(int)
    result = pyqtSignal(str)
    error = pyqtSignal(str)
    started = pyqtSignal()
    finished = pyqtSignal()
    cancelled = pyqtSignal()

    def __init__(self, url, action, extra_param=None, config=None):
        super().__init__()
        self.url = url
        self.action = action
        self.extra_param = extra_param
        self.config = config or {}
        self.retries = self.config.get('retries', 3)
        self.timeout = self.config.get('timeout', 10)
        self.priority = self.config.get('priority', QThread.NormalPriority)
        self.jitter = self.config.get('jitter', 0.1)
        self._is_running = True
        self.mutex = QMutex()
        self.condition = QWaitCondition()
        self.start_time = None
        self.thread_pool = QThreadPool.globalInstance()
        self.process_pool = ProcessPoolExecutor(max_workers=4)
        self.cache = lru_cache(maxsize=10)
    
    async def run(self):
        self.started.emit()
        self.start_time = time.time()
        try:
            logging.info(f"Thread started with URL: {self.url}, Action: {self.action}, Extra Param: {self.extra_param}")
            self.pre_execute()

            if self.action == "download":
                result = await self.download_data()
            elif self.action == "process":
                result = await self.process_data()
            elif self.action == "ai_analysis":
                result = await self.ai_analysis()
            else:
                raise ValueError("Unknown action")

            logging.info("Thread completed successfully")
            self.result.emit(result)
            self.post_execute()
        except Exception as e:
            logging.error(f"Error occurred: {e}")
            self.error.emit(str(e))
        finally:
            self.finished.emit()

    async def download_data(self):
        attempt = 0
        backoff_time = 1
        while attempt < self.retries:
            with QMutexLocker(self.mutex):
                if not self._is_running:
                    logging.info("Thread was cancelled during download")
                    self.cancelled.emit()
                    return "Download cancelled"
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(self.url, timeout=self.timeout) as response:
                        response.raise_for_status()
                        content_type = response.headers.get('Content-Type', '').lower()
                        data = await self.handle_content_type(response, content_type)

                        for i in range(100):
                            await asyncio.sleep(0.1)
                            self.progress.emit(i + 1)

                        return f"Downloaded data: {data[:100]}..."
            except (aiohttp.ClientError, aiohttp.http_exceptions.HttpProcessingError) as e:
                logging.warning(f"Attempt {attempt + 1} failed: {e}")
                attempt += 1
                await asyncio.sleep(backoff_time + self.jitter * backoff_time)
                backoff_time *= 2
                if attempt >= self.retries:
                    raise NetworkException(f"Failed to download data after {self.retries} attempts")
            except asyncio.TimeoutError as e:
                logging.error(f"Timeout error: {e}")
                raise NetworkException(f"Timeout occurred: {e}")
        return ""

    async def handle_content_type(self, response, content_type):
        if 'application/json' in content_type:
            data = json.dumps(await response.json())
        elif 'application/xml' in content_type or 'text/xml' in content_type:
            tree = ET.ElementTree(ET.fromstring(await response.text()))
            data = ET.tostring(tree.getroot(), encoding='unicode')
        else:
            data = await response.text()
        return data

    async def process_data(self):
        for i in range(100):
            with QMutexLocker(self.mutex):
                if not self._is_running:
                    logging.info("Thread was cancelled during processing")
                    self.cancelled.emit()
                    return "Processing cancelled"
            await asyncio.sleep(0.1)
            self.progress.emit(i + 1)
        return f"Processed data with param: {self.extra_param}"

    async def ai_analysis(self):
        if self.extra_param == "sentiment_analysis":
            return await self.perform_sentiment_analysis()
        elif self.extra_param == "image_classification":
            return await self.perform_image_classification()
        elif self.extra_param == "text_summarization":
            return await self.perform_text_summarization()
        elif self.extra_param == "text_generation":
            return await self.perform_text_generation()
        elif self.extra_param == "named_entity_recognition":
            return await self.perform_named_entity_recognition()
        elif self.extra_param == "object_detection":
            return await self.perform_object_detection()
        else:
            raise AIProcessingException("Unknown AI analysis task")

    @lru_cache(maxsize=10)
    async def perform_sentiment_analysis(self):
        sentiment_pipeline = pipeline("sentiment-analysis")
        text = await self.download_data()
        result = sentiment_pipeline(text)
        return json.dumps(result)

    @lru_cache(maxsize=10)
    async def perform_image_classification(self):
        classification_pipeline = pipeline("image-classification")
        image_data = await self.download_data()
        image = Image.open(io.BytesIO(image_data))
        preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        image_tensor = preprocess(image).unsqueeze(0)
        result = classification_pipeline(image_tensor)
        return json.dumps(result)

    @lru_cache(maxsize=10)
    async def perform_text_summarization(self):
        summarization_pipeline = pipeline("summarization")
        text = await self.download_data()
        result = summarization_pipeline(text)
        return json.dumps(result)

    @lru_cache(maxsize=10)
    async def perform_text_generation(self):
        tokenizer = AutoTokenizer.from_pretrained("gpt2")
        model = AutoModelForSequenceClassification.from_pretrained("gpt2")
        text = await self.download_data()
        inputs = tokenizer(text, return_tensors="pt")
        outputs = model.generate(**inputs)
        result = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return result

    @lru_cache(maxsize=10)
    async def perform_named_entity_recognition(self):
        ner_pipeline = pipeline("ner")
        text = await self.download_data()
        result = ner_pipeline(text)
        return json.dumps(result)

    @lru_cache(maxsize=10)
    async def perform_object_detection(self):
        object_detection_pipeline = pipeline("object-detection")
        image_data = await self.download_data()
        image = Image.open(io.BytesIO(image_data))
        preprocess = transforms.Compose([
            transforms.Resize((800, 800)),
            transforms.ToTensor(),
        ])
        image_tensor = preprocess(image).unsqueeze(0)
        result = object_detection_pipeline(image_tensor)
        return json.dumps(result)

    def stop(self):
        with QMutexLocker(self.mutex):
            self._is_running = False
            self.condition.wakeAll()
        logging.info("Stop signal received")

    def pre_execute(self):
        logging.info("Pre-execution hook")

    def post_execute(self):
        logging.info("Post-execution hook")

    def set_priority(self, priority):
        self.priority = priority

    @staticmethod
    def calculate_eta(progress, start_time):
        elapsed_time = time.time() - start_time
        if progress == 0:
            return float('inf')
        eta = elapsed_time * (100 - progress) / progress


class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enrco Browser")
        self.setWindowIcon(QIcon.fromTheme("browser"))
        self.setGeometry(100, 100, 1200, 800)
        
        self.default_homepage = "https://www.google.com"
        self.default_search_engine = "https://www.google.com/search?q="
        self.browser = QWebEngineView()
        self.history = []
        self.bookmarks = []
        
        self.init_ui()
        self.show_name_with_fade()
        self.create_browser()  # Initialize the browser after fade
        
        self.thread_pool = QThreadPool.globalInstance()

    def init_ui(self):
        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.toolbar.addWidget(self.url_bar)

        back_btn = QAction("Back", self)
        back_btn.triggered.connect(self.browser_back)
        self.toolbar.addAction(back_btn)

        forward_btn = QAction("Forward", self)
        forward_btn.triggered.connect(self.browser_forward)
        self.toolbar.addAction(forward_btn)

        reload_btn = QAction("Reload", self)
        reload_btn.triggered.connect(self.browser_reload)
        self.toolbar.addAction(reload_btn)

        stop_btn = QAction("Stop", self)
        stop_btn.triggered.connect(self.browser_stop)
        self.toolbar.addAction(stop_btn)

        home_btn = QAction("Home", self)
        home_btn.triggered.connect(self.navigate_home)
        self.toolbar.addAction(home_btn)

        settings_btn = QAction("Settings", self)
        settings_btn.triggered.connect(self.show_settings)
        self.toolbar.addAction(settings_btn)

        history_btn = QAction("History", self)
        history_btn.triggered.connect(self.show_history)
        self.toolbar.addAction(history_btn)

        bookmarks_btn = QAction("Bookmarks", self)
        bookmarks_btn.triggered.connect(self.show_bookmarks)
        self.toolbar.addAction(bookmarks_btn)

        clear_data_btn = QAction("Clear Data", self)
        clear_data_btn.triggered.connect(self.clear_browsing_data)
        self.toolbar.addAction(clear_data_btn)

        # AI Tools
        ai_tools_btn = QToolButton()
        ai_tools_btn.setText("AI Tools")
        ai_tools_btn.setPopupMode(QToolButton.MenuButtonPopup)
        ai_menu = QMenu()
        
        ai_summarize_action = QAction("Summarize Page", self)
        ai_summarize_action.triggered.connect(lambda: self.perform_ai_task("text_summarization"))
        ai_menu.addAction(ai_summarize_action)
        
        ai_sentiment_action = QAction("Analyze Sentiment", self)
        ai_sentiment_action.triggered.connect(lambda: self.perform_ai_task("sentiment_analysis"))
        ai_menu.addAction(ai_sentiment_action)
        
        ai_ask_question_action = QAction("Ask Question", self)
        ai_ask_question_action.triggered.connect(lambda: self.perform_ai_task("text_generation"))
        ai_menu.addAction(ai_ask_question_action)
        
        ai_translate_action = QAction("Translate Page", self)
        ai_translate_action.triggered.connect(lambda: self.perform_ai_task("named_entity_recognition"))
        ai_menu.addAction(ai_translate_action)
        
        ai_extract_keywords_action = QAction("Extract Keywords", self)
        ai_extract_keywords_action.triggered.connect(lambda: self.perform_ai_task("object_detection"))
        ai_menu.addAction(ai_extract_keywords_action)
        
        ai_tools_btn.setMenu(ai_menu)
        self.toolbar.addWidget(ai_tools_btn)

    def navigate_home(self):
        self.browser.setUrl(QUrl(self.default_homepage))

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith('http'):
            url = self.default_search_engine + url
        self.browser.setUrl(QUrl(url))

    def update_url(self, q):
        self.url_bar.setText(q.toString())
        if q.toString() not in self.history:
            self.history.append(q.toString())

    def show_history(self):
        dialog = QDialog(self)
        dialog.setWindowTitle('History')
        layout = QVBoxLayout()

        history_list = QListWidget()
        history_list.addItems(self.history)
        layout.addWidget(history_list)

        dialog.setLayout(layout)
        dialog.exec_()

    def show_bookmarks(self):
        dialog = QDialog(self)
        dialog.setWindowTitle('Bookmarks')
        layout = QVBoxLayout()

        bookmarks_list = QListWidget()
        bookmarks_list.addItems(self.bookmarks)
        layout.addWidget(bookmarks_list)

        dialog.setLayout(layout)
        dialog.exec_()

    def clear_browsing_data(self):
        profile = self.browser.page().profile()
        profile.clearAllVisitedLinks()
        profile.clearHttpCache()
        profile.clearAllVisitedLinks()
        self.history = []
        self.bookmarks = []
        QMessageBox.information(self, 'Clear Browsing Data', 'Browsing data has been cleared.')

    def show_settings(self):
        settings_dialog = QDialog(self)
        settings_dialog.setWindowTitle('Settings')
        layout = QVBoxLayout()

        homepage_label = QLabel('Homepage:')
        layout.addWidget(homepage_label)
        homepage_input = QLineEdit(self.default_homepage)
        layout.addWidget(homepage_input)

        search_engine_label = QLabel('Search Engine:')
        layout.addWidget(search_engine_label)
        search_engine_input = QLineEdit(self.default_search_engine)
        layout.addWidget(search_engine_input)

        def save_settings():
            self.default_homepage = homepage_input.text()
            self.default_search_engine = search_engine_input.text()
            settings_dialog.close()

        save_button = QPushButton('Save')
        save_button.clicked.connect(save_settings)
        layout.addWidget(save_button)

        settings_dialog.setLayout(layout)
        settings_dialog.exec_()

    def perform_ai_task(self, task_type):
        self.progress_dialog = QProgressDialog("Performing AI task...", "Cancel", 0, 100, self)
        self.progress_dialog.setWindowModality(Qt.WindowModal)
        self.progress_dialog.show()

        def update_progress(value):
            self.progress_dialog.setValue(value)
            if value >= 100:
                self.progress_dialog.hide()

        url = self.browser.url().toString()
        ai_thread = DownloadThread(url, 'ai_analysis', extra_param=task_type)
        ai_thread.progress.connect(update_progress)
        ai_thread.result.connect(self.show_ai_result)
        ai_thread.error.connect(self.show_error)
        ai_thread.finished.connect(self.on_ai_task_finished)
        
        self.thread_pool.start(ai_thread)

    def show_ai_result(self, result):
        result_dialog = QDialog(self)
        result_dialog.setWindowTitle('AI Result')
        layout = QVBoxLayout()
        result_label = QLabel(result)
        layout.addWidget(result_label)
        result_dialog.setLayout(layout)
        result_dialog.exec_()

    def show_error(self, error_message):
        QMessageBox.critical(self, 'Error', error_message)

    def on_ai_task_finished(self):
        logging.info("AI Task finished")

    def show_name_with_fade(self):
        self.welcome_label = QLabel("Welcome to Enrco Browser!", self)
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.welcome_label.setStyleSheet("font-size: 24px; color: #333333;")
        self.setCentralWidget(self.welcome_label)

        self.animation = QPropertyAnimation(self.welcome_label, b"windowOpacity")
        self.animation.setDuration(2000)
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.finished.connect(self.remove_welcome_label)
        self.animation.start()

    @pyqtSlot()
    def remove_welcome_label(self):
        self.welcome_label.deleteLater()
        self.create_browser()  # Create the browser widget after the label is removed

    def create_browser(self):
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl(self.default_homepage))
        self.setCentralWidget(self.browser)
        self.browser.urlChanged.connect(self.update_url)
        self.browser.page().profile().downloadRequested.connect(self.on_download_requested)

    def browser_back(self):
        if self.browser:
            self.browser.back()

    def browser_forward(self):
        if self.browser:
            self.browser.forward()

    def browser_reload(self):
        if self.browser:
            self.browser.reload()

    def browser_stop(self):
        if self.browser:
            self.browser.stop()

    def on_download_requested(self, download_item):
        download_dialog = QFileDialog(self, "Save File")
        download_dialog.setAcceptMode(QFileDialog.AcceptSave)
        download_dialog.selectFile(download_item.suggestedFileName())  # Automatically select the suggested file name
        download_dialog.setDefaultSuffix(download_item.suggestedFileName().split('.')[-1])
        if download_dialog.exec_() == QFileDialog.Accepted:
            download_path = download_dialog.selectedFiles()[0]
            download_item.setPath(download_path)
            download_item.accept()

            self.show_download_progress(download_item)

    def show_download_progress(self, download_item):
        progress_dialog = QProgressDialog("Downloading...", "Cancel", 0, 100, self)
        progress_dialog.setWindowModality(Qt.WindowModal)
        progress_dialog.show()

        def update_progress(received_bytes, total_bytes):
            if total_bytes > 0:
                progress = int((received_bytes / total_bytes) * 100)
                progress_dialog.setValue(progress)
            else:
                progress_dialog.setValue(0)

        download_item.downloadProgress.connect(update_progress)

        def on_download_finished():
            progress_dialog.setValue(100)
            progress_dialog.hide()

        download_item.finished.connect(on_download_finished)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = Browser()
    window.show()
    sys.exit(app.exec_())
