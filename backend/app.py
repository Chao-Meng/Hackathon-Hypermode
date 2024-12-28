from flask import Flask, request, jsonify
from neo4j import GraphDatabase
import openai

from flask import Flask, request, jsonify
from neo4j import GraphDatabase

app = Flask(__name__)

# 配置 Neo4j 数据库连接
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "mypassword"))
@app.route('/')
def home():
    return "Welcome to the Travel Recommendation API!"

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 415

        data = request.get_json()
        user_preferences = data.get("user_preferences", [])
        if not user_preferences:
            return jsonify({"error": "user_preferences is required"}), 400

        # 在 Neo4j 中查询数据
        query = """
        MATCH (c:City)-[:HAS_ATTRACTION]->(a:Attraction)
        WHERE ANY(tag IN $preferences WHERE tag IN a.tags)
        RETURN c.name AS city, a.name AS attraction, a.tags AS tags
        """
        results = []
        with driver.session() as session:
            query_results = session.run(query, preferences=user_preferences)
            for record in query_results:
                results.append({
                    "city": record["city"],
                    "attraction": record["attraction"],
                    "tags": record["tags"]
                })

        if not results:
            results = [{"city": "Unknown", "attraction": "Unknown", "tags": []}]

        return jsonify({"user_preferences": user_preferences, "recommendations": results}), 200

    except Exception as e:
        print(f"Error occurred: {e}")  # new 输出异常信息
        return jsonify({"error": f"Internal server error: {e}"}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)



#hard code for recommend
# from flask import Flask, request, jsonify
# from flask_cors import CORS
#
# app = Flask(__name__)
# CORS(app)  # 允许跨域请求
#
# # 示例数据
# tourism_data = [
#     {"destination": "Kyoto, Japan", "tags": ["nature scenery", "culture"]},
#     {"destination": "Paris, France", "tags": ["food", "culture"]},
#     {"destination": "Banff, Canada", "tags": ["nature scenery", "outdoor"]},
#     {"destination": "Bangkok, Thailand", "tags": ["food", "nightlife"]},
#     {"destination": "Sydney, Australia", "tags": ["beaches", "outdoor"]},
#     {"destination": "Cairo, Egypt", "tags": ["history", "culture"]},
#     {"destination": "New York, USA", "tags": ["city life", "food", "culture"]},
#     {"destination": "Cape Town, South Africa", "tags": ["nature scenery", "adventure"]}
# ]
#
#
# @app.route('/')
# def home():
#     return "Welcome to the Travel Recommendation API!"
#
# @app.route('/health', methods=['GET'])
# def health():
#     return jsonify({"status": "healthy"}), 200
#
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
#         # 动态推荐逻辑
#         user_preferences = [pref.strip().lower() for pref in user_preferences.split(",")]
#         recommendations = []
#
#         for destination in tourism_data:
#             matching_tags = [tag for tag in destination["tags"] if tag in user_preferences]
#             if matching_tags:
#                 recommendations.append({
#                     "destination": destination["destination"],
#                     "reason": f"Matched your preference for: {', '.join(matching_tags)}"
#                 })
#
#         # 如果没有匹配到结果
#         if not recommendations:
#             recommendations = [{
#                 "destination": "Unknown",
#                 "reason": "No matching destinations found for your preferences."
#             }]
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
# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5001)