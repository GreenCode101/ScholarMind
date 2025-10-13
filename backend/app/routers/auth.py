from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse
from schemas.user_schema import UserCreate, UserLogin
from firebase_admin import auth
from core.firebase_init import firebase
from fastapi.requests import Request

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", 
             status_code=status.HTTP_200_OK, 
             tags=["Authentication"],
             summary="User Login",
             description=
                """
                Authenticate a user using email and password.

                This endpoint verifies the provided credentials with Firebase Authentication.
                On success, it returns a valid **Firebase ID token** that can be used to
                access protected routes.
                """
            )
async def login(data : UserLogin):
    email = data.email
    password = data.password
    try:
        user = firebase.auth().sign_in_with_email_and_password(email, password)
        token = user['idToken']
        return JSONResponse(status_code=status.HTTP_200_OK, content={
            "message": "User logged in successfully",
            "token": token
        })
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")



@router.post("/signup", 
             status_code=status.HTTP_201_CREATED, 
             tags=["Authentication"],
             summary="User Signup",
             description=
             """
                Register a new user with Firebase Authentication.

                This endpoint creates a new user account in Firebase using the provided
                email and password.  
                It returns the created user's **UID** and **email** on success.
                """
            )
async def signup(data : UserCreate):
    email = data.email
    password = data.password
    try:
        user = auth.create_user(
            email=email,
            password=password
        )
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={
            "message": "User created successfully",
            "uid": user.uid,
            "email": user.email
        })
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post('/ping', 
             status_code=status.HTTP_200_OK, 
             tags=["Authentication"],
             summary="Token Validation",
             description=
                """
                Verify a user's Firebase ID token.

                This endpoint checks whether the provided token in the **Authorization header**
                is valid and returns the authenticated user's UID.  
                It can be used to test if a user session is still valid or if the token has expired.
                """
            )
async def validate_token(request:Request):
    jwt = request.headers.get('Authorization')
    user = auth.verify_id_token(jwt)
    return user.get('uid')
