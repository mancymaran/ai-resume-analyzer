from flask import Flask, request, render_template_string
import PyPDF2
import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Create Flask app
app = Flask(__name__)

# Simple HTML page
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Resume Analyzer</title>
</head>
<body>
    <h1>AI Resume Analyzer</h1>
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="resume" required>
        <button type="submit">Upload Resume</button>
    </form>

    {% if text %}
        <h2>Extracted Text:</h2>
        <p>{{ text }}</p>
    {% endif %}
</body>
</html>
"""

# Function to extract text from PDF
def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Main route
@app.route("/", methods=["GET", "POST"])
def home():
    text = ""
    if request.method == "POST":
        file = request.files["resume"]
        text = extract_text_from_pdf(file)
    return render_template_string(HTML_PAGE, text=text)

# Run the server
if __name__ == "__main__":
    print("Starting server...")
    app.run(host="127.0.0.1", port=5000, use_reloader=False)