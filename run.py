import os
from Application import create_app
from Application.config import Config


app = create_app()

if __name__ == "__main__":
    if not os.path.exists(Config.UPLOAD_FOLDER):
        os.makedirs(Config.UPLOAD_FOLDER)
    app.run(debug=True, host='172.24.1.1', port='5000')