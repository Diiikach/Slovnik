from pydantic import BaseModel


class User(BaseModel):
    cnt: int
    last_used: list[int]


class Quiz(BaseModel):
    pos: int
    user: str


class QuizContent(BaseModel):
    correct_variant: int
    variants: list[str]
    comment: str | None = None


class Quizs(BaseModel):
    quizs: dict[str, Quiz]
