import os
from dotenv import load_dotenv
from openai_service import OpenAIService
from qdrant_service import QdrantClientService
from database import connect_to_db, save_chat_history
from uuid import uuid4

# Load env vars
load_dotenv()

def test_services():
    print("--- DIAGNOSTIC TEST ---")
    
    # 1. Test Environment Variables
    print("\n1. Checking Environment Variables...")
    openai_key = os.getenv("OPENAI_API_KEY")
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_key = os.getenv("QDRANT_API_KEY")
    db_url = os.getenv("NEON_DB_URL")
    
    if not openai_key: print("❌ OPENAI_API_KEY missing")
    else: print("✅ OPENAI_API_KEY found")
    
    if not qdrant_url: print("❌ QDRANT_URL missing")
    else: print("✅ QDRANT_URL found")

    if not db_url: print("❌ NEON_DB_URL missing")
    else: print("✅ NEON_DB_URL found")

    # 2. Test OpenAI
    print("\n2. Testing OpenAI Connection...")
    try:
        openai_svc = OpenAIService()
        emb = openai_svc.get_embedding("Test")
        print("✅ OpenAI Embedding worked")
    except Exception as e:
        print(f"❌ OpenAI Failed: {e}")
        return

    # 3. Test Qdrant
    print("\n3. Testing Qdrant Connection...")
    try:
        qdrant_svc = QdrantClientService()
        results = qdrant_svc.search_book_knowledge(emb)
        print(f"✅ Qdrant Search worked (Found {len(results)} results)")
    except Exception as e:
        print(f"❌ Qdrant Failed: {e}")
        return

    # 4. Test Database
    print("\n4. Testing Database Connection...")
    try:
        conn = connect_to_db()
        print("✅ Database Connected")
        conn.close()
    except Exception as e:
        print(f"❌ Database Failed: {e}")
        print("   (Check your NEON_DB_URL in .env)")
        return

    print("\n✅✅ ALL SYSTEMS GO! The backend is fine locally.")

if __name__ == "__main__":
    test_services()
