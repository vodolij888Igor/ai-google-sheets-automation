"""Service layer for analyzing simulated sheet rows with OpenAI."""

import json
import os
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

from app.schemas.sheet_schema import AnalyzedRow, SheetRowInput

load_dotenv()

ALLOWED_CATEGORIES = {
    "customer_feedback",
    "sales_lead",
    "invoice_processing",
    "support_request",
    "operations",
    "other",
}
ALLOWED_PRIORITIES = {"low", "medium", "high"}


class SheetServiceError(Exception):
    """Known service-layer error that can be mapped to HTTP errors."""

    def __init__(self, message: str, status_code: int) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code


def _build_prompt(row_text: str) -> str:
    """Create a clear instruction prompt for structured row analysis."""
    return f"""
Analyze the following spreadsheet row text and return ONLY valid JSON.

Row text:
{row_text}

Required JSON shape:
{{
  "summary": "short concise summary",
  "category": "one of customer_feedback, sales_lead, invoice_processing, support_request, operations, other",
  "priority": "one of low, medium, high",
  "recommended_action": "clear next action"
}}
"""


def _extract_json_object(content: str) -> dict[str, Any]:
    """Parse JSON object from model output."""
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        start = content.find("{")
        end = content.rfind("}")
        if start == -1 or end == -1 or start >= end:
            raise SheetServiceError(
                "OpenAI returned an invalid non-JSON response for row analysis.",
                status_code=502,
            ) from None
        try:
            return json.loads(content[start : end + 1])
        except json.JSONDecodeError as exc:
            raise SheetServiceError(
                "OpenAI returned malformed JSON for row analysis.",
                status_code=502,
            ) from exc


def _normalize_analysis(parsed: dict[str, Any]) -> dict[str, str]:
    """Validate and normalize model output values."""
    summary = str(parsed.get("summary", "")).strip()
    category = str(parsed.get("category", "other")).strip().lower()
    priority = str(parsed.get("priority", "medium")).strip().lower()
    recommended_action = str(parsed.get("recommended_action", "")).strip()

    if not summary:
        summary = "No summary provided by model."
    if category not in ALLOWED_CATEGORIES:
        category = "other"
    if priority not in ALLOWED_PRIORITIES:
        priority = "medium"
    if not recommended_action:
        recommended_action = "Review this row manually."

    return {
        "summary": summary,
        "category": category,
        "priority": priority,
        "recommended_action": recommended_action,
    }


def _analyze_single_row(client: OpenAI, row_text: str) -> dict[str, str]:
    """Call OpenAI for one row and return normalized structured data."""
    try:
        completion = client.responses.create(
            model="gpt-4o-mini",
            input=[{"role": "user", "content": _build_prompt(row_text)}],
            temperature=0.2,
        )
    except Exception as exc:
        raise SheetServiceError(
            f"OpenAI API call failed: {exc}",
            status_code=502,
        ) from exc

    content = completion.output_text.strip() if completion.output_text else ""
    if not content:
        raise SheetServiceError(
            "OpenAI returned an empty response for row analysis.",
            status_code=502,
        )

    parsed = _extract_json_object(content)
    return _normalize_analysis(parsed)


def analyze_rows(rows: list[SheetRowInput]) -> list[AnalyzedRow]:
    """Analyze each row by calling OpenAI and returning validated output."""
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise SheetServiceError(
            "OPENAI_API_KEY is missing. Set it in your .env file before calling this endpoint.",
            status_code=503,
        )

    client = OpenAI(api_key=api_key)
    analyzed: list[AnalyzedRow] = []

    for row in rows:
        analysis = _analyze_single_row(client=client, row_text=row.text)
        analyzed.append(
            AnalyzedRow(
                row_id=row.row_id,
                summary=analysis["summary"],
                category=analysis["category"],
                priority=analysis["priority"],
                recommended_action=analysis["recommended_action"],
            )
        )

    return analyzed
