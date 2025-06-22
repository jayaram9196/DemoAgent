
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
