import pickle
import subprocess
import os
import sqlite3
import random
import hashlib
from flask import Flask, request, render_template_string, jsonify
import yaml
import json

app = Flask(__name__)

# 🔴 КРИТИЧЕСКИЕ УЯЗВИМОСТИ

# 1. Уязвимость: Небезопасная десериализация
@app.route('/unpickle', methods=['POST'])
def unpickle_data():
    data = request.get_data()
    obj = pickle.loads(data)  # SONAR: Critical - Unsafe deserialization
    return str(obj)

# 2. Уязвимость: Command Injection
@app.route('/execute', methods=['GET'])
def execute_command():
    cmd = request.args.get('cmd', 'ls')
    # Опасное использование shell=True
    result = subprocess.check_output(cmd, shell=True)  # SONAR: Critical - Command injection
    return result.decode('utf-8')

# 3. Уязвимость: SQL Injection
@app.route('/search', methods=['GET'])
def search_users():
    username = request.args.get('username', '')
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    
    # Прямая подстановка в SQL
    query = f"SELECT * FROM users WHERE username = '{username}'"  # SONAR: Critical - SQL injection
    cursor.execute(query)
    return jsonify(cursor.fetchall())

# 🔴 СЕРЬЕЗНЫЕ УЯЗВИМОСТИ

# 4. Уязвимость: XSS
@app.route('/hello', methods=['GET'])
def hello_xss():
    name = request.args.get('name', 'World')
    # Потенциальный XSS
    template = f"<h1>Hello, {name}!</h1>"  # SONAR: Major - Potential XSS
    return render_template_string(template)

# 5. Уязвимость: Path Traversal
@app.route('/readfile', methods=['GET'])
def read_file():
    filename = request.args.get('file', 'test.txt')
    # Возможность читать любые файлы
    with open(filename, 'r') as f:  # SONAR: Major - Path traversal
        return f.read()

# 6. Уязвимость: Небезопасная YAML загрузка
@app.route('/yaml-load', methods=['POST'])
def yaml_load():
    data = request.get_data(as_text=True)
    obj = yaml.load(data, Loader=yaml.Loader)  # SONAR: Critical - Unsafe YAML load
    return str(obj)

# 🔴 УЯЗВИМОСТИ БЕЗОПАСНОСТИ

# 7. Хардкодный пароль
DB_PASSWORD = "super_secret_password_123"  # SONAR: Major - Hardcoded password

# 8. Weak cryptography
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()  # SONAR: Major - Weak hash

# 9. Небезопасная случайность
def generate_api_key():
    return str(random.randint(1000, 9999))  # SONAR: Major - Insecure randomness

# 10. Debug mode in production
if __name__ == '__main__':
    app.run(debug=True)  # SONAR: Major - Debug mode enabled

# 🔴 CODE SMELLS И БАГИ

# 11. Бесконечный цикл
def process_data():
    while True:  # SONAR: Bug - Endless loop
        print("Processing...")

# 12. Неиспользуемый код
def unused_function():  # SONAR: Code smell - Unused function
    return "I'm never used"

# 13. Дублирование кода
def calculate_area(width, height):
    return width * height

def calculate_rectangle_area(w, h):  # SONAR: Code smell - Duplicated code
    return w * h

# 14. Слишком сложная функция
def complicated_function(x, y, z):
    result = 0
    for i in range(10):
        if x > y and y < z or x == y and y != z or x < y and y > z:
            result += i * x * y * z
            if result > 100:
                for j in range(5):
                    result -= j
                    while result < 50:
                        result += 1
    return result  # SONAR: Code smell - Overly complex function