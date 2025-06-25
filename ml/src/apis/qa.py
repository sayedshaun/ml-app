import os
from litserve import LitAPI
from src.schema import QAInput, QAResponse
from src.models.qa import QAModel
from pathlib import Path



class QA(LitAPI):
    def setup(self, device):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join("data", "qa_onnx")
        self.model = QAModel(model_path, device)
    
    async def decode_request(self, request: QAInput) -> QAInput:
        return QAInput(question=request.question, context=request.context)
    
    async def predict(self, input: QAInput) -> dict:
        output = self.model(input.question, input.context)
        return output

    async def encode_response(self, output: dict) -> QAResponse:
        return QAResponse(answer=output["answer"], score=output["score"])
