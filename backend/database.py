import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from uuid import UUID
from typing import Optional, List, Dict, Any
import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
from datetime import datetime, timedelta
import hashlib

def connect_to_db():
    """Establishes a connection to the Neon Postgres database."""
    try:
        conn = psycopg2.connect(os.getenv("NEON_DB_URL"))
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        raise


# ============================================
# T007: Users Table
# ============================================
def create_users_table():
    """Creates the users table for authentication."""
    conn = None
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                email VARCHAR(255) NOT NULL UNIQUE,
                password_hash VARCHAR(255) NOT NULL,
                name VARCHAR(255),
                email_verified BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
            CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
            """
        )
        conn.commit()
        cur.close()
        print("✅ Users table created/verified")
    except Exception as e:
        print(f"Error creating users table: {e}")
        raise
    finally:
        if conn:
            conn.close()


# ============================================
# T008: User Profiles Table
# ============================================
def create_user_profiles_table():
    """Creates the user_profiles table for background information."""
    conn = None
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS user_profiles (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                user_id UUID NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
                software_exp VARCHAR(20) NOT NULL DEFAULT 'intermediate',
                hardware_exp VARCHAR(30) NOT NULL DEFAULT 'none',
                robotics_bg VARCHAR(20) NOT NULL DEFAULT 'student',
                languages TEXT[] DEFAULT ARRAY['python'],
                learning_goals TEXT,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                CONSTRAINT chk_software_exp CHECK (software_exp IN ('beginner', 'intermediate', 'expert')),
                CONSTRAINT chk_hardware_exp CHECK (hardware_exp IN ('none', 'arduino_rpi', 'jetson_industrial')),
                CONSTRAINT chk_robotics_bg CHECK (robotics_bg IN ('student', 'hobbyist', 'professional'))
            );
            CREATE INDEX IF NOT EXISTS idx_user_profiles_user_id ON user_profiles(user_id);
            """
        )
        conn.commit()
        cur.close()
        print("✅ User profiles table created/verified")
    except Exception as e:
        print(f"Error creating user_profiles table: {e}")
        raise
    finally:
        if conn:
            conn.close()


# ============================================
# T009: Sessions Table
# ============================================
def create_sessions_table():
    """Creates the sessions table for authentication tokens."""
    conn = None
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS sessions (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                token_hash VARCHAR(255) NOT NULL,
                expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                ip_address VARCHAR(45),
                user_agent TEXT
            );
            CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions(user_id);
            CREATE INDEX IF NOT EXISTS idx_sessions_token_hash ON sessions(token_hash);
            CREATE INDEX IF NOT EXISTS idx_sessions_expires_at ON sessions(expires_at);
            """
        )
        conn.commit()
        cur.close()
        print("✅ Sessions table created/verified")
    except Exception as e:
        print(f"Error creating sessions table: {e}")
        raise
    finally:
        if conn:
            conn.close()


# ============================================
# T010: Content Cache Table
# ============================================
def create_content_cache_table():
    """Creates the content_cache table for personalized/translated content."""
    conn = None
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS content_cache (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                user_id UUID REFERENCES users(id) ON DELETE CASCADE,
                chapter_id VARCHAR(255) NOT NULL,
                content_type VARCHAR(20) NOT NULL,
                language VARCHAR(20) NOT NULL DEFAULT 'en',
                original_hash VARCHAR(64) NOT NULL,
                cached_content TEXT NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                expires_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() + INTERVAL '7 days',
                CONSTRAINT chk_content_type CHECK (content_type IN ('personalized', 'translated')),
                CONSTRAINT chk_language CHECK (language IN ('en', 'roman_urdu')),
                UNIQUE(user_id, chapter_id, content_type, language)
            );
            CREATE INDEX IF NOT EXISTS idx_content_cache_lookup ON content_cache(user_id, chapter_id, content_type, language);
            CREATE INDEX IF NOT EXISTS idx_content_cache_expires ON content_cache(expires_at);
            """
        )
        conn.commit()
        cur.close()
        print("✅ Content cache table created/verified")
    except Exception as e:
        print(f"Error creating content_cache table: {e}")
        raise
    finally:
        if conn:
            conn.close()


