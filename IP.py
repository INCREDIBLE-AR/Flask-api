from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# API Route
@app.route('/check_ip', methods=['GET'])
def check_ip():
    # Get the IP address from query parameters
    ip = request.args.get('ip', default=None)
    
    if not ip:
        return jsonify({"error": "IP address is required"}), 400

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json',
        'Referer': 'https://uselessnoobs.com/'
    }

    try:
        # External API Call
        response = requests.get(f"https://uselessnoobs.com/ip.php?ip={ip}", headers=headers)
        json_data = response.json()  # Parse as JSON
        return jsonify(json_data), response.status_code
    except requests.exceptions.JSONDecodeError:
        return jsonify({"error": "Could not parse response as JSON"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
