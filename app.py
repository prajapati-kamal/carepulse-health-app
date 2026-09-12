from flask import Flask, render_template, request, jsonify
import database
import chatbot_engine

app = Flask(__name__)

# Initialize database tables on startup
database.init_db()

@app.route("/")
def index():
    return render_template("index.html")

# ================= CHATBOT ENDPOINTS =================

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    user_message = data.get("message", "").strip()
    
    if not user_message:
        return jsonify({"error": "Message is required"}), 400
        
    # Save user message
    database.save_chat_message("user", user_message)
    
    # Generate bot response
    bot_reply = chatbot_engine.generate_health_response(user_message)
    
    # Save bot message
    database.save_chat_message("bot", bot_reply["text"])
    
    return jsonify({
        "reply": bot_reply["text"],
        "category": bot_reply.get("category", "general"),
        "suggestions": bot_reply.get("suggestions", [])
    })

@app.route("/api/chat/history", methods=["GET"])
def chat_history():
    history = database.get_recent_chat_history()
    return jsonify({"history": history})

@app.route("/api/chat/clear", methods=["POST"])
def chat_clear():
    database.clear_chat_history()
    return jsonify({"status": "success", "message": "Chat history cleared"})

# ================= DAILY TRACKER ENDPOINTS =================

@app.route("/api/tracker", methods=["GET"])
def get_tracker():
    date_str = request.args.get("date")
    tracker_data = database.get_daily_tracker(date_str)
    return jsonify(tracker_data)

@app.route("/api/tracker", methods=["POST"])
def update_tracker():
    data = request.get_json() or {}
    date_str = data.pop("date", None)
    updated = database.update_daily_tracker(date_str, **data)
    return jsonify(updated)

# ================= MEDICATION ENDPOINTS =================

@app.route("/api/medications", methods=["GET"])
def get_medications():
    date_str = request.args.get("date")
    meds = database.get_medications(date_str)
    return jsonify({"medications": meds})

@app.route("/api/medications", methods=["POST"])
def add_medication():
    data = request.get_json() or {}
    name = data.get("name", "").strip()
    dosage = data.get("dosage", "").strip()
    time_str = data.get("time", "").strip()
    date_str = data.get("date")
    
    if not name or not time_str:
        return jsonify({"error": "Medication name and time are required"}), 400
        
    med = database.add_medication(name, dosage, time_str, date_str)
    return jsonify(med), 201

@app.route("/api/medications/<int:med_id>/toggle", methods=["POST"])
def toggle_medication(med_id):
    result = database.toggle_medication(med_id)
    if not result:
        return jsonify({"error": "Medication not found"}), 404
    return jsonify(result)

@app.route("/api/medications/<int:med_id>", methods=["DELETE"])
def delete_medication(med_id):
    database.delete_medication(med_id)
    return jsonify({"status": "success", "deleted_id": med_id})

# ================= HEALTH CALCULATOR ENDPOINTS =================

@app.route("/api/calculator/bmi", methods=["POST"])
def calculate_bmi():
    data = request.get_json() or {}
    try:
        height_cm = float(data.get("height_cm", 0))
        weight_kg = float(data.get("weight_kg", 0))
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid height or weight values"}), 400
        
    if height_cm <= 50 or height_cm >= 260 or weight_kg <= 20 or weight_kg >= 350:
        return jsonify({"error": "Please enter realistic height (50-260 cm) and weight (20-350 kg) values"}), 400
        
    height_m = height_cm / 100.0
    bmi = round(weight_kg / (height_m ** 2), 1)
    
    # Calculate ideal weight range (BMI 18.5 - 24.9)
    min_ideal_weight = round(18.5 * (height_m ** 2), 1)
    max_ideal_weight = round(24.9 * (height_m ** 2), 1)
    
    if bmi < 18.5:
        category = "Underweight"
        color = "#eab308" # yellow
        advice = "Focus on nutrient-dense meals, healthy fats (nuts, avocados), and resistance training to build healthy muscle mass."
    elif 18.5 <= bmi <= 24.9:
        category = "Normal / Healthy Weight"
        color = "#10b981" # green
        advice = "Great job! Maintain your current routine with regular exercise, balanced nutrition, and adequate hydration."
    elif 25.0 <= bmi <= 29.9:
        category = "Overweight"
        color = "#f97316" # orange
        advice = "Aim for a moderate calorie deficit, increase daily movement (8,000+ steps), and focus on whole foods and fiber."
    else:
        category = "Obesity"
        color = "#ef4444" # red
        advice = "Consult a physician or dietitian for a structured, sustainable weight management and cardiovascular wellness plan."
        
    return jsonify({
        "bmi": bmi,
        "category": category,
        "color": color,
        "min_ideal_weight": min_ideal_weight,
        "max_ideal_weight": max_ideal_weight,
        "advice": advice
    })

@app.route("/api/calculator/water-calorie", methods=["POST"])
def calculate_water_calorie():
    data = request.get_json() or {}
    try:
        weight_kg = float(data.get("weight_kg", 70))
        age = int(data.get("age", 28))
        gender = data.get("gender", "male").lower()
        activity = data.get("activity", "moderate")
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid input values"}), 400
        
    # Water calculation: approx 35 ml per kg of body weight
    base_water_ml = weight_kg * 35
    activity_multiplier_water = {
        "sedentary": 1.0,
        "light": 1.1,
        "moderate": 1.25,
        "active": 1.4,
        "very_active": 1.55
    }.get(activity, 1.2)
    
    total_water_ml = int(round(base_water_ml * activity_multiplier_water))
    water_cups = round(total_water_ml / 250, 1) # 250 ml standard cup
    
    # Calorie calculation: Mifflin-St Jeor Formula approximation
    # BMR: Men = 10*weight + 6.25*height(est) - 5*age + 5
    # For quick approximation:
    if gender == "male":
        bmr = (10 * weight_kg) + (6.25 * 175) - (5 * age) + 5
    else:
        bmr = (10 * weight_kg) + (6.25 * 162) - (5 * age) - 161
        
    activity_multiplier_cal = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very_active": 1.9
    }.get(activity, 1.55)
    
    tdee = int(round(bmr * activity_multiplier_cal))
    
    return jsonify({
        "recommended_water_ml": total_water_ml,
        "recommended_water_cups": water_cups,
        "estimated_daily_calories": tdee,
        "bmr": int(round(bmr))
    })

