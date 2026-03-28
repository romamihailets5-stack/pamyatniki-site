import csv
import sqlite3
import cloudinary
import cloudinary.uploader

# Настройки Cloudinary
cloudinary.config(
    cloud_name="dobqrqjji",
    api_key="281524648686869",
    api_secret="Tx-5xbRmB9T-BG8DgpXTso-cmT4"
)

# Подключение к базе
conn = sqlite3.connect("monuments.db")
c = conn.cursor()

with open('monuments.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, delimiter='\t')  # <-- через табуляцию
    for row in reader:
        upload_result = cloudinary.uploader.upload(row['image_path'])
        image_url = upload_result["secure_url"]
        public_id = upload_result["public_id"]

        c.execute(
            "INSERT INTO monuments (name, location, price, image, material, description, public_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (row['name'], row['location'], float(row['price']), image_url, row['material'], row['description'], public_id)
        )

conn.commit()
conn.close()
print("Готово! Памятники загружены.")