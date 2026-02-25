from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
import crud, models, schemas, auth
from database import get_db

router = APIRouter(
    tags=["users"]
)

@router.post("/register", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        print(f"Registration attempt for username: {user.username}, email: {user.email}", flush=True)
        db_user = crud.get_user(db, username=user.username)
        if db_user:
            raise HTTPException(status_code=400, detail="Username already registered")
        created_user = crud.create_user(db=db, user=user)
        print(f"User created successfully: {created_user.username}", flush=True)
        return created_user
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error during registration: {str(e)}", flush=True)
        raise HTTPException(status_code=500, detail=f"Registration error: {str(e)}")

@router.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    print(f"Login attempt for username: {form_data.username}", flush=True)
    user = crud.get_user(db, username=form_data.username)
    if not user:
        print("User not found", flush=True)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not auth.verify_password(form_data.password, user.hashed_password):
        print("Password verification failed", flush=True)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=schemas.User)
def read_users_me(current_user: models.User = Depends(auth.get_current_active_user)):
    return current_user
@router.post("/admin/create-admin", response_model=schemas.User)
def create_admin(
    admin_data: schemas.UserCreate,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new admin user. Only accessible to existing admins."""
    
    # Check if current user is admin
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can create new admin accounts"
        )
    
    # Check if username already exists
    db_user = crud.get_user(db, username=admin_data.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # Force role to admin
    admin_data.role = "admin"
    
    # Create the admin user
    try:
        new_admin = crud.create_user(db=db, user=admin_data)
        print(f"New admin created: {new_admin.username} by {current_user.username}", flush=True)
        return new_admin
    except Exception as e:
        print(f"Error creating admin: {str(e)}", flush=True)
        raise HTTPException(status_code=500, detail=f"Error creating admin: {str(e)}")