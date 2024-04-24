from flask import json, jsonify, request
from langchain.output_parsers import PydanticOutputParser
from PyPDF2 import PdfReader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from typing_extensions import Concatenate
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate
    )

import os

from src.helpers.qa_helper import QAHelper


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
    
    def ExtractQA(self):
        response_data_json = {}
        try:
            pdfReader = PdfReader("src\\controllers\\UPSCExam02_removed_removed.pdf")
            
            raw_text = ''

            for i, page in enumerate(pdfReader.pages):
                content = page.extract_text()
                if content:
                    raw_text += content
            
            
            # template = f"""
            #             Analyze the document provided completely. 
            #             And extract all the question with description, 
            #             and options if present.
            #             Analyze the question correctly and provide correct answer from the given options only if present 
            #             or else provide correct answer. 
            #             Also small description and hint not exceeding 2 lines for correct answer.
            #             group the all extracted question based on question type.
                        
            #             context: {raw_text}
                        
            #             output format :
            #             question_type: ''
            #             question: 'question'
            #             options: []
            #             correct_answer: 'option1'
            #             description: 'description'
            #             hint: 'hint'
            #         """
            
            template = f"""
                        I want you to act as a question analyzer and classifier for a given document. 
                        Analyze the document thoroughly, extract all the questions with descriptions and options 
                        if available, and correctly identify the question type. Provide the correct answer from 
                        the given options, or if not present, provide the correct answer. 
                        Additionally, include a brief description and hint (not exceeding 2 lines) for the correct answer. 
                        Group the extracted questions based on question type. 
                        
                        Context: {raw_text} 
                        
                        Output format should be as below: 
                        question_type: 'question type' 
                        question: 'question' 
                        options: [] 
                        correct_answer: 'option1' 
                        description: 'description' 
                        hint: 'hint'
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
            
        except Exception as e:
            print(e)
        
        return response_data_json
    
    