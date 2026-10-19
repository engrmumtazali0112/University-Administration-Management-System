"""Run: python check_db.py  -> tells you exactly what is wrong with DATABASE_URL (never prints the password)."""
import os
from pathlib import Path
from urllib.parse import urlsplit, unquote

from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent / ".env"
print(".env found:", env_path.exists(), "->", env_path)
load_dotenv(env_path, override=True)

url = os.environ.get("DATABASE_URL", "")
if not url:
    raise SystemExit("DATABASE_URL is NOT set. Add it to .env")

u = urlsplit(url)
pw = unquote(u.password or "")
print("scheme:", u.scheme, "| user:", u.username, "| host:", u.hostname, "| db:", u.path.lstrip("/"))
print("password length:", len(pw))
if "PASTE" in pw.upper() or "PASSWORD" in pw.upper() or "NEW" in pw.upper() and len(pw) < 16:
    raise SystemExit("Password is still a PLACEHOLDER. Paste the real Neon password.")

import psycopg2
try:
    c = psycopg2.connect(url)
    cur = c.cursor()
    cur.execute("select version()")
    print("CONNECTED OK:", cur.fetchone()[0][:40])
except Exception as e:
    print("FAILED:", str(e).strip())