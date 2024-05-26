from PyQt5.QtCore import QThread, QTime, pyqtSignal
from PyQt5.QtWebEngineWidgets import QWebEngineDownloadItem

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
