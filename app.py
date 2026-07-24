from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

from flask import Flask, render_template, request, jsonify, redirect  # ← добавьте redirect в импорт
import os

app = Flask(__name__)

# ===== ЭТОТ КОД ВСТАВЬТЕ СЮДА! =====
@app.route('/')
def home():
    return redirect('/tg/app/')
# ====================================

@app.route('/tg/app/')
def index():
    return render_template('index.html')

@app.route('/tg/app/submit', methods=['POST'])
def submit():
    data = request.get_json()
    print(f"Получены данные: {data}")
    return jsonify({"status": "ok", "message": "Данные получены!"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

@app.route('/tg/app/')
def index():
    return render_template('index.html')

@app.route('/tg/app/submit', methods=['POST'])
def submit():
    data = request.get_json()
    print(f"Получены данные: {data}")
    return jsonify({"status": "ok", "message": "Данные получены!"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)