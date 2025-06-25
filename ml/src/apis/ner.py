import os
from litserve import LitAPI
from src.schema import NERInput, NEROutput
from src.models.ner import NERModel


class NER(LitAPI):
    def setup(self, device):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join("data", "ner_onnx")
        self.model = NERModel(model_path, device)

    async def decode_request(self, request: NERInput) -> NERInput:
        return NERInput(input=request.input)

    async def predict(self, input: NERInput) -> dict:
        output = self.model(input.input)
        return output

    async def encode_response(self, output: dict) -> NEROutput:
        return NEROutput(entities=output)
    