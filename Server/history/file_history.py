from langchain_community.chat_message_histories import FileChatMessageHistory
import os

def get_session_history(session_id: str):
    """
    Returns a FileChatMessageHistory object for the given session_id.
    Stores the JSON files in the Server/data/history/ directory.
    This provides persistent conversation memory across user sessions.
    """
    base_dir = os.path.dirname(os.path.dirname(__file__))
    history_dir = os.path.join(base_dir, 'data', 'history')
    os.makedirs(history_dir, exist_ok=True)
    
    # Clean the session_id to prevent directory traversal
    safe_session_id = "".join(c for c in session_id if c.isalnum() or c in ('-', '_')).rstrip()
    if not safe_session_id:
        safe_session_id = "default"
        
    file_path = os.path.join(history_dir, f"{safe_session_id}.json")
    return FileChatMessageHistory(file_path)
