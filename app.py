from flask import Flask, request
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline

app = Flask(__name__)

# Initialize summarization pipeline outside the function
summariser = pipeline('summarization', model='sshleifer/distilbart-cnn-12-6', revision='a4f8f3e', framework="pt")

@app.route('/summary', methods=['GET'])
def summary_api():
    url = request.args.get('url', '')
    video_id = url.split('=')[1]
    transcript = get_transcript(video_id)
    summary = get_summary(transcript)
    return summary, 200

def get_transcript(video_id):
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    transcript = ' '.join([d['text'] for d in transcript_list])
    return transcript

def get_summary(transcript):
    # Split transcript into chunks and summarize
    chunks = [transcript[i:i+1000] for i in range(0, len(transcript), 1000)]
    summary = ' '.join([summariser(chunk, max_length=100, min_length=50, do_sample=False)[0]['summary_text'] for chunk in chunks])
    return summary

if __name__ == '__main__':
    app.run()
