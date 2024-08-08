Here's an updated version of the README, including details for both posting and searching through the `/post` endpoint:

---

# Flask API Application

This Flask application is designed to handle several functionalities, including user authentication, vectorizing content, storing and searching vectors using Qdrant, keyword extraction using RAKE, and creating Google Calendar events. Below is a detailed guide to understanding and running the application.

## Table of Contents
- [Features](#features)
- [Setup and Installation](#setup-and-installation)
- [Environment Variables](#environment-variables)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Usage](#usage)
- [Dependencies](#dependencies)

## Features
1. **User Authentication**: Authenticate users using Firebase Firestore.
2. **Vectorization and Similarity Search**: Vectorize content using `llama-cpp-python` and perform similarity searches using Qdrant.
3. **Keyword Extraction**: Extract keywords from text using RAKE.
4. **Google Calendar Integration**: Create calendar events using Google Calendar API.

## Setup and Installation

### 1. Clone the Repository
```bash
git clone https://github.com/LiveWiresSRM2023/Curious-Bees.git
cd Curious-Bees/Curious-backend/Curious-Bees
```

### 2. Create and Activate Virtual Environment
```bash
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Firebase Setup
- Place your Firebase service account key file `serviceKey.json` in the root directory of your project.

### 5. Google Calendar API Setup
- Ensure you have `credentials.json` for Google Calendar API in the root directory.
- Generate `token.json` after the first OAuth2.0 flow.

## Environment Variables
Make sure to set the following environment variables:

- `GOOGLE_APPLICATION_CREDENTIALS`: Path to your `serviceKey.json` file for Firebase.

Example:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="path/to/serviceKey.json"
```

## Running the Application
```bash
python app.py
```

The application will run on `http://127.0.0.1:5000/` by default.

## API Endpoints

### 1. Home
- **URL**: `/`
- **Method**: `GET`
- **Description**: Check if the API is running.
- **Response**: `{"Flask API" : "Running"}`

### 2. Process Data
- **URL**: `/post`
- **Method**: `POST`
- **Description**: Process data by either storing it in the database or performing a similarity search based on the provided `type` field.
- **Request Body**:
  ```json
  {
    "user_id": "string",
    "type": "string",  // 'post' for storing data, 'search' for similarity search
    "content": "string",
    "id": "string"
  }
  ```
- **Response**: 
  - For `type: post`:
    ```json
    {
      "msg": "Data processed successfully"
    }
    ```
  - For `type: search`:
    ```json
    {
      "id1": score1,
      "id2": score2,
      "id3": score3
    }
    ```
  - Unauthorized or Error:
    ```json
    {
      "msg": "Unauthorized access"  // or
      "msg": "There was an error"
    }
    ```

### 3. Extract Keywords
- **URL**: `/keywords`
- **Method**: `POST`
- **Description**: Extract keywords from the provided text content.
- **Request Body**:
  ```json
  {
    "user_id": "string",
    "content": "string"
  }
  ```
- **Response**:
  ```json
  {
    "keywords": ["keyword1", "keyword2", "keyword3"]
  }
  ```

### 4. Create Event
- **URL**: `/create_event`
- **Method**: `POST`
- **Description**: Create a Google Calendar event.
- **Request Body**:
  ```json
  {
    "user_id": "string",
    "summary": "string",
    "description": "string",
    "start_time": "string",
    "end_time": "string",
    "attendees": ["string"]
  }
  ```
- **Response**:
  ```json
  {
    "msg": "Event created successfully",
    "link": "event_link"
  }
  ```

## Usage

### Example: Process Data
#### Posting Data
```bash
curl -X POST http://127.0.0.1:5000/post -H "Content-Type: application/json" -d '{
  "user_id": "user123",
  "type": "post",
  "content": "This is a test content.",
  "id": "content123"
}'
```

#### Searching Data
```bash
curl -X POST http://127.0.0.1:5000/post -H "Content-Type: application/json" -d '{
  "user_id": "user123",
  "type": "search",
  "content": "This is a test content.",
  "id": "content123"
}'
```

### Example: Extract Keywords
```bash
curl -X POST http://127.0.0.1:5000/keywords -H "Content-Type: application/json" -d '{
  "user_id": "user123",
  "content": "This is a sample text for keyword extraction."
}'
```

### Example: Create Event
```bash
curl -X POST http://127.0.0.1:5000/create_event -H "Content-Type: application/json" -d '{
  "user_id": "user123",
  "summary": "Team Meeting",
  "description": "Discussion about the upcoming project.",
  "start_time": "2024-08-15T10:00:00-07:00",
  "end_time": "2024-08-15T11:00:00-07:00",
  "attendees": ["email1@example.com", "email2@example.com"]
}'
```



For any issues or contributions, feel free to raise a pull request or create an issue in the repository.

---
