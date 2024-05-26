from transformers import pipeline

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
