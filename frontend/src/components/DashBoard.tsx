import React, { useEffect, useState } from "react";

interface RoomData {
  number_of_listeners: number;
  total_play_time: number;
  most_played_song: string;
  top_artist: string;
}

const DashBoard = () => {
  const [data, setData] = useState<Record<string, RoomData> | null>(null);

  useEffect(() => {
    fetch("http://localhost:5000/api/dashboard", {
      headers: {
        Accept: "application/json",
      },
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const contentType = response.headers.get("content-type");
        if (!contentType || !contentType.includes("application/json")) {
          throw new TypeError("Oops, we haven't got JSON!");
        }
        return response.json();
      })
      .then((data) => {
        console.log("Data from server:", data);
        setData(data);
      })
      .catch((error) => console.error("Error:", error.message));
  }, []);

  if (!data) {
    return <div>Loading...</div>;
  }

  return (
    <>
      {Object.keys(data).map((room, index) => (
        <div key={room}>
          <h2>{room}</h2>
          <p>Anzahl der Hörer: {JSON.stringify(data[room])}</p>
          <p>Gesamtspielzeit: 1</p>
          <p>Am häufigsten gespieltes Lied: 1</p>
          <p>Top-Künstler: 1</p>
          <img
            src={`http://localhost:5000/dashboard/charts/${index + 1}`}
            alt={`${index + 1} chart`}
          />
        </div>
      ))}
      {/* {Object.keys(data).map((room) => (
        <div>
          <h2>{room}</h2>
          <img
            src={`http://localhost:5000/dashboard/charts/${room}`}
            alt={`${room} chart`}
          />
        </div>
      ))} */}
    </>
  );
};

export default DashBoard;
