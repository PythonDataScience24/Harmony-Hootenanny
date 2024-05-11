// WebSocketTest.js

import React, { useState, useEffect } from "react";
import socket from "./socket"; // Import the socket object

function WebSocketTest() {
    const [messages, setMessages] = useState([]);
    const [data, setData] = useState();

    useEffect(() => {
        // Connect when the component mounts
        socket.connect();

        // Emit "user_join" event
        socket.emit("user_join", "Manuel");

        // Listen for "chat" events
        socket.on("chat", (data) => {
            setData(data);
        });

        // Clean up: disconnect when the component unmounts
        return () => {
            socket.disconnect();
        };
    }, []); // Empty dependency array ensures this effect runs only once
    useEffect(() => { console.log(messages) }, [messages])

    useEffect(() => {
        console.log("data updated received")
        if (data) {
            setMessages((messages) => [...messages, data]);
        }
    }, [data])
    return (
        <>
            <h1>Hello WebSockets!</h1>
            {messages.map((message) => {
                return <div>
                    {JSON.stringify(message)}
                </div>
            })}
        </>
    );
}

export default WebSocketTest;

