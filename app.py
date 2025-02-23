from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
from bs4 import BeautifulSoup
import requests
import os
from threading import Thread
import time

app = Flask(__name__, static_folder='build/static', template_folder='build')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///forum.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')

db = SQLAlchemy(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Models
class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    comments = db.relationship('Comment', backref='thread', lazy=True)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'), nullable=False)

# Initialize database
with app.app_context():
    db.create_all()

# Serve React frontend
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react(path):
    if path and os.path.exists(os.path.join(app.template_folder, path)):
        return send_from_directory(app.template_folder, path)
    return send_from_directory(app.template_folder, 'index.html')

# Fetch book prices from AbeBooks
def fetch_book_prices():
    books = [
        {"title": "Python Crash Course", "isbn": "1593279280"},
        {"title": "Flask Web Development", "isbn": "1449372627"}
    ]
    while True:
        book_data = []
        for book in books:
            try:
                url = f"https://www.abebooks.com/servlet/SearchResults?kn={book['isbn']}"
                headers = {"User-Agent": "Mozilla/5.0"}
                response = requests.get(url, headers=headers, timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')
                price_elem = soup.select_one(".srp-item-price")
                price = float(price_elem.text.replace('$', '').strip()) if price_elem else 0.0
                book_data.append({"title": book["title"], "price": price})
            except Exception as e:
                book_data.append({"title": book["title"], "price": 0.0})
                print(f"Error fetching {book['title']}: {e}")
        socketio.emit('book_prices', book_data)
        time.sleep(60)

# Start background task
Thread(target=fetch_book_prices, daemon=True).start()

# API Routes
@app.route('/threads', methods=['GET'])
def get_threads():
    threads = Thread.query.all()
    return jsonify([{"id": t.id, "title": t.title, "content": t.content} for t in threads])

@app.route('/threads', methods=['POST'])
def create_thread():
    data = request.json
    thread = Thread(title=data['title'], content=data['content'])
    db.session.add(thread)
    db.session.commit()
    socketio.emit('new_thread', {"id": thread.id, "title": thread.title, "content": thread.content})
    return jsonify({"message": "Thread created"}), 201

@app.route('/threads/<int:thread_id>/comments', methods=['POST'])
def add_comment(thread_id):
    data = request.json
    comment = Comment(content=data['content'], thread_id=thread_id)
    db.session.add(comment)
    db.session.commit()
    socketio.emit('new_comment', {"thread_id": thread_id, "content": comment.content})
    return jsonify({"message": "Comment added"}), 201

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=False)