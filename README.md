# AI Cybersecurity Assistant

A local AI-powered cybersecurity analysis assistant that uses a locally hosted Large Language Model (LLM) to analyze security events and return structured cybersecurity assessments.

The application combines:

- FastAPI for the backend API
- Streamlit for the web interface
- Pydantic for structured response validation
- A locally hosted LLM for cybersecurity reasoning
- OpenAI-compatible API communication

The application is designed to analyze security events using an evidence-first approach. It separates observed facts from inferences and unknown information, estimates severity and confidence, and provides defensive recommendations.

## Features

- Threat identification
- Severity assessment
- Confidence estimation
- Observed-fact extraction
- Security inferences
- Identification of unknown information
- Defensive recommendations
- Structured JSON output
- Pydantic response validation
- Local LLM inference
- Streamlit web interface
- FastAPI backend
- Session-based recent analysis history

## Architecture

```text
User
  |
  v
Streamlit Frontend
  |
  v
FastAPI Backend
  |
  v
Cybersecurity Analyzer
  |
  v
OpenAI-Compatible Local LLM API
  |
  v
Local Language Model
  |
  v
Structured JSON Analysis
  |
  v
Pydantic Validation
  |
  v
Streamlit Results
```

The current implementation uses **LM Studio** as the local LLM server.

## Important: The Local LLM Is Not Included

The GitHub repository contains the application code, but it does **not** contain the locally downloaded language model.

The current development setup uses:

```text
qwen/qwen3.5-9b
```

The model files are stored locally by the LLM application and are not part of this repository.

Anyone cloning this project must:

1. Install a local LLM runtime.
2. Download a compatible model.
3. Start the local LLM server.
4. Configure the application to communicate with that server.
5. Start the FastAPI backend.
6. Start the Streamlit frontend.

Large model files should not be committed to a normal Git repository.

## Recommended Local LLM Setup: LM Studio

The current version of this project is configured for **LM Studio**.

LM Studio provides a graphical interface for downloading and running local open-source language models and can expose an OpenAI-compatible API.

Download LM Studio from:

https://lmstudio.ai/

### 1. Install LM Studio

Install LM Studio and open it.

### 2. Download a compatible model

Inside LM Studio:

1. Open the model/download section.
2. Search for a suitable instruction/chat model.
3. Download the model.

The current development environment uses:

```text
qwen/qwen3.5-9b
```

You may use another compatible instruction-following model if desired. If you use another model, update the `MODEL` value in `analyzer.py`.

### 3. Start the local model server

Start the selected model and enable the local API server in LM Studio.

The current application expects the OpenAI-compatible API at:

```text
http://localhost:1234/v1
```

The application sends requests to:

```text
http://localhost:1234/v1/chat/completions
```

Make sure the server is running before starting the application.

## Local LLM Configuration

The current `analyzer.py` contains:

```python
BASE_URL = "http://localhost:1234/v1"
MODEL = "qwen/qwen3.5-9b"
```

`BASE_URL` identifies the local LLM API server and `MODEL` identifies the model exposed by that server.

If another user downloads a different model, they should change the `MODEL` value to match the model available in their local server.

## Running the Project

### Requirements

Recommended environment:

- Python 3.12+
- Git
- LM Studio or another OpenAI-compatible local LLM server
- A locally downloaded instruction/chat model
- Sufficient RAM/VRAM for the selected model

Python dependencies are listed in `requirements.txt`.

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd ai-cybersecurity-assistant
```

Replace `<YOUR_GITHUB_REPOSITORY_URL>` with the actual GitHub repository URL.

### 2. Create a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

You should see `(.venv)` at the beginning of the PowerShell prompt.

### 3. Install dependencies

With the virtual environment activated:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Start the local LLM

Before starting the application, make sure LM Studio is running, the local server is enabled, and the selected model is loaded.

Default base URL:

```text
http://localhost:1234/v1
```

### 5. Start the FastAPI backend

Open a PowerShell terminal in the project directory and activate the environment if needed:

```powershell
.\.venv\Scripts\Activate.ps1
```

Then start FastAPI:

```powershell
uvicorn app:app --reload
```

The API should be available at:

```text
http://127.0.0.1:8000
```

Analysis endpoint:

```text
http://127.0.0.1:8000/analyze
```

### 6. Start the Streamlit frontend

Open a second PowerShell terminal, navigate to the project, and activate the virtual environment:

```powershell
cd "C:\path\to\ai-cybersecurity-assistant"
.\.venv\Scripts\Activate.ps1
```

Run:

```powershell
streamlit run frontend.py
```

Streamlit will normally provide:

```text
http://localhost:8501
```

Open that address in your browser.

## Running Components

The complete application uses three running components:

```text
Local LLM
   |
   | localhost:1234
   v
FastAPI
   |
   | localhost:8000
   v
Streamlit
   |
   | localhost:8501
   v
User
```

All three components must be running for the complete workflow to function.

## Testing the Backend

You can test the FastAPI endpoint directly from PowerShell:

```powershell
Invoke-RestMethod `
  -Uri "http://127.0.0.1:8000/analyze" `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"event":"A Windows computer received 500 failed login attempts from the same external IP address within 5 minutes."}' |
  ConvertTo-Json -Depth 10
