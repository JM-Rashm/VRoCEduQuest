from flask import json, jsonify, request
import os
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate
    )
from langchain.output_parsers import PydanticOutputParser

from src.helpers.qa_helper import QAHelper

# os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"
# model = Ollama(model="llama2")


class QuizController:
    def __init__(self) -> None:
        self.parser = PydanticOutputParser(pydantic_object=QAHelper)
        self.model = ChatOpenAI(openai_api_key=os.environ['OPENAI_API_KEY'], temperature=0)
    
    def getQAList(self):
        payload = request.get_json()
        subject=payload["subject"]
        level=payload["level"], 
        age=payload["age"]
        language=payload["language"]
        
        template = f"""
            I want you to act as a quiz master creating objective questions for a quiz. 
            Create and return 3 questions for only {level} level. 
            Design questions on {subject} that cater to the difficulty level of {level} based on the {age}-year-old student in the {language} language. 

            Craft engaging and age-appropriate questions that challenge and stimulate the minds of each group, 
            ensuring the content is both educational and enjoyable.
        """
        
        human_prompt = HumanMessagePromptTemplate.from_template("{user_request}\n{format_instructions}")
        chat_prompt = ChatPromptTemplate.from_messages([human_prompt])

        formatted_request = chat_prompt.format_prompt(
            user_request=template,
            format_instructions=self.parser.get_format_instructions()
        ).to_messages()

        results = self.model(formatted_request, temperature=0.8)
        print(results)
        results_values = self.parser.parse(results.content)  
        response_data_dict = results_values.model_dump()  # Convert Pydantic model to dictionary
        response_data_json = json.dumps(response_data_dict)
        
        # try:
        #     print("Hello")
        # except Exception as exception:
        #    print(exception)    
        
        # response = BaseResponseModel(data, response_status, response_message)
        # return GenericConverter.to_json(response), response_status  
        # print(response)
        return response_data_json
    
    