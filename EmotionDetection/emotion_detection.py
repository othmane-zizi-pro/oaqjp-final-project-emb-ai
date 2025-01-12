import requests
import logging

logger = logging.getLogger(__name__)

def emotion_detector(text_to_analyze):
    logger.info(f"Analyzing text: {text_to_analyze}")
    
    if not text_to_analyze.strip():
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }
    
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {'grpc-metadata-mm-model-id': 'emotion_aggregated-workflow_lang_en_stock'}
    input_json = {'raw_document': {'text': text_to_analyze}}
    
    try:
        response = requests.post(url, json=input_json, headers=headers)
        logger.debug(f"Response status code: {response.status_code}")
        
        if response.status_code == 400:
            return {
                'anger': None,
                'disgust': None,
                'fear': None,
                'joy': None,
                'sadness': None,
                'dominant_emotion': None
            }
            
        response.raise_for_status()
        emotions = response.json()
        emotion_scores = emotions['emotionPredictions'][0]['emotion']
        
        return {
            'anger': emotion_scores['anger'],
            'disgust': emotion_scores['disgust'],
            'fear': emotion_scores['fear'],
            'joy': emotion_scores['joy'],
            'sadness': emotion_scores['sadness'],
            'dominant_emotion': max(emotion_scores.items(), key=lambda x: x[1])[0]
        }
        
    except Exception as e:
        logger.exception("Error in emotion_detector")
        return None