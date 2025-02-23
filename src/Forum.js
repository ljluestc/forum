import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';

const socket = io('/'); // Connect to root since Flask serves both

function Forum() {
    const [threads, setThreads] = useState([]);
    const [title, setTitle] = useState('');
    const [content, setContent] = useState('');

    useEffect(() => {
        fetchThreads();
        socket.on('new_thread', (thread) => setThreads((prev) => [...prev, thread]));
        socket.on('new_comment', (comment) => console.log('New comment:', comment));
        return () => {
            socket.off('new_thread');
            socket.off('new_comment');
        };
    }, []);

    const fetchThreads = async () => {
        const response = await fetch('/threads');
        const data = await response.json();
        setThreads(data);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        await fetch('/threads', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title, content })
        });
        setTitle('');
        setContent('');
    };

    return (
        <div className="forum">
            <h2>Threads</h2>
            <form onSubmit={handleSubmit}>
                <input 
                    type="text" 
                    value={title} 
                    onChange={(e) => setTitle(e.target.value)} 
                    placeholder="Thread Title" 
                    required 
                />
                <textarea 
                    value={content} 
                    onChange={(e) => setContent(e.target.value)} 
                    placeholder="Content" 
                    required 
                />
                <button type="submit">Post Thread</button>
            </form>
            <ul>
                {threads.map(thread => (
                    <li key={thread.id}>
                        <h3>{thread.title}</h3>
                        <p>{thread.content}</p>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default Forum;