import json
import requests

def test_keyword_extraction():
    url = "http://localhost:5000/keywords"

    data = {
        "user_id": "123",
        "content": "This is an example of content for keyword extraction."
    }

    json_data = json.dumps(data)
    response = requests.post(url, data=json_data, headers={"Content-Type": "application/json"})

    if response.status_code == 200:
        print("Success! Response:", response.json())
    else:
        print("Error:", response.status_code, response.text)

def post_data():
    url = "http://localhost:5000/post"

    data = {
        "user_id": "123",
        "type": "post",
        "content": "This is an example post content.",
        "id": "301f6620-2a27-48f4-a284-be74e0566680"
    }

    json_data = json.dumps(data)
    response = requests.post(url, data=json_data, headers={"Content-Type": "application/json"})

    if response.status_code == 200:
        print("Success! Response:", response.json())
    else:
        print("Error:", response.status_code, response.text)

def search_data():
    url = "http://localhost:5000/post"

    data = {
        "user_id": "123",
        "type": "search",
        "content": "This is the content to search for.",
        "id": "301f6620-2a27-48f4-a284-be74e0566680"
    }

    json_data = json.dumps(data)
    response = requests.post(url, data=json_data, headers={"Content-Type": "application/json"})

    if response.status_code == 200:
        print("Success! Response:", response.json())
    else:
        print("Error:", response.status_code, response.text)


def create_event():
    url = 'http://localhost:5000/create_event'
    data = {
        'user_id': '123',
        'summary': 'Vangana vanakanga na',
        'description': 'Vanga Palagalam.',
        'start_time': '2024-07-28T04:00:00-07:00',  # Adjust the date and time as needed
        'end_time': '2024-07-28T05:00:00-07:00',    # Adjust the date and time as needed
        'attendees': 'snikilpaul@gmail.com, ns6032@srmist.edu.in,rs3322@srmist.edu.in,skroshan.me@gmail.com'  # Add more emails separated by commas
    }

    # Convert the attendees to the required format
    attendees_list = [email.strip() for email in data['attendees'].split(',')]
    data['attendees'] = attendees_list

    json_data = json.dumps(data)
    response = requests.post(url, data=json_data, headers={"Content-Type": "application/json"})

    if response.status_code == 200:
        print('Event created successfully:')
        print(response.json())
    else:
        print('Failed to create event:')
        print(response.status_code)
        print(response.text)

def main():
    print("Choose an option:")
    print("1. Test Keyword Extraction")
    print("2. Post Data")
    print("3. Search Data")
    print("4. Create Event")

    choice = input("Enter your choice (1, 2, 3 or 4): ")

    if choice == '1':
        test_keyword_extraction()
    elif choice == '2':
        post_data()
    elif choice == '3':
        search_data()
    elif choice == '4':
        create_event()
    else:
        print("Invalid choice. Please enter 1, 2, 3 or 4.")

if __name__ == '__main__':
    main()
