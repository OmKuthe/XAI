# model.py - Updated for enhanced dataset
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime

df = pd.read_csv("data/events.csv")

# Ensure all numeric columns are properly formatted
numeric_columns = ['price', 'rating', 'popularity', 'prize_pool', 'min_team_size', 'max_team_size']
for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

# Ensure price is numeric when loading data
df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(0)

# Create enhanced combined text for better recommendations
df['combined'] = (
    df['category'] + " " + 
    df['subcategory'].fillna('') + " " + 
    df['description'].fillna('') + " " +
    df['tags'].fillna('') + " " +
    df['college_name'].fillna('') + " " +
    df['techfest_name'].fillna('')
)

vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
tfidf_matrix = vectorizer.fit_transform(df['combined'])

def get_recommendations(user_interest):
    """Simple recommendation based on text similarity"""
    user_vec = vectorizer.transform([user_interest])
    similarity = cosine_similarity(user_vec, tfidf_matrix)[0]

    df['score'] = similarity
    return df.sort_values(by='score', ascending=False).head(3)

def create_feature_vector(event, user_interest, user_city, budget, preferred_type):
    """Create comprehensive feature vector with all event attributes"""
    features = {}
    
    # Convert budget to numeric
    try:
        budget_value = float(budget)
    except (ValueError, TypeError):
        budget_value = float('inf')
    
    # Ensure event price is numeric
    price_value = float(event['price']) if pd.notna(event['price']) else 0

    # Enhanced text data for interest matching
    text_data = f"{event.get('category', '')} {event.get('subcategory', '')} {event.get('description', '')} {event.get('college_name', '')}".lower()
    user_words = user_interest.lower().split()

    # 🔹 Interest match (improved with partial matching)
    interest_matches = sum(1 for word in user_words if word in text_data)
    features["interest_match"] = min(1.0, interest_matches / max(1, len(user_words)))

    # 🔹 Location match
    features["location_match"] = 1 if str(event["city"]).lower() == str(user_city).lower() else 0

    # 🔹 Price score (relative to user budget)
    if price_value == 0:
        features["price_score"] = 1.0
    elif price_value <= budget_value:
        features["price_score"] = 1 - (price_value / budget_value)
    else:
        features["price_score"] = max(-1.0, - (price_value - budget_value) / budget_value)

    # 🔹 Popularity score
    popularity_value = float(event["popularity"]) if pd.notna(event["popularity"]) else 0
    features["popularity_score"] = popularity_value / 5 if popularity_value > 0 else 0

    # 🔹 Rating score
    rating_value = float(event["rating"]) if pd.notna(event["rating"]) else 0
    features["rating_score"] = rating_value / 5 if rating_value > 0 else 0

    # 🔹 Event type match (Solo/Team/Both)
    event_type = str(event["event_type"]).lower() if pd.notna(event["event_type"]) else ""
    preferred_type_str = str(preferred_type).lower() if preferred_type else ""
    features["event_type_match"] = 1 if event_type == preferred_type_str else 0
    
    # 🔹 Prize pool score (bonus for events with good prizes)
    prize_value = float(event["prize_pool"]) if pd.notna(event["prize_pool"]) else 0
    features["prize_score"] = min(1.0, prize_value / 50000)  # Normalize up to 50k prize
    
    # 🔹 College reputation score
    college_category = str(event.get("college_category", "")).lower()
    if "premier" in college_category:
        features["college_reputation"] = 1.0
    elif "highly reputed" in college_category:
        features["college_reputation"] = 0.8
    elif "notable" in college_category:
        features["college_reputation"] = 0.6
    else:
        features["college_reputation"] = 0.4
    
    # 🔹 Date proximity score (events sooner get higher score)
    try:
        start_date = pd.to_datetime(event["start_date"])
        days_until = (start_date - datetime.now()).days
        if days_until < 0:
            features["date_score"] = 0  # Past event
        elif days_until <= 7:
            features["date_score"] = 1.0  # This week
        elif days_until <= 30:
            features["date_score"] = 0.8  # This month
        elif days_until <= 90:
            features["date_score"] = 0.5  # Within 3 months
        else:
            features["date_score"] = 0.3  # Later
    except:
        features["date_score"] = 0.5  # Default if date not available

    return features

