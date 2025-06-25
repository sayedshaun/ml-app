from pydantic import BaseModel, Field

class SentimentInput(BaseModel):
    input: str = Field(..., example="This product is great!")

class SentimentOutput(BaseModel):
    sentiment: str = Field(..., example="POSITIVE")
    score: float = Field(..., example=0.99)

class NERInput(BaseModel):
    input: str = Field(..., example="Barack Obama is the 44th president of the United States")

class Entity(BaseModel):
    entity: str
    type: str
    score: float | None = None

class NEROutput(BaseModel):
    entities: list[tuple[str, str, float]] = Field(
        ...,
        example=[
            ("Barack Obama", "PER", 0.99),
            ("United States", "LOC", 0.95)
        ]
    )

class QAInput(BaseModel):
    question: str = Field(..., example="What is the capital of France?")
    context: str = Field(..., example="France is a country in Europe and its capital is Paris.")

class QAOutput(BaseModel):
    answer: str = Field(..., example="Paris")
    score: float = Field(..., example=0.99)