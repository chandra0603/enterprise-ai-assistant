from app.database.database import get_connection


class ConversationRepository:

    def __init__(self):
        print("ConversationRepository initialized")
        self.create_table()

    def create_table(self):
        print("Creating SQLite table...")
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                role TEXT,
                content TEXT
            )
        """)

        conn.commit()
        conn.close()

    def save_message(self, session_id: str, role: str, content: str):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO conversations(session_id, role, content)
            VALUES (?, ?, ?)
        """, (session_id, role, content))

        conn.commit()
        conn.close()

    def get_history(self, session_id: str):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT role, content
            FROM conversations
            WHERE session_id = ?
            ORDER BY id
        """, (session_id,))

        rows = cursor.fetchall()

        conn.close()

        history = []

        for role, content in rows:
            history.append({
                "role": role,
                "content": content
            })

        return history

    # Compatibility method so RAGService doesn't need to change
    def add_message(self, session_id: str, role: str, content: str):
        self.save_message(session_id, role, content)