import argparse
import io
import os
import datetime
from PIL import Image, ImageDraw, ImageFont
import torch
from flask import Flask, render_template, request, flash, url_for, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # For flashing messages

# Add Jinja2 custom date filter
@app.template_filter('now')
def _jinja2_filter_now(format_string, timezone="UTC"):
    return datetime.datetime.now().strftime(format_string)

# Define upload folder and ensure it exists
UPLOAD_FOLDER = os.path.join("static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Ensure images folder exists
IMAGES_FOLDER = os.path.join("static", "images")
os.makedirs(IMAGES_FOLDER, exist_ok=True)

# Ensure reports folder exists
REPORTS_FOLDER = os.path.join("static", "reports")
os.makedirs(REPORTS_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def predict():
    result_image_url = None
    original_image = None
    damage_data = []

    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part in the request.")
            return render_template("index.html")
        file = request.files["file"]
        if file.filename == "":
            flash("No file selected.")
            return render_template("index.html")
        
        # Save the uploaded file to disk
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)
        original_image = filename
        
        # Load image with PIL (convert to RGB for consistency)
        try:
            img = Image.open(file_path).convert("RGB")
        except Exception as e:
            flash(f"Error opening image: {e}")
            return render_template("index.html")
        
        # ------------------------------
        # YOLOv5 Inference & Manual Drawing
        # ------------------------------
        results = model(img, size=640)
        # Each box: [x1, y1, x2, y2, conf, class_idx]
        boxes = results.xyxy[0].cpu().numpy()
        names = results.names  # class names

        # Create a copy for drawing
        draw_img = img.copy()
        draw = ImageDraw.Draw(draw_img)
        # Try loading a larger TrueType font (size 40); fallback to default if unavailable
        try:
            font = ImageFont.truetype("arial.ttf", 40)
        except Exception as e:
            font = ImageFont.load_default()

        # Process each detected damage
        for *xyxy, conf, cls_idx in boxes:
            x1, y1, x2, y2 = xyxy
            cls_name = names[int(cls_idx)]
            confidence = float(conf) * 100
            label = f"{cls_name} {conf:.2f}"

            # Add to damage data for display in table
            severity = "High" if confidence > 90 else "Medium" if confidence > 75 else "Low"
            location = "Front" if y1 < img.height / 3 else "Rear" if y1 > 2 * img.height / 3 else "Side"
            damage_data.append({
                "type": cls_name,
                "location": location,
                "confidence": confidence,
                "severity": severity
            })

            # Draw bounding box
            draw.rectangle([x1, y1, x2, y2], outline="red", width=3)

            # Use textbbox to measure label size
            text_bbox = draw.textbbox((0, 0), label, font=font)
            text_w = text_bbox[2] - text_bbox[0]
            text_h = text_bbox[3] - text_bbox[1]

            # Position label above the box if there's space
            y_text = y1 - text_h if (y1 - text_h) > 0 else y1

            # Draw a filled rectangle behind the text
            draw.rectangle([x1, y_text, x1 + text_w, y_text + text_h], fill="red")
            # Draw label text
            draw.text((x1, y_text), label, fill="white", font=font)

        # ------------------------------
        # Enlarge the annotated image
        # ------------------------------
        scale_factor = 2
        enlarged_width = draw_img.width * scale_factor
        enlarged_height = draw_img.height * scale_factor
        enlarged_img = draw_img.resize((enlarged_width, enlarged_height), resample=Image.Resampling.LANCZOS)

        # Save the enlarged annotated image
        annotated_image_path = os.path.join(IMAGES_FOLDER, "annotated_image.jpg")
        enlarged_img.save(annotated_image_path)

        # Provide the annotated image URL to display
        result_image_url = url_for("static", filename="images/annotated_image.jpg")
    
    return render_template("index.html", result_image=result_image_url, original_image=original_image, damage_data=damage_data)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/tracking')
def tracking():
    vin_data = [
        {
            'vin': 'VIN-123',
            'step': 'Step 3 - AI Damage Scan',
            'location': 'Zone B - Scanning Bay',
            'damage': 'Dent on rear left door',
            'tire_pressure': [32, 33, 31, 34],
            'image_path': 'https://via.placeholder.com/150x100?text=Damaged+Car',
            'map_location': 'https://via.placeholder.com/400x225?text=Warehouse+Map'
        },
        {
            'vin': 'VIN-124',
            'step': 'Step 1 - Entry',
            'location': 'Gate A',
            'damage': 'None',
            'tire_pressure': [33, 32, 32, 33],
            'image_path': 'https://via.placeholder.com/150x100?text=Clean+Car',
            'map_location': 'https://via.placeholder.com/400x225?text=Warehouse+Map'
        }
    ]
    return render_template('tracking.html', vehicles=vin_data)

@app.route('/generate-report', methods=['POST'])
def generate_report():
    # Here you would generate a PDF report with the damage analysis
    # For demonstration, we'll return a success message
    
    # Mock data for demonstration
    report_data = {
        'report_id': datetime.datetime.now().strftime('%Y%m%d%H%M%S'),
        'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'success': True
    }
    
    return jsonify(report_data)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask app exposing YOLOv5 models")
    parser.add_argument("--port", default=5000, type=int, help="port number")
    args = parser.parse_args()

    # Load YOLOv5 model from torch hub
    model = torch.hub.load("ultralytics/yolov5", "yolov5s", pretrained=True)
    model.eval()

    app.run(host="0.0.0.0", port=args.port, debug=False)