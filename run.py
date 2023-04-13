from Application import create_app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host='172.24.1.1', port='5000')