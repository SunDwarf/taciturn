from app import app

if __name__ == '__main__':
    app.run(app.config["DEBUG_HOST"], port=app.config["DEBUG_PORT"], debug=True)
