from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
import random

app = FastAPI()

# Disable CORS. Do not remove this for full-stack development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class TripRequest(BaseModel):
    location: str
    days: int
    budget: float

class Place(BaseModel):
    name: str
    description: str
    price: float
    category: str

class ItineraryResponse(BaseModel):
    location: str
    days: int
    budget: float
    total_cost: float
    places: Dict[str, List[Place]]

MOCK_PLACES = {
    "paris": {
        "historical": [
            {"name": "Louvre Museum", "description": "World's largest art museum", "price": 17.0},
            {"name": "Musée d'Orsay", "description": "Impressionist masterpieces", "price": 16.0},
            {"name": "Palace of Versailles", "description": "Opulent royal palace", "price": 20.0},
            {"name": "Arc de Triomphe", "description": "Iconic triumphal arch", "price": 13.0},
            {"name": "Sainte-Chapelle", "description": "Gothic chapel with stunning stained glass", "price": 11.5},
        ],
        "food": [
            {"name": "Le Comptoir du Relais", "description": "Traditional French bistro", "price": 45.0},
            {"name": "L'As du Fallafel", "description": "Famous falafel in the Marais", "price": 8.0},
            {"name": "Pierre Hermé", "description": "Luxury macarons and pastries", "price": 15.0},
            {"name": "Breizh Café", "description": "Modern crêperie", "price": 25.0},
            {"name": "Du Pain et des Idées", "description": "Artisanal bakery", "price": 12.0},
        ],
        "scenic": [
            {"name": "Eiffel Tower", "description": "Iconic iron lattice tower", "price": 29.4},
            {"name": "Seine River Cruise", "description": "Scenic boat tour", "price": 15.0},
            {"name": "Montmartre & Sacré-Cœur", "description": "Historic hilltop district", "price": 0.0},
            {"name": "Luxembourg Gardens", "description": "Beautiful palace gardens", "price": 0.0},
            {"name": "Trocadéro Gardens", "description": "Best Eiffel Tower views", "price": 0.0},
        ],
        "nightlife": [
            {"name": "Moulin Rouge", "description": "Famous cabaret show", "price": 87.0},
            {"name": "Buddha-Bar", "description": "Upscale cocktail lounge", "price": 35.0},
            {"name": "Le Marais Bars", "description": "Trendy bar district", "price": 25.0},
            {"name": "Lido de Paris", "description": "Glamorous cabaret", "price": 75.0},
            {"name": "Hemingway Bar", "description": "Classic cocktail bar at The Ritz", "price": 40.0},
        ]
    },
    "tokyo": {
        "historical": [
            {"name": "Tokyo National Museum", "description": "Japan's oldest and largest museum", "price": 12.0},
            {"name": "Senso-ji Temple", "description": "Ancient Buddhist temple", "price": 0.0},
            {"name": "Imperial Palace", "description": "Emperor's primary residence", "price": 0.0},
            {"name": "Meiji Shrine", "description": "Shinto shrine in forest setting", "price": 0.0},
            {"name": "Tokyo National Museum of Modern Art", "description": "Premier modern art collection", "price": 5.0},
        ],
        "food": [
            {"name": "Tsukiji Outer Market", "description": "Fresh sushi and street food", "price": 20.0},
            {"name": "Ramen Yokocho", "description": "Famous ramen alley", "price": 12.0},
            {"name": "Sukiyabashi Jiro", "description": "World-renowned sushi restaurant", "price": 300.0},
            {"name": "Izakaya Torikizoku", "description": "Popular yakitori chain", "price": 15.0},
            {"name": "Gonpachi", "description": "Traditional Japanese dining", "price": 45.0},
        ],
        "scenic": [
            {"name": "Tokyo Skytree", "description": "Tallest structure in Japan", "price": 25.0},
            {"name": "Shibuya Crossing", "description": "World's busiest pedestrian crossing", "price": 0.0},
            {"name": "Cherry Blossom Viewing", "description": "Seasonal sakura experience", "price": 0.0},
            {"name": "Tokyo Bay Cruise", "description": "Scenic harbor tour", "price": 18.0},
            {"name": "Roppongi Hills Observatory", "description": "City skyline views", "price": 20.0},
        ],
        "nightlife": [
            {"name": "Golden Gai", "description": "Tiny bars in Shinjuku", "price": 30.0},
            {"name": "Robot Restaurant", "description": "Quirky robot show", "price": 65.0},
            {"name": "Karaoke Box", "description": "Private karaoke rooms", "price": 25.0},
            {"name": "Roppongi Clubs", "description": "International nightlife district", "price": 40.0},
            {"name": "Sake Tasting Bar", "description": "Traditional sake experience", "price": 35.0},
        ]
    },
    "new york": {
        "historical": [
            {"name": "Metropolitan Museum of Art", "description": "World-class art collection", "price": 30.0},
            {"name": "9/11 Memorial & Museum", "description": "Moving tribute to victims", "price": 26.0},
            {"name": "Statue of Liberty", "description": "Symbol of freedom", "price": 23.5},
            {"name": "Ellis Island", "description": "Immigration history museum", "price": 23.5},
            {"name": "Museum of Natural History", "description": "Dinosaurs and planetarium", "price": 28.0},
        ],
        "food": [
            {"name": "Katz's Delicatessen", "description": "Famous pastrami sandwiches", "price": 25.0},
            {"name": "Joe's Pizza", "description": "Classic New York slice", "price": 8.0},
            {"name": "Peter Luger Steak House", "description": "Legendary steakhouse", "price": 120.0},
            {"name": "Russ & Daughters", "description": "Appetizing shop since 1914", "price": 35.0},
            {"name": "Xi'an Famous Foods", "description": "Hand-pulled noodles", "price": 15.0},
        ],
        "scenic": [
            {"name": "Central Park", "description": "Urban oasis in Manhattan", "price": 0.0},
            {"name": "Brooklyn Bridge", "description": "Iconic suspension bridge", "price": 0.0},
            {"name": "High Line", "description": "Elevated park on old railway", "price": 0.0},
            {"name": "Top of the Rock", "description": "Empire State Building views", "price": 39.0},
            {"name": "Staten Island Ferry", "description": "Free harbor views", "price": 0.0},
        ],
        "nightlife": [
            {"name": "Broadway Show", "description": "World-class theater", "price": 150.0},
            {"name": "Rooftop Bar 230 Fifth", "description": "Empire State Building views", "price": 45.0},
            {"name": "Comedy Cellar", "description": "Famous comedy club", "price": 35.0},
            {"name": "Jazz at Lincoln Center", "description": "Premier jazz venue", "price": 75.0},
            {"name": "Speakeasy PDT", "description": "Hidden cocktail bar", "price": 40.0},
        ]
    }
}

