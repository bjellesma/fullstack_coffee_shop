import os 
from dotenv import load_dotenv
load_dotenv()

DATABASE_NAME=os.environ["DATABASE_NAME"]
AUTH0_DOMAIN=os.environ["AUTH0_DOMAIN"]
ALGORITHM=os.environ["ALGORITHM"]
API_AUDIENCE=os.environ["API_AUDIENCE"]