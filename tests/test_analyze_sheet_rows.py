"""Tests for POST /analyze-sheet-rows (OpenAI mocked; no real API calls)."""

import json
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

VALID_PAYLOAD = {
    "sheet_name": "Customer Feedback",
    "rows": [
        {
            "row_id": 1,
            "text": "Customer says the product is useful but onboarding is confusing.",
        }
    ],
}


def test_analyze_sheet_rows_success_returns_200(
    client: TestClient,
    patch_openai_client: MagicMock,
) -> None:
    with patch.dict("os.environ", {"OPENAI_API_KEY": "test-key-not-used-real-api"}):
        response = client.post("/analyze-sheet-rows", json=VALID_PAYLOAD)

    assert response.status_code == 200
    data = response.json()
    assert data["sheet_name"] == "Customer Feedback"
    assert "analyzed_rows" in data
    assert isinstance(data["analyzed_rows"], list)
    assert len(data["analyzed_rows"]) == 1

    row = data["analyzed_rows"][0]
    for key in (
        "row_id",
        "summary",
        "category",
        "priority",
        "recommended_action",
    ):
        assert key in row

    assert row["row_id"] == 1
    assert row["priority"] in ("low", "medium", "high")


def test_analyzed_rows_each_has_required_fields(
    client: TestClient,
    patch_openai_client: MagicMock,
) -> None:
    payload = {
        "sheet_name": "Multi Row",
        "rows": [
            {"row_id": 1, "text": "First row."},
            {"row_id": 2, "text": "Second row."},
        ],
    }
    completion = MagicMock()
    completion.output_text = json.dumps(
        {
            "summary": "S",
            "category": "operations",
            "priority": "low",
            "recommended_action": "A",
        }
    )
    mock_client = MagicMock()
    mock_client.responses.create.return_value = completion

    with (
        patch.dict("os.environ", {"OPENAI_API_KEY": "test"}),
        patch("app.services.sheet_service.OpenAI", return_value=mock_client),
    ):
        response = client.post("/analyze-sheet-rows", json=payload)

    assert response.status_code == 200
    analyzed = response.json()["analyzed_rows"]
    assert isinstance(analyzed, list)
    assert len(analyzed) == 2
    for item in analyzed:
        assert set(item.keys()) >= {
            "row_id",
            "summary",
            "category",
            "priority",
            "recommended_action",
        }
        assert item["priority"] in ("low", "medium", "high")


@pytest.mark.parametrize(
    "payload",
    [
        {},  # missing sheet_name and rows
        {"sheet_name": "Only name"},  # missing rows
        {"rows": [{"row_id": 1, "text": "x"}]},  # missing sheet_name
        {
            "sheet_name": "X",
            "rows": [{"row_id": 0, "text": "invalid row_id"}],
        },
        {
            "sheet_name": "X",
            "rows": [{"row_id": 1}],  # missing text
        },
        {
            "sheet_name": "X",
            "rows": [],  # empty rows list
        },
    ],
)
def test_analyze_sheet_rows_invalid_body_returns_422(
    client: TestClient,
    payload: dict,
) -> None:
    response = client.post("/analyze-sheet-rows", json=payload)
    assert response.status_code == 422


def test_missing_openai_api_key_returns_503(client: TestClient) -> None:
    # Override any key from the developer's shell or .env-loaded value.
    with patch.dict("os.environ", {"OPENAI_API_KEY": ""}):
        response = client.post("/analyze-sheet-rows", json=VALID_PAYLOAD)

    assert response.status_code == 503
    detail = response.json().get("detail", "")
    assert "OPENAI_API_KEY" in str(detail)


def test_openai_api_failure_returns_502(
    client: TestClient,
    patch_openai_client: MagicMock,
) -> None:
    mock_client = patch_openai_client.return_value
    mock_client.responses.create.side_effect = RuntimeError("simulated upstream failure")

    with patch.dict("os.environ", {"OPENAI_API_KEY": "test"}):
        response = client.post("/analyze-sheet-rows", json=VALID_PAYLOAD)

    assert response.status_code == 502
    detail = response.json().get("detail", "")
    assert "OpenAI" in str(detail) or "failed" in str(detail).lower()
