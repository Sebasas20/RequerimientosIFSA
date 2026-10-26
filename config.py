import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

class Config:
    _db_url = os.environ.get('DATABASE_URL', '').strip('"\'')
    if _db_url.startswith('postgres://'):
        _db_url = _db_url.replace('postgres://', 'postgresql://', 1)
    SQLALCHEMY_DATABASE_URI = _db_url.replace('postgresql://', 'postgresql+psycopg2://', 1) if _db_url.startswith('postgresql://') else _db_url
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    SECRET_KEY = os.environ['SECRET_KEY']

    JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM', 'HS256')
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES', 480))

    CACHE_TYPE = os.environ.get('CACHE_TYPE', 'RedisCache')
    CACHE_REDIS_HOST = os.environ.get('CACHE_REDIS_HOST', 'localhost')
    CACHE_REDIS_PORT = int(os.environ.get('CACHE_REDIS_PORT', 6379))
    CACHE_REDIS_DB = int(os.environ.get('CACHE_REDIS_DB', 0))
    CACHE_REDIS_URL = os.environ.get('CACHE_REDIS_URL', 'redis://localhost:6379/0')
    CACHE_DEFAULT_TIMEOUT = int(os.environ.get('CACHE_DEFAULT_TIMEOUT', 300))  
    
    CACHE_TIMEOUT_DAILY = 300     
    CACHE_TIMEOUT_HISTORICAL = 3600  
    CACHE_TIMEOUT_STATIC = 86400

    N8N_WEBHOOK_INFO_REQUERIDA_URL = os.environ.get(
        'N8N_WEBHOOK_INFO_REQUERIDA_URL',
        'https://n8n.gif-amp.com/webhook/ticket-informacion-requerida'
    ).strip('"\'')
    N8N_WEBHOOK_SECRET = os.environ.get('N8N_WEBHOOK_SECRET', '').strip('"\'')
