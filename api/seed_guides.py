import psycopg2
import os
import uuid
from dotenv import load_dotenv
from faker import Faker
import random

load_dotenv()
fake = Faker("ar_SA")  # توليد بيانات واقعية بالعربي

# الاتصال بـ Supabase
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT")
)
cur = conn.cursor()

# إعدادات التوليد
NUM_GUIDES = 50
regions = ["أبها", "النماص", "خميس مشيط", "رجال ألمع", "تنومة", "بيشة"]
specializations = [
    "تاريخ", "ثقافة", "طبيعة", "مغامرات", "تسوق", "طعام", "جولات جبلية"
]

# حذف البيانات القديمة (اختياري أثناء الاختبار)
#cur.execute("DELETE FROM guides;")

# توليد وإدخال البيانات
for _ in range(NUM_GUIDES):
    guide_id = str(uuid.uuid4())
    name = fake.name()
    region = random.choice(regions)
    bio = f"مرشد متخصص في {random.choice(specializations)} ويقدّم جولات ممتعة في منطقة {region}."
    rating = round(random.uniform(2.5, 5.0), 2)

    cur.execute("""
        INSERT INTO guides (id, name, region, bio, rating)
        VALUES (%s, %s, %s, %s, %s)
    """, (guide_id, name, region, bio, rating))

conn.commit()
cur.close()
conn.close()

print(f"✅ تم توليد {NUM_GUIDES} مرشد سياحي بنجاح.")
