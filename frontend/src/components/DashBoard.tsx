import React, { useEffect, useState } from 'react';

interface RoomData {
    numberOfListeners: number;
    totalPlayTime: number;
    mostPlayedSong: string;
    topArtist: string;
}

const DashBoard = () => {
    const [data, setData] = useState<Record<string, RoomData> | null>(null);

    useEffect(() => {
        fetch('/dashboard')
            .then(response => response.json())
            .then(data => {
                console.log(data);
                setData(data);
            })
            .catch(error => console.error('Error:', error));
    }, []);

    if (!data) {
        return <div>Loading...</div>;
    }

    return (
        <div>
            {Object.keys(data).map(room => (
                <div key={room}>
                    <h2>{room}</h2>
                    <p>Anzahl der Hörer: {data[room].numberOfListeners}</p>
                    <p>Gesamtspielzeit: {data[room].totalPlayTime}</p>
                    <p>Am häufigsten gespieltes Lied: {data[room].mostPlayedSong}</p>
                    <p>Top-Künstler: {data[room].topArtist}</p>
                </div>
            ))}
        </div>
    );
};

export default DashBoard;