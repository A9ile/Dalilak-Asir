from faker import Faker
import random
import uuid
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
fake = Faker('ar_SA')

# إعداد الاتصال
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT")
)
cur = conn.cursor()

# مجموعة اهتمامات افتراضية
interest_pool = [
    "التاريخ", "المغامرات", "الجبال", "المتاحف", "الطبيعة", "الفن", "التصوير", "التسوق", "القرى التراثية"
]

def generate_user_interests():
    # جلب كل معرفات المستخدمين من جدول users
    cur.execute("SELECT id FROM users;")
    user_ids = [row[0] for row in cur.fetchall()]
    
    user_interests = []
    for user_id in user_ids:
        num_interests = random.randint(1, 3)  # من 1 إلى 3 اهتمامات لكل مستخدم
        interests = random.sample(interest_pool, num_interests)
        for interest in interests:
            entry = {
                "id": str(uuid.uuid4()),
                "user_id": user_id,
                "interest": interest
            }
            user_interests.append(entry)
    
    return user_interests

def seed_user_interests():
    interests = generate_user_interests()
    for item in interests:
        cur.execute("""
            INSERT INTO user_interests (id, user_id, interest)
            VALUES (%s, %s, %s)
        """, (item["id"], item["user_id"], item["interest"]))
    
    conn.commit()
    print(f"🎉 تم إدخال {len(interests)} اهتمام بنجاح.")

seed_user_interests()
cur.close()
conn.close()
