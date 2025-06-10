from flask import Flask, render_template, request
import pymysql

app = Flask(__name__)

# MySQL 연결 함수
def get_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='!@kddies123',
        db='gunsan_food',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    keyword = request.form['keyword']
    category = request.form['category']

    conn = get_connection()
    cursor = conn.cursor()

    # 쿼리문 (Python 포맷팅 사용 안 함)
    query = """
        SELECT f.*, 
               CASE 
                   WHEN EXISTS (
                       SELECT 1 
                       FROM franchise.franchise fr
                       WHERE f.업소명 LIKE CONCAT('%%', REPLACE(TRIM(fr.프랜차이즈명), '\r', ''), '%%')
                   ) THEN '프랜차이즈'
                   ELSE '비프랜차이즈'
               END AS 프랜차이즈여부
        FROM gunsan_food.food_places f
        WHERE (f.업소명 LIKE %s OR f.지번 LIKE %s)
          AND (%s = '' OR f.음식종류 = %s)
    """

    # 변수 바인딩 처리 (SQL Injection 방지)
    cursor.execute(query, (f"%{keyword}%", f"%{keyword}%", category, category))
    results = cursor.fetchall()

    conn.close()
    return render_template('result.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
