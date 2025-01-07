import os
import unittest
from unittest.mock import patch
import json
import requests
from app import app

class FlaskAppTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()
        cls.client.testing = True

    def test_gemini_generate_intro_success(self):
        with patch('requests.post') as mocked_post, patch.dict(os.environ, {"GEMINI_API_KEY": "mocked_api_key"}):
            mocked_post.return_value.status_code = 200
            mocked_post.return_value.json.return_value = {
                'candidates': [
                    {
                        'content': {
                            'parts': [
                                {'text': 'Generated intro'}
                            ]
                        }
                    }
                ]
            }
            
            data = {'prompt': 'Write an intro for my YouTube channel on tech tutorials.'}
            
            response = self.client.post('/gemini-generate-intro', 
                                        data=json.dumps(data), 
                                        content_type='application/json')
            
            self.assertEqual(response.status_code, 200)
            
            response_json = response.get_json()

            self.assertIn('intro', response_json)
            self.assertEqual(response_json['intro'], "Generated intro")

    def test_gemini_generate_intro_missing_prompt(self):
        data = {}
        response = self.client.post('/gemini-generate-intro', 
                                    data=json.dumps(data), 
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        response_json = response.get_json()
        self.assertEqual(response_json['error'], 'Prompt is required')

    def test_gemini_generate_intro_invalid_json(self):
        response = self.client.post('/gemini-generate-intro', 
                                    data="Invalid JSON", 
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, 400)

    def test_gemini_generate_intro_server_error(self):
        with patch('requests.post') as mocked_post:
            mocked_post.side_effect = requests.exceptions.RequestException('External API failure')

            os.environ['GEMINI_API_KEY'] = 'mocked_api_key'

            data = {
                'prompt': 'Write an intro for my YouTube channel on tech tutorials.'
            }
            response = self.client.post('/gemini-generate-intro', 
                                        data=json.dumps(data), 
                                        content_type='application/json')

            self.assertEqual(response.status_code, 500)
            response_json = response.get_json()
            self.assertEqual(response_json['error'], 'API error: External API failure')

    def test_chatgpt_generate_intro_success(self):
        with patch('requests.post') as mocked_post, patch.dict(os.environ, {"CHATGPT_API_KEY": "mocked_api_key"}):
            mocked_post.return_value.status_code = 200
            mocked_post.return_value.json.return_value = {'choices': [{'message': {'content': 'Generated intro'}}]}

            data = {
                'prompt': 'Write an intro for my YouTube channel on tech tutorials.'
            }
            response = self.client.post('/chatgpt-generate-intro', 
                                        data=json.dumps(data), 
                                        content_type='application/json')

            self.assertEqual(response.status_code, 200)
            response_json = response.get_json()
            self.assertIn('intro', response_json)

    def test_chatgpt_generate_intro_missing_prompt(self):
        data = {}
        response = self.client.post('/chatgpt-generate-intro', 
                                    data=json.dumps(data), 
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        response_json = response.get_json()
        self.assertEqual(response_json['error'], 'Prompt is required')

    def test_chatgpt_generate_intro_invalid_json(self):
        response = self.client.post('/chatgpt-generate-intro', 
                                    data="Invalid JSON", 
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, 400)

    def test_chatgpt_generate_intro_server_error(self):
        with patch('requests.post') as mocked_post:
            mocked_post.side_effect = requests.exceptions.RequestException('External API failure')

            os.environ['CHATGPT_API_KEY'] = 'mocked_api_key'

            data = {
                'prompt': 'Write an intro for my YouTube channel on tech tutorials.'
            }
            response = self.client.post('/chatgpt-generate-intro', 
                                        data=json.dumps(data), 
                                        content_type='application/json')

            self.assertEqual(response.status_code, 500)
            response_json = response.get_json()
            self.assertEqual(response_json['error'], 'API error: External API failure')
    

    def test_claude_generate_intro_success(self):
        with patch('requests.post') as mocked_post, patch.dict(os.environ, {"CLAUDE_API_KEY": "mocked_api_key"}):
            mocked_post.return_value.status_code = 200
            mocked_post.return_value.json.return_value = {'completion': 'Generated intro'}

            data = {'prompt': 'Write an intro for my YouTube channel on tech tutorials.'}
            response = self.client.post('/claude-generate-intro',
                                        data=json.dumps(data),
                                        content_type='application/json')

            self.assertEqual(response.status_code, 200)
            response_json = response.get_json()
            self.assertIn('intro', response_json)
            self.assertEqual(response_json['intro'], 'Generated intro')

    def test_claude_generate_intro_missing_prompt(self):
        data = {}
        response = self.client.post('/claude-generate-intro',
                                    data=json.dumps(data),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 400)
        response_json = response.get_json()
        self.assertEqual(response_json['error'], 'Prompt is required')

    def test_claude_generate_intro_server_error(self):
        with patch('requests.post') as mocked_post:
            mocked_post.side_effect = requests.exceptions.RequestException('External API failure')
            os.environ['CLAUDE_API_KEY'] = 'mocked_api_key'

            data = {'prompt': 'Write an intro for my YouTube channel on tech tutorials.'}
            response = self.client.post('/claude-generate-intro',
                                        data=json.dumps(data),
                                        content_type='application/json')

            self.assertEqual(response.status_code, 500)
            response_json = response.get_json()
            self.assertEqual(response_json['error'], 'API error: External API failure')

    def test_claude_generate_intro_invalid_api_key(self):
        with patch('requests.post') as mocked_post, patch.dict(os.environ, {"CLAUDE_API_KEY": ""}):
            mocked_post.return_value.status_code = 403
            mocked_post.return_value.json.return_value = {'error': 'Invalid API key'}

            data = {'prompt': 'Write an intro for my YouTube channel on tech tutorials.'}
            response = self.client.post('/claude-generate-intro',
                                        data=json.dumps(data),
                                        content_type='application/json')

            self.assertEqual(response.status_code, 500)
            response_json = response.get_json()
            self.assertEqual(response_json['error'], 'API key not provided')
    
    def test_huggingface_generate_intro_success(self):
        with patch('requests.post') as mocked_post, patch.dict(os.environ, {"HUGGINGFACE_API_KEY": "mocked_api_key"}):
            mocked_post.return_value.status_code = 200
            mocked_post.return_value.json.return_value = [{'generated_text': 'Generated intro text'}]

            data = {
                'prompt': 'Write an intro for my YouTube channel on tech tutorials.'
            }
            response = self.client.post('/huggingface-generate-intro', 
                                        data=json.dumps(data), 
                                        content_type='application/json')

            self.assertEqual(response.status_code, 200)
            response_json = response.get_json()
            self.assertIn('intro', response_json)
            self.assertEqual(response_json['intro'], 'Generated intro text')

    def test_huggingface_generate_intro_missing_prompt(self):
        data = {}
        response = self.client.post('/huggingface-generate-intro', 
                                    data=json.dumps(data), 
                                    content_type='application/json')

        self.assertEqual(response.status_code, 400)
        response_json = response.get_json()
        self.assertEqual(response_json['error'], 'Prompt is required')

    def test_huggingface_generate_intro_invalid_json(self):
        response = self.client.post('/huggingface-generate-intro', 
                                    data="Invalid JSON", 
                                    content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_huggingface_generate_intro_server_error(self):
        with patch('requests.post') as mocked_post:
            mocked_post.side_effect = requests.exceptions.RequestException('External API failure')

            os.environ['HUGGINGFACE_API_KEY'] = 'mocked_api_key'

            data = {
                'prompt': 'Write an intro for my YouTube channel on tech tutorials.'
            }
            response = self.client.post('/huggingface-generate-intro', 
                                        data=json.dumps(data), 
                                        content_type='application/json')

            self.assertEqual(response.status_code, 500)
            response_json = response.get_json()
            self.assertEqual(response_json['error'], 'API error: External API failure')

    def test_huggingface_generate_intro_invalid_api_key(self):
        with patch('requests.post') as mocked_post, patch.dict(os.environ, {"HUGGINGFACE_API_KEY": ""}):
            mocked_post.return_value.status_code = 403
            mocked_post.return_value.json.return_value = {'error': 'Invalid API key'}

            data = {'prompt': 'Write an intro for my YouTube channel on tech tutorials.'}
            response = self.client.post('/huggingface-generate-intro',
                                        data=json.dumps(data),
                                        content_type='application/json')

            self.assertEqual(response.status_code, 500)
            response_json = response.get_json()
            self.assertEqual(response_json['error'], 'API key not provided')

if __name__ == '__main__':
    unittest.main()