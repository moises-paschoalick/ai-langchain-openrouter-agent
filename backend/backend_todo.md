# Backend Changes Required

1.  **DELETE /threads/{conversation_id}**
    *   **Reason**: To allow users to permanently delete a thread from the server memory.
    *   **Current State**: Frontend only deletes from local storage; server retains data until restart.
    *   **Files to Modify**:
        *   `routes/thread_routes.py`: Add `@thread_bp.route("/threads/<conversation_id>", methods=["DELETE"])`.
        *   `services/memory_service.py`: Add `delete_thread(conversation_id)`.
        *   `repositories/conversation_repository.py`: Add `delete(conversation_id)`.
