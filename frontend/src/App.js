import React from 'react';
import Forum from './Forum';
import BookList from './BookList';

function App() {
    return (
        <div className="app">
            <h1>Book Forum</h1>
            <div className="container">
                <Forum />
                <BookList />
            </div>
        </div>
    );
}

export default App;