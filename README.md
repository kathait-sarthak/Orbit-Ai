# 🚀 Orbit-AI (V3.0-RESILIENT)
### The Agentic Co-Founder for Windows PowerShell.

Orbit-AI is a reasoning-based shell engine that transforms natural language prompts into fully-structured, multi-environment codebases. Built to handle complex directory logic, dependency management, and server-side resilience.



## ✨ Key Features
* **V3.0 Resilience:** Built-in exponential backoff to handle high-demand AI server spikes (503/429).
* **PowerShell Hardened:** Native support for Windows directory logic and semicolon command chaining.
* **Multi-Stack Agent:** Automatically manages `npm`, `pip`, and `venv` in a single deployment cycle.
* **Project Manifest:** Every build is automatically logged for audit and recovery.

## 🛠️ Installation
1. Clone the repo: `git clone https://github.com/YOUR_USERNAME/orbit-ai.git`
2. Install dependencies: `npm install`
3. Add your `.env` file with `GEMINI_API_KEY`.

## 🕹️ Quick Start
Run the engine:
```powershell
npm start

## Try this prompt:

"Create a folder 'orbit_api'. Set up a venv, install 'flask', and create a 'hello.py' that returns JSON."
