# AI Google Sheets Automation - FastAPI Backend

## Project Overview
This project is a portfolio-ready backend API that simulates Google Sheets automation with AI-style analysis.
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
|-- requirements.txt
`-- README.md
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
      "summary": "Customer says the product is useful but onboarding is confusing.",
      "category": "product_feedback",
      "priority": "medium",
      "recommended_action": "Document feedback and improve product guidance."
    }
  ]
}
```

## Current Limitations (Version 1)
- Uses deterministic placeholder logic (no real LLM call yet).
- No direct Google Sheets API integration yet.
- Classification and recommendations are rule-based and simplistic.
- No authentication, persistence, or background processing.

## Future Improvements
- Integrate OpenAI or another LLM provider for higher-quality analysis.
- Connect directly to Google Sheets API for scheduled or event-driven ingestion.
- Add auth and role-based access for production deployment.
- Add database storage for analysis history and analytics dashboards.
- Add tests (unit + integration) and CI/CD pipeline.

## Why This Project Matters for Portfolio
This project demonstrates:
- API design for automation workflows
- schema-first request/response validation
- service-layer architecture that is ready for AI provider integration
- practical business framing, not just technical implementation
