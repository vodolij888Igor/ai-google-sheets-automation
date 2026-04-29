"""Pydantic schemas for sheet row analysis API."""

from typing import List

from pydantic import BaseModel, Field


class SheetRowInput(BaseModel):
    """Represents one simulated Google Sheets row."""

    row_id: int = Field(..., gt=0, description="Unique row number from the sheet.")
    text: str = Field(
        ...,
        min_length=1,
        description="Raw customer feedback text from a sheet row.",
    )


class AnalyzeSheetRowsRequest(BaseModel):
    """Request payload for row analysis."""

    sheet_name: str = Field(..., min_length=1, description="Name of the source sheet.")
    rows: List[SheetRowInput] = Field(
        ...,
        min_length=1,
        description="Rows to analyze from the sheet.",
    )


class AnalyzedRow(BaseModel):
    """Structured AI-like output for one row."""

    row_id: int
    summary: str
    category: str
    priority: str
    recommended_action: str


class AnalyzeSheetRowsResponse(BaseModel):
    """Response payload containing analyzed rows."""

    sheet_name: str
    analyzed_rows: List[AnalyzedRow]
