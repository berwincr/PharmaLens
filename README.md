# 💊 PharmaLens

> An AI-powered medicine information and pharmacy discovery agent built using the ReAct architecture.

PharmaLens is an AI agent that helps users obtain reliable general information about medicines, search for pharmacy availability information, and create medication reminders.

The project combines an **LLM, three tools, ReAct reasoning, and long-term memory** to demonstrate the core concepts of an AI agent.

---

## 🚀 Key Components

### 🤖 LLM

PharmaLens uses:

- **OpenRouter** — LLM API provider
- **Model:** `openai/gpt-5-nano`
- **OpenAI Python SDK** — used to communicate with OpenRouter

The LLM acts as the decision-making component of the agent. It determines which tool should be used based on the user's request and generates the final response from the retrieved information.

---

## 🛠️ Three Tools

PharmaLens provides three main tools:

### 1. 🔎 Medical Information Search

**Sources:**
- RxNorm
- MedlinePlus

The tool identifies medicines using RxNorm and retrieves general educational information from MedlinePlus.

Example:

```text
User:
What is paracetamol?

Agent:
→ Medical Information Search
→ RxNorm
→ MedlinePlus
→ Final Answer
```

### 2. 💊 Pharmacy Search

**Technology:**
- Tavily Search API

The tool searches the web for pharmacies, medicine listings, and availability information based on the medicine and location provided by the user.

Example:

```
User:
Find pharmacies that list paracetamol in Chennai.

Agent:
→ Pharmacy Search
→ Tavily
→ Pharmacy listings/search results
→ Final Answer

```

> Pharmacy search results are web search results and are not guaranteed to represent real-time stock. Users should verify availability directly with the pharmacy.

### 3. ⏰ Medication Reminder

The reminder tool allows users to create, view, and cancel medication reminders.

It uses:

- JSON persistent storage
- APScheduler

Example:

```
User:
Remind me to take Vitamin D at 9 PM every day.

Agent:
→ Medication Reminder Tool
→ Save reminder
→ Scheduler
→ Reminder triggered
```
> The agent does not decide medication schedules. It only stores and triggers schedules explicitly provided by the user.

---

## 🧠 Long-Term Memory

PharmaLens implements long-term persistent memory using JSON storage.

Memory is stored in:

`backend/data/memory.json`

The agent can:

- Save user-provided preferences/information
- Retrieve previously stored information
- Retain information after the agent is restarted

Example:
```
Session 1

User:
Remember that I prefer bullet-point explanations.

Agent:
→ Save Memory
→ memory.json

After restarting:

Session 2

User:
What do you remember about me?

Agent:
→ Recall Memory
→ Retrieves saved information
Memory Architecture
             User
               │
               ▼
          ReAct Agent
               │
        ┌──────┴──────┐
        ▼             ▼
   Save Memory    Recall Memory
        │             │
        └──────┬──────┘
               ▼
          memory.json
               │
               ▼
      Persistent Long-Term
             Memory

```
---

## 🔄 ReAct Architecture

PharmaLens follows a ReAct-style agent workflow:

                    User
                      │
                      ▼
                  ┌───────┐
                  │  LLM  │
                  └───┬───┘
                      │
                 Decide Action
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
     Medical       Pharmacy    Reminder
      Search        Search       Tool
          │           │           │
          └───────────┼───────────┘
                      ▼
                  Observation
                      │
                      ▼
                     LLM
                      │
                      ▼
                Final Answer

The agent can select the appropriate tool based on the user's request.

---
### Technology stack

| Category        | Technology           |
| --------------- | -------------------- |
| LLM             | GPT-5 Nano           |
| LLM Provider    | OpenRouter           |
| Agent Pattern   | ReAct                |
| Medical Search  | RxNorm + MedlinePlus |
| Web Search      | Tavily               |
| Reminder        | APScheduler          |
| Memory          | JSON                 |
| Backend         | Python               |
| API Framework   | FastAPI              |
| Version Control | Git + GitHub         |

---
## ⚙️ Setup
1. Clone the repository `git clone https://github.com/berwincr/PharmaLens.git`

Move into the project: `cd PharmaLens`

2. Move into the backend `cd backend`

3. Create a virtual environment `python -m venv venv`
   
      Windows PowerShell
   `.\venv\Scripts\Activate.ps1`

You should see: `(venv)` in your terminal.

4. Install dependencies `pip install -r requirements.txt`

---

## 🔐 Environment Variables

Create a file named: `backend/.env`

Add the following:

     RXNORM_BASE_URL=https://rxnav.nlm.nih.gov/REST

     MEDLINEPLUS_CONNECT_URL=https://connect.medlineplus.gov/service

     OPENROUTER_API_KEY=your_openrouter_api_key

     TAVILY_API_KEY=your_tavily_api_key

  > A .env.example file is provided for your reference

---

## ▶️ Running PharmaLens

All commands below should be executed from: `backend/` with the virtual environment activated.

### Run the ReAct Agent
`python -m agent.react_agent`

The agent can then be tested with queries such as:

     What is paracetamol?
     Find pharmacies listing paracetamol in Chennai.
     Remind me to take Vitamin D at 9 PM every day.
     What do you remember about me?
     
### Run the Reminder Scheduler

**The scheduler runs separately from the agent.**

Open another terminal.

Navigate to: `cd PharmaLens/backend`

Activate the virtual environment: `.\venv\Scripts\Activate.ps1`

Then run: `python -m scheduler.reminder_scheduler`

You should see:

     Medication reminder scheduler started.

The scheduler checks stored reminders and triggers them when their scheduled time is reached.

### 🧪 Testing
- Test Medical Search
`python tests/test_medical_search.py`

- Test Pharmacy Search
`python tools/pharmacy_search.py`

- Test Medication Reminder
`python tools/medicine_reminder.py`

- Test Memory
`python -m memory.memory_manager`

---

### ⚠️ Disclaimer

PharmaLens is an educational project.

It is not a substitute for professional medical advice, diagnosis, or treatment.

Always consult a qualified healthcare professional for personal medical decisions.



