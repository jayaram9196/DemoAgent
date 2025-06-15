
# # from google.adk.agents import Agent
# # from google.adk.models.lite_llm import LiteLlm

# # from textblob import TextBlob
# # from dotenv import load_dotenv
# # import os

# # load_dotenv()
# # GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# # print("API Key Loaded:", GOOGLE_API_KEY)

# # MODEL = LiteLlm(
# #     model="gemini/gemini-1.5-flash",
# #     provider="google",
# #     api_key=GOOGLE_API_KEY  # ✅ THIS IS REQUIRED
# # )

# # def get_sentiment(text: str):
# #     sentiment = TextBlob(text).sentiment
# #     return sentiment.polarity

# # root_agent = Agent(
# #     name="text_analysis_agent",
# #     model=MODEL,
# #     description="Agent to analyse a given text",
# #     instruction="You are a text analyst agent with ability to analyse a given text and also to provide the sentiment in the text",
# #     tools=[get_sentiment],
# # )

# from google.adk.agents import Agent, SequentialAgent
# from google.adk.models.lite_llm import LiteLlm
# from dotenv import load_dotenv
# import os

# # Load environment variables
# load_dotenv()

# # Initialize the model
# model = LiteLlm(
#     model="gemini/gemini-1.5-flash",
#     provider="google",
#     api_key=os.getenv("GOOGLE_API_KEY")  # ✅ Explicitly pass the key
# )

# # Sub-Agent 1: Market Data Fetcher
# fetch_agent = Agent(
#     name="fetch_market_data",
#     model=model,
#     description="Fetch market-related data for a given domain and location.",
#     instruction="Collect raw data points and sources about the specified industry in the specified location."
# )

# # Sub-Agent 2: Trend Analyzer
# trend_agent = Agent(
#     name="analyze_market_trends",
#     model=model,
#     description="Analyze the market trends based on collected data.",
#     instruction="Identify trends, growth rates, and changing customer behavior."
# )

# # Sub-Agent 3: Competitor Analyzer
# competitor_agent = Agent(
#     name="identify_competitors",
#     model=model,
#     description="Identify major competitors and their strategies.",
#     instruction="List key players in the industry and summarize their approaches."
# )

# # Final Summary Agent
# summary_agent = Agent(
#     name="generate_report",
#     model=model,
#     description="Create a complete market research summary.",
#     instruction="Using previous outputs, write a complete market research report. and generate a pdf with graphs for the trends and financial calculations"
# )

# # ✅ Compose the multi-agent system using SequentialAgent
# root_agent = SequentialAgent(
#     name="market_research_pipeline",
#     # description="Pipeline that performs step-by-step market research",
#     # instruction="Perform end-to-end market research for a domain and location using sub-agents.",
#     sub_agents=[
#         fetch_agent,
#         trend_agent,
#         competitor_agent,
#         summary_agent,
#     ]
# )

from google.adk.agents import Agent, SequentialAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools import FunctionTool
from dotenv import load_dotenv
import os
import json
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from datetime import datetime
import numpy as np
from bs4 import BeautifulSoup
import yfinance as yf
from serpapi import GoogleSearch
import time

# Load environment variables
load_dotenv()

# Initialize the model
model = LiteLlm(
    model="gemini/gemini-1.5-flash",
    provider="google",
    api_key=os.getenv("GOOGLE_API_KEY")
)

