# Import the required modules
import PyPDF2 # For reading and writing PDF files
import os # For file operations
import webbrowser # For opening the browser
from flask import Flask, request, send_file # For creating a web app and handling requests
from werkzeug.utils import secure_filename # For securing file names

# Create a Flask app object
app = Flask(__name__)

# Set the upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

# Configure the app with the upload folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Define a function to check if a file has an allowed extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Define a route for the home page
@app.route('/')
def index():
    # Return a simple HTML form for uploading a PDF file and entering a password
    return '''
    <!doctype html>
    <title>Upload and Unlock PDF File</title>
    <h1>Upload and Unlock PDF File</h1>
    <form method="post" enctype="multipart/form-data" action="/unlock">
      <p><input type="file" name="file" accept="application/pdf"></p>
      <p><input type="password" name="password" placeholder="Enter password"></p>
      <p><input type="submit" value="Upload and Unlock"></p>
    </form>
    '''

# Define a route for the unlock action
@app.route('/unlock', methods=['POST'])
def unlock():
    # Check if the request has a file and a password
    if 'file' not in request.files or 'password' not in request.form:
        # Return an error message
        return 'Please select a file and enter a password.'
    
    # Get the file and password from the request
    file = request.files['file']
    password = request.form['password']
    
    # Check if the file name is empty
    if file.filename == '':
        # Return an error message
        return 'No file selected.'
    
    # Check if the file has an allowed extension
    if not allowed_file(file.filename):
        # Return an error message
        return 'File type must be PDF.'
    
    # Secure the file name and save it in the upload folder
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    # Open the PDF file with PyPDF2
    pdf_reader = PyPDF2.PdfFileReader(filepath)
    
    # Check if the PDF file is encrypted
    if pdf_reader.isEncrypted:
        # Try to decrypt the PDF file with the password
        try:
            pdf_reader.decrypt(password)
        except:
            # Return an error message if the password is wrong or the encryption is not supported
            return 'Wrong password or unsupported encryption.'
        
        # Create a new PDF writer object
        pdf_writer = PyPDF2.PdfFileWriter()
        
        # Loop through the pages of the PDF file and add them to the writer object
        for page in pdf_reader.pages:
            pdf_writer.addPage(page)
        
        # Generate a new file name with _unlocked suffix
        new_filename = filename.rsplit('.', 1)[0] + '_unlocked.pdf'
        new_filepath = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
        
        # Write the unlocked PDF file to the new file path
        with open(new_filepath, 'wb') as new_file:
            pdf_writer.write(new_file)
        
        # Return the unlocked PDF file as an attachment with the same name adding unlocked
        return send_file(new_filepath, as_attachment=True, attachment_filename=new_filename)
    
    else:
        # Return an error message if the PDF file is not encrypted
        return 'PDF file is not encrypted.'
    

# Run the app in debug mode
if __name__ == '__main__':
    app.run(debug=True)
