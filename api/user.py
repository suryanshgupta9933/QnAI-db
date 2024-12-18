# Importing Dependencies
import uuid
import logging
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, status

from db.user import create_user, get_user

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create API Router
router = APIRouter()

# Create User Model
class CreateUser(BaseModel):
    org_id: str
    dept_id: str
    name: str
    email: str
    role: str
    profile_picture_url: str = None

# Create User
@router.post("/user/create", status_code=status.HTTP_201_CREATED)
def create_user_endpoint(user: CreateUser):
    try:
        user_id = str(uuid.uuid4())
        create_user(user.org_id, user.dept_id, user_id, user.name, user.email, user.role)
        return {
            "org_id": user.org_id,
            "user_id": user_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to create user. {e}")

# Get User
@router.get("/user", status_code=status.HTTP_200_OK)
def get_user_endpoint(org_id: str, user_id: str):
    user = get_user(org_id, user_id)
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found in Organization {org_id}.")