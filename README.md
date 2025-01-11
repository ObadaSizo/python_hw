# TSP Solver with A* Algorithm

A Django web application that solves the Traveling Salesman Problem (TSP) using the A* algorithm. The application provides a user-friendly interface for adding cities, defining distances between them, and visualizing the optimal tour.

## Features

- Add cities with X and Y coordinates
- Define distances between cities
- Visualize the optimal tour using networkx and matplotlib
- Interactive web interface built with Bootstrap
- A* algorithm implementation for finding the optimal tour

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Apply database migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Run the development server:
```bash
python manage.py runserver
```

6. Visit `http://localhost:8000` in your web browser.

## Usage

1. Add cities:
   - Enter the city name and its X, Y coordinates
   - Click "Add City"

2. Define distances:
   - Select two cities from the dropdowns
   - Enter the distance between them
   - Click "Add Distance"

3. Solve TSP:
   - Click the "Solve TSP" button
   - View the optimal tour and its visualization

## Technical Details

### A* Algorithm Implementation

The A* algorithm implementation uses the following components:

- Minimum Spanning Tree (MST) heuristic for lower bound estimation
- Priority queue for efficient node exploration
- Graph representation using networkx library

### Visualization

The tour visualization is created using:

- networkx for graph manipulation
- matplotlib for plotting
- Base64 encoding for sending the plot to the frontend

## Deployment

To deploy on PythonAnywhere:

1. Create a PythonAnywhere account
2. Upload the project files
3. Create a virtual environment and install dependencies
4. Configure the WSGI file
5. Set up static files
6. Update allowed hosts in settings.py

## License

This project is licensed under the MIT License - see the LICENSE file for details. 