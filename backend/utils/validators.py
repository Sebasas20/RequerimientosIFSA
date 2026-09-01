
from functools import wraps
from flask import request, jsonify
import re

def sanitize_input(data):
    if isinstance(data, str):
        # Basic sanitization removing obvious malicious tags
        data = re.sub(r'<script.*?>.*?</script>', '', data, flags=re.IGNORECASE)
        data = data.replace('<', '&lt;').replace('>', '&gt;')
        return data.strip()
    elif isinstance(data, dict):
        return {k: sanitize_input(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [sanitize_input(i) for i in data]
    return data

def validate_json(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 400
        return f(*args, **kwargs)
    return decorated_function
