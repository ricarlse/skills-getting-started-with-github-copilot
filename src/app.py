"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.

Also includes a Motorsport Insights module delivering AI-backed sentiment
analysis for fans, drivers, teams, manufacturers, and technical innovations.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities, and motorsport AI insights")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Motorsport Club": {
        "description": "Explore MotoGP, motorcycle racing, and motorsport engineering",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["alex@mergington.edu", "ryan@mergington.edu"]
    }
}

# ---------------------------------------------------------------------------
# Motorsport Insights Data
# ---------------------------------------------------------------------------

fan_sentiments = {
    "overall": {
        "positive": 68,
        "neutral": 20,
        "negative": 12,
        "trend": "improving",
        "summary": "Fan sentiment is broadly positive following an exciting start to the season, with close championship battles driving engagement."
    },
    "top_topics": [
        {"topic": "Championship battles", "sentiment": "positive", "mentions": 45230},
        {"topic": "Rider safety measures", "sentiment": "positive", "mentions": 31540},
        {"topic": "Race formats", "sentiment": "neutral", "mentions": 18760},
        {"topic": "Ticket prices", "sentiment": "negative", "mentions": 12400},
        {"topic": "Broadcast coverage", "sentiment": "neutral", "mentions": 9870}
    ],
    "community_highlights": [
        "Record social media engagement during the opening round",
        "Fan attendance up 12% year-over-year at European venues",
        "New younger demographic (18–24) growing by 23% globally"
    ]
}

driver_sentiments = {
    "Marc Marquez": {
        "overall_sentiment": "positive",
        "fan_approval": 82,
        "performance_rating": 9.1,
        "trending_topics": ["Comeback story", "Championship contender", "Aggressive riding style"],
        "sentiment_breakdown": {"positive": 74, "neutral": 14, "negative": 12},
        "key_insight": "Fans celebrate Marquez's resilience and return to front-running form."
    },
    "Pecco Bagnaia": {
        "overall_sentiment": "positive",
        "fan_approval": 78,
        "performance_rating": 8.9,
        "trending_topics": ["Title defender", "Consistency", "Technical mastery"],
        "sentiment_breakdown": {"positive": 70, "neutral": 18, "negative": 12},
        "key_insight": "Respected as a technical rider who extracts maximum performance from the Ducati package."
    },
    "Jorge Martin": {
        "overall_sentiment": "positive",
        "fan_approval": 75,
        "performance_rating": 8.7,
        "trending_topics": ["Sprint race specialist", "Speed", "Championship dark horse"],
        "sentiment_breakdown": {"positive": 68, "neutral": 20, "negative": 12},
        "key_insight": "Recognized for exceptional sprint performance and growing championship pedigree."
    },
    "Fabio Quartararo": {
        "overall_sentiment": "neutral",
        "fan_approval": 71,
        "performance_rating": 7.8,
        "trending_topics": ["Yamaha struggles", "Technical feedback", "Potential"],
        "sentiment_breakdown": {"positive": 55, "neutral": 28, "negative": 17},
        "key_insight": "Fans empathize with Quartararo's situation given Yamaha's current competitiveness gap."
    },
    "Brad Binder": {
        "overall_sentiment": "positive",
        "fan_approval": 73,
        "performance_rating": 8.2,
        "trending_topics": ["Underdog hero", "KTM loyalty", "Race craft"],
        "sentiment_breakdown": {"positive": 65, "neutral": 22, "negative": 13},
        "key_insight": "Popular for consistent performances and loyalty to KTM through competitive cycles."
    }
}

team_sentiments = {
    "Ducati Lenovo Team": {
        "overall_sentiment": "positive",
        "fan_support": 85,
        "performance_rating": 9.3,
        "manufacturer": "Ducati",
        "key_insights": [
            "Dominant constructor with strong technical backing",
            "Multiple rider lineup creates internal competition that raises performance",
            "Engineering team highly regarded for rapid development cycles"
        ],
        "sentiment_breakdown": {"positive": 78, "neutral": 14, "negative": 8}
    },
    "Red Bull KTM Factory Racing": {
        "overall_sentiment": "positive",
        "fan_support": 72,
        "performance_rating": 8.0,
        "manufacturer": "KTM",
        "key_insights": [
            "Strong underdog narrative resonates with fans",
            "Austrian engineering precision and innovation praised",
            "Growing competitiveness against established manufacturers"
        ],
        "sentiment_breakdown": {"positive": 65, "neutral": 22, "negative": 13}
    },
    "Monster Energy Yamaha": {
        "overall_sentiment": "neutral",
        "fan_support": 68,
        "performance_rating": 7.2,
        "manufacturer": "Yamaha",
        "key_insights": [
            "Fans concerned about pace deficit vs. Ducati",
            "Rich heritage and loyal fanbase provide resilience",
            "Development direction under close scrutiny"
        ],
        "sentiment_breakdown": {"positive": 48, "neutral": 30, "negative": 22}
    },
    "Repsol Honda": {
        "overall_sentiment": "neutral",
        "fan_support": 70,
        "performance_rating": 7.5,
        "manufacturer": "Honda",
        "key_insights": [
            "Iconic brand with global fanbase despite recent struggles",
            "Fans hopeful for turnaround following technical restructuring",
            "Historical dominance creates high expectations"
        ],
        "sentiment_breakdown": {"positive": 52, "neutral": 28, "negative": 20}
    },
    "Aprilia Racing": {
        "overall_sentiment": "positive",
        "fan_support": 74,
        "performance_rating": 8.3,
        "manufacturer": "Aprilia",
        "key_insights": [
            "Celebrated as a success story of rapid development",
            "Small manufacturer punching above its weight",
            "Engineering culture praised for innovation and agility"
        ],
        "sentiment_breakdown": {"positive": 68, "neutral": 20, "negative": 12}
    }
}

