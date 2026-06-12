from flask import Flask, request, send_file, jsonify
import edge_tts
import asyncio
import os
import uuid

app = Flask(__name__)

@app.route('/tts', methods=['POST'])
def tts():
    data = request.json
    text = data.get('text')
    voice = data.get('voice', 'en-US-GuyNeural')

    if not text:
        return jsonify({"error": "text is required"}), 400

    filename = f"/tmp/{uuid.uuid4()}.mp3"

    async def generate():
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(filename)

    asyncio.run(generate())

    response = send_file(filename, mimetype='audio/mpeg', as_attachment=True, download_name='voice.mp3')

    @response.call_on_close
    def cleanup():
        if os.path.exists(filename):
            os.remove(filename)

    return response

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
