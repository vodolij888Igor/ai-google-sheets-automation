"""Service layer for analyzing simulated sheet rows.

This file intentionally uses placeholder logic for version 1.
Later versions can replace this with real LLM integrations.
"""

from app.schemas.sheet_schema import AnalyzedRow, SheetRowInput


def _detect_priority(text: str) -> str:
    """Simple keyword-based priority classifier."""
    lowered = text.lower()
    if any(word in lowered for word in ["urgent", "broken", "refund", "angry"]):
        return "high"
    if any(word in lowered for word in ["confusing", "slow", "issue", "problem"]):
        return "medium"
    return "low"


def _detect_category(text: str) -> str:
    """Simple keyword-based category classifier."""
    lowered = text.lower()
    if any(word in lowered for word in ["onboarding", "feature", "product", "ui", "ux"]):
        return "product_feedback"
    if any(word in lowered for word in ["price", "billing", "payment"]):
        return "billing_feedback"
    if any(word in lowered for word in ["support", "agent", "response time"]):
        return "support_feedback"
    return "general_feedback"


def _build_summary(text: str) -> str:
    """Create a short summary from raw row text."""
    cleaned = text.strip().rstrip(".")
    if len(cleaned) <= 90:
        return cleaned + "."
    return cleaned[:87].rstrip() + "..."


def _recommended_action(category: str, priority: str) -> str:
    """Return an action suggestion based on category and priority."""
    if category == "product_feedback":
        if priority == "high":
            return "Schedule a product team review within 24 hours."
        return "Document feedback and improve product guidance."
    if category == "billing_feedback":
        return "Review billing flow and update pricing communication."
    if category == "support_feedback":
        return "Investigate support workflow and improve response speed."
    return "Log this feedback and monitor for similar patterns."


def analyze_rows(rows: list[SheetRowInput]) -> list[AnalyzedRow]:
    """Analyze each row using deterministic placeholder logic."""
    analyzed: list[AnalyzedRow] = []

    for row in rows:
        category = _detect_category(row.text)
        priority = _detect_priority(row.text)
        summary = _build_summary(row.text)
        action = _recommended_action(category, priority)

        analyzed.append(
            AnalyzedRow(
                row_id=row.row_id,
                summary=summary,
                category=category,
                priority=priority,
                recommended_action=action,
            )
        )

    return analyzed
