from flask import Blueprint, request, jsonify
from services.chat_service import process_prompt

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/chat", methods=["POST"])
def chat():
    data = request.json
    prompt = data.get("prompt")

    if not prompt:
        return jsonify({"error": "Prompt é obrigatório"}), 400

    result = process_prompt(prompt)
    return jsonify(result)
