from flask import Flask
from flask_pymongo import PyMongo

# Initialize Flask App
app = Flask(__name__)

# MongoDB Configuration
mongo_conn = "mongodb+srv://abivis2k:7aNqw7B9gsAfxznS@job-cluster.ayr8p.mongodb.net/db"
mongo_params = "?tlsAllowInvalidCertificates=true&retryWrites=true&w=majority"
app.config["MONGO_URI"] = mongo_conn + mongo_params
mongodb_client = PyMongo(app)
db = mongodb_client.db

def update_existing_users():
    """
    Update existing user documents to include 'otp' and 'is_verified' fields.
    """
    # Add 'is_verified' field with default value False if it doesn't exist
    db.users.update_many(
        {'is_verified': {'$exists': False}},
        {'$set': {'is_verified': False}}
    )
    print("Added 'is_verified' field to existing users.")

    # Add 'otp' field with a default empty string if it doesn't exist
    db.users.update_many(
        {'otp': {'$exists': False}},
        {'$set': {'otp': ""}}
    )
    print("Added 'otp' field to existing users.")

if __name__ == "__main__":
    with app.app_context():
        update_existing_users()
