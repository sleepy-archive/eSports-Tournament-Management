# ESPORTS DB // TERMINAL (HONKAI STAR RAIL THEMED)
### "A high-performance Pygame dashboard for eSports tournament management, with a nice HSR theme touch."

Ever wanted to manage an eSports tournament but felt like standard database tools were just a bit too... boring? Welcome to the Terminal! This project is a fully functional SQL database dashboard wrapped in a sleek, Honkai: Star Rail-inspired UI. Whether you're tracking the Aetherium Wars or just organizing your own local brackets, why not do it in style?

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-CE-green?style=flat&logo=python)
![SQL Server](https://img.shields.io/badge/SQL_Server-MS_SQL-CC2927?style=flat&logo=microsoftsqlserver&logoColor=white)
![Honkai Star Rail](https://img.shields.io/badge/Honkai_Star_Rail-🚂-purple?style=flat)

---

## 📸 Interastral Peace Broadcast // UI Preview

<p align="center">
  <img src="assets\eSports_DEMO.png" width="48%" alt="Screenshot 1" style="border-radius: 5px;">
  &nbsp; &nbsp;
  <img src="assets\eSports_Schedule_Viewer.png" width="48%" alt="Screenshot 2" style="border-radius: 5px;">
</p>

<p align="center">
  <img src="assets\eSports_Update_Status.png" width="48%" alt="Screenshot 3" style="border-radius: 5px;">
  &nbsp; &nbsp;
  <img src="assets\eSports_Player_Graph.png" width="48%" alt="Screenshot 4" style="border-radius: 5px;">
</p>

*The UI utilizes asynchronous threading for all database queries via `pyodbc`. This ensures animations, floating UI elements, and interactive screens maintain 60FPS even when fetching complex multi-table SQL joins.*

---

## ✨ Data Bank Contents (Features)
- **Full-Fledged Tournament Tracker**: Keep tabs on your live matches, active rosters, global standings, and player combat metrics all in one place.
- **Banging OST**: Chill out to some sweet Penacony tunes ("Game Time! Planarcadia Battle Theme" plays by default) while you crunch those numbers and edit records.
- **Easter Eggs & Flavor**: Keep an eye on the system log... Silver Wolf might just try to hack your terminal if you leave it running long enough. Plus, the ticker features live "fan reactions" to your matches!
- **Buttery Smooth UI**: Built with Pygame-CE, it features floating hexes, a "breathing" core animation, and fully interactive data viewers that feel straight out of the Interastral Peace Corporation.

---

## 🛠️ Astral Express Boarding Procedure (Installation & Setup)

### 1. IPC Matrix Initialization (Database Setup)
Before diving into the Simulated Universe, the IPC database must be initialized:
1. Open **SQL Server Management Studio (SSMS)** (your databank client).
2. Navigate to the `SQL/` directory in this repository.
3. Open and execute `eSports_DB_Creation.sql` to build the schema.
4. Open and execute `eSports_Sample_Data.sql` to populate the tables.

### 2. Synesthesia Environment Calibration (Python Setup)
Download the coordinates to your local terminal and install the required Synesthesia dependencies:
```bash
git clone [https://github.com/YOUR_USERNAME/ESPORTS-DB-TERMINAL.git](https://github.com/YOUR_USERNAME/ESPORTS-DB-TERMINAL.git)
cd ESPORTS-DB-TERMINAL
python -m venv venv


# Windows Activation:
venv\Scripts\activate
# Mac/Linux Activation:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Configuration & Customization
The application is highly customizable. You can modify database connections, themes, and display settings before launching.

**A. Database Connection (`eSports_Engine.py`)**
By default, the application attempts to connect to a local SQL Server named `ASPHYXIATED`. To update this for your machine, open `eSports_Engine.py` and modify the `__init__` method:

```python
self.conn_str = (
    r"Driver={ODBC Driver 17 for SQL Server};"
    r"Server=YOUR_SERVER_NAME_HERE;"
    r"Database=EsportsTournament;"
    r"Trusted_Connection=yes;"
)
```

**B. UI Themes & Colors (`eSports_config.py`)**
The application ships with three default color palettes (Cyan, Orange, Green). You can edit these or add your own custom hex/RGB codes in the `Config` class:

```python
PALETTES: List[Dict[str, Any]] = [
    {"name": "CYAN", "bg": (10, 12, 16), "fill": (15, 20, 25), "accent": (0, 255, 255), "dim": (0, 100, 100), "text": (220, 225, 235), "dots": (20, 40, 50)},
    # Add your own custom theme dictionary here!
]
```

**C. Display Resolution (`eSports_config.py`)**
The terminal runs at `1280x720` by default. You can adjust the `WIDTH`, `HEIGHT`, and `FPS` limits directly at the top of the `Config` class to fit your monitor.

## 🎮 Navigating the Dreamscape (Usage)
Launch the terminal dashboard by executing the core script:

```
python eSports_Core.py
```
Use your mouse to navigate tabs and select database query actions.


Use the scroll wheel to navigate populated data tables and the live system log.

You can use Sample Data Generator to fill out your tables.

Press ESC to close any active data viewers or graphs.

## 🚧 Trailblazer's Warning (Disclaimer)
Just a quick heads-up: this is purely a passion project built for fun! While the Astral Express usually runs on time, you might occasionally bump into a few bugs, glitches, or space-time anomalies (aka random errors) along the way. Feel free to tinker around, fix things, and make it your own!

## ⚖️ License
Distributed under the MIT License. See LICENSE for more information.
