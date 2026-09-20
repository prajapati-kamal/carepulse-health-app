# 🏥 CarePulse - Health & Wellness Companion with 3D Visuals & AI Chatbot

A modern, responsive Health & Wellness web application featuring an interactive **AI Health Chatbot ("CareBot")**, **hardware-accelerated 3D graphics (Three.js)**, **daily vitality trackers**, and **clinical calculators**.

---

## 🌟 Key Features

### 1. 🤖 CareBot - AI Health Advisor
- **Everyday Symptom Discussion**: Evidence-backed guidance on headaches, common colds, flu, sore throats, indigestion, sleep issues, and stress.
- **Emergency Red-Flag Detection**: Automatically identifies urgent medical emergencies (chest pain, stroke symptoms, respiratory distress) and prompts emergency hotline assistance (911, 112, 108, 988).
- **Interactive Suggestion Chips**: One-click quick prompts with dynamic follow-up recommendations.
- **3D AI Companion Avatar**: Features a friendly 3D robot doctor with smooth levitation animations.

### 2. 🫀 Interactive 3D Beating Heart Engine (Three.js)
- **Real-Time 3D Anatomical Heart**: Hardware-accelerated WebGL rendering with specular shading and dual-point lighting.
- **Biologically Accurate Heartbeat**: Dual-pulse ("lub-dub") rhythmic pulsation.
- **Full 360° Interaction**: Drag to rotate in 3D using your mouse or touch screen.
- **Dynamic Controls**: Adjust simulated BPM pace (50–130 BPM), reset angle, or toggle wireframe mesh mode.

### 3. 📊 Daily Vitality Tracker
- **Hydration Tracker**: Interactive cup visualizer (250 ml per cup) with animated liquid wave progress.
- **Step Counter**: Log daily steps with progress bars and quick tags (+1,000, +2,500, +5,000).
- **Sleep Logger**: Intuitive slider to record sleep hours and restfulness.
- **Mood Check-in**: Emoji-based daily mood tracking with contextual wellness advice.

### 4. 🧮 Interactive Health Calculators
- **BMI & Ideal Weight Checker**: Computes BMI, health category, and healthy target weight range in kg.
- **Daily Water & Calorie Estimator**: Tailored recommendations based on age, gender, weight, and activity level (BMR & TDEE).
- **Blood Pressure Evaluator**: Categorizes readings against American Heart Association (AHA) clinical guidelines.

### 5. 💊 Medication & Supplement Manager
- Add daily prescriptions and vitamins with scheduled times.
- Interactive checkboxes to mark doses as taken with live progress counter.

### 6. 📚 First Aid & Emergency Directory
- Quick guides for Cold vs. Flu, 4-7-8 Breathing Technique, Mediterranean Diet, and Desk Ergonomics.
- International emergency numbers and a one-click **Emergency SOS** modal.

---

## 🚀 Quick Start (Local Setup)

### Prerequisites
- Python 3.10+
- Git

### Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/prajapati-kamal/carepulse-health-app.git
   cd carepulse-health-app
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   - On Windows, double-click `start_app.bat` or run:
     ```bash
     python app.py
     ```

4. **Open in browser**:
   Navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000).

---

## 🧪 Running Tests

The application includes an automated test suite verifying chatbot intents, calculators, and database CRUD operations:

```bash
python test_app.py
```

---

## ☁️ Deployment

### Deploy on Render.com (Free)
1. Fork or push this repository to GitHub.
2. Sign up at [render.com](https://render.com) and create a **New Web Service**.
3. Connect your repository.
4. Set:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. Click **Deploy Web Service**.

---

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).