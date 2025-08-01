import psycopg2
import os
import uuid
import random
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

# الاتصال بقاعدة البيانات
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT")
)
cur = conn.cursor()

# جلب المستخدمين والمرشدين
cur.execute("SELECT id FROM users;")
user_ids = [row[0] for row in cur.fetchall()]

cur.execute("SELECT id FROM guides;")
guide_ids = [row[0] for row in cur.fetchall()]

interactions = []

# توليد تفاعلات عشوائية
for _ in range(100):
    user_id = random.choice(user_ids)
    guide_id = random.choice(guide_ids)
    interest_match_score = round(random.uniform(0.3, 1.0), 2)
    feedback_score = round(random.uniform(2.0, 5.0), 2)
    days_ago = random.randint(0, 60)
    created_at = datetime.now() - timedelta(days=days_ago)

    interactions.append({
        "id": str(uuid.uuid4()),
        "user_id": user_id,
        "guide_id": guide_id,
        "match": interest_match_score,
        "feedback": feedback_score,
        "created_at": created_at
    })

# إدخال البيانات
for i in interactions:
    cur.execute("""
        INSERT INTO interactions (id, user_id, guide_id, interest_match_score, created_at)
        VALUES (%s, %s, %s, %s, %s)
    """, (i["id"], i["user_id"], i["guide_id"], i["match"], i["created_at"]))


conn.commit()
cur.close()
conn.close()

print(f"✅ تم إدخال {len(interactions)} تفاعل في جدول interactions.")
