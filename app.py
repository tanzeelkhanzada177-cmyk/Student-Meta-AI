import os

from flask import Flask, jsonify, request, send_from_directory
from google import genai

app = Flask(__name__)


@app.route("/")
def home():
    return send_from_directory(app.root_path, "index.html")


@app.route("/style.css")
def style():
    return send_from_directory(app.root_path, "style.css")


@app.route("/script.js")
def script():
    return send_from_directory(app.root_path, "script.js")


@app.route("/api/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Send a JSON object with topic and type."
        }), 400

    topic = data.get("topic")
    task = data.get("type", "explain")

    if not isinstance(topic, str) or not topic.strip():
        return jsonify({
            "error": "Please enter a study topic."
        }), 400

    if not isinstance(task, str) or task not in {
        "explain", "notes", "quiz"
    }:
        return jsonify({
            "error": "Choose explain, notes, or quiz."
        }), 400

    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        return jsonify({
            "error": (
                "The server is missing the GEMINI_API_KEY "
                "environment variable."
            )
        }), 503

    instructions = {
        "explain": (
            "Explain the topic clearly for a student, "
            "using simple language and examples."
        ),
        "notes": (
            "Create organized study notes with headings "
            "and concise bullet points."
        ),
        "quiz": (
            "Create 5 multiple-choice questions with four "
            "options each and an answer key."
        ),
    }

    prompt = (
        f"{instructions[task]}\n\n"
        f"Study topic: {topic.strip()}"
    )

    try:
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt,
        )

        return jsonify({
            "answer": response.text
            or "Gemini returned an empty response."
        })

    except Exception:
        app.logger.exception("Gemini request failed")

        return jsonify({
            "error": (
                "The AI request failed. "
                "Check the Flask terminal for details."
            )
        }), 502


if __name__ == "__main__":
    app.run(debug=True)

