# app.py
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # React와 연동을 위해 CORS 허용

# 기존 매크로 함수 import 또는 정의
from auto_macro import run_macro  # 예시: run_macro(date, time)

# 아래 부분은 삭제하거나 주석 처리해도 됩니다.
# @app.route("/", methods=["GET", "POST"])
# def index():
#     if request.method == "POST":
#         date = request.form["date"]
#         return "예매 매크로가 실행되었습니다!"
#     return render_template("index.html")

@app.route("/api/reserve", methods=["POST"])
def reserve():
    data = request.get_json()
    open_date = data.get("openDate")
    open_time = data.get("openTime")
    game_date_text = data.get("gameDateText")
    try:
        result = run_macro(open_date, open_time, game_date_text)
        return jsonify({"success": True, "message": result})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)