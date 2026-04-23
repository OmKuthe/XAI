# dataset.py
import pandas as pd
import random
import numpy as np
from datetime import datetime, timedelta
import os

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

# College data with comprehensive information
COLLEGES = {
    # Tier 1 - Premier Institutes
    "IIT Bombay": {
        "city": "Mumbai",
        "category": "Premier Institute",
        "rating": 4.8,
        "popularity": 5.0,
        "techfest_name": "Techfest",
        "website": "techfest.org"
    },
    "ICT Mumbai": {
        "city": "Mumbai",
        "category": "Premier Institute",
        "rating": 4.6,
        "popularity": 4.7,
        "techfest_name": "Momentum",
        "website": "momentum.ictmumbai.edu.in"
    },
    "VNIT Nagpur": {
        "city": "Nagpur",
        "category": "Premier Institute",
        "rating": 4.7,
        "popularity": 4.8,
        "techfest_name": "Axis",
        "website": "axisvnit.org"
    },
    "COEP Technological University": {
        "city": "Pune",
        "category": "Premier Institute",
        "rating": 4.5,
        "popularity": 4.6,
        "techfest_name": "Impulse",
        "website": "impulse.coep.org.in"
    },
    "VJTI Mumbai": {
        "city": "Mumbai",
        "category": "Premier Institute",
        "rating": 4.5,
        "popularity": 4.6,
        "techfest_name": "Technovanza",
        "website": "technovanza.org"
    },
    
    # Tier 2 - Highly Reputed
    "IIIT Pune": {
        "city": "Pune",
        "category": "Highly Reputed",
        "rating": 4.4,
        "popularity": 4.5,
        "techfest_name": "Cognizance",
        "website": "cognizance.org.in"
    },
    "IIIT Nagpur": {
        "city": "Nagpur",
        "category": "Highly Reputed",
        "rating": 4.3,
        "popularity": 4.4,
        "techfest_name": "Aaghaaz",
        "website": "aaghaaz.org"
    },
    "SPIT Mumbai": {
        "city": "Mumbai",
        "category": "Highly Reputed",
        "rating": 4.4,
        "popularity": 4.5,
        "techfest_name": "Impulse",
        "website": "spitimpulse.in"
    },
    "WCE Sangli": {
        "city": "Sangli",
        "category": "Highly Reputed",
        "rating": 4.3,
        "popularity": 4.4,
        "techfest_name": "Techyon",
        "website": "techyon.wce.ac.in"
    },
    "PICT Pune": {
        "city": "Pune",
        "category": "Highly Reputed",
        "rating": 4.4,
        "popularity": 4.5,
        "techfest_name": "Expedition",
        "website": "expedition.pict.edu"
    },
    "DJ Sanghvi Mumbai": {
        "city": "Mumbai",
        "category": "Highly Reputed",
        "rating": 4.3,
        "popularity": 4.4,
        "techfest_name": "Synergy",
        "website": "synergy.djsce.ac.in"
    },
    "VIT Pune": {
        "city": "Pune",
        "category": "Highly Reputed",
        "rating": 4.2,
        "popularity": 4.3,
        "techfest_name": "Vihaan",
        "website": "vihaan.vit.edu"
    },
    "MIT-WPU Pune": {
        "city": "Pune",
        "category": "Highly Reputed",
        "rating": 4.2,
        "popularity": 4.3,
        "techfest_name": "MITE",
        "website": "mite.mitwpu.edu.in"
    },
    "AIT Pune": {
        "city": "Pune",
        "category": "Highly Reputed",
        "rating": 4.1,
        "popularity": 4.2,
        "techfest_name": "Technovanza",
        "website": "aitpune.edu.in/technovanza"
    },
    "KJ Somaiya Mumbai": {
        "city": "Mumbai",
        "category": "Highly Reputed",
        "rating": 4.3,
        "popularity": 4.4,
        "techfest_name": "Sanskruti",
        "website": "sanskruti.somaiya.edu"
    },
    "Cummins Pune": {
        "city": "Pune",
        "category": "Highly Reputed",
        "rating": 4.2,
        "popularity": 4.3,
        "techfest_name": "Cumminspark",
        "website": "cumminspark.edu.in"
    },
    "SIT Pune": {
        "city": "Pune",
        "category": "Highly Reputed",
        "rating": 4.1,
        "popularity": 4.2,
        "techfest_name": "Symbiosis Techfest",
        "website": "sitpune.edu.in/techfest"
    },
    
    # Tier 3 - Notable Colleges
    "PCCOE Pune": {
        "city": "Pune",
        "category": "Notable",
        "rating": 4.0,
        "popularity": 4.1,
        "techfest_name": "Pinnacle",
        "website": "pccoepune.edu.in/pinnacle"
    },
    "Ramdeobaba Nagpur": {
        "city": "Nagpur",
        "category": "Notable",
        "rating": 4.0,
        "popularity": 4.1,
        "techfest_name": "Yantra",
        "website": "rknpec.edu.in/yantra"
    },
    "YCCE Nagpur": {
        "city": "Nagpur",
        "category": "Notable",
        "rating": 3.9,
        "popularity": 4.0,
        "techfest_name": "Techtors",
        "website": "ycce.edu/techtors"
    },
    "Raisoni Nagpur": {
        "city": "Nagpur",
        "category": "Notable",
        "rating": 3.9,
        "popularity": 4.0,
        "techfest_name": "Raisoni Techfest",
        "website": "raisoni.net/techfest"
    },
    "SPCE Mumbai": {
        "city": "Mumbai",
        "category": "Notable",
        "rating": 4.0,
        "popularity": 4.1,
        "techfest_name": "Prerana",
        "website": "spce.ac.in/prerana"
    },
    "MPSTME Mumbai": {
        "city": "Mumbai",
        "category": "Notable",
        "rating": 4.0,
        "popularity": 4.1,
        "techfest_name": "Manthan",
        "website": "mpstme.edu.in/manthan"
    },
    "TSEC Mumbai": {
        "city": "Mumbai",
        "category": "Notable",
        "rating": 3.9,
        "popularity": 4.0,
        "techfest_name": "T-Spectra",
        "website": "tsec.edu.in/t-spectra"
    },
    "VESIT Mumbai": {
        "city": "Mumbai",
        "category": "Notable",
        "rating": 3.9,
        "popularity": 4.0,
        "techfest_name": "VESITech",
        "website": "vesit.edu.in/techfest"
    },
    "GCOE Aurangabad": {
        "city": "Aurangabad",
        "category": "Notable",
        "rating": 3.8,
        "popularity": 3.9,
        "techfest_name": "Technotron",
        "website": "gcoea.ac.in/technotron"
    },
    "GHRCE Nagpur": {
        "city": "Nagpur",
        "category": "Notable",
        "rating": 3.9,
        "popularity": 4.0,
        "techfest_name": "GHRCE Techfest",
        "website": "ghrce.raisoni.net/techfest"
    },
    "VIIT Pune": {
        "city": "Pune",
        "category": "Notable",
        "rating": 3.9,
        "popularity": 4.0,
        "techfest_name": "Vishwaraj",
        "website": "viitpune.edu.in/vishwaraj"
    },
    "BVUCOE Pune": {
        "city": "Pune",
        "category": "Notable",
        "rating": 3.9,
        "popularity": 4.0,
        "techfest_name": "Bharati Techfest",
        "website": "bvucoepune.edu.in/techfest"
    },
    
    # Tier 4 - Other Notable
    "TCET Mumbai": {
        "city": "Mumbai",
        "category": "Other Notable",
        "rating": 3.8,
        "popularity": 3.9,
        "techfest_name": "Turbine",
        "website": "tcetmumbai.in/turbine"
    },
    "RSCOE Pune": {
        "city": "Pune",
        "category": "Other Notable",
        "rating": 3.8,
        "popularity": 3.9,
        "techfest_name": "RSCOE Techfest",
        "website": "rscoe.edu.in/techfest"
    },
    "FCRIT Navi Mumbai": {
        "city": "Navi Mumbai",
        "category": "Other Notable",
        "rating": 3.7,
        "popularity": 3.8,
        "techfest_name": "FCRIT Fest",
        "website": "fcrit.ac.in/fest"
    },
    "SFIT Mumbai": {
        "city": "Mumbai",
        "category": "Other Notable",
        "rating": 3.8,
        "popularity": 3.9,
        "techfest_name": "SFIT Techfest",
        "website": "sfit.ac.in/techfest"
    },
    "RAIT Navi Mumbai": {
        "city": "Navi Mumbai",
        "category": "Other Notable",
        "rating": 3.7,
        "popularity": 3.8,
        "techfest_name": "Raitram",
        "website": "rait.edu.in/raitram"
    },
    "Pillai Panvel": {
        "city": "Panvel",
        "category": "Other Notable",
        "rating": 3.7,
        "popularity": 3.8,
        "techfest_name": "Pillai Techfest",
        "website": "pillai.edu.in/techfest"
    },
    "SGGSIE&T Nanded": {
        "city": "Nanded",
        "category": "Other Notable",
        "rating": 3.8,
        "popularity": 3.9,
        "techfest_name": "SGGSTech",
        "website": "sggs.ac.in/techfest"
    },
    "PVGCOET Pune": {
        "city": "Pune",
        "category": "Other Notable",
        "rating": 3.7,
        "popularity": 3.8,
        "techfest_name": "PVG Techfest",
        "website": "pvgcoet.ac.in/techfest"
    }
}

