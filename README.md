# Flask Backend For Curious Bees

## Overview

This Flask application provides a REST API for storing, searching, and managing content in a Qdrant database, extracting keywords using RAKE, and creating events in Google Calendar. It includes endpoints for posting and deleting data, searching for similar content, extracting keywords, and creating calendar events.

## Features

- **Content Management**: Store and delete content vectors in a Qdrant database.
- **Similarity Search**: Search for similar content based on vector similarity.
- **Keyword Extraction**: Extract keywords from content using the RAKE algorithm.
- **Google Calendar Integration**: Create events in Google Calendar with the ability to include Google Meet links.

## Dependencies

- `Flask` - A micro web framework for Python.
- `Flask-CORS` - To enable CORS (Cross-Origin Resource Sharing).
- `qdrant-client` - Qdrant client library for interacting with the Qdrant database.
- `llama-cpp` - For vectorizing content.
- `firebase-admin` - Firebase Admin SDK for Firebase authentication.
- `nltk` - Natural Language Toolkit for text processing.
- `rake-nltk` - RAKE (Rapid Automatic Keyword Extraction) implementation for Python.
- `google-auth` - Google Authentication libraries.
- `google-auth-oauthlib` - OAuth 2.0 client for Google services.
- `google-api-python-client` - Google API client library.
- `requests` - For making HTTP requests.

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/LiveWiresSRM2023/Curious-Bees.git
   cd Curious-Bees
   ```

2. **Create and Activate a Virtual Environment:**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables:**
   Ensure you have the following files in your project directory:
   - `serviceKey.json` - Firebase Admin SDK service account key.
   - `credentials.json` - Google API credentials file for OAuth 2.0.

## Running the Application

To start the Flask application, run:
```bash
python app.py
```

The application will be available at `http://localhost:7000`.

## API Endpoints

### 1. **Home Route**

- **GET** `/`
- **Description**: Check if the Flask API is running.
- **Response**: `{"Flask API": "Running"}`

### 2. **Post and Delete Data**

- **POST** `/posthandler`
- **Description**: Handles both posting data to the Qdrant database and deleting vectors based on the `type` in the request data.
- **Request Payload**:
  ```json
  {
    "user_id": "string",
    "type": "post" | "delete",
    "id": "string",
    "content": "string"  // Only for type "post"
  }
  ```
- **Response**: 
  - For posting: `{"status": "Data stored successfully"}`
  - For deletion: `{"status": "Vector deleted successfully", "vector_id": "string"}`

### 3. **Search for Similar Content**

- **POST** `/search`
- **Description**: Searches for similar content based on the vectorized input.
- **Request Payload**:
  ```json
  {
    "user_id": "string",
    "content": "string"
  }
  ```
- **Response**:
  ```json
  {
    "id": "score",
    ...
  }
  ```

### 4. **Extract Keywords**

- **POST** `/keywords`
- **Description**: Extracts keywords from the provided content using RAKE.
- **Request Payload**:
  ```json
  {
    "user_id": "string",
    "content": "string"
  }
  ```
- **Response**:
  ```json
  {
    "keywords": ["keyword1", "keyword2", ...]
  }
  ```

### 5. **Create Google Calendar Event**

- **POST** `/create_event`
- **Description**: Creates a Google Calendar event with the provided details.
- **Request Payload**:
  ```json
  {
    "user_id": "string",
    "summary": "string",
    "description": "string",
    "start_time": "string (ISO 8601 format)",
    "end_time": "string (ISO 8601 format)",
    "attendees": ["email1@example.com", "email2@example.com", ...]
  }
  ```
- **Response**:
  ```json
  {
    "msg": "Event created successfully",
    "link": "string (event link)"
  }
  ```

## Notes

- **Authentication**: The current implementation of authentication always returns `True`. Update the `process_data`, `search_data`, and `extract_keywords` routes to include proper authentication checks if needed.
- **Error Handling**: Ensure proper error handling in your production environment.
- **Testing**: Use the `tester.py` script to test different endpoints. Update the script with actual endpoint paths and payloads.

## Contributing

Feel free to submit issues or pull requests to enhance the functionality of this application.



