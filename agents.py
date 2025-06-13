# agents.py
from crewai import Agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
llm = ChatOpenAI(model="gpt-4o", temperature=0)

stock_data_analyst = Agent(
    role="Stock Data Analyst",
    goal="Analyze stock financials and trends",
    backstory="An expert in financial data with deep insight into market behavior.",
    llm=llm
)

investment_advisor = Agent(
    role="Investment Advisor",
    goal="Recommend investment strategies based on risk and timeline",
    backstory="A seasoned investor who tailors recommendations to client needs.",
    llm=llm
)
