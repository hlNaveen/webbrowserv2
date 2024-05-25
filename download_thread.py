#download_thread.py

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
from PyQt5.QtCore import QThread, pyqtSignal, QRunnable, QThreadPool, QMutex, QMutexLocker, QWaitCondition
from queue import PriorityQueue
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from functools import lru_cache

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