manufacturer_sentiments = {
    "Ducati": {
        "overall_sentiment": "positive",
        "brand_reputation": 92,
        "innovation_score": 9.4,
        "market_perception": "Industry leader",
        "key_insights": [
            "Perceived as the benchmark for MotoGP technology",
            "Desmodromic valve system and aerodynamics set industry standards",
            "Strong road-bike brand halo effect from racing success"
        ],
        "sentiment_breakdown": {"positive": 82, "neutral": 12, "negative": 6},
        "industry_impact": "Ducati's aero innovations have driven aerodynamic rule changes across the sport, influencing competitor R&D direction."
    },
    "Honda": {
        "overall_sentiment": "neutral",
        "brand_reputation": 85,
        "innovation_score": 7.8,
        "market_perception": "Transitioning",
        "key_insights": [
            "Legacy brand with unmatched historical prestige",
            "Current on-track struggles create temporary perception gap",
            "Engineering culture remains highly respected globally"
        ],
        "sentiment_breakdown": {"positive": 58, "neutral": 26, "negative": 16},
        "industry_impact": "Honda's investment in alternative powertrains and hydrogen technology positions it as a long-term mobility leader beyond motorsport."
    },
    "Yamaha": {
        "overall_sentiment": "neutral",
        "brand_reputation": 82,
        "innovation_score": 7.5,
        "market_perception": "Recovery phase",
        "key_insights": [
            "Beloved for balanced, rideable chassis philosophy",
            "Fans patient but expecting visible progress",
            "Strong brand loyalty sustains positive perception"
        ],
        "sentiment_breakdown": {"positive": 54, "neutral": 28, "negative": 18},
        "industry_impact": "Yamaha's electronic chassis control research has influenced road-bike traction and stability systems used in consumer motorcycles worldwide."
    },
    "KTM": {
        "overall_sentiment": "positive",
        "brand_reputation": 80,
        "innovation_score": 8.6,
        "market_perception": "Challenger brand",
        "key_insights": [
            "Austrian manufacturer praised for rapid development pace",
            "Off-road DNA translates well into MotoGP chassis dynamics",
            "Young rider development program highly regarded"
        ],
        "sentiment_breakdown": {"positive": 70, "neutral": 20, "negative": 10},
        "industry_impact": "KTM's advanced WP suspension technology, developed through MotoGP, is now standard in premium off-road and adventure motorcycles."
    },
    "Aprilia": {
        "overall_sentiment": "positive",
        "brand_reputation": 78,
        "innovation_score": 8.8,
        "market_perception": "Rising challenger",
        "key_insights": [
            "Celebrated for remarkable performance trajectory",
            "V4 engine architecture praised for power delivery innovations",
            "Small team efficiency seen as a model for other manufacturers"
        ],
        "sentiment_breakdown": {"positive": 72, "neutral": 18, "negative": 10},
        "industry_impact": "Aprilia's aerodynamic package development has contributed to the broader industry adoption of active aero concepts in high-performance motorcycles."
    }
}

