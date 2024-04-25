
# Flask Application with Qdrant Integration

This Flask application integrates with Qdrant for vectorized storing of posts and searching similar posts. It provides endpoints for both storing data and searching for similar content.

## Prerequisites

- Python 3.x
- Flask
- Qdrant Client

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/LiveWiresSRM2023/Curious-Bees
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up Qdrant:

   - Obtain API key and URL from Qdrant
   - Create `password.py` with your API key and URL stored in the variables of the same name

## Usage

1. Start the Flask server:

   ```bash
   python SE&DB_API.py
   ```

2. Send POST requests to store data:

   ```http
   POST /data
   Content-Type: application/json

   {
       "user_id": "<user_id>",
       "type": "post",
       "content": "<content>",
       "id_token": "<id_token>"
   }
   ```

3. Send POST requests to search for similar content:

   ```http
   POST /search
   Content-Type: application/json

   {
       "user_id": "<user_id>",
       "type": "search",
       "content": "<content>",
       "id_token": "<id_token>"
   }
   ```

4. Vectorize and Send Data to Database:

   We've implemented the `vectorize_content` and `send_db` functions in our Flask application. When sending a POST request with data, we vectorize the content using these functions and store it in the database along with its ID.

5. Vectorize Query and Find Similar Posts:

   We've also implemented the `similarity` function in our Flask application. When sending a POST request for searching, we vectorize the content of the query and compare it with existing posts in the database to find similar ones. These similar posts are then sent back to the user.

## Contributing

Contributions to improve the versatility and functionality of this project are welcome! Your effort in making this project robust is much appreciated!

