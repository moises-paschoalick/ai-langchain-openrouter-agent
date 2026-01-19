from flask import Blueprint, request, jsonify
from services.chat_service import ChatService

chat_bp = Blueprint("chat", __name__)
chat_service = ChatService()

@chat_bp.route("/chat", methods=["POST"])
def chat():
    data = request.json
    conversation_id = data.get("conversation_id")
    prompt = data.get("prompt")

    if not conversation_id or not prompt:
        return jsonify({"error": "conversation_id and prompt are required"}), 400

    result = chat_service.process_prompt(conversation_id, prompt)
    return jsonify(result)
