import os
import numpy as np
import scipy
import onnxruntime as ort
from typing import List, Dict, Tuple
from transformers import AutoTokenizer

class NERModel:
    def __init__(
            self, model_name: str, 
            device: List[str] = ["CPUExecutionProvider", "CUDAExecutionProvider"]
        ) -> None:
        self.model = ort.InferenceSession(os.path.join(model_name, "model.onnx"), providers=device)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.id2label = {
            0: "O",
            1: "B-DATE",
            2: "I-DATE",
            3: "B-PER",
            4: "I-PER",
            5: "B-ORG",
            6: "I-ORG",
            7: "B-LOC",
            8: "I-LOC"
        }
        self.label2id={
            "B-DATE": 1,
            "B-LOC": 7,
            "B-ORG": 5,
            "B-PER": 3,
            "I-DATE": 2,
            "I-LOC": 8,
            "I-ORG": 6,
            "I-PER": 4,
            "O": 0
        }

    def __call__(self, text: str) -> List[Tuple[str, str, float]]:
        inputs = self.tokenizer(text, return_tensors="np", add_special_tokens=True)
        onnx_inputs = {
            "input_ids": inputs["input_ids"][0].astype("int64")[None, :],
            "attention_mask": inputs["attention_mask"][0].astype("int64")[None, :]
        }
        outputs = self.model.run(None, onnx_inputs)
        scores = scipy.special.softmax(outputs[0], axis=-1)
        token_scores = scores[0]
        pred = token_scores.argmax(axis=-1)
        tokens = self.tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])

        result = []
        curr_token, curr_label_id, curr_prob = None, None, None
        for token, label_id, score_vec in zip(tokens[1:-1], pred[1:-1], token_scores[1:-1]):
            if token.startswith("##"):
                curr_token += token[2:]
            else:
                if curr_token is not None:
                    result.append((curr_token, self.id2label[curr_label_id], curr_prob))
                curr_token   = token
                curr_label_id = label_id
            curr_prob = float(score_vec[label_id])

        if curr_token is not None:
            result.append((curr_token, self.id2label[curr_label_id], curr_prob))
        return result