Movie Ticket Booking System
Internship Major Project | Backend Development

A fully functional, high-performance backend system for managing movie ticket bookings, built with FastAPI. This project marks my first major milestone during my internship, integrating core backend concepts from Day 1 through Day 6, including CRUD operations, multi-step workflows, and data validation.

🎯 Project Objective
The primary goal is to build a robust RESTful API that handles the end-to-end lifecycle of movie bookings—from browsing available shows to processing reservations with strict data integrity.

🚀 Key Features & Tech Stack
Framework: FastAPI (Python)

Validation: Pydantic (Schema enforcement & Data integrity)

CRUD Operations: Full Create, Read, Update, and Delete capabilities for Movies, Users, and Bookings.

Search & Discovery: Integrated filtering, sorting, and pagination for movie catalogs.

Business Logic: Multi-step workflows for seat selection and booking confirmation.

🛠 Technical Implementation (Day 1 - Day 6 Concepts)

1. API Architecture
   GET APIs: Optimized endpoints for fetching movie details, theater lists, and user history.

POST APIs: Secure endpoints for user registration and booking requests using Pydantic models for request body validation.

2. Core Logic & Helpers
   Helper Functions: Modularized utility functions for price calculations, availability checks, and format conversions.

Validation: Strict type-checking and custom error handling to ensure zero-fault data entry.

3. Data Management
   Search: Query parameters for searching movies by title or genre.

Sorting & Pagination: Efficient data retrieval to handle large catalogs without performance degradation.

Multi-step Workflows: Logic to handle the transition from "Seat Selection" → "Validation" → "Booking Confirmation."

📂 Project Structure
Plaintext
.
├── app/
│ ├── main.py # FastAPI initialization & routing
│ ├── models/ # Pydantic schemas & Data models
│ ├── api/ # Route handlers (GET, POST, etc.)
│ ├── core/ # Business logic & Multi-step workflows
│ └── utils/ # Helper functions & Pagination logic
├── requirements.txt # Project dependencies
└── README.md # Project documentation
⚙️ Getting Started
Prerequisites
Python 3.8+

Pip (Python Package Manager)

Installation
Clone the repository:

Bash
git clone https://github.com/Mangesh9i7/Movie-tickit-booking.git
cd Movie-tickit-booking
Install dependencies:

Bash
pip install -r requirements.txt
Run the server:

Bash
uvicorn app.main:app --reload
Access Documentation:
Open http://127.0.0.1:8000/docs to view the interactive Swagger UI.

📈 Internship Progress
This project successfully implements the following curriculum:

[x] Day 1-2: FastAPI setup, GET/POST basics, and Pydantic validation.

[x] Day 3-4: CRUD operations and Helper function modularity.

[x] Day 5-6: Advanced Search, Sorting, Pagination, and Complex Workflows.
