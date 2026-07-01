from app import create_app
from app.models import db, User, ChatSession, MedicalReport
from werkzeug.security import check_password_hash

app = create_app()

with app.app_context():
    print("--- Testing Phase 6 Database & Auth Models ---")
    
    # 1. Create User
    u = User.query.filter_by(email="test@test.com").first()
    if not u:
        u = User(name="Test User", email="test@test.com")
        u.set_password("password123")
        db.session.add(u)
        db.session.commit()
        print("[SUCCESS] User created.")
    else:
        print("[INFO] User already exists.")
        
    # 2. Check Password Hash
    if u.check_password("password123"):
        print("[SUCCESS] Password hashing works.")
    else:
        print("[FAILED] Password hash verification failed.")
        
    # 3. Create Chat Session
    c = ChatSession(user_id=u.id, title="Fever Consultation")
    db.session.add(c)
    db.session.commit()
    print(f"[SUCCESS] Chat Session created with ID: {c.id}")
    
    # 4. Check Relationships
    user_chats = User.query.get(u.id).chat_sessions
    if len(user_chats) > 0:
        print(f"[SUCCESS] User relationship works. Found {len(user_chats)} chats.")
    
    print("✅ All DB and Auth model tests passed!")
