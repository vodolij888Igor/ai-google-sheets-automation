"""FastAPI entrypoint for AI Google Sheets Automation backend."""

from fastapi import FastAPI, HTTPException

from app.schemas.sheet_schema import AnalyzeSheetRowsRequest, AnalyzeSheetRowsResponse
from app.services.sheet_service import SheetServiceError, analyze_rows

app = FastAPI(
    title="AI Google Sheets Automation API",
    version="0.1.0",
    description=(
        "Portfolio backend API that accepts simulated Google Sheets rows "
        "and returns structured AI-like analysis."
    ),
)


@app.get("/health", tags=["system"])
def health_check() -> dict[str, str]:
    """Basic health endpoint for quick environment verification."""
    return {"status": "ok"}


@app.post("/analyze-sheet-rows", response_model=AnalyzeSheetRowsResponse, tags=["analysis"])
def analyze_sheet_rows(payload: AnalyzeSheetRowsRequest) -> AnalyzeSheetRowsResponse:
    """Analyze incoming sheet rows using OpenAI and return structured output."""
    try:
        analyzed_rows = analyze_rows(payload.rows)
    except SheetServiceError as exc:
        # Service errors are intentionally converted to HTTP-level status codes.
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc

    return AnalyzeSheetRowsResponse(
        sheet_name=payload.sheet_name,
        analyzed_rows=analyzed_rows,
    )
