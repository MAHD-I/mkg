from flask import Flask, request, send_file
import os
from moviepy.editor import VideoFileClip

app = Flask(__name__)

@app.route('/extract-audio', methods=['POST'])
def extract_audio():
    if 'video' not in request.files:
        return {"error": "No video file provided"}, 400

    video_file = request.files['video']
    video_path = "video.mp4"
    audio_path = "audio.ogg"

    video_file.save(video_path)

    try:
        # استخراج صدا از ویدیو
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path, codec="libvorbis", bitrate="64k")
        video.close()

        return send_file(audio_path, mimetype="audio/ogg", as_attachment=True, download_name="audio.ogg")

    except Exception as e:
        return {"error": str(e)}, 500

    finally:
        # حذف فایل‌های موقت
        os.remove(video_path)
        os.remove(audio_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
