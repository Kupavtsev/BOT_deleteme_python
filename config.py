import os
import dotenv


dotenv.load_dotenv()
TOKEN = os.getenv("API_TOKEN")
EMAIL_PASSWORD = os.getenv("email_password")