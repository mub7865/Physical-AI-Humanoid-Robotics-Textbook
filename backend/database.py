import os
from uuid import UUID
from typing import Optional
import psycopg2
from psycopg2 import sql
from datetime import datetime

def connect_to_db():
    """Establishes a connection to the Neon Postgres database."""
    try:
        conn = psycopg2.connect(os.getenv("NEON_DB_URL"))
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        raise

def create_chat_history_table():
    """Creates the chat_history table if it doesn't exist."""
    conn = None
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS chat_history (
                conversation_id UUID PRIMARY KEY,
                user_message TEXT NOT NULL,
                bot_response TEXT NOT NULL,
                selected_text TEXT,
                timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
            );
            """
        )
        conn.commit()
        cur.close()
    except Exception as e:
        print(f"Error creating chat_history table: {e}")
        raise
    finally:
        if conn:
            conn.close()

def save_chat_history(conversation_id: UUID, user_message: str, bot_response: str, selected_text: Optional[str]):
    """Saves chat conversation to the chat_history table."""
    conn = None
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute(
            sql.SQL(
                """
                INSERT INTO chat_history (conversation_id, user_message, bot_response, selected_text)
                VALUES (%s, %s, %s, %s);
                """
            ),
            (conversation_id, user_message, bot_response, selected_text),
        )
        conn.commit()
        cur.close()
    except Exception as e:
        print(f"Error saving chat history: {e}")
        raise
    finally:
        if conn:
            conn.close()

# Ensure table is created when this module is imported
# This might be problematic in a FastAPI context if not handled carefully,
# better to call it explicitly in main.py startup event.
# create_chat_history_table()
