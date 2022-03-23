from app.main.model.user import User
from app.main.service.v1.auth_helper import Auth
from flask import request
from app.main.service.v1 import image_helper
from flask_uploads import UploadNotAllowed
from app.main.config import STATIC_FOLDER, UPLOAD_FOLDER
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename
from app.main.util.v1.fileupload_util import upload_file_to_bucket 
import os
import hashlib
import jwt
import datetime
from app.main.config import image_name_size
from wand.image import Image
import uuid
from app.main.config import  profile_pic_dir
from app.main.util.v1.database import save_db
from app.main.util.v1.apiResponse import apiresponse

import os
import logging

logging_str = "[%(asctime)s: %(levelname)s: %(module)s]: %(message)s"
log_dir = "/tmp/image_service/logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(filename=os.path.join(log_dir, 'running_logs.log'), level=logging.INFO, format=logging_str,
                    filemode="a")

def image_save(new_request, bucket_dir):
    try:
        try:
            data = new_request.files
        except RequestEntityTooLarge as e:
            return apiresponse(False, 'Image File Too Large', None), 413
            
        
        resp, status = Auth.get_logged_in_user(request)
        user_id = resp['data'].id
        user_role = resp['data'].role
        file = data['image']
        
        if 'image' not in data:
            message = 'No image part in the request'

        elif file.filename == '':
            message = 'No image selected for uploading'
            
        elif len(file.filename) > image_name_size:
            message = 'File name is too Large'
        elif file:
            # resp, status = Auth.get_logged_in_user(request)
            # user_id = resp['data']['id']
            # folder = UPLOAD_FOLDER
            file_name = bytes(secure_filename(bucket_dir+"_"+str(user_role)+"_"+str(user_id)),"utf-8")
            hash_file_name = hashlib.sha256(file_name)
            filename = hash_file_name.hexdigest()
            extension = file.filename.split(".")[-1]
            filename = f"{filename}.{extension}"

            file_path = UPLOAD_FOLDER + f"/{filename}"
            if os.path.exists(file_path) or os.path.isfile(file_path):
                os.remove(file_path)

            image_path = image_helper.save_image(data["image"],name = filename)

            image = Image(filename = image_path)
            image.resize(400, 365)

            image.compression_quality = 60
            image.save(filename=image_path)

            # here we only return the basename of the image and hide the internal folder structure from our user
            basename = image_helper.get_basename(image_path)
        
            #File Upload
            #url = upload_file_to_bucket(image_path, bucket_dir)
            
            # os.remove(image_path)

            data = {
                'image':basename, 
                # 'preview':url 
            }
        
            return apiresponse(True, 'Image Uploaded Successfully', data), 200

        
        return apiresponse(False, message, None), 400


    except UploadNotAllowed:  # forbidden file type
        extension = image_helper.get_extension(data["image"])
        return apiresponse(False, f'Image format not allowed. Please upload {extension} format images', None), 400
        

    except Exception as e:
        return apiresponse(False, str(e), None), 500

def image_upload(filename, bucket_dir, name):

    file_path = UPLOAD_FOLDER + f"/{filename}"

    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        return apiresponse(False, 'File does not exist', None), 400


    extension = image_helper.get_extension(file_path)
        
    unique = uuid.uuid4()
    new_file_path = UPLOAD_FOLDER + "/" +secure_filename(f"{bucket_dir}_{name}_{datetime.datetime.utcnow()}_{unique}") + extension  
    os.rename(file_path, new_file_path)
    image_path = new_file_path
    url = upload_file_to_bucket(image_path, bucket_dir)
    os.remove(image_path)

    return url, 200

def profle_pic_image_save(new_request, bucket_dir):
    
    """
    Saves image to s3 bucket for profile picture selection
    
    Parameters: request, bucket_dir
    Return type: __dict__, Integer
    """
    try:
        try:
            data = new_request.files
        except RequestEntityTooLarge as e:
            return apiresponse(False, 'Image File Too Large', None), 413
        
        resp, status = Auth.get_logged_in_user(request)
        user_name = resp['data'].name
        user_id = resp['data'].id
        user_role = resp['data'].role
        file = data['image']
        
        user_object = resp['data']

        if 'image' not in data:
            message = 'No image part in the request'

        elif file.filename == '':
            message = 'No image selected for uploading'
            
        elif len(file.filename) > image_name_size:
            message = 'File name is too Large'
        
        elif file:
    
            file_name = secure_filename(str(user_role)+"_"+str(user_name['name'])+"_"+str(user_id))
            extension = file.filename.split(".")[-1]
            filename = f"{file_name}.{extension}"

            file_path = UPLOAD_FOLDER + f"/{filename}"
            if os.path.exists(file_path) or os.path.isfile(file_path):
                os.remove(file_path)

            image_path = image_helper.save_image(data["image"],name = filename)

            image = Image(filename = image_path)
            image.resize(400, 365)

            image.compression_quality = 60
            image.save(filename=image_path)

            # here we only return the basename of the image and hide the internal folder structure from our user
            # basename = image_helper.get_basename(image_path)
        
            #File Upload
            url = upload_file_to_bucket(image_path, bucket_dir)
            
            os.remove(image_path)
            
            user_object.image = url
            save_db(user_object)
            
            return apiresponse(True, 'Image Uploaded Successfully', url), 200
        
        return apiresponse(False, message, None), 400
            

    except UploadNotAllowed:  # forbidden file type
        extension = image_helper.get_extension(data["image"])
        return apiresponse(False, f'Image format not allowed. Please upload {extension} format images', None), 400

    except Exception as e:
        return apiresponse(False, str(e), None), 500
        
    
