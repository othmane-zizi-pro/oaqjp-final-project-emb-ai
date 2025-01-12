"""
This module implements a Flask server for emotion detection.
It provides endpoints for analyzing text and detecting emotions.
"""

import logging
from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask("Emotion Detection")

@app.route("/")
def render_index_page():
    """
    Renders the main page of the application.
    Returns:
        str: Rendered HTML template
    """
    return render_template('index.html')

@app.route("/emotionDetector")
def emotion_detector_handler():
    """
    Handles emotion detection requests.
    Returns:
        str: Formatted emotion analysis result or error message
    """
    text = request.args.get('textToAnalyze')
    logger.info("Received request with text: %s", text)
    if not text or not text.strip():
        logger.warning("Empty text received")
        return "Invalid text! Please try again!"
    try:
        logger.debug("Calling emotion_detector")
        result = emotion_detector(text)
        logger.info("Emotion detector returned: %s", result)
        if result is None or result.get('dominant_emotion') is None:
            logger.error("Invalid emotion detection result")
            return "Invalid text! Please try again!"
        formatted_response = (
            f"For the given statement, the system response is "
            f"'anger': {result['anger']}, "
            f"'disgust': {result['disgust']}, "
            f"'fear': {result['fear']}, "
            f"'joy': {result['joy']} and "
            f"'sadness': {result['sadness']}. "
            f"The dominant emotion is {result['dominant_emotion']}."
        )
        logger.info("Sending response: %s", formatted_response)
        return formatted_response
    except (KeyError, ValueError) as error:
        logger.exception("Error processing request")
        return f"Error processing emotions: {str(error)}"

if __name__ == "__main__":
    logger.info("Starting server")
    app.run(host='0.0.0.0', port=5000)
    