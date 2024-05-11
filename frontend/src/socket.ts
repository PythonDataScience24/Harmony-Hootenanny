import { io } from "socket.io-client";

const URL = process.env.NODE_ENV === "production" ? undefined : "http://localhost:5000";
// @ts-ignore
const socket = io(URL, {
    autoConnect: false,
    cors: {
        origin: "http://localhost:5000",
        methods: ["GET", "POST"],
    },
});

export default socket;