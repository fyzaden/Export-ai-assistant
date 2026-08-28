import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "export_ai_assistant.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    return connection


def init_db():
    connection = get_connection()
    cursor = connection.cursor()

    # Conversations
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Messages
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id INTEGER NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (conversation_id)
                REFERENCES conversations(id)
        )
    """)

    # Leads
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            message TEXT,
            session_id TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Eski database'lerde company kolonu yoksa ekle
    cursor.execute("PRAGMA table_info(leads)")
    columns = [row["name"] for row in cursor.fetchall()]

    if "company" not in columns:
        cursor.execute("""
            ALTER TABLE leads
            ADD COLUMN company TEXT
        """)

    connection.commit()
    connection.close()


def create_conversation(session_id: str) -> int:
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO conversations (session_id)
        VALUES (?)
        """,
        (session_id,)
    )

    conversation_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return conversation_id


def get_or_create_conversation(session_id: str) -> int:
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id
        FROM conversations
        WHERE session_id = ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (session_id,)
    )

    row = cursor.fetchone()

    if row:
        connection.close()
        return row["id"]

    cursor.execute(
        """
        INSERT INTO conversations (session_id)
        VALUES (?)
        """,
        (session_id,)
    )

    conversation_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return conversation_id


def save_message(
    conversation_id: int,
    role: str,
    content: str
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO messages (
            conversation_id,
            role,
            content
        )
        VALUES (?, ?, ?)
        """,
        (
            conversation_id,
            role,
            content
        )
    )

    connection.commit()
    connection.close()


def get_messages(conversation_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT role, content
        FROM messages
        WHERE conversation_id = ?
        ORDER BY id ASC
        """,
        (conversation_id,)
    )

    rows = cursor.fetchall()

    connection.close()

    return [
        {
            "role": row["role"],
            "text": row["content"]
        }
        for row in rows
    ]


def create_lead(
    name: str,
    phone: str,
    company: str = "",
    message: str = "",
    session_id: str = ""
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO leads (
            name,
            phone,
            company,
            message,
            session_id
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            name,
            phone,
            company,
            message,
            session_id
        )
    )

    lead_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return lead_id

def get_leads():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            name,
            phone,
            company,
            message,
            session_id,
            created_at
        FROM leads
        ORDER BY id DESC
        """
    )

    rows = cursor.fetchall()

    connection.close()

    return [
        {
            "id": row["id"],
            "name": row["name"],
            "phone": row["phone"],
            "company": row["company"],
            "message": row["message"],
            "session_id": row["session_id"],
            "created_at": row["created_at"]
        }
        for row in rows
    ]