technical_innovations = [
    {
        "name": "Advanced Aerodynamic Packages",
        "category": "Aerodynamics",
        "description": "Sophisticated winglets, fairings, and swingarm downforce devices that increase stability at high speed.",
        "motorcycle_industry_impact": "Road-legal superbikes now incorporate aerodynamic elements derived from MotoGP, improving high-speed stability and reducing lift by up to 40%.",
        "manufacturing_industry_impact": "CFD (Computational Fluid Dynamics) simulation tools developed for MotoGP are now standard in automotive and industrial product design pipelines.",
        "adoption_rate": "High",
        "year_introduced": 2015
    },
    {
        "name": "Ride Height Devices",
        "category": "Chassis Technology",
        "description": "Pneumatic or mechanical systems that lower the motorcycle's centre of gravity on corner exit to maximise acceleration.",
        "motorcycle_industry_impact": "Inspired adjustable suspension pre-load and ride-height features in premium adventure and sports-touring motorcycles.",
        "manufacturing_industry_impact": "Precision actuator and hydraulic micro-system manufacturing techniques have been adopted in industrial automation and robotics.",
        "adoption_rate": "Medium",
        "year_introduced": 2019
    },
    {
        "name": "Seamless-Shift Gearboxes",
        "category": "Powertrain",
        "description": "Dual-clutch-style gearboxes enabling power-neutral gear changes with no torque interruption.",
        "motorcycle_industry_impact": "Quickshifter and auto-blipper technology in consumer motorcycles owes its development to seamless-shift R&D.",
        "manufacturing_industry_impact": "Precision gear-machining tolerances and materials science breakthroughs have been adopted in high-performance automotive transmissions.",
        "adoption_rate": "High",
        "year_introduced": 2012
    },
    {
        "name": "Unified Electronics Platform (MSMA ECU)",
        "category": "Electronics",
        "description": "Standardised ECU running sophisticated algorithms for traction control, anti-wheelie, engine braking, and launch control.",
        "motorcycle_industry_impact": "Cornering ABS, traction control, and IMU-based safety systems in road bikes trace their lineage to MotoGP electronics research.",
        "manufacturing_industry_impact": "Software validation and safety-critical embedded systems processes developed for motorsport ECUs are now applied in automotive ADAS and EV control units.",
        "adoption_rate": "Very High",
        "year_introduced": 2016
    },
    {
        "name": "Carbon Fibre Composite Structures",
        "category": "Materials Science",
        "description": "Lightweight, high-stiffness carbon fibre used in frames, swingarms, bodywork, and braking components.",
        "motorcycle_industry_impact": "Carbon-ceramic brake discs, carbon wheels, and composite bodywork are now available on flagship consumer motorcycles.",
        "manufacturing_industry_impact": "Automated fibre placement and resin-transfer moulding processes refined in motorsport are used in aerospace, wind energy, and electric vehicle battery enclosures.",
        "adoption_rate": "High",
        "year_introduced": 2000
    },
    {
        "name": "Holeshot Device (Launch Control Systems)",
        "category": "Chassis Technology",
        "description": "Mechanisms that compress the front forks or rear suspension to optimise crouch position and anti-wheelie geometry at race starts.",
        "motorcycle_industry_impact": "Inspired advanced launch control modes and anti-wheelie maps in consumer sports motorcycles.",
        "manufacturing_industry_impact": "Micro-hydraulic locking mechanisms developed for holeshot devices are being explored for industrial quick-set clamping applications.",
        "adoption_rate": "Medium",
        "year_introduced": 2019
    },
    {
        "name": "Predictive AI Race Strategy Tools",
        "category": "Artificial Intelligence",
        "description": "Machine learning models that analyse tyre degradation, fuel load, and competitor pace to recommend pit-stop and riding-style strategies in real time.",
        "motorcycle_industry_impact": "Tyre monitoring AI is beginning to be integrated into premium motorcycle connectivity platforms for road safety.",
        "manufacturing_industry_impact": "Predictive maintenance AI pipelines developed for MotoGP telemetry are deployed in smart factory equipment monitoring and Industry 4.0 applications.",
        "adoption_rate": "Growing",
        "year_introduced": 2021
    }
]


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


# ---------------------------------------------------------------------------
# Motorsport Insights Endpoints
# ---------------------------------------------------------------------------

@app.get("/insights/fan-sentiments")
def get_fan_sentiments():
    """Return aggregated fan sentiment data"""
    return fan_sentiments


@app.get("/insights/driver-sentiments")
def get_driver_sentiments():
    """Return sentiment data for each driver"""
    return driver_sentiments


@app.get("/insights/driver-sentiments/{driver_name}")
def get_driver_sentiment(driver_name: str):
    """Return sentiment data for a specific driver"""
    if driver_name not in driver_sentiments:
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver_sentiments[driver_name]


@app.get("/insights/team-sentiments")
def get_team_sentiments():
    """Return sentiment data for each team"""
    return team_sentiments


@app.get("/insights/team-sentiments/{team_name}")
def get_team_sentiment(team_name: str):
    """Return sentiment data for a specific team"""
    if team_name not in team_sentiments:
        raise HTTPException(status_code=404, detail="Team not found")
    return team_sentiments[team_name]


@app.get("/insights/manufacturer-sentiments")
def get_manufacturer_sentiments():
    """Return sentiment data for each manufacturer"""
    return manufacturer_sentiments


@app.get("/insights/manufacturer-sentiments/{manufacturer_name}")
def get_manufacturer_sentiment(manufacturer_name: str):
    """Return sentiment data for a specific manufacturer"""
    if manufacturer_name not in manufacturer_sentiments:
        raise HTTPException(status_code=404, detail="Manufacturer not found")
    return manufacturer_sentiments[manufacturer_name]


@app.get("/insights/technical-innovations")
def get_technical_innovations():
    """Return list of technical innovations and their industry impact"""
    return technical_innovations


@app.get("/insights")
def get_all_insights():
    """Return a summary of all motorsport insights"""
    return {
        "fan_sentiments": fan_sentiments,
        "driver_sentiments": driver_sentiments,
        "team_sentiments": team_sentiments,
        "manufacturer_sentiments": manufacturer_sentiments,
        "technical_innovations": technical_innovations
    }
