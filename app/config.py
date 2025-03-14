import os

class Config:
    UPLOAD_FOLDER = os.path.abspath(os.path.dirname(__file__)) + '/uploads'
    REQUEST_MAX_SIZE = 5 * 1024 * 1024 * 1024
    REQUEST_TIMEOUT	= 60*30
    RESPONSE_TIMEOUT = 60*30
    KEEP_ALIVE_TIMEOUT = 60*30
