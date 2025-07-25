# ⚽ Fantasy Premier League Price Optimizer API

Welcome to the **Fantasy Price Optimizer API**! This project helps you build the **optimal FPL (Fantasy Premier League)** team based on your **budget** and **existing squad**, using 🔬 **mathematical optimization**.

🛰️ **Hosted at:**  
🔗 [https://fantasy-price-finder-project.onrender.com](https://fantasy-price-finder-project.onrender.com)

---

## 🤔 Problem Statement

Fantasy Premier League players often struggle to **find the best price ranges** for their squad members. Many spend too much on a few star players, leaving **insufficient budget** to build a balanced team. This results in weaker overall squads and missed points opportunities.

Our API solves this by **optimizing your entire team**, ensuring you get the **best value for your budget** across all positions — balancing star power with affordable players to maximize total points.

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

## 🚀 Deployment

This API is deployed using **[Render](https://render.com)** — a simple cloud platform for hosting web apps.


### 🔌 API Usage


## 🌐 Base URL

```text
https://fantasy-price-finder-project.onrender.com
```
### 📌 Endpoints

### `GET /`
Check if the API is running.

**Example Response:**
```json
{
  "message": "Fantasy API is running!"
}
```

### `POST /`

## 🚀 How It Works

Provide your **current existing team** as a **flat list** of players by **position** and **price bracket**, and get back the **full optimized team** — including both **starting lineup** and **bench** — automatically filled to meet **FPL rules** and **budget constraints**.

You send a **JSON body** with your current player counts by position and price bracket. The API completes your squad with the best possible remaining players, ensuring:

- ⚽ **Total squad size:** 15 players  
- 📐 **Proper formation:** 2 GKs, 5 DEFs, 5 MIDs, 3 FWDs  
- 🪑 **Bench size:** exactly 4 players — 1 GK + up to 3 others (max 2 per position)  
- 💰 **Budget-friendly bench:** bench is filled with the **cheapest eligible players** to maximize your budget for the starters  




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
