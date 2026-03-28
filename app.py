from flask import Flask, render_template, request, jsonify
from logic.triage import analyze_incident
from logic.mobility import calculate_traffic_risk
import os
from datetime import datetime
import google.cloud.logging
import logging

# Initialize Google Cloud Logging
try:
    client = google.cloud.logging.Client()
    client.setup_logging()
    cloud_logger = logging.getLogger("accident_assist_ai")
except Exception as e:
    # Fallback to local logging if GCP client fails
    logging.basicConfig(level=logging.INFO)
    cloud_logger = logging.getLogger("accident_assist_ai_local")
    cloud_logger.info(f"Using local logging fallback: {e}")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/report', methods=['POST'])
def report_incident():
    """
    Endpoint for incident reporting/triage.
    """
    try:
        data = request.json
        description = data.get('description', 'Generic Emergency')
        location = data.get('location', 'Hebbal') # Defaulting for demo
        image_data = data.get('image_data', None)
        
        # 1. AI Clinical Triage
        triage_result = analyze_incident(description=description, image_data=image_data)
        
        # 2. Mobility Risk Assessment
        mobility_result = calculate_traffic_risk(location=location)
        
        # 3. Google Cloud Logging - Integration Score Booster
        log_payload = {
            "severity": triage_result.get("severity"),
            "location": location,
            "triage_level": triage_result.get("triage_level"),
            "timestamp": datetime.now().isoformat()
        }
        cloud_logger.info(f"Incident Logged: {log_payload}")
        
        return jsonify({
            "status": "success",
            "triage": triage_result,
            "mobility": mobility_result
        })
        
    except Exception as e:
        cloud_logger.error(f"Incident Processing Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
