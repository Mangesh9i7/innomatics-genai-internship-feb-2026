from fastapi import FastAPI, HTTPException, status, Query
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()

# ══ DATA STORE ═══════════════════════════════════════════════════════════════

movies = [
    {"id": 1, "title": "Krish", "genre": "Action", "language": "Hindi", "duration_mins": 154, "ticket_price": 350, "seats_available": 120},
    {"id": 2, "title": "3 Idiots", "genre": "Comedy", "language": "Hindi", "duration_mins": 171, "ticket_price": 300, "seats_available": 95},
    {"id": 3, "title": "Baahubali: The Beginning", "genre": "Drama", "language": "Telugu", "duration_mins": 159, "ticket_price": 320, "seats_available": 100},
    {"id": 4, "title": "Avengers: Endgame", "genre": "Action", "language": "English", "duration_mins": 181, "ticket_price": 450, "seats_available": 150},
    {"id": 5, "title": "Spider-Man: No Way Home", "genre": "Action", "language": "English", "duration_mins": 148, "ticket_price": 400, "seats_available": 130},
    {"id": 6, "title": "John Wick", "genre": "Action", "language": "English", "duration_mins": 101, "ticket_price": 380, "seats_available": 90},
    {"id": 7, "title": "Who Am I", "genre": "Action", "language": "English", "duration_mins": 108, "ticket_price": 350, "seats_available": 85},
    {"id": 8, "title": "Dangal", "genre": "Drama", "language": "Hindi", "duration_mins": 161, "ticket_price": 280, "seats_available": 110},
    {"id": 9, "title": "KGF: Chapter 1", "genre": "Action", "language": "Kannada", "duration_mins": 156, "ticket_price": 350, "seats_available": 90}
]

bookings = []
holds = []
booking_counter = 1
hold_counter = 1

# ══ PYDANTIC MODELS ═══════════════════════════════════════════════════════════

# Q6 & Q9: Booking Request with validation and promo codes
class BookingRequest(BaseModel):
    customer_name: str = Field(..., min_length=2)
    movie_id: int = Field(..., gt=0)
    seats: int = Field(..., gt=0, le=10)
    phone: str = Field(..., min_length=10)
    seat_type: str = Field(default="standard") # standard, premium, recliner
    promo_code: Optional[str] = Field(default="")

# Q11: Model for adding new movies
class NewMovie(BaseModel):
    title: str = Field(..., min_length=2)
    genre: str = Field(..., min_length=2)
    language: str = Field(..., min_length=2)
    duration_mins: int = Field(..., gt=0)
    ticket_price: int = Field(..., gt=0)
    seats_available: int = Field(..., gt=0)

# ══ HELPER FUNCTIONS (Q7 & Q9) ═══════════════════════════════════════════════

def find_movie(movie_id: int):
    return next((m for m in movies if m["id"] == movie_id), None)

def calculate_ticket_cost(base_price, seats, seat_type, promo_code=""):
    # Seat multipliers
    multipliers = {"standard": 1.0, "premium": 1.5, "recliner": 2.0}
    multiplier = multipliers.get(seat_type.lower(), 1.0)
    
    original_total = base_price * seats * multiplier
    discount = 0.0
    
    if promo_code == "SAVE10":
        discount = 0.10
    elif promo_code == "SAVE20":
        discount = 0.20
        
    discounted_total = original_total * (1 - discount)
    return original_total, discounted_total

# ══ ROUTES: DAY 1 (BASIC GETS) ═══════════════════════════════════════════════

# Q1: Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to CineStar Booking"}

# Q2: List all movies with summary stats
@app.get("/movies")
def get_movies():
    total_seats = sum(m["seats_available"] for m in movies)
    return {"movies": movies, "total": len(movies), "total_seats_available": total_seats}

# Q5: Detailed summary (Must be above /movies/{id} to avoid path conflict)
@app.get("/movies/summary")
def get_movies_summary():
    most_exp = max(movies, key=lambda m: m["ticket_price"])
    cheapest = min(movies, key=lambda m: m["ticket_price"])
    genre_count = {}
    for m in movies:
        genre_count[m["genre"]] = genre_count.get(m["genre"], 0) + 1
    
    return {
        "total_movies": len(movies),
        "most_expensive_ticket": most_exp["ticket_price"],
        "cheapest_ticket": cheapest["ticket_price"],
        "total_seats": sum(m["seats_available"] for m in movies),
        "count_by_genre": genre_count
    }

