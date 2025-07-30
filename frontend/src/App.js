import React from "react";
import Slider from "rc-slider";
import "rc-slider/assets/index.css";
import useFPL from "./useFPL"; // adjust path if needed
import TeamDisplay from "./TeamDisplay";
import fplLogo from "./assets/fpl_logo.png";



function App() {
  const {
    searchTerm, setSearchTerm,
    positionFilter, setPositionFilter,
    teamFilter, setTeamFilter,
    priceRange, setPriceRange,
    selectedPlayers, addPlayer, removePlayer,
    handleResolveAndOptimize,
    filteredPlayers, result, resultRef,
    teamMap, positionMap, uniqueTeams,
  } = useFPL();

  
  return (
    <div className="p-6 sm:p-8 max-w-4xl mx-auto bg-gray-50 rounded-2xl shadow-xl font-sans">
      <div className="flex items-center justify-center gap-4 mb-6">
        <img src={fplLogo} alt="FPL Logo" className="w-20 h-20 object-contain"  />
        <h1 className="text-4xl font-bold text-purple-900">
          FPL Optimizer
        </h1>
      </div>
      <h2 className="text-2xl font-semibold text-purple-800 mb-4">Select Players</h2>

      <div className="flex flex-wrap gap-4 mb-6">
        <input
          type="text"
          placeholder="Search player name"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="flex-1 min-w-[200px] p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
        />

        <select
          value={positionFilter}
          onChange={(e) => setPositionFilter(e.target.value)}
          className="p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
        >
          <option value="">All Positions</option>
          <option value="1">GK</option>
          <option value="2">DEF</option>
          <option value="3">MID</option>
          <option value="4">FWD</option>
        </select>

        <select
          value={teamFilter}
          onChange={(e) => setTeamFilter(e.target.value)}
          className="p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
        >
          <option value="">All Teams</option>
          {uniqueTeams.map((teamId) => (
            <option key={teamId} value={teamId}>
              {teamMap[teamId] || `Team ${teamId}`}

            </option>
          ))}
        </select>
      </div>

      <div className="mb-6">
        <label className="block font-semibold text-purple-900 mb-2">
          Price Range: £{priceRange[0]}M - £{priceRange[1]}M
        </label>
        <Slider
          range
          min={3.5}
          max={14.5}
          step={0.1}
          defaultValue={priceRange}
          onChange={(value) => setPriceRange(value)}
          trackStyle={[{ backgroundColor: "#00ff87" }]}
          handleStyle={[
            { borderColor: "#37003c", backgroundColor: "#37003c" },
            { borderColor: "#37003c", backgroundColor: "#37003c" },
          ]}
        />
      </div>

      <ul className="max-h-60 overflow-y-auto border border-gray-300 bg-white p-4 rounded-lg shadow-sm mb-6">
        {filteredPlayers.length === 0 && (
          <li className="text-gray-500 italic">No players found</li>
        )}
        {filteredPlayers.map((p) => (
          <li
            key={p.id}
            className="cursor-pointer py-1 border-b border-gray-200 hover:bg-purple-50 px-2 rounded transition-all"
            onClick={() => addPlayer(p.web_name)}
          >
            <span className="font-semibold text-purple-800">{p.web_name}</span>{" "}
            ({positionMap[p.element_type]} - {teamMap[p.team]} - £
            {(p.now_cost / 10).toFixed(1)})
          </li>
        ))}
      </ul>

      <div className="mb-6">
        <strong className="block mb-2 text-purple-900">Selected Players:</strong>
        {selectedPlayers.length === 0 && <span className="text-gray-500">None</span>}
        {selectedPlayers.map((name) => (
          <span
            key={name}
            className="inline-block bg-purple-900 text-green-300 px-3 py-1 rounded-full mr-2 mb-2 cursor-pointer hover:opacity-80 transition"
            onClick={() => removePlayer(name)}
            title="Click to remove"
          >
            {name} &times;
          </span>
        ))}
      </div>

      <button
        onClick={handleResolveAndOptimize}
        className="bg-purple-900 hover:bg-purple-800 text-white px-6 py-2 rounded-lg shadow transition"
      >
        Resolve & Optimize
      </button>

      {result && (
        <div ref={resultRef}>
          <TeamDisplay
            starting={result.starting}
            bench={result.bench}
          />
        </div>
      )}
    </div>
  );
};

export default App;