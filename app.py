import os
from flask import Flask
from datetime import timedelta
from flask_migrate import Migrate
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from dotenv import load_dotenv
import cloudinary

from models.baseModel import db
from resources.loginResource import LoginResource
from resources.signupResource import SignupResource
from resources.recordResource import RecordResource
from resources.adminResource import AdminResource

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
api = Api(app)

# Configure JWT
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)

jwt = JWTManager(app)


# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

# Configure DB
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)


# Initialize other extensions
bcrypt = Bcrypt(app)
CORS(app, resources={r"/*": {"origins": "*"}})

# Auth routes
api.add_resource(SignupResource, "/signup")
api.add_resource(LoginResource, "/login","/profile")

# User routes
api.add_resource(RecordResource, "/records", "/records/<int:record_id>")


# Admin routes
api.add_resource(AdminResource, "/admin/records", "/admin/records/<int:record_id>")# Run the server
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5555)) 
    app.run(host="0.0.0.0", port=port, debug=True)
