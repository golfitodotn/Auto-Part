import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_TOKEN")
ADMIN_USER_ID = os.environ.get("LINE_ADMIN_ID")

@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()

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

    requests.post(
        "https://api.line.me/v2/bot/message/push",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}"
        },
        json={
            "to": ADMIN_USER_ID,
            "messages": [{"type": "text", "text": msg}]
        }
    )

    return jsonify({"status": "ok"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
