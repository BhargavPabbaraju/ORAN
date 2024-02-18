from app import flask_app
# from testApp import app

def run_flask():
    flask_app.run(port=5000, host="localhost", debug=True)

# def run_test_flask():
#     app.run(port=5000, host="localhost", debug=True)

if __name__ == "__main__":
    # Running flask app instance on port 5000
    run_flask()
    # run_test_flask()