# ============================================
# T011: Modify Chat History Table
# ============================================
def create_chat_history_table():
    """Creates the chat_history table if it doesn't exist, with user_id column."""
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
                timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
                user_id UUID REFERENCES users(id) ON DELETE SET NULL
            );
            CREATE INDEX IF NOT EXISTS idx_chat_history_user_id ON chat_history(user_id);
            """
        )
        conn.commit()
        cur.close()
        print("✅ Chat history table created/verified with user_id")
    except Exception as e:
        print(f"Error creating chat_history table: {e}")
        raise
    finally:
        if conn:
            conn.close()


def add_user_id_to_chat_history():
    """Adds user_id column to existing chat_history table if not exists."""
    conn = None
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute(
            """
            DO $$
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM information_schema.columns
                    WHERE table_name='chat_history' AND column_name='user_id'
                ) THEN
                    ALTER TABLE chat_history ADD COLUMN user_id UUID REFERENCES users(id) ON DELETE SET NULL;
                    CREATE INDEX IF NOT EXISTS idx_chat_history_user_id ON chat_history(user_id);
                END IF;
            END $$;
            """
        )
        conn.commit()
        cur.close()
        print("✅ User ID column added to chat_history (if not exists)")
    except Exception as e:
        print(f"Error adding user_id to chat_history: {e}")
    finally:
        if conn:
            conn.close()


# ============================================
# Initialize All Tables
# ============================================
def init_all_tables():
    """Initialize all database tables for the bonus features."""
    print("🔄 Initializing database tables...")
    create_users_table()
    create_user_profiles_table()
    create_sessions_table()
    create_content_cache_table()
    create_chat_history_table()
    add_user_id_to_chat_history()
    print("✅ All database tables initialized!")


# ============================================
# User CRUD Operations
# ============================================
def create_user(email: str, password_hash: str, name: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Create a new user and return the user data."""
    conn = None
    try:
        conn = connect_to_db()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(
            """
            INSERT INTO users (email, password_hash, name)
            VALUES (%s, %s, %s)
            RETURNING id, email, name, created_at;
            """,
            (email, password_hash, name)
        )
        user = dict(cur.fetchone())
        conn.commit()
        cur.close()
        return user
    except psycopg2.errors.UniqueViolation:
        return None  # Email already exists
    except Exception as e:
        print(f"Error creating user: {e}")
        raise
    finally:
        if conn:
            conn.close()


def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    """Get user by email address."""
    conn = None
    try:
        conn = connect_to_db()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(
            "SELECT * FROM users WHERE email = %s;",
            (email,)
        )
        result = cur.fetchone()
        cur.close()
        return dict(result) if result else None
    except Exception as e:
        print(f"Error getting user by email: {e}")
        raise
    finally:
        if conn:
            conn.close()


def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
    """Get user by ID."""
    conn = None
    try:
        conn = connect_to_db()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(
            "SELECT id, email, name, created_at FROM users WHERE id = %s;",
            (user_id,)
        )
        result = cur.fetchone()
        cur.close()
        return dict(result) if result else None
    except Exception as e:
        print(f"Error getting user by id: {e}")
        raise
    finally:
        if conn:
            conn.close()


# ============================================
# User Profile CRUD Operations
# ============================================
def create_user_profile(
    user_id: str,
    software_exp: str = "intermediate",
    hardware_exp: str = "none",
    robotics_bg: str = "student",
    languages: List[str] = None,
    learning_goals: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """Create a user profile."""
    conn = None
    if languages is None:
        languages = ["python"]
    try:
        conn = connect_to_db()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(
            """
            INSERT INTO user_profiles (user_id, software_exp, hardware_exp, robotics_bg, languages, learning_goals)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING *;
            """,
            (user_id, software_exp, hardware_exp, robotics_bg, languages, learning_goals)
        )
        profile = dict(cur.fetchone())
        conn.commit()
        cur.close()
        return profile
    except Exception as e:
        print(f"Error creating user profile: {e}")
        raise
    finally:
        if conn:
            conn.close()


def get_user_profile(user_id: str) -> Optional[Dict[str, Any]]:
    """Get user profile by user ID."""
    conn = None
    try:
        conn = connect_to_db()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(
            "SELECT * FROM user_profiles WHERE user_id = %s;",
            (user_id,)
        )
        result = cur.fetchone()
        cur.close()
        return dict(result) if result else None
    except Exception as e:
        print(f"Error getting user profile: {e}")
        raise
    finally:
        if conn:
            conn.close()


def update_user_profile(
    user_id: str,
    software_exp: Optional[str] = None,
    hardware_exp: Optional[str] = None,
    robotics_bg: Optional[str] = None,
    languages: Optional[List[str]] = None,
    learning_goals: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """Update user profile."""
    conn = None
    try:
        conn = connect_to_db()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        # Build dynamic update query
        updates = []
        values = []
        if software_exp is not None:
            updates.append("software_exp = %s")
            values.append(software_exp)
        if hardware_exp is not None:
            updates.append("hardware_exp = %s")
            values.append(hardware_exp)
        if robotics_bg is not None:
            updates.append("robotics_bg = %s")
            values.append(robotics_bg)
        if languages is not None:
            updates.append("languages = %s")
            values.append(languages)
        if learning_goals is not None:
            updates.append("learning_goals = %s")
            values.append(learning_goals)

        if not updates:
            return get_user_profile(user_id)

        updates.append("updated_at = NOW()")
        values.append(user_id)

        query = f"UPDATE user_profiles SET {', '.join(updates)} WHERE user_id = %s RETURNING *;"
        cur.execute(query, values)
        profile = cur.fetchone()
        conn.commit()
        cur.close()
        return dict(profile) if profile else None
    except Exception as e:
        print(f"Error updating user profile: {e}")
        raise
    finally:
        if conn:
            conn.close()


# ============================================
# Session CRUD Operations
# ============================================
def create_session(user_id: str, token_hash: str, expires_at: datetime, ip_address: Optional[str] = None, user_agent: Optional[str] = None) -> Dict[str, Any]:
    """Create a new session."""
    conn = None
    try:
        conn = connect_to_db()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(
            """
            INSERT INTO sessions (user_id, token_hash, expires_at, ip_address, user_agent)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id, user_id, expires_at, created_at;
            """,
            (user_id, token_hash, expires_at, ip_address, user_agent)
        )
        session = dict(cur.fetchone())
        conn.commit()
        cur.close()
        return session
    except Exception as e:
        print(f"Error creating session: {e}")
        raise
    finally:
        if conn:
            conn.close()


def get_session_by_token_hash(token_hash: str) -> Optional[Dict[str, Any]]:
    """Get session by token hash."""
    conn = None
    try:
        conn = connect_to_db()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(
            """
            SELECT * FROM sessions
            WHERE token_hash = %s AND expires_at > NOW();
            """,
            (token_hash,)
        )
        result = cur.fetchone()
        cur.close()
        return dict(result) if result else None
    except Exception as e:
        print(f"Error getting session: {e}")
        raise
    finally:
        if conn:
            conn.close()


def delete_session(token_hash: str) -> bool:
    """Delete a session (logout)."""
    conn = None
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM sessions WHERE token_hash = %s;",
            (token_hash,)
        )
        deleted = cur.rowcount > 0
        conn.commit()
        cur.close()
        return deleted
    except Exception as e:
        print(f"Error deleting session: {e}")
        raise
    finally:
        if conn:
            conn.close()


def delete_user_sessions(user_id: str) -> int:
    """Delete all sessions for a user."""
    conn = None
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM sessions WHERE user_id = %s;",
            (user_id,)
        )
        count = cur.rowcount
        conn.commit()
        cur.close()
        return count
    except Exception as e:
        print(f"Error deleting user sessions: {e}")
        raise
    finally:
        if conn:
            conn.close()