# Web data fetching tools
def search_market_data(query: str, location: str = "India") -> str:
    """
    Search for market data using SerpAPI or web scraping.
    
    Args:
        query: Search query for market data
        location: Geographic location for the search
    
    Returns:
        JSON string with search results and extracted data
    """
    try:
        # Option 1: Using SerpAPI (requires API key)
        if os.getenv("SERPAPI_KEY"):
            search = GoogleSearch({
                "q": f"{query} {location} market data statistics",
                "api_key": os.getenv("SERPAPI_KEY"),
                "num": 10
            })
            results = search.get_dict()
            
            # Extract relevant information
            extracted_data = {
                "search_query": query,
                "location": location,
                "organic_results": []
            }
            
            if "organic_results" in results:
                for result in results["organic_results"][:5]:
                    extracted_data["organic_results"].append({
                        "title": result.get("title", ""),
                        "snippet": result.get("snippet", ""),
                        "link": result.get("link", "")
                    })
            
            return json.dumps(extracted_data, indent=2)
        
        # Option 2: Basic web scraping (fallback)
        else:
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}+{location.replace(' ', '+')}+market+data"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            try:
                response = requests.get(search_url, headers=headers, timeout=10)
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract basic information (limited due to Google's restrictions)
                search_results = {
                    "search_query": query,
                    "location": location,
                    "status": "basic_search_completed",
                    "note": "For better results, configure SERPAPI_KEY in your environment"
                }
                
                return json.dumps(search_results, indent=2)
            
            except Exception as e:
                return json.dumps({
                    "error": f"Web search failed: {str(e)}",
                    "suggestion": "Please provide market data manually or configure SERPAPI_KEY"
                })
    
    except Exception as e:
        return json.dumps({"error": f"Search error: {str(e)}"})

def fetch_financial_data(symbols: str, period: str = "5y") -> str:
    """
    Fetch financial data for companies using yfinance.
    
    Args:
        symbols: Comma-separated stock symbols (e.g., "TSLA,BYDDY,TATAMOTORS.NS")
        period: Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
    
    Returns:
        JSON string with financial data
    """
    try:
        symbol_list = [s.strip() for s in symbols.split(",")]
        financial_data = {
            "symbols": symbol_list,
            "period": period,
            "data": {}
        }
        
        for symbol in symbol_list:
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period=period)
                info = ticker.info
                
                if not hist.empty:
                    financial_data["data"][symbol] = {
                        "company_name": info.get("longName", symbol),
                        "sector": info.get("sector", "Unknown"),
                        "current_price": float(hist['Close'].iloc[-1]) if len(hist) > 0 else 0,
                        "price_history": {
                            "dates": [str(date.date()) for date in hist.index],
                            "prices": [float(price) for price in hist['Close'].values]
                        },
                        "volume_history": [int(vol) for vol in hist['Volume'].values],
                        "market_cap": info.get("marketCap", 0),
                        "pe_ratio": info.get("trailingPE", 0)
                    }
                
            except Exception as e:
                financial_data["data"][symbol] = {"error": f"Failed to fetch data: {str(e)}"}
        
        return json.dumps(financial_data, indent=2)
    
    except Exception as e:
        return json.dumps({"error": f"Financial data fetch error: {str(e)}"})

def analyze_market_trends(data_json: str) -> str:
    """
    Analyze market trends from provided data and generate insights.
    
    Args:
        data_json: JSON string containing market data
    
    Returns:
        JSON string with trend analysis
    """
    try:
        data = json.loads(data_json)
        analysis = {
            "analysis_date": datetime.now().isoformat(),
            "trends": {},
            "insights": [],
            "recommendations": []
        }
        
        # Analyze financial data if present
        if "data" in data and isinstance(data["data"], dict):
            for symbol, symbol_data in data["data"].items():
                if "price_history" in symbol_data and "error" not in symbol_data:
                    prices = symbol_data["price_history"]["prices"]
                    if len(prices) > 1:
                        # Calculate trend metrics
                        price_change = ((prices[-1] - prices[0]) / prices[0]) * 100
                        volatility = np.std(prices) / np.mean(prices) * 100
                        
                        analysis["trends"][symbol] = {
                            "price_change_percent": round(price_change, 2),
                            "volatility_percent": round(volatility, 2),
                            "trend_direction": "bullish" if price_change > 0 else "bearish",
                            "current_price": prices[-1],
                            "price_range": [min(prices), max(prices)]
                        }
                        
                        # Generate insights
                        if price_change > 20:
                            analysis["insights"].append(f"{symbol} shows strong bullish trend with {price_change:.1f}% growth")
                        elif price_change < -20:
                            analysis["insights"].append(f"{symbol} shows bearish trend with {abs(price_change):.1f}% decline")
                        
                        if volatility > 30:
                            analysis["insights"].append(f"{symbol} exhibits high volatility ({volatility:.1f}%)")
        
        # Generate recommendations
        if analysis["trends"]:
            bullish_count = sum(1 for trend in analysis["trends"].values() if trend["trend_direction"] == "bullish")
            total_count = len(analysis["trends"])
            
            if bullish_count / total_count > 0.6:
                analysis["recommendations"].append("Market shows overall positive sentiment - consider growth investments")
            else:
                analysis["recommendations"].append("Market shows mixed signals - consider diversified approach")
        
        return json.dumps(analysis, indent=2)
    
    except Exception as e:
        return json.dumps({"error": f"Analysis error: {str(e)}"})

