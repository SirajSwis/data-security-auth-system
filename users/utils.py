import hashlib
import re

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def validate_first_last_name(name):
    pattern = r'^[A-Za-z]+$'
    return re.match(pattern, name) is not None

def validate_id_number(id_number):
    pattern = r'^\d{9}$'
    return re.match(pattern, id_number) is not None

def validate_credit_card_number(card_number):
    pattern = r'^\d{4}\s\d{4}\s\d{4}\s\d{4}$'
    return re.match(pattern, card_number) is not None

def validate_valid_date(valid_date):
    pattern = r'^(0[1-9]|1[0-2])\/\d{2}$'
    return re.match(pattern, valid_date) is not None

def validate_cvc(cvc):
    pattern = r'^\d{3}$'
    return re.match(pattern, cvc) is not None

def contains_forbidden_chars(input_text):
    pattern = r"[\'\";=]|--|\b(OR|AND|DROP|UNION|SELECT)\b"
    return re.search(pattern, input_text, re.IGNORECASE) is not None

def contains_forbidden_query(query):
    pattern = r"\b(DROP|DELETE|ALTER|INSERT|UPDATE|TRUNCATE)\b"
    return re.search(pattern, query, re.IGNORECASE) is not None
