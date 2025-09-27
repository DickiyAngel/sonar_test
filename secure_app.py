import secrets
import subprocess
import os
import sqlite3
from flask import Flask, request, render_template, escape, jsonify
import yaml
import bcrypt
from pathlib import Path

app = Flask(__name__)

# 🟢 БЕЗОПАСНЫЕ АЛЬТЕРНАТИВЫ

# 1. Безопасная альтернатива десериализации
@app.route('/unpickle', methods=['POST'])
def unpickle_data():
    # Используем JSON вместо pickle
    data = request.get_json()
    return jsonify({"status": "Use JSON for serialization"})

# 2. Безопасное выполнение команд
@app.route('/execute', methods=['GET'])
def execute_command():
    allowed_commands = {'ls': ['ls', '-la'], 'pwd': ['pwd']}
    cmd = request.args.get('cmd', 'ls')
    
    if cmd in allowed_commands:
        result = subprocess.run(
            allowed_commands[cmd], 
            capture_output=True, 
            text=True, 
            shell=False  # Без shell!
        )
        return result.stdout
    return "Command not allowed"

# 3. Защита от SQL Injection
@app.route('/search', methods=['GET'])
def search_users():
    username = request.args.get('username', '')
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    
    # Параметризованные запросы
    query = "SELECT * FROM users WHERE username = ?"
    cursor.execute(query, (username,))
    return jsonify(cursor.fetchall())

# 4. Защита от XSS
@app.route('/hello', methods=['GET'])
def hello_xss():
    name = request.args.get('name', 'World')
    safe_name = escape(name)  # Экранирование вывода
    return f"<h1>Hello, {safe_name}!</h1>"

# 5. Защита от Path Traversal
@app.route('/readfile', methods=['GET'])
def read_file():
    filename = request.args.get('file', 'test.txt')
    base_dir = Path('/safe/directory')
    file_path = (base_dir / filename).resolve()
    
    # Проверка что файл внутри разрешенной директории
    if base_dir.resolve() not in file_path.parents:
        return "Access denied", 403
    
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return "File not found", 404

# 6. Безопасная YAML загрузка
@app.route('/yaml-load', methods=['POST'])
def yaml_load():
    data = request.get_data(as_text=True)
    obj = yaml.safe_load(data)  # Безопасный загрузчик
    return str(obj)

# 🟢 БЕЗОПАСНЫЕ ПРАКТИКИ

# 7. Пароль из переменных окружения
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'default_strong_password')

# 8. Strong cryptography
def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)

# 9. Криптографически безопасная случайность
def generate_api_key():
    return secrets.token_urlsafe(32)

# 10. Production mode
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)

# 🟢 ЧИСТЫЙ КОД

# 11. Защита от бесконечных циклов
def process_data(max_iterations=1000):
    for i in range(max_iterations):
        print("Processing...")
        if i >= max_iterations - 1:
            break

# 13. Устранение дублирования
def calculate_area(width, height):
    return width * height

# 14. Упрощение сложной функции
def simplified_function(x, y, z):
    # Логика упрощена для примера
    if x > y:
        return min(x * y * z, 100)
    return max(x + y + z, 0)