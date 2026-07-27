from flask import Flask, render_template, request, jsonify, redirect
import os
import psycopg2
from datetime import datetime

app = Flask(__name__)

# Подключение к базе данных
DATABASE_URL = os.getenv("DATABASE_URL")

@app.route('/')
def home():
    return redirect('/tg/app/')

@app.route('/tg/app/')
def index():
    return render_template('index.html')

@app.route('/tg/app/submit', methods=['POST'])
def submit():
    data = request.get_json()
    print(f"Получены данные: {data}")
    return jsonify({"status": "ok", "message": "Данные получены!"})

# ===== СТАТИСТИКА ИЗ БАЗЫ ДАННЫХ =====
@app.route('/api/stats/<int:user_id>')
def get_stats(user_id):
    """Возвращает статистику по поручениям пользователя"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        # Всего поручений
        cur.execute("SELECT COUNT(*) FROM assignments WHERE user_id = %s", (user_id,))
        total = cur.fetchone()[0]
        
        # Выполненных
        cur.execute("SELECT COUNT(*) FROM assignments WHERE user_id = %s AND status = 'completed'", (user_id,))
        completed = cur.fetchone()[0]
        
        # Активных (не выполненных)
        cur.execute("SELECT COUNT(*) FROM assignments WHERE user_id = %s AND status != 'completed'", (user_id,))
        active = cur.fetchone()[0]
        
        # Просроченных
        today = datetime.now().date()
        cur.execute("""
            SELECT COUNT(*) FROM assignments 
            WHERE user_id = %s AND status != 'completed' AND deadline < %s
        """, (user_id, today))
        overdue = cur.fetchone()[0]
        
        cur.close()
        conn.close()
        
        return jsonify({
            "total": total,
            "completed": completed,
            "active": active,
            "overdue": overdue
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)