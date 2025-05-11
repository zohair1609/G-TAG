# AutoPDI - Vehicle Damage Detection System

AutoPDI is an AI-powered web application that automates vehicle damage detection and inspection processes for car dealerships, repair shops, and insurance companies.

## Features

- **AI-Powered Damage Detection**: Utilizes YOLOv5 to automatically detect and classify car damage from uploaded images
- **Smart Inspection Checklist**: 20-point vehicle inspection system with AI-suggested results and technician override
- **Vehicle Tracking Dashboard**: Real-time monitoring of vehicles through the inspection process
- **Analytics Dashboard**: Performance metrics, damage statistics, and inspection trends
- **Responsive Design**: Mobile-friendly interface works on any device

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap
- **AI/ML**: YOLOv5 for object detection
- **Data Visualization**: Chart.js
- **UI Components**: Font Awesome, Google Fonts

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/AutoPDI.git
   cd AutoPDI
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv env
   source env/bin/activate  # On Windows, use: env\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   python flask_app.py
   ```

5. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## Usage

### Damage Detection
1. Navigate to the home page
2. Upload an image of a vehicle
3. The system will automatically detect and highlight damaged areas
4. Review the damage assessment and inspection checklist

### Vehicle Tracking
1. Navigate to the tracking page
2. View vehicles currently in the inspection process
3. Monitor their progress through various inspection stages
4. Check diagnostics and damage reports in real-time

### Analytics Dashboard
1. Navigate to the dashboard page
2. View key performance metrics
3. Analyze damage detection trends
4. Review inspection histories and outcomes

## Project Structure

```
AutoPDI/
├── flask_app.py           # Main application file
├── requirements.txt       # Python dependencies
├── static/                # Static assets
│   ├── css/               # CSS stylesheets
│   ├── js/                # JavaScript files
│   └── images/            # Uploaded and processed images
└── templates/             # HTML templates
    ├── base.html          # Base template with common elements
    ├── index.html         # Home page with upload functionality
    ├── tracking.html      # Vehicle tracking dashboard
    ├── dashboard.html     # Analytics dashboard
    └── about.html         # About page
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- YOLOv5 by Ultralytics
- Bootstrap CSS Framework
- Font Awesome Icons
- Chart.js for data visualization 