# Event categories and subcategories
EVENT_CATEGORIES = {
    "Robotics": ["Bot Battle", "Line Follower", "Robo Race", "Drone Racing", "Pick and Place Robot"],
    "Coding": ["Hackathon", "Code Debugging", "Algorithm Challenge", "Web Dev Battle", "AI Challenge"],
    "Electronics": ["Circuit Design", "PCB Design", "IoT Workshop", "Embedded Systems", "Project Exhibition"],
    "Mechanical": ["CAD Design", "Go Kart Racing", "Bridge Building", "Aeromodelling", "RC Car Racing"],
    "Civil": ["Structural Design", "Surveying", "Building Design", "Water Management", "Sustainable Design"],
    "Management": ["Case Study", "Business Plan", "Marketing Challenge", "Finance Quiz", "HR Summit"],
    "Design": ["Poster Making", "Logo Design", "3D Modeling", "UI/UX Challenge", "Photography"],
    "Technical Paper": ["Research Paper", "Technical Writing", "Project Presentation", "Innovation Challenge"],
    "Workshop": ["AI/ML Workshop", "Robotics Workshop", "Web Dev Workshop", "IoT Workshop", "Cloud Computing"],
    "Competition": ["Quiz", "Debate", "Group Discussion", "Treasure Hunt", "Model Making"]
}

