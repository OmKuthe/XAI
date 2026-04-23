# explain.py - Enhanced for better XAI explanations
import shap
import pandas as pd
import numpy as np

def explain_prediction(model, feature_df):
    """
    Generate SHAP explanations for model predictions
    
    Args:
        model: Trained RandomForest model
        feature_df: DataFrame containing features (without event_id and score)
    
    Returns:
        List of explanation dictionaries for each prediction
    """
    # Prepare features (drop non-feature columns if they exist)
    feature_cols = [col for col in feature_df.columns if col not in ['event_id', 'score']]
    X = feature_df[feature_cols].fillna(0)
    
    # Create SHAP explainer
    try:
        # For tree-based models like RandomForest
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(X)
        
        # Handle different return types
        if isinstance(shap_values, list):
            shap_values = shap_values[1] if len(shap_values) > 1 else shap_values[0]
        
    except Exception as e:
        print(f"SHAP explanation error: {e}")
        # Fallback to simpler explanation method
        return fallback_explanations(model, X)
    
    explanations = []
    for i in range(len(X)):
        feature_impacts = dict(zip(feature_cols, shap_values[i]))
        explanations.append(feature_impacts)
    
    return explanations

def fallback_explanations(model, X):
    """
    Fallback method using feature importance when SHAP fails
    """
    # Get global feature importances
    feature_importances = dict(zip(X.columns, model.feature_importances_))
    
    # For each sample, use global importance as proxy
    explanations = []
    for i in range(len(X)):
        # Calculate local importance based on feature values
        local_importance = {}
        for col in X.columns:
            feature_value = X.iloc[i][col]
            global_importance = feature_importances[col]
            # Combine global importance with feature value
            local_importance[col] = global_importance * feature_value
        
        explanations.append(local_importance)
    
    return explanations

def split_explanations(explanation_dict):
    """
    Split explanations into positive and negative factors
    
    Args:
        explanation_dict: Dictionary of feature impacts
    
    Returns:
        Tuple of (positive_factors, negative_factors)
    """
    positives = []
    negatives = []

    # Enhanced feature mapping with better descriptions
    feature_map_positive = {
        "interest_match": "🎯 Matches your interests",
        "location_match": "📍 Near your location",
        "price_score": "💰 Budget friendly",
        "popularity_score": "🔥 Popular event",
        "rating_score": "⭐ Highly rated",
        "event_type_match": "👥 Matches your preferred type",
        "prize_score": "🏆 Attractive prize pool",
        "college_reputation": "🏛️ Prestigious college",
        "date_score": "📅 Happening soon"
    }

    feature_map_negative = {
        "location_match": "📍 Far from your location",
        "price_score": "💸 Too expensive",
        "popularity_score": "📊 Less popular",
        "rating_score": "⭐ Lower rating",
        "event_type_match": "👥 Not preferred type",
        "prize_score": "🏆 Small prize pool",
        "college_reputation": "🏛️ Lower college reputation",
        "date_score": "📅 Event far in future"
    }

    # Sort features by impact magnitude
    sorted_features = sorted(explanation_dict.items(), key=lambda x: abs(x[1]), reverse=True)
    
    for feature, value in sorted_features:
        if feature in ["event_id", "score"]:
            continue

        # Convert to percentage
        percent = round(value * 100)

        # Skip negligible impacts
        if abs(percent) < 2:
            continue

        if percent > 0:
            label = feature_map_positive.get(feature, f"✓ {feature.replace('_', ' ').title()}")
            positives.append(f"{label} (+{percent}%)")
        else:
            label = feature_map_negative.get(feature, f"✗ {feature.replace('_', ' ').title()}")
            negatives.append(f"{label} ({percent}%)")

    return positives[:3], negatives[:2]  # Return top 3 positive and top 2 negative

def get_negative_reasons(explanation_dict):
    """
    Extract only negative reasons for recommendation
    
    Args:
        explanation_dict: Dictionary of feature impacts
    
    Returns:
        List of negative reasons
    """
    negatives = []

    feature_map = {
        "location_match": "📍 Far from your location",
        "price_score": "💸 Too expensive for your budget",
        "popularity_score": "📊 Lower popularity among users",
        "rating_score": "⭐ Lower than average rating",
        "event_type_match": "👥 Different from preferred type",
        "prize_score": "🏆 Small prize pool",
        "college_reputation": "🏛️ Lower college reputation",
        "date_score": "📅 Event scheduled far in future"
    }

    # Sort by most negative impact
    sorted_items = sorted(explanation_dict.items(), key=lambda x: x[1])

    for feature, value in sorted_items:
        if value < -0.05:  # Lower threshold for negative impact
            label = feature_map.get(feature, f"✗ {feature.replace('_', ' ').title()}")
            percentage = round(value * 100)
            negatives.append(f"{label} ({percentage}%)")

        if len(negatives) == 3:  # Get up to 3 negative reasons
            break

    return negatives

