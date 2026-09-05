# 💊 PharmaLens

> An AI-powered medicine information and pharmacy discovery agent built using a ReAct architecture.

PharmaLens is an AI agent that helps users find reliable, easy-to-understand information about medicines and discover pharmacy listings based on a medicine and location.

The project combines an LLM with external tools to retrieve information instead of relying entirely on the model's internal knowledge.

## ✨ Features

- 🔎 **Medicine Information Search**
  - Searches RxNorm to identify medicines.
  - Retrieves educational information from MedlinePlus.
  - Provides source-backed medicine information.

- 🏪 **Pharmacy Discovery**
  - Searches the web for pharmacies and medicine listings.
  - Supports location-based searches.
  - Uses Tavily for web search.
  - Clearly distinguishes web listings from confirmed real-time stock.

- 🤖 **ReAct Agent**
  - Uses an LLM to decide when a tool is required.
  - Executes external tools based on the user's request.
  - Processes tool results before generating the final response.

- 🔐 **Secure API Configuration**
  - API keys are stored in environment variables.
  - `.env` is excluded from version control.

- 🛡️ **Medical Safety**
  - Designed for general medical education.
  - Does not diagnose medical conditions.
  - Does not prescribe medicines.
  - Does not provide personalized treatment plans or dosage recommendations.

## 🏗️ Architecture

```text
                         USER
                           │
                           ▼
                  ┌─────────────────┐
                  │   ReAct Agent   │
                  │                 │
                  │ OpenRouter LLM  │
                  └────────┬────────┘
                           │
                    Tool Selection
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
   ┌─────────────────────┐   ┌─────────────────────┐
   │ Medical Information │   │ Pharmacy Discovery  │
   │       Tool          │   │       Tool          │
   └──────────┬──────────┘   └──────────┬──────────┘
              │                         │
       ┌──────┴──────┐             ┌────┴─────┐
       ▼             ▼             ▼          │
    RxNorm      MedlinePlus      Tavily       │
       │             │             │          │
       └─────────────┴─────────────┴──────────┘
                           │
                           ▼
                    Tool Observations
                           │
                           ▼
                     Final Response

```

## 💻 Tech Stack
### Backend
- Python
- FastAPI
- OpenAI Python SDK
- python-dotenv
### AI
- OpenRouter
- openai/gpt-5-nano
- ReAct-style tool calling
### External APIs
- RxNorm API
- MedlinePlus Connect
- Tavily Search API
### Testing
- Pytest

---

## ⚙️ Setup
1. Clone the repository
`git clone https://github.com/berwincr/PharmaLens.git`
`cd PharmaLens`
2. Create a virtual environment
`python -m venv backend/venv`
3. Activate the virtual environment
Windows PowerShell
`backend\venv\Scripts\Activate.ps1`
Windows CMD
`backend\venv\Scripts\activate`
4. Install dependencies
`pip install -r backend/requirements.txt`
5. Configure environment variables
    - Create:
         `backend/.env`
    - Add:
         `OPENROUTER_API_KEY=your_openrouter_api_key`
         `TAVILY_API_KEY=your_tavily_api_key`

          RXNORM_BASE_URL=https://rxnav.nlm.nih.gov/REST
          MEDLINEPLUS_CONNECT_URL=https://connect.medlineplus.gov/service

> Never commit your .env file or expose your API keys publicly.

6. Run the agent

From the backend directory:

    `cd backend`
    `python agent/react-agent.py`


## 🧪 Running Tests

From the project root: `pytest`

You can also run the individual medical search test: `python backend/tests/test_medical_search.py`

### Disclaimer

PharmaLens provides general educational information and should not be used as a substitute for professional medical advice, diagnosis, or treatment.
