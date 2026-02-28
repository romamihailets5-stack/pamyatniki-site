import sqlite3
import os

DB_NAME = "monuments.db"

def add_monument(name, location, price, image="", material="", description=""):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "INSERT INTO monuments (name, location, price, image, material, description) VALUES (?, ?, ?, ?, ?, ?)",
        (name, location, price, image, material, description)
    )
    conn.commit()
    conn.close()
    print(f"✅ Памятник '{name}' добавлен!")

def delete_monument(monument_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM monuments WHERE id=?", (monument_id,))
    conn.commit()
    conn.close()
    print(f"❌ Памятник с ID={monument_id} удалён!")

def list_monuments():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, name, location, price FROM monuments")
    monuments = c.fetchall()
    conn.close()
    if monuments:
        print("\nСписок памятников:")
        for m in monuments:
            print(f"ID={m[0]} | {m[1]} | Місто: {m[2]} | Ціна: {m[3]} ₴")
    else:
        print("\nПамятники в базе отсутствуют.")

def main_menu():
    while True:
        print("\n=== Меню управления памятниками ===")
        print("1. Показать все памятники")
        print("2. Добавить памятник")
        print("3. Удалить памятник")
        print("4. Выход")

        choice = input("Выберите действие (1-4): ")

        if choice == "1":
            list_monuments()
        elif choice == "2":
            name = input("Название памятника: ")
            location = input("Место расположения: ")
            price = float(input("Цена (грн): "))
            image = input("Путь к фото (например images/photo.jpg, оставьте пустым если нет): ")
            material = input("Материал: ")
            description = input("Описание памятника: ")
            add_monument(name, location, price, image, material, description)
        elif choice == "3":
            monument_id = int(input("Введите ID памятника для удаления: "))
            delete_monument(monument_id)
        elif choice == "4":
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main_menu()