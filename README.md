# ⚽ Fantasy Premier League Optimizer (Full Stack)

Welcome to the **FPL Optimizer**, a full-stack web application that helps you build the most optimized **Fantasy Premier League** squad based on your budget, using real data and mathematical optimization techniques.

🌐 **Live App**: [https://fantasy-optimizer-full-stack.onrender.com](https://fantasy-optimizer-full-stack.onrender.com)

---

## 📦 Tech Stack

* **Backend**: [Flask](https://flask.palletsprojects.com/) (Python) + [cvxpy](https://www.cvxpy.org/) for mathematical optimization
* **Frontend**: [React](https://reactjs.org/) + [Tailwind CSS](https://tailwindcss.com/)
* **Deployment**: [Render](https://render.com) (Single Full-Stack Service)

---

## 🧠 Problem Statement

Fantasy Premier League (FPL) players struggle to build the best team with limited budget. Most spend too much on stars and end up with weak benches. This project helps:

* Select the optimal squad of **15 players**
* Stay within budget constraints
* Follow FPL rules (2 GK, 5 DEF, 5 MID, 3 FWD)
* Automatically complete missing spots based on performance and price

---

## 💻 Features

### 🔧 Backend (API)

* Accepts partially completed squads as input
* Analyzes FPL JSON data
* Outputs optimal full squads (starting + bench)
* Mathematical optimization ensures best use of budget

### 🎨 Frontend (React + Tailwind)

* Elegant UI to search and filter players
* Interactive range slider for price selection
* Visual team display on football pitch
* Logo, colors, and transitions styled with Tailwind

---

## 🖼️ Visual UI Highlights

* Logo added for branding
* Player avatars placed on football pitch (with price + position)
* Hover animations and shadows for interaction

---

## 📊 How to Use the App

1. **Search** players by name, position, and team
2. **Select** known players in your squad
3. **Set** budget range using slider
4. **Click** "Resolve & Optimize"
5. See your full squad (with subs) on a **visual pitch**

---

## ⚙️ Example API Usage

### `POST /`

**Request:**

```json
{
  "existing_team": {
    "DEF 4.0-4.5m": 5,
    "FWD 10-10.5m": 3
  }
}
```

**Response:**

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

---

## 🚀 Deployment

The entire stack is deployed on [Render](https://render.com):

* One full-stack **Docker** service
* Serves both Flask API and React static build from `/frontend/build`

---

## 🧪 Run Locally

```bash
# Clone repo
https://github.com/souleimen284/fantasy_optimizer.git

# Navigate into project root
cd fantasy_optimizer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install backend dependencies
pip install -r requirements.txt

# Build frontend
cd frontend
npm install
npm run build

# Run backend (serves React build from static folder)
cd ..
python app.py
```

---

## 📂 Folder Structure

```
fantasy_optimizer/
├── app.py             # Flask API
├── requirements.txt
├── Dockerfile         # Full-stack Docker config
├── frontend/          # React frontend
│   ├── public/
│   ├── src/
│   └── build/         # Production build
├── fpl_data.json      # Raw FPL player data
└── README.md
```

---

## 👨‍💻 Author

**Souleimen Ben Hmida**

If you like this project, please ⭐ the repo and feel free to contribute!

---

## 📢 Future Ideas

* Add player statistics from official FPL API
* Allow saving and sharing custom squads
* Real-time budget tracking and error checks
