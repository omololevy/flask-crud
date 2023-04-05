from app import app
from views import employees

app.register_blueprint(employees)

# starting the app
if __name__ == "__main__":
    app.run(port=5000, debug=True)