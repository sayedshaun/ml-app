import scipy.signal
import scipy.stats
from transformers import AutoTokenizer
from typing import List, Dict, Tuple
import onnxruntime as ort
import os
import numpy as np


class QAModel:
    def __init__(self, model_name: str, device: str = "cpu") -> None:
        self.session = ort.InferenceSession(os.path.join(model_name, "model.onnx"))
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    def __call__(self, question: str, context: str) -> Dict[str, str]:
        inputs = self.tokenizer(question, context, return_tensors="np")
        onnx_inputs = {
            "input_ids": inputs["input_ids"][0].astype("int64")[None, :],
            "attention_mask": inputs["attention_mask"][0].astype("int64")[None, :]
        }
        outputs = self.session.run(None, onnx_inputs)
        start_prob = self.softmax(outputs[1], dim=-1)
        end_prob = self.softmax(outputs[0], dim=-1)
        start_index = start_prob.argmax().item()
        end_index = end_prob.argmax().item()
        predict_answer_tokens = inputs.input_ids[0, start_index : end_index + 1]
        answer = self.tokenizer.decode(predict_answer_tokens)
        score = (start_prob[0, start_index] * end_prob[0, end_index]).item()
        return {"answer": answer, "score": score}
    
    @staticmethod
    def softmax(x: np.ndarray, dim: int) -> np.ndarray:
        e_x = np.exp(x - np.max(x, axis=dim, keepdims=True))
        return e_x / np.sum(e_x, axis=dim, keepdims=True)