# ============================================
# Content Cache Operations
# ============================================
def get_cached_content(
    chapter_id: str,
    content_type: str,
    language: str = "en",
    user_id: Optional[str] = None,
    original_hash: Optional[str] = None
) -> Optional[str]:
    """Get cached content if available and not expired."""
    conn = None
    try:
        conn = connect_to_db()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        if user_id:
            query = """
                SELECT cached_content FROM content_cache
                WHERE chapter_id = %s AND content_type = %s AND language = %s
                AND user_id = %s AND expires_at > NOW()
            """
            params = [chapter_id, content_type, language, user_id]
        else:
            query = """
                SELECT cached_content FROM content_cache
                WHERE chapter_id = %s AND content_type = %s AND language = %s
                AND user_id IS NULL AND expires_at > NOW()
            """
            params = [chapter_id, content_type, language]

        if original_hash:
            query += " AND original_hash = %s"
            params.append(original_hash)

        cur.execute(query + ";", params)
        result = cur.fetchone()
        cur.close()
        return result["cached_content"] if result else None
    except Exception as e:
        print(f"Error getting cached content: {e}")
        return None
    finally:
        if conn:
            conn.close()


def save_cached_content(
    chapter_id: str,
    content_type: str,
    cached_content: str,
    original_hash: str,
    language: str = "en",
    user_id: Optional[str] = None
) -> bool:
    """Save content to cache."""
    conn = None
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO content_cache (chapter_id, content_type, language, user_id, original_hash, cached_content)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (user_id, chapter_id, content_type, language)
            DO UPDATE SET cached_content = EXCLUDED.cached_content,
                          original_hash = EXCLUDED.original_hash,
                          created_at = NOW(),
                          expires_at = NOW() + INTERVAL '7 days';
            """,
            (chapter_id, content_type, language, user_id, original_hash, cached_content)
        )
        conn.commit()
        cur.close()
        return True
    except Exception as e:
        print(f"Error saving cached content: {e}")
        return False
    finally:
        if conn:
            conn.close()


def clear_user_cache(user_id: str, chapter_id: Optional[str] = None) -> int:
    """Clear cached content for a user."""
    conn = None
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        if chapter_id:
            cur.execute(
                "DELETE FROM content_cache WHERE user_id = %s AND chapter_id = %s;",
                (user_id, chapter_id)
            )
        else:
            cur.execute(
                "DELETE FROM content_cache WHERE user_id = %s;",
                (user_id,)
            )
        count = cur.rowcount
        conn.commit()
        cur.close()
        return count
    except Exception as e:
        print(f"Error clearing user cache: {e}")
        return 0
    finally:
        if conn:
            conn.close()


def hash_content(content: str) -> str:
    """Generate MD5 hash of content for cache validation."""
    return hashlib.md5(content.encode()).hexdigest()

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