def create_market_chart(data_json: str, chart_type: str, title: str) -> str:
    """
    Create a chart from market data and return the file path.
    """
    try:
        data = json.loads(data_json)
        
        plt.figure(figsize=(12, 8))
        plt.style.use('seaborn-v0_8')
        
        if chart_type == 'financial_line' and "data" in data:
            # Create financial line chart
            for symbol, symbol_data in data["data"].items():
                if "price_history" in symbol_data and "error" not in symbol_data:
                    dates = pd.to_datetime(symbol_data["price_history"]["dates"])
                    prices = symbol_data["price_history"]["prices"]
                    company_name = symbol_data.get("company_name", symbol)
                    plt.plot(dates, prices, marker='o', linewidth=2, label=company_name)
            
            plt.xlabel("Date")
            plt.ylabel("Stock Price")
            plt.legend()
            plt.xticks(rotation=45)
        
        elif chart_type == 'trend_comparison' and "trends" in data:
            # Create trend comparison chart
            symbols = list(data["trends"].keys())
            price_changes = [data["trends"][symbol]["price_change_percent"] for symbol in symbols]
            
            colors = ['green' if pc > 0 else 'red' for pc in price_changes]
            plt.bar(symbols, price_changes, color=colors, alpha=0.7)
            plt.xlabel("Companies")
            plt.ylabel("Price Change (%)")
            plt.xticks(rotation=45)
            plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        
        elif chart_type == 'market_cap_pie' and "data" in data:
            # Create market cap pie chart
            symbols = []
            market_caps = []
            for symbol, symbol_data in data["data"].items():
                if "market_cap" in symbol_data and symbol_data["market_cap"] > 0:
                    symbols.append(symbol_data.get("company_name", symbol))
                    market_caps.append(symbol_data["market_cap"])
            
            if market_caps:
                plt.pie(market_caps, labels=symbols, autopct='%1.1f%%', startangle=90)
        
        else:
            # Fallback to basic chart types
            if 'x' in data and 'y' in data:
                if chart_type == 'line':
                    plt.plot(data['x'], data['y'], marker='o', linewidth=2)
                elif chart_type == 'bar':
                    plt.bar(data['x'], data['y'], color='skyblue', alpha=0.7)
                plt.xlabel(data.get('xlabel', 'X-axis'))
                plt.ylabel(data.get('ylabel', 'Y-axis'))
        
        plt.title(title, fontsize=14, fontweight='bold')
        plt.tight_layout()
        
        # Save chart
        chart_path = f"chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{chart_type}.png"
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return chart_path
    
    except Exception as e:
        return f"Error creating chart: {str(e)}"

