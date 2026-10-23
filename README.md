# AI Incident Analyzer

A FastAPI application that parses software incident reports, builds a structured prompt, and uses an AI model to generate a structured incident analysis.

## Features

- Validates incident input using Pydantic.
- Normalizes incident messages and extracts keywords.
- Builds prompts with explicit diagnostic and safety instructions.
- Requests structured analysis from the OpenAI API.
- Validates analysis output using an `AnalysisResult` model.
- Returns controlled HTTP errors for configuration and provider failures.
- Includes automated tests for parsing, prompt construction, service orchestration, model validation, and API error handling.

## Architecture

```text
Incident Request
      |
      v
FastAPI Router
      |
      v
IncidentService
      |
      +----> Parser
      |
      +----> PromptBuilder
      |
      +----> LLMService
                  |
                  v
              OpenAI API
                  |
                  v
          AnalysisResult
                  |
                  v
             API Response
```

## Requirements

- Python 3.10 or compatible
- An OpenAI API key
- An OpenAI model available to your API account

## Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd incident-analyser
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

For development and testing:

```powershell
python -m pip install -r requirements-dev.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env` and set your own API key and an available model.

Never commit `.env` or share your API key publicly.

### 5. Run the application

```powershell
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` to explore the API.

## API endpoint

### `POST /incidents/analyze`

Example request:

```json
{
  "service": "payment-service",
  "severity": "ERROR",
  "message": "Database connection was lost after 15 seconds",
  "count": 5
}
```

The response contains:

- `likely_issue`
- `possible_impact`
- `recommended_action`
- `confidence`
- `missing_information`

The AI-generated analysis is advisory. Its conclusions and confidence score are not guaranteed to be correct, and recommended actions are not automatically executed.

## Error handling

- `503 Service Unavailable`: AI analysis is not configured.
- `502 Bad Gateway`: The AI provider failed or returned an unusable response.

## Run tests

```powershell
python -m pytest -v
```

## Current limitations

- The parser uses basic normalization and stop-word filtering.
- AI analysis quality and confidence calibration have not yet been evaluated systematically.
- Automated tests mock the LLM; a real API integration test is still required.
- Authentication, rate limiting, production deployment, and monitoring have not yet been implemented.

## Security

- Keep API credentials in environment variables.
- Do not commit `.env`.
- Treat incident messages as untrusted input.
- Validate model output before using it.
- Review AI recommendations before taking operational action.

## License

No license has been selected yet. Add a license before explicitly granting others permission to reuse or distribute this project.
