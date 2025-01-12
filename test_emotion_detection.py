import unittest
from EmotionDetection.emotion_detection import emotion_detector

class TestEmotionDetector(unittest.TestCase):
    def test_emotion_detector(self):
        test_cases = [
            ("I am glad this happened", "joy"),
            ("I am really mad about this", "anger"),
            ("I feel disgusted just hearing about this", "disgust"),
            ("I am so sad about this", "sadness"),
            ("I am really afraid that this will happen", "fear")
        ]
        
        for text, expected_emotion in test_cases:
            result = emotion_detector(text)
            self.assertIsNotNone(result, f"Result should not be None for text: {text}")
            self.assertIn('dominant_emotion', result, f"Result should contain dominant_emotion for text: {text}")
            self.assertEqual(result['dominant_emotion'], expected_emotion, 
                           f"Expected {expected_emotion} but got {result['dominant_emotion']} for text: {text}")

if __name__ == "__main__":
    unittest.main()