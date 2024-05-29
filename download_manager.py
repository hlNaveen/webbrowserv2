from PyQt5.QtWebEngineWidgets import QWebEngineDownloadItem
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QFileDialog

class DownloadManager(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.downloads = []

    def handle_download_requested(self, download):
        download_path, _ = QFileDialog.getSaveFileName(None, "Save File", download.url().fileName())
        if download_path:
            download.setPath(download_path)
            download.accept()
            self.downloads.append(download)
            download.finished.connect(lambda: self.download_finished(download))

    def download_finished(self, download):
        self.downloads.remove(download)
        print(f"Download finished: {download.path()}")
