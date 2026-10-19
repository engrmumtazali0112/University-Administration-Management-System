"""
Run:  python set_database_url.py
You can paste EITHER the full Neon connection string OR just the password (starts with npg_).
Saves DATABASE_URL to .env and tests the connection.
"""
import re
from pathlib import Path
from urllib.parse import quote, urlsplit, urlunsplit

# Your current Neon project (UAMS / production)
HOST = "ep-snowy-leaf-b4eeysg0-pooler.c-6.us-east-2.aws.neon.tech"
USER = "neondb_owner"
DB = "neondb"

env_path = Path(__file__).resolve().parent / ".env"

raw = input("Paste the Neon connection string OR just the password, then press Enter: ").strip().strip("'\"")
if raw.lower().startswith("psql "):
    raw = raw[5:].strip().strip("'\"")
if not raw:
    raise SystemExit("Nothing was pasted. Right-click in the terminal to paste, then press Enter.")

if raw.startswith(("postgres://", "postgresql://")):
    parts = urlsplit(raw)
    if not parts.password or "*" in parts.password:
        raise SystemExit("Password is hidden (****). In Neon click 'Show password', then copy again.")
    url = urlunsplit((parts.scheme, parts.netloc, parts.path, "sslmode=require", ""))
else:
    url = f"postgresql://{USER}:{quote(raw, safe='')}@{HOST}/{DB}?sslmode=require"

text = env_path.read_text(encoding="utf-8") if env_path.exists() else ""
line = f"DATABASE_URL={url}"
if re.search(r"^DATABASE_URL=.*$", text, flags=re.M):
    text = re.sub(r"^DATABASE_URL=.*$", lambda m: line, text, flags=re.M)
else:
    text = text.rstrip("\n") + "\n" + line + "\n"
env_path.write_text(text, encoding="utf-8")
print("Saved DATABASE_URL to .env | host:", urlsplit(url).hostname)

import psycopg2

try:
    conn = psycopg2.connect(url)
    cur = conn.cursor()
    cur.execute("select current_user, current_database()")
    print("CONNECTED OK ->", cur.fetchone())
    print("Next: python manage.py migrate")
except Exception as e:
    print("FAILED:", str(e).strip())