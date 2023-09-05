from flask import Request
import uuid
import time

from exceptions import ValidationError

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

MSG_CAPTION_BLANK = "Caption cannot be blank."
MSG_FILE_MISSING = "File is missing."
MSG_INVALID_EXTENSION = "Invalid file extension"

def validate(request: Request):
    # Generate an ID for the post
    post_id = str(uuid.uuid4())

    # Make sure the caption is not blank
    caption = request.form['caption']
    if (caption.isspace() or caption == ""):
        raise ValidationError(MSG_CAPTION_BLANK)

    # Make sure the image exists
    file = request.files['imageupload']
    if (file is None):
        raise ValidationError(MSG_FILE_MISSING)

    # Make sure the file has a valid extension
    extension = get_extension(file.filename)
    if (extension not in ALLOWED_EXTENSIONS):
        raise ValidationError(MSG_INVALID_EXTENSION)
    
    # Standardize the file name
    file_name = f"image_{post_id}.{extension}"

    # Make a timestamp
    datetime = int(time.time())

    return {
        "id": post_id,
        "caption": caption,
        "datetime": datetime,
        "file": file,
        "file_name": file_name 
    }

def get_extension(filename):
    # Return the extension when given a file name
    return filename.rsplit('.', 1)[1].lower()

