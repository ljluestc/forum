import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';

const socket = io(process.env.REACT_APP_API_URL || 'http://localhost:5000');

function BookList() {
    const [books, setBooks] = useState([]);

    useEffect(() => {
        socket.on('book_prices', (data) => setBooks(data));
        return () => socket.off('book_prices');
    }, []);

    return (
        <div className="book-list">
            <h2>Real-Time Book Prices (AbeBooks)</h2>
            <ul>
                {books.map((book, index) => (
                    <li key={index}>
                        {book.title}: ${book.price.toFixed(2)}
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default BookList;