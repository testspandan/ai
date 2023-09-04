from django.shortcuts import render
import os
import requests
from time import sleep

def index(request):
    if request.method == 'POST':
        input_text = request.POST.get('input_text', '')

        payload = {
            "input_face": "https://storage.googleapis.com/dara-c1b52.appspot.com/daras_ai/media/aa56941c-c6fc-11ed-9ff7-02420a000128/natya2%20-%20Made%20with%20Clipchamp.mp4",
            "input_audio": "https://storage.googleapis.com/dara-c1b52.appspot.com/daras_ai/media/6dcd03b4-a799-11ed-9033-02420a0001d8/google_tts_gen.wav",
            "face_padding_top": 3,
            "face_padding_bottom": 16,
            "face_padding_left": 12,
            "face_padding_right": 6,
            "text_prompt": input_text,  # Use user input here
            "tts_provider": "GOOGLE_TTS",
            "uberduck_voice_name": "the-rock",
            "uberduck_speaking_rate": 1,
            "google_voice_name": "en-IN-Wavenet-A",
            "google_speaking_rate": 1.2,
            "google_pitch": -1.75,
        }

        response = requests.post(
            "https://api.gooey.ai/v3/LipsyncTTS/async/?example_id=yqihlh3w",
            headers={
                "Authorization": "Bearer " + os.environ["GOOEY_API_KEY"],
            },
            json=payload,
        )

        assert response.ok, response.content

        status_url = response.headers["Location"]
        while True:
            response = requests.get(
                status_url, headers={"Authorization": "Bearer " + os.environ["GOOEY_API_KEY"]}
            )
            assert response.ok, response.content
            result = response.json()
            if result["status"] == "completed":
                output_url = result['output']['output_video']
                return render(request, 'myapp/result.html', {'output_url': output_url})
            elif result["status"] == "failed":
                return render(request, 'myapp/error.html')
            else:
                sleep(3)

    return render(request, 'myapp/index.html')
