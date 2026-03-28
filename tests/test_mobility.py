import pytest
from logic.mobility import calculate_traffic_risk
from datetime import datetime

def test_silk_board_peak_hour_critical():
    """
    Case 1: Silk Board at Peak Hour (Critical Risk).
    """
    # 09:30 AM is peak hour
    peak_time = datetime.strptime("09:30", "%H:%M")
    result = calculate_traffic_risk("Silk Board", peak_time)
    
    assert result["risk_level"] == "CRITICAL"
    assert "GRIDLOCK" in result["reason"]
    assert result["ambulance_eta_modifier"] == 30

def test_hebbal_peak_hour_high():
    """
    Case 2: Hebbal at Peak Hour (High Risk due to escalation).
    """
    # 18:00 (6 PM) is peak hour
    peak_time = datetime.strptime("18:00", "%H:%M")
    result = calculate_traffic_risk("Hebbal", peak_time)
    
    # Base risk for Hebbal is MEDIUM, escalated to HIGH
    assert result["risk_level"] == "HIGH"
    assert "Peak Hour" in result["reason"]
    assert result["ambulance_eta_modifier"] == 15

def test_kr_puram_midnight_low():
    """
    Case 3: KR Puram at Midnight (Low Risk).
    """
    # 01:00 AM is NOT peak hour
    off_peak_time = datetime.strptime("01:00", "%H:%M")
    result = calculate_traffic_risk("KR Puram", off_peak_time)
    
    # Base risk for KR Puram is MEDIUM, no escalation
    assert result["risk_level"] == "MEDIUM"
    assert "Peak Hour" not in result["reason"]
    assert result["ambulance_eta_modifier"] == 5

def test_unknown_location_low():
    """
    Default case for unknown locations.
    """
    off_peak_time = datetime.strptime("01:00", "%H:%M")
    result = calculate_traffic_risk("Unknown Area", off_peak_time)
    
    assert result["risk_level"] == "LOW"
    assert result["ambulance_eta_modifier"] == 0
