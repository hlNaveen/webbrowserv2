#ai functions.py

from transformers import pipeline
from transformers.pipelines import AggregationStrategy
from sentence_transformers import SentenceTransformer
from bertopic import BERTopic
import numpy as np
from scipy.spatial import distance

class AIFunctions:
    def __init__(self):
        # Summarization
        self.summarizer_abstractive = pipeline("summarization", model="facebook/bart-large-cnn")
        self.summarizer_extractive = pipeline("summarization", model="google/pegasus-xsum")

        # Sentiment Analysis
        self.sentiment_analyzer = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")

        # Question Answering
        self.qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")

        # Translation
        self.translator = pipeline("translation_en_to_fr")  # Support multiple languages

        # Feature Extraction
        self.keyword_extractor = pipeline("feature-extraction", model="bert-base-uncased")

        # Named Entity Recognition
        self.ner = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english")
        self.ner_linking = pipeline("entity-linking")

        # Text Generation
        self.text_generator_gpt2 = pipeline("text-generation", model="gpt2")
        self.text_generator_gpt3 = pipeline("text-generation", model="EleutherAI/gpt-neo-2.7B")

        # Language Detection
        self.language_detector = pipeline("text-classification", model="papluca/xlm-roberta-base-language-detection")

        # Text Classification
        self.text_classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

        # Text Similarity
        self.text_similarity = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

        # Paraphrasing
        self.paraphraser = pipeline("text2text-generation", model="tuner007/pegasus_paraphrase")

        # Emotion Detection
        self.emotion_detector = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")

        # Spell and Grammar Check
        self.spell_checker = pipeline("fill-mask", model="bert-base-uncased")

        # Text-to-Speech
        self.text_to_speech = pipeline("text-to-speech")

        # Speech-to-Text
        self.speech_to_text = pipeline("automatic-speech-recognition", model="facebook/wav2vec2-large-960h")

        # Tokenization
        self.tokenizer = pipeline("token-classification", model="bert-base-cased")

        # POS Tagging
        self.pos_tagger = pipeline("ner", model="dslim/bert-base-NER")

        # Coreference Resolution
        self.coref_resolution = pipeline("coreference-resolution")

        # Zero-Shot Classification
        self.zero_shot_classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

        # Topic Modeling
        self.topic_modeling = BERTopic()

        # Question Generation
        self.question_generator = pipeline("text2text-generation", model="valhalla/t5-small-qg-prepend")

        # Intent Recognition
        self.intent_recognizer = pipeline("text-classification", model="textattack/bert-base-uncased-CoLA")

        # Semantic Search
        self.semantic_searcher = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')

        # Text Style Transfer
        self.style_transfer = pipeline("text2text-generation", model="prithivida/parrot_paraphraser_on_T5")

        # Aspect-Based Sentiment Analysis
        self.aspect_sentiment = pipeline("text-classification", model="cardiffnlp/twitter-roberta-base-sentiment")

        # Text Simplification
        self.text_simplifier = pipeline("text2text-generation", model="t5-base")

        # Text Anonymization
        self.text_anonymizer = pipeline("ner", model="dslim/bert-base-NER")

        # Text Augmentation
        self.text_augmenter = pipeline("text2text-generation", model="t5-small")

    def summarize_text(self, text, model="abstractive"):
        try:
            if model == "extractive":
                summary = self.summarizer_extractive(text, max_length=130, min_length=30, do_sample=False)
            else:
                summary = self.summarizer_abstractive(text, max_length=130, min_length=30, do_sample=False)
            return summary[0]['summary_text']
        except Exception as e:
            return f"Error summarizing text: {str(e)}"

    def analyze_sentiment(self, text):
        try:
            sentiment = self.sentiment_analyzer(text)
            return sentiment[0]
        except Exception as e:
            return f"Error analyzing sentiment: {str(e)}"

    def answer_question(self, context, question):
        try:
            answer = self.qa_pipeline(question=question, context=context)
            return answer['answer']
        except Exception as e:
            return f"Error answering question: {str(e)}"

    def translate_text(self, text, target_language="fr"):
        try:
            if target_language != "fr":
                return f"Translation to {target_language} not supported yet."
            translation = self.translator(text)
            return translation[0]['translation_text']
        except Exception as e:
            return f"Error translating text: {str(e)}"

    def extract_keywords(self, text):
        try:
            keywords = self.keyword_extractor(text)
            return keywords[0]  # Simplified for demonstration
        except Exception as e:
            return f"Error extracting keywords: {str(e)}"

    def detect_language(self, text):
        try:
            language = self.language_detector(text)
            return language[0]['label']
        except Exception as e:
            return f"Error detecting language: {str(e)}"

    def recognize_entities(self, text):
        try:
            entities = self.ner(text)
            return entities
        except Exception as e:
            return f"Error recognizing entities: {str(e)}"

    def link_entities(self, text):
        try:
            linked_entities = self.ner_linking(text)
            return linked_entities
        except Exception as e:
            return f"Error linking entities: {str(e)}"

    def generate_text(self, prompt, model="gpt2", max_length=50):
        try:
            if model == "gpt3":
                generated_text = self.text_generator_gpt3(prompt, max_length=max_length, num_return_sequences=1)
            else:
                generated_text = self.text_generator_gpt2(prompt, max_length=max_length, num_return_sequences=1)
            return generated_text[0]['generated_text']
        except Exception as e:
            return f"Error generating text: {str(e)}"

    def classify_text(self, text, candidate_labels):
        try:
            classification = self.text_classifier(text, candidate_labels=candidate_labels)
            return classification
        except Exception as e:
            return f"Error classifying text: {str(e)}"

    def measure_text_similarity(self, text1, text2):
        try:
            embeddings1 = self.text_similarity.encode(text1)
            embeddings2 = self.text_similarity.encode(text2)
            similarity = 1 - distance.cosine(embeddings1, embeddings2)
            return similarity
        except Exception as e:
            return f"Error measuring text similarity: {str(e)}"

    def paraphrase_text(self, text):
        try:
            paraphrases = self.paraphraser(text)
            return paraphrases[0]['generated_text']
        except Exception as e:
            return f"Error paraphrasing text: {str(e)}"

    def detect_emotions(self, text):
        try:
            emotions = self.emotion_detector(text)
            return emotions
        except Exception as e:
            return f"Error detecting emotions: {str(e)}"

    def check_spelling(self, text):
        try:
            spell_checked = self.spell_checker(text)
            return spell_checked
        except Exception as e:
            return f"Error checking spelling: {str(e)}"

    def convert_text_to_speech(self, text):
        try:
            speech = self.text_to_speech(text)
            return speech
        except Exception as e:
            return f"Error converting text to speech: {str(e)}"

    def convert_speech_to_text(self, audio):
        try:
            text = self.speech_to_text(audio)
            return text['text']
        except Exception as e:
            return f"Error converting speech to text: {str(e)}"

    def tokenize_text(self, text):
        try:
            tokens = self.tokenizer(text)
            return tokens
        except Exception as e:
            return f"Error tokenizing text: {str(e)}"

    def pos_tag_text(self, text):
        try:
            pos_tags = self.pos_tagger(text)
            return pos_tags
        except Exception as e:
            return f"Error tagging parts of speech: {str(e)}"

    def resolve_coreferences(self, text):
        try:
            resolved = self.coref_resolution(text)
            return resolved
        except Exception as e:
            return f"Error resolving coreferences: {str(e)}"

