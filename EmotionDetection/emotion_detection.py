import requests
import json

def emotion_detector(text_to_analyze):
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {
        'grpc-metadata-mm-model-id': 'emotion_aggregated-workflow_lang_en_stock'
    }
    input_json = {
        'raw_document': {
            'text': text_to_analyze
        }
    }

    try:
        response = requests.post(url, json=input_json, headers=headers, timeout=5)
        response.raise_for_status()
        
        # Parse the response JSON
        response_json = json.loads(response.text)
        
        # Extract emotion scores
        emotions = response_json['emotionPredictions'][0]['emotion']
        
        # Create formatted output
        output = {
            'anger': emotions['anger'],
            'disgust': emotions['disgust'],
            'fear': emotions['fear'],
            'joy': emotions['joy'],
            'sadness': emotions['sadness'],
            'dominant_emotion': max(emotions.items(), key=lambda x: x[1])[0]
        }
        
        return output
        
    except requests.exceptions.Timeout:
        print("Request timed out")
        return None
    except requests.exceptions.ConnectionError:
        print("Connection error occurred")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None
    except (KeyError, json.JSONDecodeError) as e:
        print(f"Error parsing response: {e}")
        return None