from typing import Literal

from dotenv import load_dotenv
from fastapi import FastAPI
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field

load_dotenv()

app = FastAPI()


class Review(BaseModel):
    text: str


class Analysis(BaseModel):
    label: Literal["positive", "negative", "neutral"]
    score: int = Field(ge=1, le=5)
    theme: str = Field(pattern=r"^[a-z]+$")


model = ChatGroq(model="openai/gpt-oss-20b", temperature=0)
structured_model = model.with_structured_output(Analysis)


@app.post("/analyze", response_model=Analysis)
def analyze(review: Review):
    return structured_model.invoke(
        [
            (
                "system",
                "Analyze customer reviews. Return a label of positive, negative, "
                "or neutral; a score from 1 (very bad) to 5 (very good); and "
                "one lowercase word for the main topic, such as delivery, taste, "
                "price, service, or quality.",
            ),
            ("human", f"Review: {review.text}"),
        ]
    )
