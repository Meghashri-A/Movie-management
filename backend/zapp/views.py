from distutils import errors
import json
import os
from bson import ObjectId
from django.forms import ValidationError
from django.http import JsonResponse
from django.views import View
import pymongo
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, NotFound, PermissionDenied
import jwt, datetime
from django.conf import settings
from db_connection import db
import hashlib

def is_admin_user(payload):
    users_collection = db['user_dets']
    admin = users_collection.find_one({"_id": ObjectId(payload['id'])})
    return admin['username'] == 'admin'

class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        
        if not username or not password or not email:
            raise ValidationError("Username, password, and email are required.")

        users_collection = db['user_dets']

        if users_collection.find_one({"$or": [{"username": username}, {"email": email}]}):
            return Response({'message': 'User already exists'}, status=400)
    
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        user = {
            "username": username,
            "password": hashed_password,
            "email": email
        }
        users_collection.insert_one(user)
        return Response({'message': 'User created successfully'}, status=201)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            raise AuthenticationFailed('Username and password are required')
        
        users_collection = db['user_dets']
        user = users_collection.find_one({"username": username})
        
        if user is None:
            raise AuthenticationFailed('User not found')
        
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        if user['password'] != hashed_password:
            raise AuthenticationFailed('Incorrect password')
        
        user_id = str(user['_id'])
        token = jwt.encode({'id': user_id}, settings.SECRET_KEY, algorithm='HS256')
        
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'access': token,
            'username': user['username'], 
            'message': 'Login successful'
        }
        return response
    
def admin_required(view_func):
    def wrapped_func(self, request, *args, **kwargs):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            if not is_admin_user(payload):
                raise PermissionDenied('You do not have permission to perform this action')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        return view_func(self, request, *args, **kwargs)
    return wrapped_func

from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

class AddMovieView(APIView):
    @admin_required  
    def post(self, request):
        movie_name = request.data.get('movie_name')
        yor = request.data.get('yor')
        language = request.data.get('language')
        genre = request.data.get('genre')
        description = request.data.get('description')
        cast_and_crew = request.data.get('cast_and_crew')
        #picture_url = request.data.get('picture_url')  # Get picture URL from request data
        if not (movie_name and yor and language and genre and description and cast_and_crew):
            return Response({'message': 'All fields are required'}, status=400)

        movies_collection = db['movie_list']  # Get or create 'movie_list' collection


        existing_movie = movies_collection.find_one({'movie_name': movie_name})
        if existing_movie:
            return Response({'message': 'Movie already exists'}, status=400)


        movie = {
            'movie_name': movie_name,
            'yor': yor,
            'language': language,
            'genre': genre,
            'description': description,
            'cast_and_crew': cast_and_crew,
           # 'picture_url': picture_url 
        }

        try:
            movies_collection.insert_one(movie)  
        except errors.PyMongoError as e:
            return Response({'message': f'Failed to add movie: {str(e)}'}, status=500)

        return Response({'message': 'Movie added successfully'}, status=201)


class ReadMoviesView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')  
        if not token:
            raise AuthenticationFailed('Unauthenticated!')  
        
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])  
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')   
        movies_collection = db['movie_list']  
        movies = list(movies_collection.find({}))

       
        for movie in movies:
            movie['_id'] = str(movie['_id'])
            for key, value in movie.items():
                if isinstance(value, bytes):
                    movie[key] = value.decode('utf-8', errors='ignore')

        return Response(movies)
    
class UpdateMovieView(APIView):
    @admin_required
    def put(self, request, movie_id):
        token = request.COOKIES.get('jwt') 
        if not token:
            raise AuthenticationFailed('Unauthenticated!')  
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])  
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!') 
        
        if not is_admin_user(payload):
            raise PermissionDenied('You do not have permission to perform this action') 
        
        movies_collection = db['movie_list'] 
        update_fields = {
            key: request.data.get(key) for key in ['movie_name', 'yor', 'language', 'genre', 'description', 'cast_and_crew']
            if request.data.get(key) is not None
        }
        if not update_fields:
            return Response({'message': 'No fields to update'}, status=400)
        try:
            result = movies_collection.update_one({"_id": ObjectId(movie_id)}, {"$set": update_fields})
        except Exception as e:
            return Response({'message': f'Failed to update movie: {str(e)}'}, status=500)
        if result.modified_count == 0:
            return Response({'message': 'No field was changed in the form, try again'}, status=404)
        return Response({'message': 'Movie updated successfully'})


