# from google.adk.agents import Agent, SequentialAgent
# from google.adk.models.lite_llm import LiteLlm
# # from google.adk.tools import tool
# from google.adk.tools.decorators import tool

# from dotenv import load_dotenv
# import os, requests, json
# import pandas as pd
# import matplotlib.pyplot as plt

# # Load environment
# load_dotenv()
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# def get_supply_chain_risk_score(region: str, product_type: str) -> float:
#     # Mock logic: calculate a risk score
#     risk_data = {
#         ("Asia", "electronics"): 0.8,
#         ("Europe", "pharma"): 0.4,
#         ("USA", "automotive"): 0.3
#     }
#     return risk_data.get((region, product_type), 0.5)

# # Model setup
# model = LiteLlm(
#     model="gemini/gemini-1.5-flash",
#     provider="google",
#     api_key=GOOGLE_API_KEY
# )

# # Tool: UN Comtrade API fetch
# @tool
# def fetch_un_comtrade_data(params: dict) -> dict:
#     """Fetches trade data from UN Comtrade based on parameters like 'reporter', 'partner', 'year', etc."""
#     base_url = "https://comtrade.un.org/api/get"
#     params.setdefault("max", 5)
#     response = requests.get(base_url, params=params)
#     return response.json()

# # Tool: World Bank indicator fetch
# @tool
# def fetch_world_bank_indicator(country_code: str, indicator: str) -> dict:
#     """Fetch World Bank economic indicator for a given country."""
#     url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/{indicator}?format=json"
#     response = requests.get(url)
#     return response.json()

# # Tool: Upload + Analyze CSV
# @tool
# def analyze_uploaded_csv(file_path: str) -> dict:
#     """Reads uploaded CSV and returns basic insights."""
#     df = pd.read_csv(file_path)
#     summary = df.describe(include="all").to_dict()
#     return summary

# # Tool: Chart generator from JSON
# @tool
# def generate_chart_from_json(data_json: str) -> str:
#     """Generates line chart from JSON string with 'labels' and 'values'."""
#     data = json.loads(data_json)
#     plt.figure(figsize=(8, 4))
#     plt.plot(data["labels"], data["values"], marker='o')
#     plt.title("Supply Chain Trend")
#     plt.xlabel("Year")
#     plt.ylabel("Value")
#     path = "/mnt/data/supply_chain_chart.png"
#     plt.savefig(path)
#     plt.close()
#     return path

# # Agent 1: Data Fetcher
# data_agent = Agent(
#     name="data_collector",
#     model=model,
#     description="Collect supply chain data from APIs and files",
#     instruction="Use available tools to fetch trade data, economic indicators, or read uploaded CSV files",
#     tools=[fetch_un_comtrade_data, fetch_world_bank_indicator, analyze_uploaded_csv]
# )

# # Agent 2: Analyzer
# analysis_agent = Agent(
#     name="supply_chain_analyst",
#     model=model,
#     description="Analyze trends in supply chain data",
#     instruction="Process and interpret trade and economic data to detect patterns and risks",
# )

# # Agent 3: Visualizer
# viz_agent = Agent(
#     name="data_visualizer",
#     model=model,
#     description="Generate supply chain charts",
#     instruction="Generate charts using the tool based on provided JSON with trends",
#     tools=[generate_chart_from_json]
# )

# # Agent 4: Final Summary Generator
# summary_agent = Agent(
#     name="supply_chain_summary",
#     model=model,
#     description="Summarize the overall supply chain insight",
#     instruction="Generate executive summary from data and analysis; include risks, trends, and opportunities."
# )

# # Root Multi-Agent System
# root_agent = SequentialAgent(
#     name="supply_chain_advisor",
#     sub_agents=[
#         data_agent,
#         analysis_agent,
#         viz_agent,
#         summary_agent
#     ]
# )

from google.adk.agents import Agent, SequentialAgent
from google.adk.models.lite_llm import LiteLlm
from dotenv import load_dotenv
import os

# Load environment variables (make sure GOOGLE_API_KEY is set in your .env)
load_dotenv()

# Initialize the Google Gemini model
model = LiteLlm(
    model="gemini/gemini-1.5-flash",
    provider="google",
    api_key=os.getenv("GOOGLE_API_KEY")
)

# --- Tool Function (without decorators) ---
def get_supply_chain_risk_score(region: str, product_type: str) -> float:
    # Simulate a risk scoring system
    risk_map = {
        ("Asia", "electronics"): 0.8,
        ("Europe", "pharma"): 0.4,
        ("USA", "automotive"): 0.3,
        ("India", "textiles"): 0.6,
    }
    return risk_map.get((region, product_type), 0.5)

# --- Sub-Agents ---

# 1. Fetch Market & Logistics Data
fetch_data_agent = Agent(
    name="fetch_logistics_data",
    model=model,
    description="Fetch current logistics and supply chain data",
    instruction="Collect relevant logistics info for the given region and product type.",
)

# 2. Analyze Risks
risk_analysis_agent = Agent(
    name="analyze_risks",
    model=model,
    description="Analyze supply chain risks based on data",
    instruction="Identify risk factors from delays, costs, regulations, etc.",
    tools=[get_supply_chain_risk_score]  # Function passed directly, no decorators
)

# 3. Suggest Optimizations
optimization_agent = Agent(
    name="optimize_supply_chain",
    model=model,
    description="Suggest supply chain optimizations",
    instruction="Provide recommendations for improving supply chain resilience and cost-efficiency.",
)

# 4. Generate Report
report_agent = Agent(
    name="generate_supply_chain_report",
    model=model,
    description="Summarize findings and recommendations",
    instruction="Write a detailed report including risks and suggestions in structured format.",
)

# --- Compose the Multi-Agent System ---
root_agent = SequentialAgent(
    name="supply_chain_advisor_pipeline",
    sub_agents=[
        fetch_data_agent,
        risk_analysis_agent,
        optimization_agent,
        report_agent
    ]
)

