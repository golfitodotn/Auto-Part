import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_TOKEN")
ADMIN_USER_ID = os.environ.get("LINE_ADMIN_ID")

def push_message(to, msg):
    requests.post(
        "https://api.line.me/v2/bot/message/push",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}"
        },
        json={
            "to": to,
            "messages": [{"type": "text", "text": msg}]
        }
    )

@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()

    brand = data.get("brand", "")
    model = data.get("model", "")
    year = data.get("year", "")
    part = data.get("part", "")
    note = data.get("note", "")
    photos = data.get("photos", 0)
    user_id = data.get("userId")

    lines = [
        f"🚗 รถ: {brand}{' ' + model if model else ''} ปี {year}",
        f"🔧 อะไหล่: {part}",
    ]
    if note:
        lines.append(f"📝 หมายเหตุ: {note}")
    if photos > 0:
        lines.append(f"📷 แนบรูป {photos} รูป")

    msg = "\n".join(lines)

    # ส่งหาลูกค้าใน OA
    if user_id:
        push_message(user_id, f"✅ ได้รับคำขอแล้วครับ!\n\n{msg}\n\nร้านจะติดต่อกลับภายใน 30 นาที – 2 ชั่วโมง")

    # แจ้ง Admin
    if ADMIN_USER_ID:
        push_message(ADMIN_USER_ID, f"📥 มีคำขออะไหล่ใหม่!\n\n{msg}")

    return jsonify({"status": "ok"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
