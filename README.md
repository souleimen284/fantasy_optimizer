# ⚽ Fantasy Premier League Price Finder API

Welcome to the **Fantasy Price Finder API**! This project helps you build the **optimal FPL (Fantasy Premier League)** team based on your **budget** and **existing squad**, using 🔬 **mathematical optimization**.

🛰️ **Hosted at:**  
🔗 [https://fantasy-price-finder-project.onrender.com](https://fantasy-price-finder-project.onrender.com)

---

## 🧠 What It Does

This API uses **Python**, **Flask**, and **cvxpy** to generate the best possible team of **15 players** (🧤 Starting XI + 🪑 4 Bench) based on your input.

🔍 It:
- Loads real FPL data from `fpl_data.json`
- Groups players by **price brackets** and **positions**
- Fills missing slots in your squad using:
  - 📊 Points vs. Price analysis
  - 💰 Remaining budget
  - ✅ FPL rules (2 GKs, 5 DEFs, 5 MIDs, 3 FWDs)
  - 🪑 Picks the **cheapest bench** players first

🎯 Perfect for:
- Saving time selecting players manually
- Making sure you **get maximum points for your budget**
- Auto-completing your team while staying FPL-legal ✅

---

## 🔌 API Usage

### 🌐 Base URL

```text
https://fantasy-price-finder-project.onrender.com
```
## 📌 Endpoints

### `GET /`
Check if the API is running.

**Example Response:**
```json
{
  "message": "Fantasy API is running!"
}
```

### `POST /`
Provide your current existing team (a flat list of players by position and price bracket) and get back the full optimized team — including both starting lineup and bench — automatically filled to meet FPL rules and budget constraints.

How it works:
You send a JSON body with your current player counts by position and price bracket. The API completes your squad with the best possible remaining players, ensuring:

Total squad size of 15 players

Proper formation: 2 GKs, 5 DEFs, 5 MIDs, 3 FWDs

Bench has exactly 4 players: 1 GK + up to 3 others (max 2 per position)

The bench is filled with the cheapest eligible players to maximize your budget for the starters



**Example request:** 
```json
{
  "existing_team": {
    
            "DEF 4.0-4.5m": 5,
            "FWD 10-10.5m": 3
  }
}

```

**Example Response:**
```json
{
    "bench": {
        "DEF 4.0-4.5m": 2,
        "GK 5.5-6.0m": 1,
        "MID 4.5-5.0m": 1
    },
    "starting": {
        "DEF 4.0-4.5m": 3,
        "FWD 10-10.5m": 3,
        "GK 5.5-6.0m": 1,
        "MID 13.5-14.0m": 1,
        "MID 4.5-5.0m": 1,
        "MID 7.5-8.0m": 2
    }
}
```
