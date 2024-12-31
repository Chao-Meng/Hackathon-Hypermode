
from flask import Flask, request, jsonify
from neo4j import GraphDatabase

app = Flask(__name__)

# 配置 Neo4j
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "mypassword"))

@app.route('/')
def home():
    return "Welcome to the Travel Recommendation API!"

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        # 检查请求是否为 JSON
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 415

        # 获取用户的偏好
        data = request.get_json()
        user_preferences = data.get("user_preferences", [])
        if not user_preferences:
            return jsonify({"error": "user_preferences is required"}), 400

        # 查询 Neo4j 知识图谱
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

        # 如果没有找到匹配的结果
        if not results:
            return jsonify({"error": "No matching destinations found"}), 404

        # 模拟 GPT-4 的推荐生成部分
        recommendations = f"Based on your preferences {user_preferences}, we recommend visiting: "
        for result in results:
            recommendations += f"{result['city']} for its {result['attraction']} ({', '.join(result['tags'])}). "

        return jsonify({
            "user_preferences": user_preferences,
            "knowledge_graph_results": results,
            "ai_recommendations": recommendations
        }), 200

    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": f"Internal server error: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
