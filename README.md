# Automated Outreach Pipeline

An end-to-end command-line automation tool that accepts a seed company domain, discovers lookalikes, sources executive decision-makers, resolves work emails, and schedules personalized email outreach[cite: 2].

## 🏗️ Project Architecture
The project uses an **Interface-Driven Design** pattern to isolate third-party service logic from the core pipeline orchestrator[cite: 2]:

- `main.py`: The single CLI application managing pipeline flow and data hand-offs[cite: 2].
- `services/ocean.py`: Handles lookalike company expansion (Stage 1)[cite: 2].
- `services/prospeo.py`: Targets decision-makers via live API filtering (Stage 2)[cite: 2, 3].
- `services/eazyreach.py`: Resolves LinkedIn profiles to corporate emails (Stage 3)[cite: 2].
- `services/brevo.py`: Handles automated transactional email dispatching (Stage 4)[cite: 2].

## 🛡️ Defensive Engineering & Mock Fallbacks
To bypass external vendor authentication delays and keep credentials secure during staging, the service layer is built with native local mock environments[cite: 2]. 

If an API key is absent from the `.env` file (such as during Stage 1 and Stage 3 evaluation testing), the application gracefully falls back to isolated testing frameworks[cite: 2]. This ensures the pipeline's automation logic can be run and verified end-to-end right out of the box[cite: 2].

## 🚀 How to Run

1. Clone the repository and navigate into the directory.
2. Install dependencies:
```bash
   pip install -r requirements.txt
