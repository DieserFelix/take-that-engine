import os, sys, json
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv(os.path.join(BASE_DIR, ".env"))
sys.path.append(BASE_DIR)

CORS_ORIGINS = json.loads(os.environ["CORS_ORIGINS"])
SECRET_KEY = os.environ["SECRET_KEY"]