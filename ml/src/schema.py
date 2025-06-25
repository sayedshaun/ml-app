from pydantic import BaseModel, Field

class SentimentInput(BaseModel):
    input: str = Field(..., example="This product is great!")

class SentimentOutput(BaseModel):
    sentiment: str = Field(..., example="POSITIVE")
    score: float = Field(..., example=0.99)

class NERInput(BaseModel):
    input: str = Field(..., example="Barack Obama is the 44th president of the United States")

class NEROutput(BaseModel):
    entities: list[tuple[str, str, float]] = Field(..., example=[{"entity": "Barack Obama", "type": "PER"}, {"entity": "United States", "type": "LOC"}])

class QAInput(BaseModel):
    question: str = Field(..., example="What is the capital of France?")
    context: str = Field(..., example="France is a country in Europe and its capital is Paris.")

class QAResponse(BaseModel):
    answer: str = Field(..., example="Paris")
    score: float = Field(..., example=0.99)