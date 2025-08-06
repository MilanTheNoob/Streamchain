from flask import Flask, request, send_from_directory, jsonify, render_template_string
from datetime import datetime
import os

app = Flask(__name__)
UPLOAD_DIR = 'streams'
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.route('/')
def index():
    return render_template_string('''
        <h2>Upload or View Stream</h2>
        <form action="/upload" method="post" enctype="multipart/form-data">
            <input type="text" name="stream_id" placeholder="Stream ID" required>
            <input type="file" name="frame" required>
            <button type="submit">Upload Frame</button>
        </form>
        <hr>
        <form action="/view" method="get">
            <input type="text" name="stream_id" placeholder="Stream ID to view" required>
            <button type="submit">View Stream</button>
        </form>
    ''')

@app.route('/upload', methods=['POST'])
def upload():
    stream_id = request.form['stream_id']
    frame = request.files['frame']
    stream_path = os.path.join(UPLOAD_DIR, stream_id)
    os.makedirs(stream_path, exist_ok=True)
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S%f') + '.jpg'
    filepath = os.path.join(stream_path, timestamp)
    frame.save(filepath)
    return 'Frame uploaded', 200

@app.route('/view', methods=['GET'])
def view():
    stream_id = request.args.get('stream_id')
    stream_path = os.path.join(UPLOAD_DIR, stream_id)
    if not os.path.exists(stream_path):
        return 'Stream not found', 404
    files = sorted(os.listdir(stream_path))[-30:]  # Return last 30 frames
    image_tags = ''.join([f'<img src="/stream/{stream_id}/{file}" width="300"><br>' for file in files])
    return f"<h3>Viewing Stream: {stream_id}</h3>" + image_tags

@app.route('/latest/<stream_id>')
def latest_frame(stream_id):
    stream_path = os.path.join(UPLOAD_DIR, stream_id)
    if not os.path.exists(stream_path):
        return 'Not found', 404
    files = sorted(os.listdir(stream_path))
    if not files:
        return 'No frames', 404
    return send_from_directory(stream_path, files[-1])

@app.route('/stream/<stream_id>/<filename>')
def stream_image(stream_id, filename):
    return send_from_directory(os.path.join(UPLOAD_DIR, stream_id), filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

