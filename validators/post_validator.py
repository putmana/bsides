from flask import Request
import uuid
import time

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

def validate(request: Request):
    # Generate an ID for the post
    post_id = str(uuid.uuid4())

    # Make sure the caption is not blank
    caption = request.form['caption']
    assert caption != "", "Caption must not be blank!"

    # Make sure the image exists
    file = request.files['imageupload']
    assert file != None, "No file provided"

    # Make sure the file has a valid extension
    extension = get_extension(file.filename)
    assert extension in ALLOWED_EXTENSIONS, f"Invalid file extension: {extension}"
    
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