# Solo vs Team events
EVENT_TYPES = ["Solo", "Team", "Both"]
TEAM_SIZES = {
    "Solo": [1, 1],
    "Team": [2, 5],
    "Both": [1, 5]
}

# Price ranges based on event type
PRICE_RANGES = {
    "Robotics": [200, 1500],
    "Coding": [0, 500],
    "Electronics": [300, 2000],
    "Mechanical": [500, 3000],
    "Civil": [200, 1500],
    "Management": [100, 1000],
    "Design": [0, 500],
    "Technical Paper": [0, 300],
    "Workshop": [500, 3000],
    "Competition": [0, 300]
}

# Prizes based on event category
PRIZES = {
    "Robotics": [5000, 10000, 20000, 50000],
    "Coding": [3000, 5000, 10000, 25000],
    "Electronics": [4000, 8000, 15000, 30000],
    "Mechanical": [5000, 10000, 20000, 50000],
    "Civil": [3000, 6000, 10000, 20000],
    "Management": [2000, 5000, 10000, 20000],
    "Design": [1000, 3000, 5000, 10000],
    "Technical Paper": [1000, 2000, 5000, 10000],
    "Workshop": [0, 0, 0, 0],  # Workshops usually don't have prizes
    "Competition": [2000, 5000, 10000, 20000]
}

def generate_event_description(college_name, college_info, category, subcategory, event_type):
    """Generate rich description for events"""
    templates = [
        f"🎯 {college_name} presents {subcategory} - an exciting {category.lower()} event at {college_info['techfest_name']}! "
        f"Test your skills and compete with the best minds from across Maharashtra.",
        
        f"Join us for {subcategory} at {college_name}'s {college_info['techfest_name']}! "
        f"This {category.lower()} event challenges participants to showcase their expertise in {category.lower()} domain.",
        
        f"🚀 {college_name} invites you to participate in {subcategory} during {college_info['techfest_name']}. "
        f"A perfect platform for {category.lower()} enthusiasts to demonstrate their talents.",
        
        f"💡 {subcategory} at {college_info['techfest_name']} - {college_name}. "
        f"Compete in this {category.lower()} event and win exciting prizes! Open for all engineering students."
    ]
    
    # Add team/solo info
    if event_type == "Solo":
        templates.append(f"🎯 Solo event - Individual participation only. Showcase your personal skills in {category}!")
    elif event_type == "Team":
        templates.append(f"👥 Team event - Form your dream team and compete together!")
    else:
        templates.append(f"🤝 Open for both solo and team participation!")
    
    return random.choice(templates)

