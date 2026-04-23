# app.py - Enhanced version with better error handling and logging
from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from explain import get_negative_reasons, explain_prediction, split_explanations, generate_comprehensive_explanation
from model import get_recommendations_with_features, get_event_details
from flask_cors import CORS
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Enhanced CORS configuration
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Load dataset once
try:
    df = pd.read_csv("data/events.csv")
    logger.info(f"✅ Loaded {len(df)} events from dataset")
except Exception as e:
    logger.error(f"❌ Failed to load dataset: {str(e)}")
    df = pd.DataFrame()  # Empty dataframe as fallback

@app.route("/recommend", methods=["POST", "OPTIONS"])
def recommend():
    """Get personalized event recommendations with XAI explanations"""
    
    # Handle preflight OPTIONS request
    if request.method == "OPTIONS":
        return '', 200
    
    try:
        # Get and validate request data
        data = request.json
        logger.info(f"📥 Received request: {data}")
        
        # Extract parameters with defaults
        interest = data.get("interest", "")
        city = data.get("city", "Pune")
        budget = float(data.get("budget", 500))
        event_type = data.get("event_type", "Both")
        
        # Validate inputs
        if not interest:
            return jsonify({"error": "Interest field is required"}), 400
        
        if budget <= 0:
            return jsonify({"error": "Budget must be greater than 0"}), 400
        
        # Get recommendations
        logger.info(f"🔍 Getting recommendations for: interest='{interest}', city='{city}', budget={budget}, type='{event_type}'")
        
        results, model, feature_df = get_recommendations_with_features(
            df,
            interest,
            city,
            budget,
            event_type
        )
        
        # Check if we got any results
        if results.empty:
            logger.warning("No recommendations found")
            return jsonify({
                "message": "No events found matching your criteria",
                "recommendations": [],
                "user_preferences": {
                    "interest": interest,
                    "city": city,
                    "budget": budget,
                    "event_type": event_type
                }
            }), 200
        
        # Get explanations for top recommendations
        top_n = min(5, len(results))  # Get up to 5 recommendations
        explanations = explain_prediction(model, feature_df.head(top_n))
        
        final_output = []
        
        for i, (_, row) in enumerate(results.head(top_n).iterrows()):
            # Get explanations for this event
            if i < len(explanations):
                pos, neg = split_explanations(explanations[i])
            else:
                pos, neg = ["✓ Matches your interests"], ["⚠️ No detailed explanation available"]
            
            # Calculate match score (normalize to percentage)
            raw_score = float(row.get("score", 0))
            # Normalize score to 0-100 range (assuming scores are typically 0-1.5)
            normalized_score = min(100, max(0, (raw_score / 1.5) * 100))
            
            # Get team size info if available
            team_info = ""
            if pd.notna(row.get("min_team_size", 0)) and row.get("max_team_size", 0) > 0:
                if row.get("event_type") == "Solo":
                    team_info = "Solo Event"
                elif row.get("event_type") == "Team":
                    team_info = f"Team Event ({int(row['min_team_size'])}-{int(row['max_team_size'])} members)"
                else:
                    team_info = f"Open for {int(row['min_team_size'])}-{int(row['max_team_size'])} participants"
            
            # Get prize info if available
            prize_info = ""
            if pd.notna(row.get("prize_pool", 0)) and row.get("prize_pool", 0) > 0:
                prize_info = f"🏆 Prize Pool: ₹{int(row['prize_pool']):,}"
            
            # Build event object
            event_obj = {
                "id": int(row.get("event_id", i)),
                "event": row.get("name", "Unnamed Event"),
                "college": row.get("college_name", "Unknown College"),
                "techfest": row.get("techfest_name", ""),
                "score": round(normalized_score, 1),
                "description": row.get("description", "No description available"),
                "category": row.get("category", "General"),
                "subcategory": row.get("subcategory", ""),
                "city": row.get("city", "Unknown"),
                "price": int(row.get("price", 0)),
                "rating": float(row.get("rating", 0)),
                "popularity": float(row.get("popularity", 0)),
                "event_type": row.get("event_type", "Both"),
                "team_info": team_info,
                "prize_info": prize_info,
                "start_date": row.get("start_date", ""),
                "explanation": pos[:3] if pos else ["✓ Good match for your preferences"],  # Top 3 positive reasons
                "why_not": neg[:2] if neg else [],  # Top 2 negative reasons
                "registration_link": row.get("registration_link", "#")
            }
            
            final_output.append(event_obj)
        
        # Add metadata to response
        response = {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "user_preferences": {
                "interest": interest,
                "city": city,
                "budget": budget,
                "event_type": event_type
            },
            "total_found": len(final_output),
            "recommendations": final_output
        }
        
        logger.info(f"✅ Successfully returned {len(final_output)} recommendations")
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"❌ Error in recommend endpoint: {str(e)}", exc_info=True)
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "An error occurred while getting recommendations"
        }), 500

@app.route("/event/<int:event_id>", methods=["GET"])
def get_event(event_id):
    """Get detailed information about a specific event"""
    try:
        event_details = get_event_details(event_id)
        if event_details:
            return jsonify({
                "success": True,
                "event": event_details
            }), 200
        else:
            return jsonify({
                "success": False,
                "error": "Event not found"
            }), 404
    except Exception as e:
        logger.error(f"Error fetching event {event_id}: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "events_loaded": len(df),
        "model_ready": True
    }), 200

@app.route("/feedback", methods=["POST"])
def feedback():
    """Collect user feedback for recommendations"""
    try:
        data = request.json
        feedback_data = {
            "timestamp": datetime.now().isoformat(),
            "event_id": data.get("event_id"),
            "feedback": data.get("feedback"),  # "helpful" or "not_helpful"
            "user_preferences": data.get("preferences", {})
        }
        
        # Save feedback to file (can be replaced with database)
        import os
        feedback_file = "feedback_log.csv"
        
        if not os.path.exists(feedback_file):
            pd.DataFrame([feedback_data]).to_csv(feedback_file, index=False)
        else:
            df_feedback = pd.read_csv(feedback_file)
            df_feedback = pd.concat([df_feedback, pd.DataFrame([feedback_data])], ignore_index=True)
            df_feedback.to_csv(feedback_file, index=False)
        
        logger.info(f"📝 Feedback recorded for event {data.get('event_id')}")
        
        return jsonify({
            "success": True,
            "message": "Thank you for your feedback!"
        }), 200
    except Exception as e:
        logger.error(f"Error saving feedback: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == "__main__":
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000)