class DeleteMovieView(APIView):
    @admin_required
    def delete(self, request, movie_id):
        token = request.COOKIES.get('jwt') 
        if not token:
            raise AuthenticationFailed('Unauthenticated!')  
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])  
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        
        if not is_admin_user(payload):
            raise PermissionDenied('You do not have permission to perform this action') 
        
        movies_collection = db['movie_list']  
        movie = movies_collection.find_one({'_id': ObjectId(movie_id)})
        if not movie:
            raise NotFound('Movie not found')
        movies_collection.delete_one({'_id': ObjectId(movie_id)})
        return Response({'message': 'Movie deleted successfully'}, status=204)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'Logout successful'
        }
        return response
    

class getmovbyid(APIView):
    def get(self, request, movie_id):
        token = request.COOKIES.get('jwt')  
        if not token:
            raise AuthenticationFailed('Unauthenticated!')  
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        
        if not is_admin_user(payload):
            raise PermissionDenied('You do not have permission to perform this action') 
        
        movies_collection = db['movie_list'] 
        movie = movies_collection.find_one({'_id': ObjectId(movie_id)})
        if not movie:
            raise NotFound('Movie not found') 
        
        movie['_id'] = str(movie['_id']) 
        return Response(movie)  
    
from rest_framework.decorators import api_view
from rest_framework.response import Response
@api_view(['GET'])
def isauthenticated(request):
    token = request.COOKIES.get('jwt')  
    if not token:
        return Response({'authenticated': False})

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return Response({'authenticated': True})
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('JWT token has expired')
    except jwt.InvalidTokenError:
        raise AuthenticationFailed('Invalid JWT token')
    