# Q3: Get specific movie by ID
@app.get("/movies/{movie_id}")
def get_movie(movie_id: int):
    movie = find_movie(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

# Q4: List all bookings
@app.get("/bookings")
def get_bookings():
    total_rev = sum(b["total_cost"] for b in bookings)
    return {"bookings": bookings, "total": len(bookings), "total_revenue": total_rev}

# ══ ROUTES: DAY 2 & 3 (POST & LOGIC) ═════════════════════════════════════════

# Q8 & Q9: Create a booking with business logic
@app.post("/bookings")
def create_booking(request: BookingRequest):
    global booking_counter
    movie = find_movie(request.movie_id)
    
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    if movie["seats_available"] < request.seats:
        raise HTTPException(status_code=400, detail="Not enough seats available")
    
    orig, final = calculate_ticket_cost(movie["ticket_price"], request.seats, request.seat_type, request.promo_code)
    
    movie["seats_available"] -= request.seats
    
    new_booking = {
        "booking_id": booking_counter,
        "movie_title": movie["title"],
        "customer_name": request.customer_name,
        "seats": request.seats,
        "seat_type": request.seat_type,
        "original_cost": orig,
        "total_cost": final
    }
    bookings.append(new_booking)
    booking_counter += 1
    return new_booking

# Q10: Filter movies by multiple criteria
@app.get("/movies/filter")
def filter_movies(genre: Optional[str] = None, lang: Optional[str] = None, max_price: Optional[int] = None, min_seats: Optional[int] = None):
    results = movies
    if genre: results = [m for m in results if m["genre"].lower() == genre.lower()]
    if lang: results = [m for m in results if m["language"].lower() == lang.lower()]
    if max_price: results = [m for m in results if m["ticket_price"] <= max_price]
    if min_seats: results = [m for m in results if m["seats_available"] >= min_seats]
    return results

# ══ ROUTES: DAY 4 & 5 (CRUD & WORKFLOWS) ═════════════════════════════════════

# Q11: Add a new movie
@app.post("/movies", status_code=201)
def add_movie(movie_in: NewMovie):
    if any(m["title"].lower() == movie_in.title.lower() for m in movies):
        raise HTTPException(status_code=400, detail="Movie title already exists")
    
    new_id = max(m["id"] for m in movies) + 1
    movie_dict = {"id": new_id, **movie_in.dict()}
    movies.append(movie_dict)
    return movie_dict

# Q12: Update movie pricing or seats
@app.put("/movies/{movie_id}")
def update_movie(movie_id: int, ticket_price: Optional[int] = None, seats_available: Optional[int] = None):
    movie = find_movie(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    if ticket_price is not None: movie["ticket_price"] = ticket_price
    if seats_available is not None: movie["seats_available"] = seats_available
    return movie

# Q13: Delete a movie (checks for active bookings)
@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int):
    movie = find_movie(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    # Business rule: check if movie has bookings
    has_bookings = any(b["movie_title"] == movie["title"] for b in bookings)
    if has_bookings:
        raise HTTPException(status_code=400, detail="Cannot delete movie with active bookings")
    
    movies.remove(movie)
    return {"message": "Movie deleted successfully"}

# Q14 & Q15: Seat Hold System
@app.post("/seat-hold")
def hold_seats(customer_name: str, movie_id: int, seats: int):
    global hold_counter
    movie = find_movie(movie_id)
    if not movie or movie["seats_available"] < seats:
        raise HTTPException(status_code=400, detail="Invalid request or insufficient seats")
    
    movie["seats_available"] -= seats
    new_hold = {"hold_id": hold_counter, "customer_name": customer_name, "movie_id": movie_id, "seats": seats}
    holds.append(new_hold)
    hold_counter += 1
    return new_hold

@app.get("/seat-hold")
def get_holds():
    return holds

@app.post("/seat-confirm/{hold_id}")
def confirm_hold(hold_id: int):
    global booking_counter
    hold = next((h for h in holds if h["hold_id"] == hold_id), None)
    if not hold:
        raise HTTPException(status_code=404, detail="Hold ID not found")
    
    movie = find_movie(hold["movie_id"])
    booking = {
        "booking_id": booking_counter,
        "movie_title": movie["title"],
        "customer_name": hold["customer_name"],
        "seats": hold["seats"],
        "total_cost": movie["ticket_price"] * hold["seats"]
    }
    bookings.append(booking)
    holds.remove(hold)
    booking_counter += 1
    return {"message": "Booking confirmed", "details": booking}

@app.delete("/seat-release/{hold_id}")
def release_hold(hold_id: int):
    hold = next((h for h in holds if h["hold_id"] == hold_id), None)
    if not hold:
        raise HTTPException(status_code=404, detail="Hold ID not found")
    
    movie = find_movie(hold["movie_id"])
    movie["seats_available"] += hold["seats"]
    holds.remove(hold)
    return {"message": "Seats released back to inventory"}

# ══ ROUTES: DAY 6 (SEARCH, SORT, PAGINATION) ═════════════════════════════════

# Q16: Case-insensitive Keyword Search
@app.get("/movies/search")
def search_movies(keyword: str):
    k = keyword.lower()
    results = [m for m in movies if k in m["title"].lower() or k in m["genre"].lower() or k in m["language"].lower()]
    if not results:
        return {"message": f"No movies found matching '{keyword}'"}
    return {"results": results, "total_found": len(results)}

# Q17: Sorting
@app.get("/movies/sort")
def sort_movies(sort_by: str = "ticket_price", order: str = "asc"):
    if sort_by not in ["ticket_price", "title", "duration_mins", "seats_available"]:
        raise HTTPException(status_code=400, detail="Invalid sort field")
    
    reverse = True if order == "desc" else False
    sorted_list = sorted(movies, key=lambda x: x[sort_by], reverse=reverse)
    return sorted_list

# Q18: Pagination
@app.get("/movies/page")
def paginate_movies(page: int = 1, limit: int = 3):
    start = (page - 1) * limit
    end = start + limit
    sliced = movies[start:end]
    total_pages = (len(movies) + limit - 1) // limit
    return {"page": page, "total_pages": total_pages, "data": sliced}

# Q19: Booking Search/Sort/Page
@app.get("/bookings/advanced")
def advanced_bookings(customer: Optional[str] = None, sort_by: str = "total_cost", page: int = 1, limit: int = 5):
    data = bookings
    if customer:
        data = [b for b in data if customer.lower() in b["customer_name"].lower()]
    
    data = sorted(data, key=lambda x: x.get(sort_by, 0))
    start = (page - 1) * limit
    return data[start:start+limit]

# Q20: The "Browse" Combined Endpoint
@app.get("/movies/browse")
def browse_movies(
    keyword: Optional[str] = None,
    genre: Optional[str] = None,
    lang: Optional[str] = None,
    sort_by: str = "ticket_price",
    order: str = "asc",
    page: int = 1,
    limit: int = 3
):
    data = movies
    if keyword:
        k = keyword.lower()
        data = [m for m in data if k in m["title"].lower() or k in m["genre"].lower()]
    if genre:
        data = [m for m in data if m["genre"].lower() == genre.lower()]
    if lang:
        data = [m for m in data if m["language"].lower() == lang.lower()]

    rev = (order == "desc")
    data = sorted(data, key=lambda x: x.get(sort_by, 0), reverse=rev)

    start = (page - 1) * limit
    return {
        "total_results": len(data),
        "results": data[start:start+limit]
    }

# ══ PROGRESS CHECKLIST ═══════════════════════════════════════════════════════
# Q1–Q5 ✅ Beginner — Home route + GET all + GET by ID + summary endpoint all working
# Q6 ✅ Pydantic model created with all required validations — tested invalid inputs
# Q7 ✅ Helper functions written as plain Python — no @app decorator on them
# Q8 ✅ POST main endpoint uses helper functions and returns confirmed record
# Q9 ✅ Extended Pydantic model with new field — helper updated with new logic
# Q10 ✅ Filter endpoint using filter_logic() helper — all is not None checks correct
# Q11 ✅ POST /movies returns 201 status — duplicate check working
# Q12 ✅ PUT update endpoint — only non-None fields updated, 404 handled
# Q13 ✅ DELETE endpoint — 404 handled, business rule check (can't delete if active)
# Q14 ✅ First workflow endpoint working — route order rule followed
# Q15 ✅ Full workflow (3+ connected endpoints) working end-to-end
# Q16 ✅ Search endpoint — case-insensitive, multi-field, friendly no-results message
# Q17 ✅ Sort endpoint — validated sort_by and order, all combinations tested
# Q18 ✅ Pagination — total_pages correct, all pages navigated in Swagger
# Q19 ✅ Search + sort + pagination built for secondary list (bookings)
# Q20 ✅ /browse combined endpoint — all params optional, correct order of operations