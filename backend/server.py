from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
import os
import requests
import subprocess
import json
import logging
from bson import ObjectId  # Import to handle ObjectId conversion
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
# MongoDB Configuration
app.config["MONGO_URI"] = f"mongodb+srv://{os.getenv('MONGODB_USERNAME')}:{os.getenv('MONGODB_PASSWORD')}@cluster0.nsgw5.mongodb.net/gph?retryWrites=true&w=majority&appName=Cluster0"
mongo = PyMongo(app)
gph_temp = os.getenv('gph_temp')

# Hello World Endpoint
@app.route('/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Hello World"}), 200

# Run External Script
import time

def run_your_script(search_type, degree, depth, platform, data):
    try:
        # Define script paths based on platform
        script_path = {
            "Instagram": os.getenv('INSTAGRAM_SCRIPT_PATH', './instagram/main.py'),
            "Twitter": os.getenv('TWITTER_SCRIPT_PATH', './twitter/main.py')
        }.get(platform)

        if not script_path or not os.path.exists(script_path):
            return {"error": "Unsupported platform or script not found"}, 400

        # Define output file paths based on platform and search type
        # output_file = {
        #     ("Instagram", "User"): os.getenv('INSTAGRAM_USER_OUTPUT', './instagram/instagram_user_posts.json'),
        #     ("Instagram", "Hashtag"): os.getenv('INSTAGRAM_HASHTAG_OUTPUT', './instagram/instagram_hashtag_posts.json'),
        #     ("Twitter", "User"): os.getenv('TWITTER_USER_OUTPUT', './twitter/twitter_user_posts.json'),
        #     ("Twitter", "Hashtag"): os.getenv('TWITTER_HASHTAG_OUTPUT', './twitter/twitter_hashtag_posts.json')
        # }.get((platform, search_type))

        # if not output_file:
        #     return {"error": "Invalid search type or output file not found"}, 400

        # Execute the script
        process = subprocess.run(
            ["python3", script_path, (search_type), (degree), (depth), platform, (data)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        output_file = {
            ("Instagram", "User"): os.getenv('INSTAGRAM_USER_OUTPUT', './instagram/instagram_user_posts.json'),
            ("Instagram", "Hashtag"): os.getenv('INSTAGRAM_HASHTAG_OUTPUT', './instagram/instagram_hashtag_posts.json'),
            ("Twitter", "User"): os.getenv('TWITTER_USER_OUTPUT', './twitter/twitter_user_posts.json'),
            ("Twitter", "Hashtag"): os.getenv('TWITTER_HASHTAG_OUTPUT', './twitter/twitter_hashtag_posts.json')
        }.get((platform, search_type))

        if not output_file:
            return {"error": "Invalid search type or output file not found"}, 400
        
        

        # Load and return the JSON output from the script's output file
        with open(output_file, 'r') as json_file:
            output_data = json.load(json_file)

        return output_data

    except subprocess.CalledProcessError as e:
        logging.error(f"Script execution failed: {e.stderr}")
        return {"error": f"Script execution failed: {e.stderr}"}, 500
    except FileNotFoundError:
        logging.error("Output file not found.")
        return {"error": "Output file not found."}, 500
    except json.JSONDecodeError:
        logging.error("Failed to decode JSON from the output file.")
        return {"error": "Failed to decode JSON from the output file."}, 500
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return {"error": str(e)}, 500

# Search Endpoint
@app.route('/search', methods=['POST'])
def search():
    data = request.json
    search_type = data.get('searchType')
    degree_of_search = data.get('degreeOfSearch')
    depth_of_search = data.get('depthOfSearch')
    platform = data.get('platform')
    search_data = data.get('data')

    print("Search Type:", search_type)
    print("Degree of Search:", degree_of_search)
    print("Depth of Search:", depth_of_search)
    print("Platform:", platform)
    print("Data:", search_data)

    try:
        # Run the external script with the provided parameters
        print(request.scheme, request.host)
        result = run_your_script(search_type, degree_of_search, depth_of_search, platform, search_data)
        print(result)
        if not result:
            raise ValueError("No data returned from script execution.")

        # Send the result JSON to the /process-comments endpoint
        process_comments_url = f"{request.scheme}://{request.host}/process-comments"
        print(process_comments_url)
        process_comments_response = requests.post(process_comments_url, json=result)

        if process_comments_response.status_code != 200:
            raise Exception(f"Error in processing comments: {process_comments_response.text}")

        return jsonify({
            "message": "Data processed successfully",
            "processCommentsResponse": process_comments_response.json(),
        }), 200

    except Exception as error:
        logging.error("Error during the search process: %s", error)
        return jsonify({"error": "Error processing search and comments"}), 500

# Helper function to convert ObjectId to string
def convert_objectid(document):
    if "_id" in document:
        document["_id"] = str(document["_id"])
    return document

# Fetch All Documents from MongoDB
@app.route('/fetch-all', methods=['GET'])
def fetch_all():
    try:
        documents = mongo.db.gph_temp.find()
        result = [convert_objectid(doc) for doc in documents]
        return jsonify(result), 200
    except Exception as error:
        logging.error("Error fetching data: %s", error)
        return jsonify({"error": "Error fetching data"}), 500

# Process Comments Endpoint
@app.route('/process-comments', methods=['POST'])
def process_comments():
    data = request.json
    # print(data)
    try:
        for post in data['posts']:
            for comment in post['comments']:
                api_url = f"{os.getenv('ML_URL')}/process-comment?comment={requests.utils.quote(comment['comment'])}"
                print(api_url)
                response = requests.get(api_url)

                output = response.json().get('output')
                print(output)
                parsed_output = eval(output.replace("'", '"'))  # Be cautious with eval

                if parsed_output[0]['label'] == "LABEL_1":
                    query = {'username': comment['username'], 'comment': comment['comment']}
                    existing_document = mongo.db.gph_temp.find_one(query)

                    if not existing_document:
                        new_document = {
                            'username': comment['username'],
                            'comment': comment['comment'],
                            'profileLink': comment['profile_link'],
                        }
                        mongo.db.gph_temp.insert_one(new_document)
                        print("Element added")
                    else:
                        print("Element already exists")

        return jsonify({"message": "Processing complete"}), 200

    except Exception as error:
        logging.error("Error processing comments: %s", error)
        return jsonify({"error": "Error processing comments"}), 500

# CRUD Operations
@app.route('/create', methods=['POST'])
def create():
    collection_key = request.json.get('collectionKey')
    document = request.json.get('document')

    try:
        result = mongo.db[collection_key].insert_one(document)
        return jsonify(result.inserted_id), 200
    except Exception as error:
        return jsonify({"error": str(error)}), 500

@app.route('/read', methods=['GET'])
def read():
    collection_key = request.args.get('collectionKey')
    query = request.args.get('query')

    try:
        document = mongo.db[collection_key].find_one(eval(query))
        return jsonify(document), 200
    except Exception as error:
        return jsonify({"error": str(error)}), 500

@app.route('/update', methods=['PUT'])
def update():
    collection_key = request.json.get('collectionKey')
    query = request.json.get('query')
    update_data = request.json.get('update')

    try:
        result = mongo.db[collection_key].update_one(eval(query), {'$set': update_data})
        return jsonify(result.modified_count), 200
    except Exception as error:
        return jsonify({"error": str(error)}), 500

@app.route('/delete', methods=['DELETE'])
def delete():
    collection_key = request.json.get('collectionKey')
    query = request.json.get('query')

    try:
        result = mongo.db[collection_key].delete_one(eval(query))
        return jsonify(result.deleted_count), 200
    except Exception as error:
        return jsonify({"error": str(error)}), 500

if __name__ == "__main__":
    app.run(port=5000,host = "0.0.0.0", debug=True)
