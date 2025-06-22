# 🧠 DemoAgent – SmartSupply AI

A multi-agent system built with Google's Agent Development Kit (ADK) to analyze regional supply chains and suggest optimizations using LLM orchestration.


🌐 **Live Demo**: [https://demoagent-1.onrender.com](https://demoagent-1.onrender.com)

---

## 🔄 Overview

SmartSupply AI is a multi-agent system designed to automate the analysis and optimization of supply chain logistics. It uses multiple agents built using the ADK to:

* Fetch and interpret market and logistics data
* Evaluate regional risk scores based on product types
* Suggest optimizations
* Generate a summarized report in the ADK web interface

---

## 🎓 Inspiration

The project was inspired by the need for intelligent automation in evaluating complex, global supply chains where logistics, cost, risk, and optimization must be balanced dynamically. Supply chain managers often struggle with fragmented data and decision-making delays. This agent-based system aims to assist decision-makers by providing fast, LLM-powered analysis.

---

## 📦 Built With

* Python 3.12
* Google Agent Development Kit (ADK)
* Gemini 1.5 Flash API (via LiteLlm)
* ADK CLI / Web Interface
* dotenv

---

## 🧰 What it Does

* Accepts a region and product type
* Fetches relevant logistics data
* Analyzes risk factors like cost, delay, regulation
* Suggests optimization strategies for resilience and efficiency
* Generates structured output summarizing the above

---

## 🧠 Architecture Diagram

![Image](https://github.com/user-attachments/assets/9cd5177d-35e1-4500-ba73-4b4b009ea032)

## 🚀 How We Built It

* Developed in **Python** using **Google ADK**
* Leveraged **Google Gemini 1.5 Flash API** with `LiteLlm`
* Created modular agents for each functional step:

  * `fetch_logistics_data`
  * `analyze_risks`
  * `optimize_supply_chain`
  * `generate_supply_chain_report`
* Orchestrated all agents using `SequentialAgent`
* Deployed and tested using the **ADK web interface**

---

## 🚫 Challenges We Ran Into

* Understanding ADK's artifact system and when it is required
* Configuring local ADK environment to run seamlessly
* Mapping realistic risk scores to product-region combinations
* Ensuring proper API key security without requiring service accounts

---

## 🏆 Accomplishments

* End-to-end working agent pipeline using Gemini
* No reliance on cloud storage or external artifact systems
* Fully reproducible setup for local or cloud deployment

---

## 📖 What We Learned

* Building scalable agent pipelines using ADK
* Effective prompt engineering for LLMs in supply chain context
* Using Google Cloud APIs without relying on full service account configuration

---

## ✨ What's Next for SmartSupply AI

* Add PDF generation using GCSArtifactService for final reports
* Introduce BigQuery integration for real-time data fetch
* Expand product/region mappings for more granular risk profiling
* Build a UI frontend for non-technical stakeholders

---

## 🔧 Setup & Testing Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/jayaram9196/DemoAgent.git
cd DemoAgent
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a `.env` file and add your API key:

```dotenv
GOOGLE_API_KEY=your_google_flash_api_key
```

> Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

### 4. Launch ADK Web Interface

```bash
adk web
```

Then navigate to: [http://localhost:8080](http://localhost:8080)


## 🚀 Deployment

🌍 **Web Demo**: [https://demoagent-1.onrender.com](https://demoagent-1.onrender.com)

Use this to interact with the multi-agent system live.

---

## 🧪 Sample Prompts for Testing

**Prompt 1: Smartphones from Shenzhen to Chennai**
```text
Please fetch current logistics data for Xiaomi Redmi Note 13 smartphones shipped from Shenzhen, China to Chennai Port, India.

I need the following information:
- Typical shipping rates (sea freight, 20 ft container or per CBM) from Shenzhen to Chennai Port
- Average customs clearance time at Chennai Port
- Trucking rates and lead times from Chennai Port to Hyderabad
- Common bottlenecks or delays along this route
- Any seasonality that affects demand or logistics for smartphones in South India
```
---

---

## 🏃‍ Hackathon Category

**Category:** Automation of Complex Processes

This system orchestrates agents to analyze complex logistical scenarios and optimize multi-step decision-making.

---