def build_feature_dataset(df, user_interest, user_city, budget, preferred_type):
    """Build feature dataset for all events"""
    feature_list = []

    for _, row in df.iterrows():
        features = create_feature_vector(
            row,
            user_interest,
            user_city,
            budget,
            preferred_type
        )
        features["event_id"] = row["event_id"]
        feature_list.append(features)

    return pd.DataFrame(feature_list)

def train_model(X):
    """Train Random Forest model with improved feature weights"""
    # Enhanced target weighting based on multiple factors
    y = (
        0.30 * X["interest_match"] +
        0.20 * X["location_match"] +
        0.15 * X["price_score"] +
        0.10 * X["rating_score"] +
        0.10 * X["popularity_score"] +
        0.05 * X["event_type_match"] +
        0.05 * X["prize_score"] +
        0.03 * X["college_reputation"] +
        0.02 * X["date_score"]
    )
    
    # Handle any NaN values
    X = X.fillna(0)
    y = y.fillna(0)

    model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10)
    model.fit(X, y)

    return model

def get_recommendations_with_features(df, user_interest, user_city, budget, preferred_type):
    """Get top recommendations with feature-based scoring"""
    feature_df = build_feature_dataset(df, user_interest, user_city, budget, preferred_type)
    
    # Drop event_id and handle any NaN values
    feature_cols = [col for col in feature_df.columns if col != 'event_id']
    X = feature_df[feature_cols].fillna(0)
    
    model = train_model(X)

    scores = model.predict(X)
    feature_df["score"] = scores

    result = df.merge(feature_df, on="event_id")
    
    # Sort by score and return top 5 recommendations
    top_results = result.sort_values(by="score", ascending=False).head(5)
    
    # Add explanation column for XAI
    top_results['explanations'] = top_results.apply(
        lambda row: generate_explanation(row, user_interest, user_city, budget), 
        axis=1
    )

    return top_results, model, feature_df

def generate_explanation(event, user_interest, user_city, budget):
    """Generate human-readable explanation for recommendation"""
    explanations = []
    
    # Interest match
    if event.get('interest_match', 0) > 0.5:
        explanations.append(f"🎯 Strongly matches your interest in {user_interest}")
    elif event.get('interest_match', 0) > 0:
        explanations.append(f"📌 Somewhat related to {user_interest}")
    
    # Location
    if event.get('location_match', 0) == 1:
        explanations.append(f"📍 Takes place in {user_city} (your city)")
    else:
        explanations.append(f"🗺️ Located in {event['city']}")
    
    # Price
    if event['price'] == 0:
        explanations.append(f"💰 Free event!")
    elif event['price'] <= budget:
        explanations.append(f"💵 Within your ₹{budget} budget (₹{event['price']})")
    else:
        explanations.append(f"💸 Costs ₹{event['price']}")
    
    # Rating
    if event['rating'] >= 4.5:
        explanations.append(f"⭐ Exceptional rating ({event['rating']}/5)")
    elif event['rating'] >= 4:
        explanations.append(f"⭐ Great rating ({event['rating']}/5)")
    
    # Prize pool
    if event.get('prize_pool', 0) > 10000:
        explanations.append(f"🏆 Prize pool of ₹{event['prize_pool']:,}")
    
    # College reputation
    if event.get('college_reputation', 0) >= 0.8:
        explanations.append(f"🏛️ Prestigious {event['college_name']}")
    
    # Team info
    if event['event_type'] == 'Team':
        explanations.append(f"👥 Team event ({event['min_team_size']}-{event['max_team_size']} members)")
    elif event['event_type'] == 'Solo':
        explanations.append(f"🎯 Solo event")
    
    return explanations[:4]  # Return top 4 explanations

# Additional utility function for getting event details
def get_event_details(event_id):
    """Get detailed information about a specific event"""
    event = df[df['event_id'] == event_id].iloc[0]
    return {
        'name': event['name'],
        'college': event['college_name'],
        'city': event['city'],
        'date': event['start_date'],
        'registration_link': event.get('registration_link', '#'),
        'description': event['description']
    }

# Function to get similar events
def get_similar_events(event_id, top_n=3):
    """Get events similar to a given event"""
    event_idx = df[df['event_id'] == event_id].index[0]
    event_vector = tfidf_matrix[event_idx]
    similarities = cosine_similarity(event_vector, tfidf_matrix)[0]
    similar_indices = similarities.argsort()[-top_n-1:-1][::-1]
    
    similar_events = df.iloc[similar_indices][['event_id', 'name', 'college_name', 'city']]
    return similar_events