def get_places_for_location(location: str) -> Dict[str, List[Dict]]:
    """Get places for a specific location, with fallback to generic places"""
    location_key = location.lower().replace(" ", "")
    
    if location_key in MOCK_PLACES:
        return MOCK_PLACES[location_key]
    
    return {
        "historical": [
            {"name": f"{location} History Museum", "description": "Local history and culture", "price": 15.0},
            {"name": f"{location} Art Gallery", "description": "Regional art collection", "price": 12.0},
            {"name": "Historic Downtown", "description": "Walking tour of historic district", "price": 8.0},
            {"name": "Cultural Center", "description": "Local cultural exhibitions", "price": 10.0},
        ],
        "food": [
            {"name": "Local Cuisine Restaurant", "description": "Traditional regional dishes", "price": 35.0},
            {"name": "Street Food Market", "description": "Local street food vendors", "price": 12.0},
            {"name": "Fine Dining Experience", "description": "Upscale local restaurant", "price": 85.0},
            {"name": "Café & Bakery", "description": "Local coffee and pastries", "price": 8.0},
        ],
        "scenic": [
            {"name": f"{location} Viewpoint", "description": "Best city/landscape views", "price": 5.0},
            {"name": "City Park", "description": "Main public park and gardens", "price": 0.0},
            {"name": "Scenic Walking Trail", "description": "Nature walk with views", "price": 0.0},
            {"name": "Observation Deck", "description": "Panoramic city views", "price": 18.0},
        ],
        "nightlife": [
            {"name": "Local Pub", "description": "Traditional local bar", "price": 25.0},
            {"name": "Night Market", "description": "Evening food and shopping", "price": 15.0},
            {"name": "Live Music Venue", "description": "Local bands and performances", "price": 30.0},
            {"name": "Cocktail Lounge", "description": "Upscale drinks and atmosphere", "price": 40.0},
        ]
    }

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

@app.post("/generate-itinerary", response_model=ItineraryResponse)
async def generate_itinerary(request: TripRequest):
    if request.days <= 0:
        raise HTTPException(status_code=400, detail="Days must be greater than 0")
    if request.budget <= 0:
        raise HTTPException(status_code=400, detail="Budget must be greater than 0")
    
    location_places = get_places_for_location(request.location)
    
    places_per_day = 4  # Roughly 1 from each category per day
    max_places_per_category = max(1, request.days)
    
    selected_places = {}
    total_cost = 0.0
    
    categories = {
        "historical": "Historical Museums & Art Galleries",
        "food": "Food Places",
        "scenic": "Scenic & Natural Places", 
        "nightlife": "Partying & Adult Entertainment"
    }
    
    for category_key, category_name in categories.items():
        available_places = location_places.get(category_key, [])
        
        selected = []
        category_budget = request.budget * 0.25  # Rough allocation per category
        
        sorted_places = sorted(available_places, key=lambda x: x["price"])
        
        for place_data in sorted_places:
            if len(selected) >= max_places_per_category:
                break
            if total_cost + place_data["price"] <= request.budget * 0.9:  # Leave some buffer
                place = Place(
                    name=place_data["name"],
                    description=place_data["description"],
                    price=place_data["price"],
                    category=category_name
                )
                selected.append(place)
                total_cost += place_data["price"]
        
        if not selected and available_places:
            cheapest = min(available_places, key=lambda x: x["price"])
            if total_cost + cheapest["price"] <= request.budget:
                place = Place(
                    name=cheapest["name"],
                    description=cheapest["description"],
                    price=cheapest["price"],
                    category=category_name
                )
                selected.append(place)
                total_cost += cheapest["price"]
        
        selected_places[category_name] = selected
    
    return ItineraryResponse(
        location=request.location,
        days=request.days,
        budget=request.budget,
        total_cost=round(total_cost, 2),
        places=selected_places
    )
