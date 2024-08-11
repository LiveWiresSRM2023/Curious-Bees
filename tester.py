import requests
import uuid
import json

BASE_URL = "http://localhost:7000"

def print_response_details(response):
    print(f"Status Code: {response.status_code}")
    print(f"Response Content: {response.text}")
    try:
        print("Response JSON:", response.json())
    except json.JSONDecodeError:
        print("Failed to decode JSON, raw response is shown above.")

def test_home():
    response = requests.get(f"{BASE_URL}/")
    print("Home Route Response:")
    print_response_details(response)

def test_post_data(user_id, vector_id, content):
    payload = {
        "user_id": user_id,
        "type": "post",
        "id": vector_id,
        "content": content
    }
    response = requests.post(f"{BASE_URL}/posthandler", json=payload)
    print("Post Data Response:")
    print_response_details(response)

def test_delete_vector(user_id, vector_id):
    payload = {
        "user_id": user_id,
        "type": "delete",
        "id": vector_id
    }
    response = requests.post(f"{BASE_URL}/posthandler", json=payload)
    print("Delete Vector Response:")
    print_response_details(response)

def test_search(user_id, content):
    payload = {
        "user_id": user_id,
        "content": content
    }
    response = requests.post(f"{BASE_URL}/search", json=payload)
    print("Search Response:")
    print_response_details(response)

def test_extract_keywords(user_id, content):
    payload = {
        "user_id": user_id,
        "content": content
    }
    response = requests.post(f"{BASE_URL}/keywords", json=payload)
    print("Extract Keywords Response:")
    print_response_details(response)

def test_create_event(user_id, summary, description, start_time, end_time, attendees):
    payload = {
        "user_id": user_id,
        "summary": summary,
        "description": description,
        "start_time": start_time,
        "end_time": end_time,
        "attendees": attendees
    }
    response = requests.post(f"{BASE_URL}/create_event", json=payload)
    print("Create Event Response:")
    print_response_details(response)

if __name__ == "__main__":
    # Test home route
    test_home()
    stri=str(uuid.uuid4())
    # Test post data
    test_post_data(user_id="123", vector_id=stri, content="This is not a sample content to store in the database.")

    # Test search
    test_search(user_id="123", content="This is a sample content to search for.")

    # Test extract keywords
    test_extract_keywords(user_id="123", content="Extract keywords from this content using RAKE algorithm.")

    # Test delete vector
    test_delete_vector(user_id="123", vector_id=stri)

    # Test create event
    test_create_event(
        user_id="123",
        summary="Team Meeting",
        description="Discuss project updates and timelines.",
        start_time="2024-08-11T10:00:00-07:00",
        end_time="2024-08-11T11:00:00-07:00",
        attendees=["attendee1@example.com", "attendee2@example.com"]
    )
