import streamlit as st
from dotenv import load_dotenv
import os
from pydantic import BaseModel
import functools
import operator
import json
from IPython.display import Image, display

from typing import Annotated, Literal, Sequence
from typing_extensions import TypedDict

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, AIMessage, ToolMessage, HumanMessage
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_experimental.tools import PythonREPLTool
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel, Field
from PIL import Image
import base64

# .env 파일 로드
load_dotenv()

# =============== OCR Enging ===============
llm = ChatOpenAI(model="gpt-4o")

class medicalOcrResponse(BaseModel):
    venous: float = Field(
        description="정맥압 (mmHg)",
        example="140"
    )
    arterial: float = Field(
        description="동맥압 (mmHg), (음수값을 가짐)",
        example="-165",
        le=0 
    )
    sys: float = Field(
        description="수축기 (mmHg)",
        example="130"
    )
    dia: float = Field(
        description="이완기 (mmHg)",
        example="75"
    )
    blood_flow: float = Field(
        description="혈류속도 (mL/min)",
        example="300"
    )
    pulse: float = Field(
        description="맥박 (bpm)",
        example="70"
    )
    
medica_ocr_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", 
         "너는 의료기기 이미지에서 필요한 의료 수치를 추출해내는 OCR agent야"
         "너가 추출해야하는 수치는 아래와 같아."
         "<추출 할 키워드>"
         "정맥압(Venous, mmHg)"
         "동맥압(Arterial, mmHg)"
         "수축기 혈압(sys, mmHg)"
         "이완기 혈압(dia, mmHg)"
         "혈류속도(Blood Flow, mL/min)"
         "맥박수(Pulse, bpm)"
         "</추출 할 키워드>"
         "의료 기기의 모니터 화면 이미지에서 위의 값을 추출해줘."
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

ocr_agent = medica_ocr_prompt | llm.with_structured_output(medicalOcrResponse)
# response = ocr_agent.invoke([message])
# =============== OCR Enging ===============

uploaded_img = st.file_uploader("Image", accept_multiple_files=False)

if uploaded_img:
    image = Image.open(uploaded_img)
    save_path = "./uploaded_image.jpg"
    st.image(image)
    image.convert("RGB").save(save_path, format="JPEG")
    
    image_path = save_path
    
    with open(image_path, "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode("utf-8")
        
    message = HumanMessage(
        content=[
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{image_data}"},
            },
        ],
    )
    response = ocr_agent.invoke([message])
    
    st.text(f"Venous : {response.venous}")
    st.text(f"Arterial : {response.arterial}")
    st.text(f"Sys : {response.sys}")
    st.text(f"Dia : {response.dia}")
    st.text(f"Blood Flow : {response.blood_flow}")
    st.text(f"Pulse : {response.pulse}")