def generate_pdf_report(content: str, charts: str, stats: str, filename: str = "market_report.pdf") -> str:
    """
    Generate a comprehensive PDF report with text, charts, and statistics.
    """
    try:
        # Set filename
        if filename == "market_report.pdf":
            filename = f"market_research_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        # Create PDF document
        doc = SimpleDocTemplate(filename, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=20,
            spaceAfter=30,
            alignment=1
        )
        story.append(Paragraph("Market Research Report", title_style))
        story.append(Spacer(1, 12))
        
        # Date
        date_style = ParagraphStyle('DateStyle', parent=styles['Normal'], fontSize=12, alignment=1)
        story.append(Paragraph(f"Generated on: {datetime.now().strftime('%B %d, %Y')}", date_style))
        story.append(Spacer(1, 20))
        
        # Main content
        content_style = ParagraphStyle('ContentStyle', parent=styles['Normal'], fontSize=11, spaceAfter=12)
        
        sections = content.split('\n\n')
        for section in sections:
            if section.strip():
                story.append(Paragraph(section.strip(), content_style))
                story.append(Spacer(1, 12))
        
        # Add statistics if available
        try:
            stats_data = json.loads(stats)
            if 'error' not in stats_data and stats_data:
                story.append(Paragraph("Statistical Analysis", styles['Heading2']))
                story.append(Spacer(1, 12))
                
                # Create statistics content
                stats_content = ""
                for key, value in stats_data.items():
                    if key not in ['analysis_date']:
                        stats_content += f"<b>{key.replace('_', ' ').title()}:</b> {value}<br/><br/>"
                
                if stats_content:
                    story.append(Paragraph(stats_content, content_style))
                    story.append(Spacer(1, 20))
        except:
            pass
        
        # Add charts if available
        try:
            charts_data = json.loads(charts)
            if isinstance(charts_data, list):
                story.append(Paragraph("Charts and Visualizations", styles['Heading2']))
                story.append(Spacer(1, 12))
                
                for chart_path in charts_data:
                    if os.path.exists(chart_path):
                        img = Image(chart_path, width=6*inch, height=3.6*inch)
                        story.append(img)
                        story.append(Spacer(1, 12))
        except:
            pass
        
        # Build PDF
        doc.build(story)
        
        return f"PDF report generated successfully: {filename}"
    
    except Exception as e:
        return f"Error generating PDF: {str(e)}"

# Create enhanced tool instances
search_tool = FunctionTool(search_market_data)
financial_tool = FunctionTool(fetch_financial_data)
analysis_tool = FunctionTool(analyze_market_trends)
chart_tool = FunctionTool(create_market_chart)
pdf_tool = FunctionTool(generate_pdf_report)

# Enhanced Agents with data fetching capabilities
data_fetcher_agent = Agent(
    name="market_data_fetcher",
    model=model,
    description="Fetch comprehensive market data from multiple sources including web search and financial APIs.",
    instruction="""You are a market data specialist. Your job is to:
    1. Search for market data using the search tool
    2. Fetch financial data for relevant companies using stock symbols
    3. Structure the collected data for analysis
    
    For the search, use specific queries like 'EV market size India 2024', 'electric vehicle sales statistics India'.
    For financial data, use relevant stock symbols (e.g., for Indian EV companies: TATAMOTORS.NS, MAHINDRA.NS, BAJAJ-AUTO.NS).
    
    Always provide structured data that can be used for visualization and analysis.""",
    tools=[search_tool, financial_tool]
)

trend_analyzer_agent = Agent(
    name="trend_analyzer",
    model=model,
    description="Analyze market trends and create visualizations from collected data.",
    instruction="""You are a market trend analyst. Your job is to:
    1. Analyze the market data provided by the data fetcher
    2. Identify key trends, growth patterns, and market dynamics
    3. Create appropriate visualizations (financial_line, trend_comparison, market_cap_pie charts)
    4. Generate insights and recommendations
    
    Use the analysis tool to process data and the chart tool to create visualizations.
    Focus on growth rates, market share changes, and competitive positioning.""",
    tools=[analysis_tool, chart_tool]
)

report_generator_agent = Agent(
    name="report_generator",
    model=model,
    description="Generate comprehensive market research reports with all analysis and visualizations.",
    instruction="""You are a report generation specialist. Your job is to:
    1. Compile all previous analysis into a comprehensive report
    2. Structure the report with executive summary, key findings, market analysis, and recommendations
    3. Include all charts and statistical analysis
    4. Generate a professional PDF report
    
    The report should be business-ready and include actionable insights.""",
    tools=[pdf_tool, chart_tool]
)

# Enhanced multi-agent system
root_agent = SequentialAgent(
    name="enhanced_market_research_pipeline",
    description="Comprehensive market research pipeline with web data fetching and analysis",
    sub_agents=[
        data_fetcher_agent,
        trend_analyzer_agent,
        report_generator_agent
    ]
)
