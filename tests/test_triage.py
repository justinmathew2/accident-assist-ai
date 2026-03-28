import pytest
from logic.triage import analyze_incident, mock_analyze_incident
import base64

def test_triage_mock_high_severity():
    """
    Test mock triage with high severity keywords.
    """
    description = "There is blood and the driver is unconscious."
    result = mock_analyze_incident(description)
    
    assert result["severity"] == "HIGH"
    assert "blood" in result["incident_summary"].lower()

def test_triage_mock_low_severity():
    """
    Test mock triage with minor incident keywords.
    """
    description = "It's just a minor scratch on the bumper."
    result = mock_analyze_incident(description)
    
    assert result["severity"] == "LOW"

def test_triage_base64_input():
    """
    Test multimodal image processing with a dummy Base64 string.
    This ensures app.py can pass image data to the logic layers.
    """
    # Dummy white pixel base64
    dummy_base64 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+cp1IEAAAAAElFTkSuQmCC"
    
    # We test the analyze_incident function (which will fallback to mock in test environment)
    result = analyze_incident(description="Visual scan of accident", image_data=dummy_base64)
    
    assert "severity" in result
    assert "recommended_actions" in result
    assert "forensic_notes" in result
    assert "ambulance_priority" in result
    assert isinstance(result["recommended_actions"], list)
