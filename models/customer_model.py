def validate_customer(data):
    required = ["name","email","phone"]

    for field in required:
        if field not in data or not data[field]:
            return f"Missing data : {field}"
    return None