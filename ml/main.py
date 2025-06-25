from src.apis.ner import NER
from src.apis.sentiment import Sentiment
from src.apis.qa import QA
from litserve import LitServer
from converter import pytorch_to_onnx


def main(args):
    pytorch_to_onnx()
    sentiment = Sentiment(api_path="/sentiment", enable_async=True)
    ner = NER(api_path="/ner", enable_async=True)
    qa = QA(api_path="/qa", enable_async=True)
    api = [sentiment, ner, qa]
    server = LitServer(api)
    server.run(port=args.port, reload=True, generate_client_file=False)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, required=True)
    args = parser.parse_args()
    main(args)


  