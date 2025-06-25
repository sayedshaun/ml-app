import subprocess
import os

def pytorch_to_onnx() -> None:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(os.path.join(base_dir, "data"), exist_ok=True)
    qa_model = "distilbert-base-uncased-distilled-squad"
    ner_model = "Davlan/distilbert-base-multilingual-cased-ner-hrl"
    sentiment_model = "distilbert-base-uncased-finetuned-sst-2-english"

    if not os.path.exists(os.path.join("data", "qa_onnx")):
        subprocess.run(
            f"optimum-cli export onnx --model {qa_model} {os.path.join('data', 'qa_onnx')}",
            shell=True,
            check=True
        )
    if not os.path.exists(os.path.join("data", "ner_onnx")):
        subprocess.run(
            f"optimum-cli export onnx --model {ner_model} {os.path.join('data', 'ner_onnx')}",
            shell=True,
            check=True
        )
    if not os.path.exists(os.path.join("data", "sentiment_onnx")):
        subprocess.run(
            f"optimum-cli export onnx --model {sentiment_model} {os.path.join('data', 'sentiment_onnx')}",
            shell=True,
            check=True
        )

if __name__ == "__main__":
    pytorch_to_onnx()