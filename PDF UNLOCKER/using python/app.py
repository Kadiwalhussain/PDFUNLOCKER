from flask import Flask, render_template, request, Response
import PyPDF2

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/unlock', methods=['POST'])
def unlock_pdf():
    try:
        pdf_file = request.files['pdfFile']
        password = request.form['password']

        # Check if a file and password were provided
        if not pdf_file or not password:
            return "Please select a PDF file and enter the password."

        # Create a PDF object and attempt to decrypt it
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        if pdf_reader.isEncrypted:
            pdf_reader.decrypt(password)
        else:
            return "The provided PDF is not encrypted."

        # Create a response with the unlocked PDF
        response = Response(pdf_reader.stream)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'inline; filename=unlocked_{pdf_file.filename}'
        return response
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