def get_positive_reasons(explanation_dict):
    """
    Extract only positive reasons for recommendation
    
    Args:
        explanation_dict: Dictionary of feature impacts
    
    Returns:
        List of positive reasons
    """
    positives = []

    feature_map = {
        "interest_match": "🎯 Strongly matches your interests",
        "location_match": "📍 Conveniently located",
        "price_score": "💰 Excellent value for money",
        "popularity_score": "🔥 Popular among peers",
        "rating_score": "⭐ Highly rated by attendees",
        "event_type_match": "👥 Perfect for your preference",
        "prize_score": "🏆 Generous prize pool",
        "college_reputation": "🏛️ Prestigious institution",
        "date_score": "📅 Perfect timing"
    }

    # Sort by most positive impact
    sorted_items = sorted(explanation_dict.items(), key=lambda x: x[1], reverse=True)

    for feature, value in sorted_items:
        if value > 0.05:  # Threshold for positive impact
            label = feature_map.get(feature, f"✓ {feature.replace('_', ' ').title()}")
            percentage = round(value * 100)
            positives.append(f"{label} (+{percentage}%)")

        if len(positives) == 3:  # Get up to 3 positive reasons
            break

    return positives

def generate_comprehensive_explanation(event_data, model, feature_df, index):
    """
    Generate a comprehensive explanation for a single recommendation
    
    Args:
        event_data: The event data row
        model: Trained model
        feature_df: Feature DataFrame
        index: Index of the event in feature_df
    
    Returns:
        Dictionary with comprehensive explanation
    """
    # Get SHAP explanations
    explanations = explain_prediction(model, feature_df)
    
    if index < len(explanations):
        explanation_dict = explanations[index]
        
        # Split into positive and negative
        positives, negatives = split_explanations(explanation_dict)
        
        # Get detailed reasons
        positive_reasons = get_positive_reasons(explanation_dict)
        negative_reasons = get_negative_reasons(explanation_dict)
        
        # Calculate overall confidence
        total_impact = sum(abs(v) for v in explanation_dict.values())
        confidence = min(100, max(0, total_impact * 100))
        
        return {
            'confidence_score': round(confidence, 1),
            'positive_factors': positive_reasons or positives,
            'negative_factors': negative_reasons or negatives,
            'all_impacts': {k: round(v * 100, 1) for k, v in explanation_dict.items() if abs(v) > 0.02}
        }
    
    return {
        'confidence_score': 50,
        'positive_factors': ['Matches your interests', 'Good value'],
        'negative_factors': [],
        'all_impacts': {}
    }

def compare_recommendations(rec1_impacts, rec2_impacts):
    """
    Compare two recommendations to explain why one is better
    
    Args:
        rec1_impacts: Impact dictionary for recommendation 1
        rec2_impacts: Impact dictionary for recommendation 2
    
    Returns:
        Comparison explanation string
    """
    diff = {}
    for feature in set(rec1_impacts.keys()) | set(rec2_impacts.keys()):
        val1 = rec1_impacts.get(feature, 0)
        val2 = rec2_impacts.get(feature, 0)
        diff[feature] = val1 - val2
    
    # Find features where first recommendation is significantly better
    better_features = [f for f, d in diff.items() if d > 0.1]
    
    if better_features:
        feature_names = [f.replace('_', ' ').title() for f in better_features[:2]]
        return f"Better match due to: {', '.join(feature_names)}"
    else:
        return "Similar overall match quality"

# Utility function to explain why an event was NOT recommended
def explain_exclusion(event, user_preferences):
    """
    Explain why a specific event was not recommended
    
    Args:
        event: Event data
        user_preferences: Dictionary with user preferences
    
    Returns:
        List of reasons for exclusion
    """
    reasons = []
    
    # Check location
    if event['city'].lower() != user_preferences.get('city', '').lower():
        reasons.append(f"📍 Location mismatch: Event in {event['city']}, you prefer {user_preferences.get('city', 'unknown')}")
    
    # Check budget
    if event['price'] > user_preferences.get('budget', float('inf')):
        reasons.append(f"💰 Budget exceeded: Event costs ₹{event['price']}, your budget is ₹{user_preferences.get('budget', 0)}")
    
    # Check event type
    if event['event_type'].lower() != user_preferences.get('type', '').lower():
        reasons.append(f"👥 Event type mismatch: {event['event_type']} vs preferred {user_preferences.get('type', 'unknown')}")
    
    # Check rating threshold
    if event['rating'] < 3:
        reasons.append(f"⭐ Low rating: {event['rating']}/5 stars")
    
    return reasons