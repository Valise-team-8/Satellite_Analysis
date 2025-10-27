# app.py
import os
from pathlib import Path
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    send_from_directory,
    session,
)
from werkzeug.utils import secure_filename
from utils.predict import predict_land_use
from utils.deforestation import detect_deforestation
import json

# -------------------------
# Config
# -------------------------
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "static" / "uploads"
MODEL_DIR = BASE_DIR / "model"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXT = {"jpg", "jpeg", "png", "tif", "tiff", "bmp"}
MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50 MB limit

app = Flask(
    __name__,
    static_folder=str(BASE_DIR / "static"),
    template_folder=str(BASE_DIR / "templates"),
)
app.config["UPLOAD_FOLDER"] = str(UPLOAD_DIR)
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH
app.secret_key = os.environ.get("FLASK_SECRET", "dev-secret-change-me")


# -------------------------
# Helpers
# -------------------------
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT


def save_file(file_storage, prefix=None):
    fname = secure_filename(file_storage.filename)
    if prefix:
        fname = f"{prefix}_{fname}"
    dest = Path(app.config["UPLOAD_FOLDER"]) / fname
    file_storage.save(dest)
    return str(dest), fname


# -------------------------
# Routes (PRG pattern)
# -------------------------
@app.route("/")
def home():
    return render_template("home.html")


# LAND USE
@app.route("/landuse", methods=["GET", "POST"])
def landuse():
    if request.method == "POST":
        file = request.files.get("image")
        if not file or file.filename == "":
            flash("Please upload an image.", "warning")
            return redirect(request.url)
        if not allowed_file(file.filename):
            flash("Unsupported file type.", "danger")
            return redirect(request.url)

        path, fname = save_file(file, prefix="landuse")
        try:
            pred_class, conf = predict_land_use(path)
            # ✅ Convert float32 to float for JSON/session compatibility
            session["last_landuse"] = {
                "class": pred_class,
                "confidence": float(conf),
                "filename": fname,
            }
        except Exception as e:
            flash(f"Prediction error: {e}", "danger")
            return redirect(request.url)

        return redirect(url_for("landuse"))

    # GET
    last = session.pop("last_landuse", None)
    uploaded_url = (
        url_for("static", filename=f"uploads/{last['filename']}")
        if last and "filename" in last
        else None
    )
    return render_template("landuse.html", result=last, uploaded_url=uploaded_url)


# DEFORESTATION
@app.route("/deforestation", methods=["GET", "POST"])
def deforestation():
    if request.method == "POST":
        before = request.files.get("before")
        after = request.files.get("after")
        if not before or not after:
            flash("Please upload both before and after images.", "warning")
            return redirect(request.url)
        if not (allowed_file(before.filename) and allowed_file(after.filename)):
            flash("Unsupported file type.", "danger")
            return redirect(request.url)

        before_path, before_fname = save_file(before, prefix="before")
        after_path, after_fname = save_file(after, prefix="after")
        try:
            change_pct, status = detect_deforestation(before_path, after_path)
            session["last_deforestation"] = {
                "change_percent": float(change_pct),  # ✅ convert to float if needed
                "status": status,
                "before_fname": before_fname,
                "after_fname": after_fname,
            }
        except Exception as e:
            flash(f"Deforestation detection error: {e}", "danger")
            return redirect(request.url)

        return redirect(url_for("deforestation"))

    last = session.pop("last_deforestation", None)
    uploaded_before = (
        url_for("static", filename=f"uploads/{last['before_fname']}")
        if last and "before_fname" in last
        else None
    )
    uploaded_after = (
        url_for("static", filename=f"uploads/{last['after_fname']}")
        if last and "after_fname" in last
        else None
    )
    return render_template(
        "deforestation.html",
        result=last,
        uploaded_before=uploaded_before,
        uploaded_after=uploaded_after,
    )


# PERFORMANCE
@app.route("/performance")
def performance():
    class_names = []
    plot_url = None
    class_file = MODEL_DIR / "class_names.json"
    plot_file = MODEL_DIR / "training_plot.png"

    if class_file.exists():
        with open(class_file, "r", encoding="utf-8") as f:
            class_names = json.load(f)
    if plot_file.exists():
        plot_url = url_for("model_file", filename="training_plot.png")
    return render_template(
        "performance.html", class_names=class_names, training_plot_url=plot_url
    )


# Serve model files (training plot)
@app.route("/model_files/<path:filename>")
def model_file(filename):
    return send_from_directory(str(MODEL_DIR), filename, as_attachment=False)


# Error handler for large uploads
@app.errorhandler(413)
def request_entity_too_large(error):
    flash(
        f"File too large. Max allowed size is {MAX_CONTENT_LENGTH // (1024*1024)} MB.",
        "danger",
    )
    return redirect(request.url)


# -------------------------
# Run
# -------------------------
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True, use_reloader=False)
