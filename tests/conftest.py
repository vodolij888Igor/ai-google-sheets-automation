"""Shared pytest fixtures."""

import json
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client() -> TestClient:
    """FastAPI app client for integration-style API tests."""
    from app.main import app

    return TestClient(app)


@pytest.fixture
def mock_openai_success() -> MagicMock:
    """Fake OpenAI completion with valid JSON matching the analysis schema."""
    completion = MagicMock()
    completion.output_text = json.dumps(
        {
            "summary": "Customer likes the product but finds onboarding unclear.",
            "category": "customer_feedback",
            "priority": "medium",
            "recommended_action": "Improve onboarding documentation.",
        }
    )
    mock_client = MagicMock()
    mock_client.responses.create.return_value = completion
    return mock_client


@pytest.fixture
def patch_openai_client(mock_openai_success: MagicMock):
    """Patch OpenAI constructor so no real API key or network is used."""
    with patch(
        "app.services.sheet_service.OpenAI",
        return_value=mock_openai_success,
    ) as mock_cls:
        yield mock_cls
