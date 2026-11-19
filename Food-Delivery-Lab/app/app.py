import json
import os

import mysql.connector
import redis
from flask import Flask, jsonify

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "mysql"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "fooduser"),
        password=os.getenv("DB_PASSWORD", "foodpass123"),
        database=os.getenv("DB_NAME", "food_delivery"),
        connection_timeout=5,
    )

def get_redis():
    return redis.Redis(
        host=os.getenv("REDIS_HOST", "redis"),
        port=int(os.getenv("REDIS_PORT", "6379")),
        decode_responses=True,
        socket_connect_timeout=3,
    )

@app.route("/")
def home():
    return jsonify({
        "service": "Food Delivery Order API",
        "status": "running"
    })

@app.route("/health")
def health():
    results = {}

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        results["mysql"] = cursor.fetchone()[0] == 1
        cursor.close()
        conn.close()
    except Exception as exc:
        results["mysql"] = False
        results["mysql_error"] = str(exc)

    try:
        client = get_redis()
        client.set("connectivity_test", "ok", ex=60)
        results["redis"] = client.get("connectivity_test") == "ok"
    except Exception as exc:
        results["redis"] = False
        results["redis_error"] = str(exc)

    status_code = 200 if results.get("mysql") and results.get("redis") else 503
    return jsonify(results), status_code

@app.route("/orders/<int:order_id>")
def get_order(order_id):
    cache = get_redis()
    cache_key = f"order:{order_id}"

    try:
        cached = cache.get(cache_key)
        if cached:
            return jsonify({
                "source": "redis",
                "order": json.loads(cached)
            })
    except redis.RedisError:
        app.logger.exception("Redis lookup failed")

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT order_id, customer, item, status "
            "FROM orders WHERE order_id = %s",
            (order_id,)
        )
        order = cursor.fetchone()
        cursor.close()
        conn.close()
    except mysql.connector.Error:
        app.logger.exception("MySQL query failed")
        return jsonify({"error": "Database unavailable"}), 503

    if order is None:
        return jsonify({"error": "Order not found"}), 404

    try:
        cache.setex(cache_key, 60, json.dumps(order))
        source = "mysql"
    except redis.RedisError:
        app.logger.exception("Redis cache write failed")
        source = "mysql"

    return jsonify({"source": source, "order": order})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
