from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
from firebase_admin import auth, credentials, initialize_app
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


from os import getenv, path
from dotenv import load_dotenv

app_base = path.dirname(__file__)
app_root = path.join(app_base, '../')

load_dotenv(dotenv_path=path.join(app_root, '.env.local'))

servicekey = {
  "type": "service_account",
  "project_id": "dues-35631",
  "private_key_id": "59e0caa20c751320be2467a7cf577a37d6638604",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCuMFv67bfksDzn\nIyITgnuCQsa+oT7Jw4XQeCDidN3ayyu4H5vpRRpwn8Gx/dlGCvE5y6KOLqpbuWBW\naojiYJS/77oZO9ISyezo0GaRQpNmizq/3Zlfi0rU9sH0TtDayDMBExgFOJk3ozQM\nMyrd04ryGjZvhvT8OEcjdZRiyTZgbWrD1W3QtlBtsesUMZmD7JtEtIKE6kPzSZpt\ngZMRANc5BtONP/uFJuspdg+NcxoRTy5hegzdwFN9wLwpUIxnjouK3ZU3Ffm+JlVb\n88pN8UMs7l/wO7gct6UnkDZGL5SHO+Hn10Qvahd3yVSFwP+CetcGdxhEJ/FY5Bp0\n/6ZpAOdbAgMBAAECggEAKoq5DDHexcWdOj5EZktp6shwTcKH2TMdjWqpbWVpgbQ5\nO0DNDU3JRVRfNB9xXz/w5lKrotoW1UwTEUf3ooJAEhh0dRE9H0WdzMaJJlUCNvsu\nIAn5GXKllhmmCQruy2A1xL9rEGtgUExVu90LTR4LQ1HPlbF6R9de2HQxB2dpFmd7\njIOt4BIXfWk4zILdaPK57XAWpOd/xqKvPY91vnJVwBF3212YGXeShhOYYwDAinpI\nJLUiXHDAqNo6PnjIoHSm0J1WO9650jZq1HIsXAX7fXmLX5iicALeWL8a5F7MRYWM\ncUH7Q8/0avluTXWxkciRVB2IZlVT5lFNqhcMpaNC4QKBgQDYMHcmZmf7E0ittHf1\nBAJXVPhzLnkYOy7KazUi91y4ZITVNMwdVJupgzRP9cMB5YY3PF2xz2baEJkQHax+\n3FqKl5m5T35wW80w8Bu3SkJX1nrLUdlKgOrNMG45UHrH5NuqECjRU3VxrbFOVeiR\nMsun8l2OW/Gig9CYjhsqRruLIwKBgQDOQ+wjuHw2E6yaZjlfN3XIdcvL9H4VQuzh\nNvCMJ7btHULRhFlTkZGfSLCktom/gzohCI6ZiRHV6Pdidj2Lt3Q/Tn4QSB3LlZbU\nmO5bZmy+b2rl8ikzed87ImOqT6lWXpidElc1gm8HsJoRJQBmQjcVSQawhMw7Y6jT\n5ZoBSfgyaQKBgQCVIRmQC6Q+tha0fIEjKxjSVXLtQWmXJXwpdbq53BjBudVHnZwP\nv4WBcVhssANNE596CtI3DfLNChYL3+xVtntejyUjh4qYxzrMP1VfIoKRRQp/pn5V\nvog58uaV8sY/jcdZkLwXaZLiUAa3GtvLDVcfCzkuMo6EpJkIIz7p8tD8MQKBgHi7\n50gNX59jqr+BoIlsdCQPV2gdx4N4diFpwCm5wWhPnWH4PzUcWwnKSaNQOZcBIBBf\n6uBSDD+SquNWZLYYfxHjRwUOwWn+OJhen/6eGH7rxr2sHpPD/XemrIHvOSaWHmyq\nZKOsooL0y2nHp9EzZvytjx3ZzZXhwtutZJTmkEIpAoGBAKl+xla6tbNLE/IeBM2s\n46cKmwUXzkP5q65yAQY+s7W1avN6btQoSN3LmO1F5p3MjDgkbd6bXS865xRg4RKJ\n21b5LrPj7i3a/1SdpOQ/0++hmWJt32e7FGySRQKDIX6mJ9xR/Y+PsdrOaTJWzxKN\n6tzRbVc7QaxoKzp7LL6svX2y\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-xdk5m@dues-35631.iam.gserviceaccount.com",
  "client_id": "109933848517873833998",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-xdk5m%40dues-35631.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
} 

cred = credentials.Certificate(servicekey)
firebase_admin.initialize_app(cred)

app = FastAPI()

# Define your domain
allowed_domains = ["localhost:3000", "127.0.0.1:8000", "next-starter-swart.vercel.app"]  # Replace with your actual domain
security = HTTPBearer()

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_domains,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        decoded_token = auth.verify_id_token(credentials.credentials)
        return decoded_token
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/backend/python")
def hello_world(request: Request, current_user: dict = Depends(get_current_user)):
    mystr = f"Hello, {current_user['name']}. This is a random sentence"
    return {"message":mystr}