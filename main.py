# import socket
import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)


@app.route('/receive', methods=['POST'])
def receive_data():
    try:
        json_data = request.get_json()
        target_host = 'https://cloud1cvig.ccg.pt:16301/mp_estimator/'
        headers = {"Content-Type": "application/json"}

        response = requests.post(target_host, data=json.dumps(json_data), headers=headers, verify=False)
        print(response.text)

        if response.status_code == 200:
            response_data = response.json()
            if response_data is not None:
                return jsonify({"response": response_data}), 200
            else:
                return jsonify({"message": "Received response is empty or null."}), 204  # No Content
        else:
            return jsonify({"message": f"Failed to send data. Status code: {response.status_code}",
                            "response": response.text}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
