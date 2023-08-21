from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from pdf_translator import PDFTranslator
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

language_mapping = {
    "English": "en",
    "Polish": "pl",
    "German": "de",
    "Russian": "ru",
    "Spanish": "es",
}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    languages = ["English", "Polish", "German", "Russian", "Spanish"]
    return render_template("index.html", languages=languages)


@app.route("/translate", methods=["POST"])
def translate():
    if "file" not in request.files:
        return jsonify(error="No file uploaded"), 400
    file = request.files["file"]
    language = request.form.get("language")
    language_code = language_mapping.get(
        language, "en"
    )  # default to English if no match found

    if file.filename == "":
        return jsonify(error="No file selected"), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)
        translator = PDFTranslator(filepath, language_code)
        translated_text = translator.translate()
        return jsonify(text=translated_text)

    return jsonify(error="Invalid file type"), 400


if __name__ == "__main__":
    app.run(debug=True)
