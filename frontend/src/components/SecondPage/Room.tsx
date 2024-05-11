import React from 'react';

interface RoomProps {
  name: string;
}

const Room: React.FC<RoomProps> = ({ name }) => {
  return (
    <div>
      <h2>{name}</h2>
      <p>Willkommen im {name}.</p>
    </div>
  );
}

export default Room;
