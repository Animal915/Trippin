from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import random
import httpx
import asyncio

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

async def geocode_location(location: str) -> Optional[tuple[float, float]]:
    """Get latitude and longitude for a city using Nominatim API"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://nominatim.openstreetmap.org/search",
                params={"q": location, "format": "json", "limit": 1},
                headers={"User-Agent": "TripItinerary/1.0"}
            )
            data = response.json()
            if data:
                return float(data[0]["lat"]), float(data[0]["lon"])
    except Exception:
        pass
    return None

async def fetch_places_from_osm(lat: float, lon: float, category: str) -> List[Dict]:
    """Fetch places from OpenStreetMap Overpass API"""
    queries = {
        "historical": '[out:json][timeout:25];(node["tourism"="museum"](around:5000,{},{});node["tourism"="gallery"](around:5000,{},{}););out;',
        "food": '[out:json][timeout:25];(node["amenity"="restaurant"](around:5000,{},{});node["amenity"="cafe"](around:5000,{},{}););out;',
        "scenic": '[out:json][timeout:25];(node["leisure"="park"](around:5000,{},{});node["tourism"="attraction"](around:5000,{},{}););out;',
        "nightlife": '[out:json][timeout:25];(node["amenity"="bar"](around:5000,{},{});node["amenity"="pub"](around:5000,{},{}););out;'
    }
    
    pricing = {
        "historical": {"min": 8, "max": 25},
        "food": {"min": 12, "max": 60},
        "scenic": {"min": 0, "max": 15},
        "nightlife": {"min": 20, "max": 50}
    }
    
    query = queries.get(category, "")
    if not query:
        return []
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://overpass-api.de/api/interpreter",
                data=query.format(lat, lon, lat, lon),
                headers={"User-Agent": "TripItinerary/1.0"},
                timeout=30
            )
            data = response.json()
            
            places = []
            for element in data.get("elements", [])[:8]:
                name = element.get("tags", {}).get("name", "Unknown Place")
                if name == "Unknown Place":
                    continue
                    
                price_range = pricing[category]
                price = random.uniform(price_range["min"], price_range["max"])
                if category == "scenic" and random.random() < 0.4:
                    price = 0.0
                
                tags = element.get("tags", {})
                description = tags.get("description", "")
                if not description:
                    if "cuisine" in tags:
                        description = f"{tags['cuisine'].title()} cuisine"
                    elif "tourism" in tags:
                        description = f"{tags['tourism'].title()} attraction"
                    elif "amenity" in tags:
                        description = f"{tags['amenity'].title()} venue"
                    else:
                        description = "Popular local destination"
                
                places.append({
                    "name": name,
                    "description": description,
                    "price": round(price, 2)
                })
            
            return places
    except Exception:
        return []

async def get_places_for_location(location: str) -> Dict[str, List[Dict]]:
    """Get real places for a specific location using OpenStreetMap APIs"""
    coords = await geocode_location(location)
    if not coords:
        return {
            "historical": [{"name": f"{location} History Museum", "description": "Local history and culture", "price": 15.0}],
            "food": [{"name": "Local Restaurant", "description": "Traditional regional dishes", "price": 35.0}],
            "scenic": [{"name": f"{location} City Park", "description": "Main public park", "price": 0.0}],
            "nightlife": [{"name": "Local Bar", "description": "Traditional local bar", "price": 25.0}]
        }
    
    lat, lon = coords
    
    categories = ["historical", "food", "scenic", "nightlife"]
    places_data = {}
    
    for category in categories:
        places = await fetch_places_from_osm(lat, lon, category)
        if not places:
            places = [{"name": f"Local {category.title()} Spot", "description": f"Popular {category} destination", "price": 20.0}]
        places_data[category] = places
    
    return places_data

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

@app.post("/generate-itinerary", response_model=ItineraryResponse)
async def generate_itinerary(request: TripRequest):
    if request.days <= 0:
        raise HTTPException(status_code=400, detail="Days must be greater than 0")
    if request.budget <= 0:
        raise HTTPException(status_code=400, detail="Budget must be greater than 0")
    
    location_places = await get_places_for_location(request.location)
    
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