@app.route("/api/calculator/bp", methods=["POST"])
def calculate_bp():
    data = request.get_json() or {}
    try:
        systolic = int(data.get("systolic", 120))
        diastolic = int(data.get("diastolic", 80))
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid blood pressure values"}), 400
        
    if systolic > 180 or diastolic > 120:
        stage = "Hypertensive Crisis"
        color = "#b91c1c"
        msg = "🚨 Extremely elevated blood pressure. Seek emergency medical evaluation immediately."
    elif systolic >= 140 or diastolic >= 90:
        stage = "Stage 2 Hypertension"
        color = "#ef4444"
        msg = "Blood pressure is high. Consult a doctor for medical management, reduce sodium, and monitor daily."
    elif (130 <= systolic <= 139) or (80 <= diastolic <= 89):
        stage = "Stage 1 Hypertension"
        color = "#f97316"
        msg = "Blood pressure is mildly high. Adopt lifestyle modifications (DASH diet, 30 min daily cardio, lower stress)."
    elif (120 <= systolic <= 129) and diastolic < 80:
        stage = "Elevated Blood Pressure"
        color = "#eab308"
        msg = "Pre-hypertension. Focus on physical activity and reducing dietary sodium to prevent progressing to hypertension."
    elif systolic < 90 or diastolic < 60:
        stage = "Low Blood Pressure (Hypotension)"
        color = "#3b82f6"
        msg = "Blood pressure is lower than normal. Stay hydrated, stand up slowly, and check with a physician if dizzy."
    else:
        stage = "Normal Blood Pressure"
        color = "#10b981"
        msg = "Your blood pressure is in the optimal healthy range! Keep up the good habits."
        
    return jsonify({
        "systolic": systolic,
        "diastolic": diastolic,
        "stage": stage,
        "color": color,
        "recommendation": msg
    })

# ================= WELLNESS ARTICLES ENDPOINT =================

@app.route("/api/wellness/articles", methods=["GET"])
def get_articles():
    articles = [
        {
            "id": 1,
            "category": "Emergency & First Aid",
            "title": "When to Go to the ER vs. Urgent Care",
            "summary": "Learn to distinguish between critical emergencies requiring an ER visit and minor ailments suitable for urgent care clinics.",
            "icon": "🚨",
            "details": "Go to the Emergency Room for: chest pain, sudden numbness or speech difficulty, severe head trauma, uncontrollable bleeding, or severe allergic reaction. Urgent care is ideal for minor cuts needing stitches, sprains, moderate fever, or urinary discomfort."
        },
        {
            "id": 2,
            "category": "Everyday Wellness",
            "title": "Cold vs. Flu: How to Spot the Difference",
            "summary": "Symptoms of colds develop gradually, while the flu hits suddenly with intense body aches, fever, and exhaustion.",
            "icon": "🤒",
            "details": "Colds usually feature runny noses, mild sneezes, and sore throats without high fever. Influenza arrives rapidly with high fevers (100°F–102°F), deep muscle aches, severe fatigue, and dry cough. Rest, fluids, and fever reducers help both."
        },
        {
            "id": 3,
            "category": "Mind & Stress",
            "title": "Mastering the 4-7-8 Breathing Technique",
            "summary": "A clinically proven breathing method to downregulate your nervous system and fall asleep faster.",
            "icon": "🧘",
            "details": "Inhale through your nose for 4 seconds, gently hold for 7 seconds, and slowly exhale through your mouth for 8 seconds. Practicing 4 repetitions activates your vagus nerve and lowers acute stress levels within 2 minutes."
        },
        {
            "id": 4,
            "category": "Nutrition",
            "title": "The Mediterranean Diet Blueprint",
            "summary": "Ranked #1 for longevity and cardiovascular health by global health organizations.",
            "icon": "🥗",
            "details": "Rich in extra-virgin olive oil, wild-caught fish, legumes, colorful vegetables, and whole grains. Promotes healthy cholesterol levels, reduces systemic inflammation, and supports brain health."
        },
        {
            "id": 5,
            "category": "Ergonomics",
            "title": "Preventing Tech Neck & Desk Fatigue",
            "summary": "Simple adjustments to protect your cervical spine and maintain healthy posture during long screen hours.",
            "icon": "💻",
            "details": "Position the top third of your computer screen at eye level. Keep your shoulders relaxed and elbows at 90 degrees. Every hour, perform 5 chin tucks and shoulder blade squeezes to release upper back tension."
        },
        {
            "id": 6,
            "category": "Sleep Health",
            "title": "Why Melatonin Cycles Matter",
            "summary": "How morning sunlight and evening blue-light restriction synchronize your internal circadian clock.",
            "icon": "🌙",
            "details": "Get 10–15 minutes of outdoor sunlight within an hour of waking to stimulate daytime cortisol and set your nighttime melatonin timer. Avoid smartphone screen use 60 minutes before bed to ensure deep REM cycles."
        }
    ]
    return jsonify({"articles": articles})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
