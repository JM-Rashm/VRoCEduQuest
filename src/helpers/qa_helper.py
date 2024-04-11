from pydantic import BaseModel, Field

class QAHelper(BaseModel):

    qa: list = Field(description='Python list of dictionaries containing question, list of options, answer and description')
    # city: str = Field(description='Give me the most popular country across the results')