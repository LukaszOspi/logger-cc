# model.py
import sqlite3
import datetime

def setup_database():
    conn = sqlite3.connect('decision_log.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS decisions (
            id INTEGER PRIMARY KEY,
            timestamp TEXT,
            area TEXT,
            decision_maker TEXT,
            decision TEXT,
            reasoning TEXT,
            status TEXT,
            due_date TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_decision(area, decision_maker, decision, reasoning, status, due_date):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect('decision_log.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO decisions (timestamp, area, decision_maker, decision, reasoning, status, due_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (timestamp, area, decision_maker, decision, reasoning, status, due_date))
    conn.commit()
    conn.close()

def update_decision(id, area, decision_maker, decision, reasoning, status, due_date):
    conn = sqlite3.connect('decision_log.db')
    c = conn.cursor()
    c.execute('''
        UPDATE decisions
        SET area = ?, decision_maker = ?, decision = ?, reasoning = ?, status = ?, due_date = ?
        WHERE id = ?
    ''', (area, decision_maker, decision, reasoning, status, due_date, id))
    conn.commit()
    conn.close()

def delete_decision(id):
    conn = sqlite3.connect('decision_log.db')
    c = conn.cursor()
    c.execute('DELETE FROM decisions WHERE id = ?', (id,))
    conn.commit()
    conn.close()

def retrieve_decisions(status_filter=None, start_date=None, end_date=None):
    conn = sqlite3.connect('decision_log.db')
    c = conn.cursor()
    query = 'SELECT * FROM decisions'
    filters = []
    if status_filter or start_date or end_date:
        query += ' WHERE'
        if status_filter:
            query += ' status = ?'
            filters.append(status_filter)
        if start_date:
            if filters:
                query += ' AND'
            query += ' timestamp >= ?'
            filters.append(start_date)
        if end_date:
            if filters:
                query += ' AND'
            query += ' timestamp <= ?'
            filters.append(end_date)
    c.execute(query, tuple(filters))
    decisions = c.fetchall()
    conn.close()
    return decisions
