from flask import Flask
from routes.products import products_bp

app = Flask(__name__)

# Register product routes
app.register_blueprint(products_bp, url_prefix="/products")


@app.route("/")
def home():
    return "Welcome to Store Pilot!"


if __name__ == "__main__":
    app.run(debug=True)