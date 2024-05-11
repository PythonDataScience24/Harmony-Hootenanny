// src/App.tsx
import React from 'react';
import useWebSocket from 'react-use-websocket';
import { io } from 'socket.io-client';


const WS_URL = 'ws://127.0.0.1:5000'; // Use the same URL as your Flask app

function WebSocketTest() {

    const URL = process.env.NODE_ENV === 'production' ? undefined : 'http://localhost:5000';
    //@ts-ignore
    const socket = io(URL, {
        autoConnect: false
    });
    socket.connect()
    return (
        <>
            <script src="https://cdn.socket.io/4.6.0/socket.io.min.js" integrity="sha384-c79GN5VsunZvi+Q/WObgk2in0CbZsHnjEqvFxC5DxHn9lTfNce2WW6h2pH6u/kF+" crossOrigin="anonymous"></script>
            <div className="App">
                <h1>Hello WebSockets!</h1>
            </div>
        </>
    );
}

export default WebSocketTest;
