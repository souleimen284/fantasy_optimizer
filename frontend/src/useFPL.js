import { useState, useEffect, useRef } from "react";
import axios from "axios";

export default function useFPL() {
  const [allPlayers, setAllPlayers] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [positionFilter, setPositionFilter] = useState("");
  const [teamFilter, setTeamFilter] = useState("");
  const [priceRange, setPriceRange] = useState([4.0, 15.0]);
  const [selectedPlayers, setSelectedPlayers] = useState([]);
  const [result, setResult] = useState(null);
  const resultRef = useRef(null);

  const positionMap = {
    1: "GK",
    2: "DEF",
    3: "MID",
    4: "FWD",
  };

  const teamMap = {
    1: "Arsenal",
    2: "Aston Villa",
    3: "Burnley",
    4: "Bournemouth",
    5: "Brentford",
    6: "Brighton",
    7: "Chelsea",
    8: "Crystal Palace",
    9: "Everton",
    10: "Fulham",
    11: "Leeds United",
    12: "Liverpool",
    13: "Manchester City",
    14: "Manchester United",
    15: "Newcastle United",
    16: "Nottingham Forest",
    17: "Sunderland",
    18: "Tottenham Hotspur",
    19: "West Ham United",
    20: "Wolverhampton",
  };

  useEffect(() => {
    async function fetchPlayers() {
      try {
        const res = await axios.get("/all-players");
        setAllPlayers(res.data.players);
      } catch (err) {
        console.error("Failed to fetch players", err);
      }
    }
    fetchPlayers();
  }, []);

  const uniqueTeams = Array.from(new Set(allPlayers.map((p) => p.team))).sort();

  const filteredPlayers = allPlayers.filter((p) => {
    const matchName = p.web_name.toLowerCase().includes(searchTerm.toLowerCase());
    const matchPos = positionFilter ? p.element_type === parseInt(positionFilter) : true;
    const matchTeam = teamFilter ? p.team === parseInt(teamFilter) : true;
    const price = p.now_cost / 10;
    const matchPrice = price >= priceRange[0] && price <= priceRange[1];
    return matchName && matchPos && matchTeam && matchPrice;
  });

  const addPlayer = (playerName) => {
    if (!selectedPlayers.includes(playerName)) {
      setSelectedPlayers((prev) => [...prev, playerName]);
    }
  };

  const removePlayer = (playerName) => {
    setSelectedPlayers((prev) => prev.filter((p) => p !== playerName));
  };

  const handleResolveAndOptimize = async () => {
    try {
      const res1 = await axios.post("/resolve-players", { player_names: selectedPlayers });
      const existingTeam = res1.data.existing_team || {};
      const res2 = await axios.post("/optimize", { existing_team: existingTeam });
      setResult(res2.data);

      // Smooth scroll to results
      setTimeout(() => {
        resultRef.current?.scrollIntoView({ behavior: "smooth" });
      }, 100);
    } catch (err) {
      alert("Error resolving or optimizing team");
      console.error(err);
    }
  };

  return {
    allPlayers,
    searchTerm,
    setSearchTerm,
    positionFilter,
    setPositionFilter,
    teamFilter,
    setTeamFilter,
    priceRange,
    setPriceRange,
    selectedPlayers,
    addPlayer,
    removePlayer,
    handleResolveAndOptimize,
    filteredPlayers,
    result,
    resultRef,
    teamMap,
    positionMap,
    uniqueTeams,
  };
}
