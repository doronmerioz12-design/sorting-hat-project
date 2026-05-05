import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

# Database connection settings
# Default local MongoDB connection string
MONGODB_URL = "mongodb://localhost:27017"

# Initialize the Asynchronous MongoDB client
# Using Motor for non-blocking database operations to ensure high performance
client = AsyncIOMotorClient(MONGODB_URL)

# Access the specific database for the project
db = client.sorting_hat_db

# Access the collection where character data and sorting history are stored
# This collection is used by HistoryManager to cache results
collection = db.characters