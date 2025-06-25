import onnxruntime as ort
from typing import List, Dict, Tuple
import os
from transformers import AutoTokenizer
import scipy


class SentimentModel:
    def __init__(
            self, model_name: str, 
            device: str = ["CPUExecutionProvider", "CUDAExecutionProvider"]):
        self.model = ort.InferenceSession(os.path.join(model_name, "model.onnx"), providers=device)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    def __call__(self, text: str) -> Dict[str, float]:
        inputs = self.tokenizer(text, return_tensors="np", add_special_tokens=True)
        onnx_inputs = {
            "input_ids": inputs["input_ids"][0].astype("int64")[None, :],
            "attention_mask": inputs["attention_mask"][0].astype("int64")[None, :]
        }
        outputs = self.model.run(None, onnx_inputs)
        scores = scipy.special.softmax(outputs[0], axis=-1)
        label_idx = int(scores[0].argmax())
        label = "negative" if label_idx == 0 else "positive"
        return {"label": label, "score": float(scores[0][label_idx])}
        