# YouTube Intro Generator API

This is a simple Flask-based API designed to generate YouTube video intros using different models. The API allows generating intros via four different platforms:

- Gemini
- ChatGPT
- Claude
- Hugging Face

## Endpoints

### 1. `/gemini-generate-intro`

**Method:** `POST`  
**Description:** Generates an intro using Gemini.  
**Request Body:**
```json
{
  "prompt": "Your video intro prompt here"
}
```

### Response:
```json
{
  "intro": "Generated intro text from Gemini"
}
```

### 2. `/chatgpt-generate-intro`

**Method:** `POST`  
**Description:** Generates an intro using ChatGPT.
**Request Body:**
```json
{
  "prompt": "Your video intro prompt here"
}
```

### Response:
```json
{
  "intro": "Generated intro text from ChatGPT"
}
```

### 3. `/claude-generate-intro`
**Method:** `POST`  
**Description:** Generates an intro using Claude.  
**Request Body:**
```json
{
  "prompt": "Your video intro prompt here"
}
```

### Response:
```json
{
  "intro": "Generated intro text from Claude"
}
```

### 4. `/huggingface-generate-intro`
**Method:** `POST`  
**Description:** GGenerates an intro using Hugging Face. 
**Request Body:**
```json
{
  "prompt": "Your video intro prompt here"
}
```

### Response:
```json
{
  "intro": "Generated intro text from Hugging Face"
}
```
