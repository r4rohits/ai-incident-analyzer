# AI Incident Analyzer

A FastAPI application that parses software incident reports, builds structured prompts, and uses configurable AI providers to generate validated incident analyses.

## Features

- Validates incident input using Pydantic.
- Normalizes incident messages and extracts keywords.
- Builds prompts with explicit diagnostic and safety instructions.
- Supports multiple AI providers: OpenAI and Google Gemini.
- Uses a provider factory to select the configured AI provider.
- Defines a common `AIProvider` contract for provider implementations.
- Validates AI-generated analysis using the `AnalysisResult` Pydantic model.
- Returns controlled HTTP errors for configuration and provider failures.
- Includes automated tests for parsing, prompt construction, provider selection, service orchestration, model validation, and API error handling.

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
      +----> AIProviderFactory
                  |
                  v
              AIProvider
                  |
          +-------+-------+
          |               |
          v               v
      LLMService     GeminiService
          |               |
          v               v
       OpenAI API      Gemini API
          |               |
          +-------+-------+
                  |
                  v
            AnalysisResult
                  |
                  v
              API Response
```

## Requirements

- Python 3.10 or compatible.
- An API key for at least one supported provider.
- An available model for the selected provider.

Supported providers:

- OpenAI
- Google Gemini

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/r4rohits/ai-incident-analyzer.git
cd ai-incident-analyzer
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

Copy `.env.example` to `.env`.

Configure the provider you want to use.

#### OpenAI

```dotenv
AI_PROVIDER=openai
OPENAI_API_KEY=your_api_key_goes_here
OPENAI_MODEL=your_available_model
```

#### Google Gemini

```dotenv
AI_PROVIDER=gemini
GEMINI_API_KEY=your_gemini_key_here
GEMINI_MODEL=your_available_model
```

Only the credentials for the selected provider are required.

Never commit `.env` or share API credentials publicly.

### 5. Run the application

```powershell
uvicorn app.main:app --reload
```

Open the interactive API documentation:

http://127.0.0.1:8000/docs

## API Endpoint

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

The AI-generated analysis is advisory. Its conclusions and confidence score are not guaranteed to be correct. Recommended actions are not automatically executed.

## Error Handling

- `503 Service Unavailable`: AI analysis is not configured.
- `502 Bad Gateway`: The AI provider failed or returned an unusable response.

## Run Tests

```powershell
python -m pytest -v
```

The automated test suite uses mocked AI provider responses. A separate live Gemini API request has also been successfully tested.

## Current Limitations

- The parser uses basic normalization and stop-word filtering.
- AI analysis quality and confidence calibration have not yet been evaluated systematically.
- Confidence scores are model-generated and are not statistically calibrated.
- Authentication, rate limiting, production deployment, and monitoring have not yet been implemented.

## Security

- Keep API credentials in environment variables.
- Never commit `.env`.
- Treat incident messages as untrusted input.
- Validate model output before using it.
- Review AI recommendations before taking operational action.

## License

No license has been selected yet. Add a license before explicitly granting others permission to reuse or distribute this project.
