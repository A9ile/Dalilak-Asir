import psycopg2
import os
from dotenv import load_dotenv
from faker import Faker
import random
import uuid

load_dotenv()
fake = Faker('ar_SA')

# البيانات الأساسية
age_groups = ["شاب", "متوسط العمر", "كبير سن"]
nationalities = ["سعودي", "يمني", "مصري", "سوري", "أردني" ,"بريطاني"]
regions = ["أبها", "خميس مشيط", "النماص", "رجال ألمع", "محايل", "بيشة"]

# توليد بيانات مزيفة
def generate_fake_users(n=10):
    users = []
    for _ in range(n):
        user = {
            "id": str(uuid.uuid4()),
            "name": fake.name(),
            "age_group": random.choice(age_groups),
            "nationality": random.choice(nationalities),
            "region": random.choice(regions),
        }
        users.append(user)
    return users

# اتصال بقاعدة البيانات
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT")
)

# إدخال المستخدمين
def insert_users(users):
    with conn:
        with conn.cursor() as cur:
            for user in users:
                cur.execute("""
                    INSERT INTO users (id, name, age_group, nationality, region)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    user['id'],
                    user['name'],
                    user['age_group'],
                    user['nationality'],
                    user['region']
                ))

if __name__ == "__main__":
    fake_users = generate_fake_users(50)
    insert_users(fake_users)
    print(f"✅ تم إدخال {len(fake_users)} مستخدم بنجاح.")
