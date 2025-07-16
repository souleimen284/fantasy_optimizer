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

##POST /optimize
Send your current team (starting + bench) and get optimized player recommendations.


**Example request:** 
{
  "existing_team": {
    "starting": {
      "DEF 4.0-4.5m": 2,
      "FWD 10-10.5m": 2
    },
    "bench": {
      "MID 6.0-6.5m": 1
    }
  }
}


**Example Response:**
{
  "starting": {
    "MID 7.0-7.5m": 2,
    "FWD 6.0-6.5m": 1
  },
  "bench": {
    "DEF 4.5-5.0m": 1,
    "GK 4.0-4.5m": 1,
    "DEF 4.0-4.5m": 1,
    "MID 5.5-6.0m": 1
  }
}