def generate_team_details(category, event_type):
    """Generate team requirements"""
    if event_type == "Solo":
        return {"min_team": 1, "max_team": 1, "team_possible": False}
    elif event_type == "Team":
        min_size = random.randint(2, 3)
        max_size = min_size + random.randint(0, 2)
        return {"min_team": min_size, "max_team": max_size, "team_possible": True}
    else:  # Both
        return {"min_team": 1, "max_team": random.randint(2, 4), "team_possible": True}

def generate_events_dataset(num_events=200):
    """Generate comprehensive events dataset"""
    events = []
    event_id = 1
    
    colleges_list = list(COLLEGES.items())
    
    for _ in range(num_events):
        # Select random college
        college_name, college_info = random.choice(colleges_list)
        
        # Select random category and subcategory
        category = random.choice(list(EVENT_CATEGORIES.keys()))
        subcategory = random.choice(EVENT_CATEGORIES[category])
        
        # Event type
        event_type = random.choice(EVENT_TYPES)
        team_details = generate_team_details(category, event_type)
        
        # Price based on category
        price_range = PRICE_RANGES[category]
        price = random.randint(price_range[0], price_range[1])
        
        # Prize money
        prize_pool = random.choice(PRIZES[category])
        
        # Generate dates (within next 6 months)
        start_date = datetime.now() + timedelta(days=random.randint(7, 180))
        duration = random.randint(1, 3)
        end_date = start_date + timedelta(days=duration)
        
        # Rating and popularity (with some variation from college base)
        rating_variation = random.uniform(-0.3, 0.3)
        rating = min(5.0, max(1.0, college_info['rating'] + rating_variation))
        
        popularity_variation = random.uniform(-0.3, 0.3)
        popularity = min(5.0, max(1.0, college_info['popularity'] + popularity_variation))
        
        # Description
        description = generate_event_description(college_name, college_info, category, subcategory, event_type)
        
        # Tags
        tags = [category, subcategory, college_info['category'], college_info['techfest_name']]
        if event_type == "Solo":
            tags.append("solo-event")
        else:
            tags.append("team-event")
        
        event = {
            "event_id": event_id,
            "name": f"{subcategory} @ {college_info['techfest_name']}",
            "college_name": college_name,
            "techfest_name": college_info['techfest_name'],
            "city": college_info['city'],
            "category": category,
            "subcategory": subcategory,
            "event_type": event_type,
            "min_team_size": team_details['min_team'],
            "max_team_size": team_details['max_team'],
            "team_possible": team_details['team_possible'],
            "price": price,
            "prize_pool": prize_pool,
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "duration_days": duration,
            "description": description,
            "tags": ", ".join(tags),
            "rating": round(rating, 1),
            "popularity": round(popularity, 1),
            "college_rating": college_info['rating'],
            "college_category": college_info['category'],
            "registration_link": f"https://{college_info['website']}/events/{event_id}",
            "contact_email": f"events@{college_info['website'].replace('https://', '')}",
            "coordinates": generate_coordinates(college_info['city'])
        }
        
        events.append(event)
        event_id += 1
    
    return pd.DataFrame(events)

def generate_coordinates(city):
    """Generate approximate coordinates for cities"""
    coordinates = {
        "Mumbai": "19.0760° N, 72.8777° E",
        "Pune": "18.5204° N, 73.8567° E",
        "Nagpur": "21.1458° N, 79.0882° E",
        "Navi Mumbai": "19.0330° N, 73.0297° E",
        "Sangli": "16.8637° N, 74.5696° E",
        "Aurangabad": "19.8762° N, 75.3433° E",
        "Nanded": "19.1383° N, 77.3210° E",
        "Panvel": "18.9920° N, 73.1120° E",
        "Solapur": "17.6599° N, 75.9064° E",
        "Kolhapur": "16.7050° N, 74.2433° E",
        "Nashik": "19.9975° N, 73.7898° E",
        "Amravati": "20.9374° N, 77.7796° E"
    }
    return coordinates.get(city, "19.0760° N, 72.8777° E")

def main():
    """Generate and save the dataset"""
    print("Generating events dataset...")
    df = generate_events_dataset(1000)  # Generate 300 events
    
    # Save to CSV
    df.to_csv("data/events.csv", index=False)
    
if __name__ == "__main__":
    main()