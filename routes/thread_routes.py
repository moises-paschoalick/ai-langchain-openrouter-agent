from flask import Blueprint, jsonify
from services.memory_service import MemoryService

thread_bp = Blueprint("threads", __name__)
memory_service = MemoryService()

@thread_bp.route("/threads", methods=["POST"])
def create_thread():
    conversation_id = memory_service.create_thread()
    return jsonify({"conversation_id": conversation_id})

@thread_bp.route("/threads/<conversation_id>/history", methods=["GET"])
def get_thread_history(conversation_id):
    history = memory_service.get_history(conversation_id)
    return jsonify([msg.to_dict() for msg in history])
