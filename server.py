from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector
import json

app = Flask("Emotion Detection")

@app.route("/")
def render_index_page():
    return render_template('index.html')

@app.route("/emotionDetector")
def emotion_detector_handler():
    text = request.args.get('textToAnalyze')
    
    if not text:
        return "Please provide text to analyze"
        
    response = emotion_detector(text)
    
    if response is None:
        return "Error processing text"
        
    try:
        # Response is already a string from emotion_detector
        emotions = json.loads(response)
        emotion_scores = emotions['emotionPredictions'][0]['emotion']
        
        # Format response
        formatted_response = f"For the given statement, the system response is 'anger': {emotion_scores['anger']}, 'disgust': {emotion_scores['disgust']}, 'fear': {emotion_scores['fear']}, 'joy': {emotion_scores['joy']} and 'sadness': {emotion_scores['sadness']}. The dominant emotion is {max(emotion_scores.items(), key=lambda x: x[1])[0]}."
        
        return formatted_response
    except Exception as e:
        print(f"Error formatting response: {e}")
        return f"Error processing emotions: {str(e)}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)