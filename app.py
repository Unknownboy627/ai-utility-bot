from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Fake database (temporary)
enabled_plugins = set()
USER_IS_PREMIUM = False  # change to True to unlock premium

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/api/enable-plugin", methods=["POST"])
def enable_plugin():
    plugin = request.json.get("plugin")
    enabled_plugins.add(plugin)
    return jsonify({"success": True})

@app.route("/api/enable-premium", methods=["POST"])
def enable_premium():
    if not USER_IS_PREMIUM:
        return jsonify({"premium": False})
    return jsonify({"premium": True})

@app.route("/api/status")
def status():
    return jsonify(list(enabled_plugins))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