```

The exact analysis values depend on the local model and its generated response.

## Structured Analysis

The analyzer validates the model response with Pydantic.

The expected structure contains exactly these fields:

```text
threat
severity
confidence
observed_facts
inferences
unknowns
recommendations
```

`severity` must be one of:

```text
Low
Medium
High
Critical
```

`confidence` must be a number from `0.0` to `1.0`.

The remaining list fields must contain arrays of strings.

This validation helps prevent malformed LLM output from being silently accepted as a valid cybersecurity assessment.

## Evidence-First Analysis

The system prompt instructs the local LLM to distinguish between three categories of information.

### Observed Facts

Information explicitly contained in the security event.

Example:

```text
500 failed login attempts occurred.
```

### Inferences

Reasonable conclusions derived from the available evidence.

Example:

```text
The activity is consistent with an automated brute-force attack.
```

### Unknowns

Information that cannot be determined from the available event.

Example:

```text
The identity of the attacker is unknown.
```

This separation helps reduce the risk of presenting assumptions as confirmed facts.

## Project Structure

```text
ai-cybersecurity-assistant/
│
├── .env
├── .gitignore
├── analyzer.py
├── app.py
├── frontend.py
├── README.md
└── requirements.txt
```

### `analyzer.py`

Responsible for communicating with the local LLM, constructing the cybersecurity analysis request, parsing JSON, and validating the response with Pydantic.

### `app.py`

Provides the FastAPI backend and exposes the `/analyze` endpoint.

### `frontend.py`

Provides the Streamlit user interface. It displays the security event input, analysis results, and recent analyses.

### `requirements.txt`

Contains the Python dependencies required by the application.

### `.env`

Reserved for environment-specific configuration or future secrets. The current version does not require an API key because the LLM is running locally.

## Using Another OpenAI-Compatible Local LLM Server

The analyzer communicates with the model through an OpenAI-compatible chat-completions API.

The current configuration is:

```python
BASE_URL = "http://localhost:1234/v1"
MODEL = "qwen/qwen3.5-9b"
```

A different OpenAI-compatible local server can potentially be used by changing these values to match that server and its model name.

## Using Ollama

Ollama can expose an OpenAI-compatible API. A typical compatible base URL is:

```text
http://localhost:11434/v1
```

For an Ollama setup, the configuration could be changed to something like:

```python
BASE_URL = "http://localhost:11434/v1"
MODEL = "your-ollama-model"
```

The model must first be downloaded in Ollama, for example:

```bash
ollama pull <model-name>
```

Then make sure Ollama is running before starting FastAPI.

Exact model names depend on the selected model and local server.

## Git and Security

Do not commit local environments, cache files, model files, or secrets to GitHub.

Typical entries to ignore include:

```text
.venv/
.env
__pycache__/
*.pyc
```

If API keys or other secrets are added to `.env`, never commit them.

Use `.env.example` to document future environment variables without exposing secret values.

## Troubleshooting

### Connection refused on port 1234

The local LLM server is probably not running. Check LM Studio and make sure its local server is enabled.

### Model not found

The model name in `MODEL` must match a model available to the selected local LLM server.

### FastAPI starts but analysis fails

Check that the local LLM server is running, the model is loaded, the API address is correct, the model name is correct, and the server exposes a compatible `/chat/completions` endpoint.

### Streamlit cannot connect to the API

Make sure FastAPI is running with:

```powershell
uvicorn app:app --reload
```

The frontend expects the backend at:

```text
http://127.0.0.1:8000/analyze
```

### LLM returns invalid JSON

The analyzer expects the LLM to return JSON containing the required fields. Different models may follow strict JSON instructions with different levels of reliability.

## Privacy

A major advantage of this architecture is that cybersecurity events can be analyzed locally:

```text
Security Event
      |
      v
Local FastAPI
      |
      v
Local LLM
```

With the default setup, events do not need to be sent to an external commercial AI API. Users should still review the privacy and telemetry settings of their chosen local LLM software.

## Limitations

This project is a prototype cybersecurity analysis assistant, not an autonomous Security Operations Center system.

The model can make incorrect inferences, misclassify events, or estimate confidence incorrectly. Results depend on the quality of the supplied event and the selected local model.

The application does not automatically execute defensive actions against systems. Human verification should be used for important security decisions.

## Future Improvements

Potential future enhancements include:

- Environment-variable based LLM configuration
- Support for multiple local LLM providers
- Persistent analysis history
- Authentication and authorization
- Database-backed event storage
- Log-file ingestion
- SIEM integration
- MITRE ATT&CK mapping
- Threat intelligence integration
- IOC extraction
- Detection-rule generation
- PDF/CSV report generation
- Streaming LLM responses
- Automated evaluation against cybersecurity datasets
- Containerized deployment

## Development Philosophy

The project separates the user interface, backend API, and analysis engine:

```text
Frontend
   |
Backend API
   |
Analysis Logic
   |
Local AI Model
```

This makes individual components easier to replace or extend without rebuilding the entire application.

The local LLM is treated as one analysis component of the application rather than the entire application itself.

## License

Add your preferred license here before publishing the repository.

For example:

```text
MIT License
```

## Author

Developed as an AI and cybersecurity portfolio project.

Built with:

- Python
- FastAPI
- Streamlit
- Pydantic
- Requests
- Local Large Language Models
- OpenAI-compatible APIs
