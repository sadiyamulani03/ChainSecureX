from auth.token_manager import (
    generate_session_token
)


active_sessions = {}


def create_session(username):
    token = generate_session_token()

    active_sessions[token] = username

    return token


def validate_session(token):
    return token in active_sessions


def get_session_user(token):
    return active_sessions.get(token)


def remove_session(token):
    if token in active_sessions:
        del active_sessions[token]