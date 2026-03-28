from datetime import datetime

# Geographic Risk Map for Bengaluru Hotspots
GEOGRAPHIC_RISK_MAP = {
    "Silk Board": {"base_risk": "HIGH", "reason": "Major Junction Congestion"},
    "Hebbal": {"base_risk": "MEDIUM", "reason": "Hebbal Flyover Congestion"},
    "KR Puram": {"base_risk": "MEDIUM", "reason": "Suspension Bridge Bottleneck"},
    "Goraguntepalya": {"base_risk": "HIGH", "reason": "Industrial Traffic/Tumkur Rd Junction"},
    "Outer Ring Road": {"base_risk": "MEDIUM", "reason": "IT Corridor Volume"}
}

RISK_LEVELS = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]

def is_peak_hour(timestamp):
    """
    Bengaluru Peak Hours: 
    Morning: 08:30 – 11:30
    Evening: 17:00 – 21:00
    """
    current_time = timestamp.time()
    
    morning_start = datetime.strptime("08:30", "%H:%M").time()
    morning_end = datetime.strptime("11:30", "%H:%M").time()
    
    evening_start = datetime.strptime("17:00", "%H:%M").time()
    evening_end = datetime.strptime("21:00", "%H:%M").time()
    
    return (morning_start <= current_time <= morning_end) or \
           (evening_start <= current_time <= evening_end)

def calculate_traffic_risk(location, timestamp=None):
    """
    Calculates traffic risk based on location and time.
    """
    if timestamp is None:
        timestamp = datetime.now()
        
    risk_info = GEOGRAPHIC_RISK_MAP.get(location, {"base_risk": "LOW", "reason": "Standard Traffic Flow"})
    base_risk = risk_info["base_risk"]
    reason = risk_info["reason"]
    
    current_risk_index = RISK_LEVELS.index(base_risk)
    peak_status = is_peak_hour(timestamp)
    
    # Risk Escalation Logic
    final_risk = base_risk
    if peak_status:
        # Escalate risk by one tier
        new_index = min(current_risk_index + 1, len(RISK_LEVELS) - 1)
        final_risk = RISK_LEVELS[new_index]
        reason = f"Peak Hour: {reason}"
        
        # Special Case: Silk Board Grade-Locked
        if location == "Silk Board":
            final_risk = "CRITICAL"
            reason = "CRITICAL - GRIDLOCK EXPECTED"

    # ETA Modifier Heuristic (in minutes)
    eta_modifier = 0
    if final_risk == "CRITICAL":
        eta_modifier = 30
    elif final_risk == "HIGH":
        eta_modifier = 15
    elif final_risk == "MEDIUM":
        eta_modifier = 5
        
    return {
        "location": location,
        "risk_level": final_risk,
        "reason": reason,
        "ambulance_eta_modifier": eta_modifier,
        "is_peak": peak_status
    }
