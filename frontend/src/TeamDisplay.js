import React from "react";
import shirtIcon from "./assets/shirt.PNG";
import pitchBg from "./assets/pitch.jpg";

function PlayerIcon({ player, style, textColor = "white" }) {
  return (
    <div
      className={`absolute text-center transition transform hover:scale-105`}
      style={{ ...style, color: textColor }}
    >
      <img
        src={shirtIcon}
        alt="shirt"
        className="w-12 sm:w-14 mx-auto drop-shadow-md"
      />
      <div className="text-xs sm:text-sm font-semibold mt-1 leading-tight tracking-wide drop-shadow-sm">
        ({player.position} - <span className="font-bold">£{player.price}</span>)
      </div>
    </div>
  );
}

function TeamDisplay({ starting = {}, bench = {} }) {
  const rowY = {
    GK: "0%",
    DEF: "18%",
    MID: "38%",
    FWD: "57%",
    BENCH: "82%",
  };

  const getXPos = (index, total) => {
    const offset = 6.5;
    const basePos = (100 / (total + 1)) * (index + 1);
    return `${basePos - offset}%`;
  };

  const parsePlayers = (data, prefix) => {
    const players = [];
    Object.entries(data).forEach(([key, count]) => {
      const [position, range] = key.split(" ");
      for (let i = 0; i < count; i++) {
        players.push({
          id: `${prefix}-${key}-${i}`,
          position,
          price: range,
        });
      }
    });
    return players;
  };

  const startingPlayers = parsePlayers(starting, "starting");
  const benchPlayers = parsePlayers(bench, "bench");

  const gk = startingPlayers.filter((p) => p.position === "GK");
  const def = startingPlayers.filter((p) => p.position === "DEF");
  const mid = startingPlayers.filter((p) => p.position === "MID");
  const fwd = startingPlayers.filter((p) => p.position === "FWD");

  return (
    <div className="mt-10">
      <div
        className="relative w-full h-[80vh] bg-center bg-contain bg-no-repeat rounded-xl shadow-lg ring-2 ring-purple-300"
        style={{ backgroundImage: `url(${pitchBg})` }}
      >
        {gk.map((p, i) => (
          <PlayerIcon
            key={p.id}
            player={p}
            style={{ top: rowY.GK, left: getXPos(i, gk.length) }}
          />
        ))}
        {def.map((p, i) => (
          <PlayerIcon
            key={p.id}
            player={p}
            style={{ top: rowY.DEF, left: getXPos(i, def.length) }}
          />
        ))}
        {mid.map((p, i) => (
          <PlayerIcon
            key={p.id}
            player={p}
            style={{ top: rowY.MID, left: getXPos(i, mid.length) }}
          />
        ))}
        {fwd.map((p, i) => (
          <PlayerIcon
            key={p.id}
            player={p}
            style={{ top: rowY.FWD, left: getXPos(i, fwd.length) }}
          />
        ))}
        {benchPlayers.map((p, i) => (
          <PlayerIcon
            key={p.id}
            player={p}
            style={{ top: rowY.BENCH, left: getXPos(i, benchPlayers.length) }}
            textColor="black"
          />
        ))}
      </div>
    </div>
  );
}

export default TeamDisplay;