class SearchMoviesView(APIView):
    def get(self, request):
        query = request.GET.get('q', '')
        if not query:
            return Response({'message': 'Query parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        movies_collection = db['movie_list']
        regex_query = {"$regex": query, "$options": "i"}
        search_criteria = {
            "$or": [
                {"movie_name": regex_query},
                {"genre": regex_query},
                {"yor": regex_query},
                {"language": regex_query},
                {"description": regex_query},
                {"cast_and_crew": regex_query}
            ]
        }
        results = list(movies_collection.find(search_criteria))
        for movie in results:
            movie['_id'] = str(movie['_id'])  

        return Response(results, status=status.HTTP_200_OK)

class FilterMoviesView(APIView):
    def get(self, request):
        genre = request.GET.get('genre', None)
        #release_year = request.GET.get('release_year', None)

        filter_criteria = {}
        if genre:
            filter_criteria['genre'] = genre
        #if release_year:
            #filter_criteria['yor'] = release_year

        movies_collection = db['movie_list']
        results = list(movies_collection.find(filter_criteria))
        for movie in results:
            movie['_id'] = str(movie['_id'])  # Convert ObjectId to string

        return Response(results, status=status.HTTP_200_OK)
    

import gridfs
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage

@method_decorator(csrf_exempt, name='dispatch')
class ImageURLView(View):
    def post(self, request):
        try:
            image_file = request.FILES['image']
            image_name = image_file.name
            picture = db['pic']

            # Save the file to the local storage
            file_path = default_storage.save(image_name, image_file)

            # Store the image name in the database
            result = picture.insert_one({'picture': image_name})
            inserted_id = str(result.inserted_id)

            return JsonResponse({'message': 'Image uploaded successfully.', 'id': inserted_id}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        
@method_decorator(csrf_exempt, name='dispatch')        
class RetrieveImageView(View):
    def get(self, request):
        try:
            picture = db['pic']
            image_docs = picture.find({}, {'picture': 1, '_id': 0})
            image_names = [doc['picture'] for doc in image_docs]

            return JsonResponse({'image_names': image_names}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)



















'''from bson import ObjectId
import pymongo
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, NotFound
import jwt, datetime
from django.conf import settings
from db_connection import db
import hashlib


class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        users_collection = db['user_dets']  # Create or get 'user_dets' collection
        if users_collection.find_one({"email": email}):
            return Response({'message': 'User already exists'}, status=400)
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        user = {
            "username": username,
            "password": hashed_password,
            "email": email
        }
        users_collection.insert_one(user)
        return Response({'message': 'User created successfully'}, status=201)


#LOGINNNNN

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            raise AuthenticationFailed('Username and password are required')
        users_collection = db['user_dets']  # Create or get 'user_dets' collection
        user = users_collection.find_one({"username": username})
        if user is None:
            raise AuthenticationFailed('User not found')
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        if user['password'] != hashed_password:
            raise AuthenticationFailed('Incorrect password')
        # Assuming user['_id'] is the ObjectId generated by MongoDB
        user_id = str(user['_id'])
        token = jwt.encode({'id': user_id}, settings.SECRET_KEY, algorithm='HS256')
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'access': token,
            'message': 'Login successful'
        }
        return response




#CRUD


#----------------CREATE----------------------------
class AddMovieView(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')  # Retrieve JWT token from cookies
        if not token:
            raise AuthenticationFailed('Unauthenticated!')  # No token found, raise error
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])  # Decode and verify token
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')  # Token expired, raise error
        movie_name = request.data.get('movie_name')
        yor = request.data.get('yor')
        language = request.data.get('language')
        genre = request.data.get('genre')
        description = request.data.get('description')
        cast_and_crew = request.data.get('cast_and_crew')
        if not (movie_name and yor and language and genre and description and cast_and_crew):
            return Response({'message': 'All fields are required'}, status=400)
        movies_collection = db['movie_list']  # Create or get 'movie_list' collection
        # Insert movie into MongoDB collection
        movie = {
            'movie_name': movie_name,
            'yor': yor,
            'language': language,
            'genre': genre,
            'description': description,
            'cast_and_crew': cast_and_crew
        }
        movies_collection.insert_one(movie)
        return Response({'message': 'Movie added successfully'}, status=201)

#-----------------------------READ------------------------------------------------
class ReadMoviesView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')  # Retrieve JWT token from cookies
        if not token:
            raise AuthenticationFailed('Unauthenticated!')  # No token found, raise error
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])  # Decode and verify token
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')  # Token expired, raise error
        movies_collection = db['movie_list']  # Get 'movie_list' collection from MongoDB
        # Fetch all movies from the collection
        movies = list(movies_collection.find({}))
        for movie in movies:
            movie['_id'] = str(movie['_id'])
        return Response(movies)
    

#-----------------------------UPDATE-------------------------
class UpdateMovieView(APIView):
    def put(self, request, movie_id):
        token = request.COOKIES.get('jwt')  # Retrieve JWT token from cookies
        if not token:
            raise AuthenticationFailed('Unauthenticated!')  # No token found, raise error
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])  # Decode and verify token
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')  # Token expired, raise error
        movies_collection = db['movie_list']  # Get 'movie_list' collection from MongoDB
        # Update movie fields based on request data
        update_fields = {
            key: request.data.get(key) for key in ['movie_name', 'yor', 'language', 'genre', 'description', 'cast_and_crew']
            if request.data.get(key) is not None
        }
        if not update_fields:
            return Response({'message': 'No fields to update'}, status=400)
        # Update the movie document in the collection
        try:
            result = movies_collection.update_one({"_id": ObjectId(movie_id)}, {"$set": update_fields})
        except Exception as e:
            return Response({'message': f'Failed to update movie: {str(e)}'}, status=500)
        if result.modified_count == 0:
            return Response({'message': 'No movie found for update'}, status=404)
        return Response({'message': 'Movie updated successfully'})
    

#-----------------------DELETE--------------------------
class DeleteMovieView(APIView):
    def delete(self, request, movie_id):
        token = request.COOKIES.get('jwt')  # Retrieve JWT token from cookies
        if not token:
            raise AuthenticationFailed('Unauthenticated!')  # No token found, raise error
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])  # Decode and verify token
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')  # Token expired, raise error
        movies_collection = db['movie_list']  # Get 'movie_list' collection from MongoDB
        # Check if the movie exists
        movie = movies_collection.find_one({'_id': ObjectId(movie_id)})
        if not movie:
            raise NotFound('Movie not found')
        # Delete the movie
        movies_collection.delete_one({'_id': ObjectId(movie_id)})
        return Response({'message': 'Movie deleted successfully'}, status=204)
    

#----------------------------LOGOUT-----BYE-------------------------
class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'Logout successful'
        }
        return response
    

class getmovbyid(APIView):
    def get(self, request, movie_id):
        token = request.COOKIES.get('jwt')  # Retrieve JWT token from cookies
        if not token:
            raise AuthenticationFailed('Unauthenticated!')  # No token found, raise error
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])  # Decode and verify token
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')  # Token expired, raise error
        
        movies_collection = db['movie_list']  # Get 'movie_list' collection from MongoDB
        movie = movies_collection.find_one({'_id': ObjectId(movie_id)})  # Find movie by ID
        if not movie:
            raise NotFound('Movie not found')  # Movie not found, raise error
        
        movie['_id'] = str(movie['_id'])  # Convert ObjectId to string
        return Response(movie)  # Return movie details'''


