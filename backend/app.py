from flask import Flask, request, jsonify
from neo4j import GraphDatabase
import openai

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 示例数据
tourism_data = [
    {"destination": "Kyoto, Japan", "tags": ["nature scenery", "culture"]},
    {"destination": "Paris, France", "tags": ["food", "culture"]},
    {"destination": "Banff, Canada", "tags": ["nature scenery", "outdoor"]},
    {"destination": "Bangkok, Thailand", "tags": ["food", "nightlife"]},
    {"destination": "Sydney, Australia", "tags": ["beaches", "outdoor"]},
    {"destination": "Cairo, Egypt", "tags": ["history", "culture"]},
    {"destination": "New York, USA", "tags": ["city life", "food", "culture"]},
    {"destination": "Cape Town, South Africa", "tags": ["nature scenery", "adventure"]}
]


@app.route('/')
def home():
    return "Welcome to the Travel Recommendation API!"

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

# @app.route('/recommend', methods=['POST'])
# def recommend():
#     try:
#         if not request.is_json:
#             return jsonify({"error": "Request must be JSON"}), 415
#
#         data = request.get_json()
#         user_preferences = data.get("user_preferences")
#         if not user_preferences:
#             return jsonify({"error": "user_preferences is required"}), 400
#
#         # 示例推荐逻辑
#         recommendations = [
#             {"destination": "Japan", "reason": "Rich in culture and nature."},
#             {"destination": "France", "reason": "Known for its cuisine and romance."}
#         ]
#
#         return jsonify({
#             "user_preferences": user_preferences,
#             "recommendations": recommendations
#         }), 200
#
#     except Exception as e:
#         print(f"Error occurred: {e}")
#         return jsonify({"error": "Internal server error"}), 500
#
# # if __name__ == '__main__':
# #     app.run(debug=True)
# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5001)


@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 415

        data = request.get_json()
        user_preferences = data.get("user_preferences")
        if not user_preferences:
            return jsonify({"error": "user_preferences is required"}), 400

        # 动态推荐逻辑
        user_preferences = [pref.strip().lower() for pref in user_preferences.split(",")]
        recommendations = []

        for destination in tourism_data:
            matching_tags = [tag for tag in destination["tags"] if tag in user_preferences]
            if matching_tags:
                recommendations.append({
                    "destination": destination["destination"],
                    "reason": f"Matched your preference for: {', '.join(matching_tags)}"
                })

        # 如果没有匹配到结果
        if not recommendations:
            recommendations = [{
                "destination": "Unknown",
                "reason": "No matching destinations found for your preferences."
            }]

        return jsonify({
            "user_preferences": user_preferences,
            "recommendations": recommendations
        }), 200

    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)