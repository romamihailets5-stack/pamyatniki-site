from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
import requests

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/images"

# ===== Telegram =====
BOT_TOKEN = "8147591467:AAHgKcfIoLihoSNQL4oiB-IVVvJfFWkCPaM"
CHAT_ID = "5171742797"

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

# ===== База данных =====
def init_db():
    conn = sqlite3.connect("monuments.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS monuments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            location TEXT,
            price REAL,
            image TEXT,
            material TEXT,
            description TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ===== Главная страница: список памятников =====
@app.route("/")
def show_monuments():
    conn = sqlite3.connect("monuments.db")
    c = conn.cursor()
    c.execute("SELECT * FROM monuments")
    monuments = c.fetchall()
    conn.close()
    return render_template("monuments.html", monuments=monuments)

# ===== Детальная страница памятника =====
@app.route("/monument/<int:id>")
def monument_detail(id):
    conn = sqlite3.connect("monuments.db")
    c = conn.cursor()
    c.execute("SELECT * FROM monuments WHERE id=?", (id,))
    monument = c.fetchone()
    conn.close()
    return render_template("monument_detail.html", monument=monument)

# ===== Добавление памятника =====
@app.route("/add", methods=["GET", "POST"])
def add_monument():
    PASSWORD = "RM1234"  # <-- сюда свой пароль
    if request.method == "POST":
        entered_password = request.form.get("password")
        if entered_password != PASSWORD:
            return "Невірний пароль!", 403

        name = request.form["name"]
        location = request.form["location"]
        price = float(request.form["price"])
        material = request.form["material"]
        description = request.form["description"]
        file = request.files["image"]

        if file:
            filename = file.filename
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)
            image_path = f"images/{filename}"

            conn = sqlite3.connect("monuments.db")
            c = conn.cursor()
            c.execute(
                "INSERT INTO monuments (name, location, price, image, material, description) VALUES (?, ?, ?, ?, ?, ?)",
                (name, location, price, image_path, material, description)
            )
            conn.commit()
            conn.close()

            # Telegram уведомление
            send_telegram_message(f"Додано новий пам'ятник!\n{name} у місті {location} за {price} ₴")
            
            return redirect(url_for("show_monuments"))

    return render_template("add_monument.html")

# ===== Заказ памятника =====
@app.route("/order/<int:monument_id>", methods=["POST"])
def order_monument(monument_id):
    user_name = request.form["user_name"]
    user_phone = request.form["user_phone"]

    conn = sqlite3.connect("monuments.db")
    c = conn.cursor()
    c.execute("SELECT name, location, price FROM monuments WHERE id=?", (monument_id,))
    monument = c.fetchone()
    conn.close()

    send_telegram_message(
        f"Замовлення пам'ятника!\n"
        f"Пам'ятник: {monument[0]}\n"
        f"Місто: {monument[1]}\n"
        f"Ціна: {monument[2]} ₴\n"
        f"Ім'я: {user_name}\n"
        f"Телефон: {user_phone}"
    )

    return f"Дякуємо, {user_name}! Ваше замовлення на пам'ятник прийнято."

@app.route('/google7a5a4a7b43c36874.html')
def google_verification():
    return "google-site-verification: google7a5a4a7b43c36874.html"

# ===== Удаление памятника с паролем =====
@app.route("/delete/<int:id>", methods=["GET", "POST"])
def delete_monument(id):
    PASSWORD = "RM1234"
    if request.method == "POST":
        entered_password = request.form.get("password")
        if entered_password != PASSWORD:
            return "Невірний пароль!", 403

        conn = sqlite3.connect("monuments.db")
        c = conn.cursor()
        # Получаем путь к изображению
        c.execute("SELECT image FROM monuments WHERE id=?", (id,))
        image_path = c.fetchone()
        if image_path:
            image_file = os.path.join("static", image_path[0])
            if os.path.exists(image_file):
                os.remove(image_file)  # удаляем файл изображения
        # Удаляем памятник из базы
        c.execute("DELETE FROM monuments WHERE id=?", (id,))
        conn.commit()
        conn.close()
        return redirect(url_for("show_monuments"))

    # GET-запрос — показываем форму ввода пароля
    return f"""
    <h3>Видалити пам'ятник</h3>
    <form method="POST">
        <label>Пароль:</label>
        <input type="password" name="password" required>
        <button type="submit">Видалити</button>
    </form>
    <a href="{url_for('show_monuments')}">Назад</a>
    """

if __name__ == "__main__":
    app.run(debug=True)