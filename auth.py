import hashlib
import hmac
import json
import os
import secrets
import sqlite3

from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api")

DB_PATH = os.environ.get("DB_PATH", "blueprint.db")


def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with db() as c:
        c.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                salt TEXT NOT NULL,
                pw_hash TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS sessions (
                token TEXT PRIMARY KEY,
                user_id TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS states (
                user_id TEXT PRIMARY KEY,
                data TEXT NOT NULL
            );
            """
        )


init_db()


def hash_password(password: str, salt: str) -> str:
    return hashlib.pbkdf2_hmac(
        "sha256", password.encode(), bytes.fromhex(salt), 200_000
    ).hex()


class Credentials(BaseModel):
    email: str
    password: str


class StateBody(BaseModel):
    state: dict


def new_session(user_id: str) -> str:
    token = secrets.token_urlsafe(32)
    with db() as c:
        c.execute("INSERT INTO sessions (token, user_id) VALUES (?, ?)", (token, user_id))
    return token


def current_user(authorization: str | None) -> sqlite3.Row:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not signed in.")
    token = authorization[len("Bearer "):]
    with db() as c:
        row = c.execute(
            """
            SELECT users.id, users.email FROM sessions
            JOIN users ON users.id = sessions.user_id
            WHERE sessions.token = ?
            """,
            (token,),
        ).fetchone()
    if row is None:
        raise HTTPException(status_code=401, detail="Session expired. Please sign in again.")
    return row


@router.post("/auth/signup")
def signup(body: Credentials):
    email = body.email.strip().lower()
    if "@" not in email:
        raise HTTPException(status_code=400, detail="Enter a valid email address.")
    if len(body.password) < 8:
        raise HTTPException(status_code=400, detail="Use at least 8 characters.")

    user_id = secrets.token_hex(8)
    salt = secrets.token_hex(16)
    pw_hash = hash_password(body.password, salt)

    try:
        with db() as c:
            c.execute(
                "INSERT INTO users (id, email, salt, pw_hash) VALUES (?, ?, ?, ?)",
                (user_id, email, salt, pw_hash),
            )
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="An account with this email already exists.")

    token = new_session(user_id)
    return {"token": token, "user": {"id": user_id, "email": email}}


@router.post("/auth/login")
def login(body: Credentials):
    email = body.email.strip().lower()
    with db() as c:
        row = c.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()

    if row is None or not hmac.compare_digest(
        hash_password(body.password, row["salt"]), row["pw_hash"]
    ):
        raise HTTPException(status_code=400, detail="Incorrect email or password.")

    token = new_session(row["id"])
    return {"token": token, "user": {"id": row["id"], "email": row["email"]}}


@router.post("/auth/logout")
def logout(authorization: str | None = Header(default=None)):
    if authorization and authorization.startswith("Bearer "):
        token = authorization[len("Bearer "):]
        with db() as c:
            c.execute("DELETE FROM sessions WHERE token = ?", (token,))
    return {"ok": True}


@router.get("/auth/me")
def me(authorization: str | None = Header(default=None)):
    user = current_user(authorization)
    return {"user": {"id": user["id"], "email": user["email"]}}


@router.get("/state")
def get_state(authorization: str | None = Header(default=None)):
    user = current_user(authorization)
    with db() as c:
        row = c.execute("SELECT data FROM states WHERE user_id = ?", (user["id"],)).fetchone()
    return {"state": json.loads(row["data"]) if row else None}


@router.put("/state")
def put_state(body: StateBody, authorization: str | None = Header(default=None)):
    user = current_user(authorization)
    with db() as c:
        c.execute(
            """
            INSERT INTO states (user_id, data) VALUES (?, ?)
            ON CONFLICT(user_id) DO UPDATE SET data = excluded.data
            """,
            (user["id"], json.dumps(body.state)),
        )
    return {"ok": True}