import psycopg2
import os
import uuid
from dotenv import load_dotenv
import random

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

# مجموعة التخصصات المتاحة
tags_pool = [
    "الطبيعة", "المغامرات", "التراث", "الفن", "التصوير", "التاريخ", "الطعام", "التسوق"
]

# جلب معرفات المرشدين
cur.execute("SELECT id FROM guides;")
guide_ids = [row[0] for row in cur.fetchall()]

# توليد التخصصات
guide_tags = []
for guide_id in guide_ids:
    num_tags = random.randint(2, 3)
    tags = random.sample(tags_pool, num_tags)
    for tag in tags:
        guide_tags.append({
            "id": str(uuid.uuid4()),
            "guide_id": guide_id,
            "tag": tag
        })

# إدخال البيانات في الجدول
for item in guide_tags:
    cur.execute("""
        INSERT INTO guide_tags (id, guide_id, tag)
        VALUES (%s, %s, %s)
    """, (item["id"], item["guide_id"], item["tag"]))

conn.commit()
cur.close()
conn.close()

print(f"🎯 تم إدخال {len(guide_tags)} تخصصًا بنجاح.")
