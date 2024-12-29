from flask import Flask, render_template, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_metaflow', methods=['POST'])
def run_metaflow():
    try:
        # Execute the Metaflow code
        result = subprocess.run(
            ['python3', 'kuliah_flow.py'], capture_output=True, text=True
        )
        return jsonify({"output": result.stdout, "error": result.stderr})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
