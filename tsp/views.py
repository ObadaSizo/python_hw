from django.shortcuts import render
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.db import transaction
from .models import City, Distance
from .tsp_solver import TSPSolver
import json
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import networkx as nx
import io
import base64

def index(request):
    cities = City.objects.all()
    distances = Distance.objects.all()
    return render(request, 'tsp/index.html', {
        'cities': cities,
        'distances': distances
    })

def add_city(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Validate required fields
            if not all(key in data for key in ['name', 'x', 'y']):
                return JsonResponse({
                    'error': 'Missing required fields: name, x, y'
                }, status=400)
            
            # Create and validate city
            city = City(
                name=data['name'],
                x_coord=float(data['x']),
                y_coord=float(data['y'])
            )
            city.full_clean()
            city.save()
            
            return JsonResponse({
                'id': city.id,
                'name': city.name,
                'x_coord': city.x_coord,
                'y_coord': city.y_coord
            })
            
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except ValueError:
            return JsonResponse({'error': 'Invalid coordinate values'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
            
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def add_distance(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Validate required fields
            if not all(key in data for key in ['city1', 'city2', 'distance']):
                return JsonResponse({
                    'error': 'Missing required fields: city1, city2, distance'
                }, status=400)
            
            # Get cities
            try:
                city1 = City.objects.get(id=data['city1'])
                city2 = City.objects.get(id=data['city2'])
            except City.DoesNotExist:
                return JsonResponse({'error': 'One or both cities not found'}, status=404)
            
            # Create and validate distance
            with transaction.atomic():
                distance = Distance(
                    city1=city1,
                    city2=city2,
                    distance=float(data['distance'])
                )
                distance.full_clean()
                distance.save()
            
            return JsonResponse({'status': 'success'})
            
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except ValueError:
            return JsonResponse({'error': 'Invalid distance value'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
            
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def solve_tsp(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
        
    try:
        cities = list(City.objects.all())
        
        if len(cities) < 2:
            return JsonResponse({'error': 'Add at least 2 cities'}, status=400)
        
        # Check if all cities are connected
        distances = Distance.objects.all()
        if len(distances) < len(cities) * (len(cities) - 1):
            return JsonResponse({
                'error': 'Not all cities are connected. Please add missing distances.'
            }, status=400)
        
        solver = TSPSolver(cities, distances)
        tour = solver.solve()
        
        if tour is None:
            return JsonResponse({'error': 'No valid tour found'}, status=400)
        
        # Generate visualization
        plt.figure(figsize=(10, 10))
        G = solver.graph
        pos = nx.get_node_attributes(G, 'pos')
        
        # Draw nodes
        nx.draw_networkx_nodes(G, pos, node_color='lightblue', 
                             node_size=500, alpha=0.8)
        
        # Draw all edges lightly
        nx.draw_networkx_edges(G, pos, alpha=0.2)
        
        # Draw tour
        tour_edges = [(solver.id_map[tour[i]], solver.id_map[tour[i+1]]) 
                     for i in range(len(tour)-1)]
        tour_edges.append((solver.id_map[tour[-1]], solver.id_map[tour[0]]))
        nx.draw_networkx_edges(G, pos, edgelist=tour_edges, 
                             edge_color='r', width=2)
        
        # Draw labels
        labels = {solver.id_map[city.id]: city.name for city in cities}
        nx.draw_networkx_labels(G, pos, labels)
        
        # Add title and axis labels
        plt.title("TSP Solution - Optimal Route")
        plt.xlabel("X Coordinate")
        plt.ylabel("Y Coordinate")
        
        # Save plot to buffer
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight', dpi=300)
        plt.close()
        
        # Convert to base64
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        graphic = base64.b64encode(image_png).decode('utf-8')
        
        # Get tour details
        tour_cities = [City.objects.get(id=city_id) for city_id in tour]
        tour_distance = solver.get_tour_distance(tour)
        
        return JsonResponse({
            'tour': [{'id': city.id, 'name': city.name} for city in tour_cities],
            'distance': tour_distance,
            'visualization': graphic
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
