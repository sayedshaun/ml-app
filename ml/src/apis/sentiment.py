import os
from litserve import LitAPI
from src.schema import SentimentInput, SentimentOutput
from src.models.sentiment import SentimentModel


class Sentiment(LitAPI):

    def setup(self, device: str) -> None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join("data", "sentiment_onnx")
        self.model = SentimentModel(model_path, device)
    
    async def decode_request(self, request: SentimentInput) -> SentimentInput:
        return SentimentInput(input=request.input)
    
    async def predict(self, input: SentimentInput) -> dict:
        output = self.model(input.input)
        return output
    
    async def encode_response(self, output: dict) -> SentimentOutput:
        return SentimentOutput(sentiment=output["label"], score=output["score"])