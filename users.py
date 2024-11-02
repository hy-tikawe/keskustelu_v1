from werkzeug.security import check_password_hash, generate_password_hash
import db

def create_user(username, password):
    password_hash = generate_password_hash(password)
    try:
        db.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", [username, password_hash])
        return True
    except:
        return False

def check_login(username, password):
    result = db.query("SELECT id, password_hash FROM users WHERE username = ?", [username])

    if len(result) == 1:
        user_id, password_hash = result[0]
        if check_password_hash(password_hash, password):
            return user_id

    return None
