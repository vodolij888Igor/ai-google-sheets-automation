# AI Google Sheets Automation - FastAPI Backend

[![Tests](https://github.com/vodolij888Igor/ai-google-sheets-automation/actions/workflows/tests.yml/badge.svg)](https://github.com/vodolij888Igor/ai-google-sheets-automation/actions/workflows/tests.yml)

## Project Overview
This project is a portfolio-ready backend API that simulates Google Sheets automation with real OpenAI-powered analysis.
It accepts rows from a sheet-like JSON payload and returns structured insights for each row.

The purpose is to demonstrate practical backend API development for an **AI Automation & Integration Developer** profile, with clear pathways to evolve into a full-stack AI product.

## Business Use Case
Teams often collect customer feedback in Google Sheets, but manually reviewing rows is slow and inconsistent.
This API shows how sheet rows can be processed automatically into:
- concise summaries
- categories
- priority levels
- recommended actions

This improves operational visibility and helps teams prioritize what to fix first.

## Tech Stack
- **Python**
- **FastAPI**
- **Pydantic**
- **Uvicorn**
- **OpenAI API**

## Project Structure
```text
.
|-- app/
|   |-- main.py
|   |-- schemas/
|   |   `-- sheet_schema.py
|   `-- services/
|       `-- sheet_service.py
|-- .env.example
|-- .gitignore
|-- pytest.ini
|-- requirements.txt
|-- tests/
`-- README.md
```

## Running Tests

Tests mock the OpenAI client so they do not call the real API and do not require a valid `OPENAI_API_KEY`.

```powershell
pip install -r requirements.txt
pytest
```

## Setup Instructions
1. Create and activate a virtual environment:
   - Windows (PowerShell):
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```
2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
3. (Optional) Copy `.env.example` to `.env` and adjust values.
   - Add your key:
     ```env
     OPENAI_API_KEY=your_openai_api_key_here
     ```
4. Run the API server:
   ```powershell
   uvicorn app.main:app --reload --port 8000
   ```
5. Open API docs:
   - Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
   - ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Required Endpoint
### `POST /analyze-sheet-rows`

### Sample Request
```json
{
  "sheet_name": "Customer Feedback",
  "rows": [
    {
      "row_id": 1,
      "text": "Customer says the product is useful but onboarding is confusing."
    }
  ]
}
```

### Sample Response
```json
{
  "sheet_name": "Customer Feedback",
  "analyzed_rows": [
    {
      "row_id": 1,
      "summary": "Customer finds the product useful but has onboarding confusion.",
      "category": "customer_feedback",
      "priority": "medium",
      "recommended_action": "Improve onboarding instructions and update help content."
    }
  ]
}
```

### Supported AI Labels
- `category`: `customer_feedback`, `sales_lead`, `invoice_processing`, `support_request`, `operations`, `other`
- `priority`: `low`, `medium`, `high`

## Screenshot

The screenshot below shows a successful POST /analyze-sheet-rows request in FastAPI Swagger UI with a 200 response.

![Swagger UI successful sheet analysis response](docs/images/swagger-sheet-analysis-code-200.png)

## Current Limitations (Version 1)
- Requires a valid `OPENAI_API_KEY` in `.env`.
- No direct Google Sheets API integration yet.
- AI output quality depends on prompt/model behavior and input quality.
- No authentication, persistence, or background processing.

## Future Improvements
- Add retries/circuit breaking and stronger observability around AI calls.
- Connect directly to Google Sheets API for scheduled or event-driven ingestion.
- Add auth and role-based access for production deployment.
- Add database storage for analysis history and analytics dashboards.
- Add CI/CD pipeline (tests are included locally with pytest).

## Why This Project Matters for Portfolio
This project demonstrates:
- API design for automation workflows
- schema-first request/response validation
- service-layer architecture that is ready for AI provider integration
- practical business framing, not just technical implementation
