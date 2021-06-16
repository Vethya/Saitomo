"""Database utils for Notes Cog"""

from bot import db

db.execute("""CREATE TABLE IF NOT EXISTS notes
                (key TEXT NOT NULL,
                guild INT NOT NULL,
                value TEXT NOT NULL);""")
db.commit()

def add_note(key: str, guild: int, value: str):
    """Add a note"""
    db.execute("INSERT INTO notes (key, guild, value) VALUES (?,?,?);", (key, guild, value))
    db.commit()

def rm_note(key: str, guild: int):
    """Remove a note"""
    db.execute("DELETE FROM notes WHERE key = ? AND guild = ?;", (key, guild))
    db.commit()

def rm_all(guild: int):
    """Remove all notes"""
    db.execute("DELETE FROM notes WHERE guild = ?;", (guild,))
    db.commit()

def update_note(key: str, guild: int, value: str):
    """Update a note"""
    db.execute("UPDATE notes SET value = ? where key = ? AND guild = ?;", (value, key, guild))
    db.commit()

def get_note(key: str, guild: int):
    """Get a note"""
    return (db.execute("SELECT key, guild, value FROM notes WHERE key = ? AND guild = ?;", (key, guild))).fetchone()

def note_list(guild: int):
    """Get all notes"""
    return (db.execute("SELECT * FROM notes WHERE guild = ?;", (guild,))).fetchall()

