import requests

@app.route('/get-ip-info', methods=['GET'])
def get_ip_info():
    ip_address = request.args.get('ip')  # Get IP from query parameter
    
    if not ip_address:
        return jsonify({"error": "Please provide an IP address as a query parameter, e.g., /get-ip-info?ip=8.8.8.8"})

    # Fetch real IP info using ip-api
    try:
        response = requests.get(f"http://ip-api.com/json/{ip_address}")
        ip_data = response.json()
        ip_data["message"] = "Coded By STLP"  # Add custom message
        return jsonify(ip_data)
    except Exception as e:
        return jsonify({"error": "Failed to fetch IP information", "details": str(e)})
