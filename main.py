import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_TOKEN")
ADMIN_USER_ID = os.environ.get("LINE_ADMIN_ID")

def push_message(to, msg):
    res = requests.post(
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
    print(f"LINE API response: {res.status_code} {res.text}")
    return res

@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()
    print(f"Received data: {data}")

    brand = data.get("brand", "")
    model = data.get("model", "")
    year = data.get("year", "")
    part = data.get("part", "")
    note = data.get("note", "")
    photos = data.get("photos", 0)

    lines = [
        f"🚗 รถ: {brand}{' ' + model if model else ''} ปี {year}",
        f"🔧 อะไหล่: {part}",
    ]
    if note:
        lines.append(f"📝 หมายเหตุ: {note}")
    if photos > 0:
        lines.append(f"📷 แนบรูป {photos} รูป")

    msg = "\n".join(lines)

    print(f"Sending to ADMIN_USER_ID: {ADMIN_USER_ID}")
    print(f"TOKEN exists: {bool(CHANNEL_ACCESS_TOKEN)}")

    if ADMIN_USER_ID:
        push_message(ADMIN_USER_ID, f"📥 มีคำขออะไหล่ใหม่!\n\n{msg}")

    return jsonify({"status": "ok"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
