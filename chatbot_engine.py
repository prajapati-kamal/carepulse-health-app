import re
import random

# Emergency keywords that indicate urgent medical situations
EMERGENCY_KEYWORDS = [
    r"\bchest pain\b", r"\bheart attack\b", r"\bpressure in chest\b",
    r"\bcan't breathe\b", r"\bcannot breathe\b", r"\bsevere shortness of breath\b", r"\bdifficulty breathing\b",
    r"\bstroke\b", r"\bface drooping\b", r"\bslurred speech\b", r"\barm weakness\b",
    r"\bsevere bleeding\b", r"\bunconscious\b", r"\bpassed out\b", r"\bseizure\b",
    r"\bsuicide\b", r"\bkill myself\b", r"\bend my life\b", r"\bself harm\b",
    r"\bpoison\b", r"\banaphylaxis\b", r"\bthroat closing\b"
]

def check_emergency(user_query: str):
    query_lower = user_query.lower()
    for pattern in EMERGENCY_KEYWORDS:
        if re.search(pattern, query_lower):
            return True
    return False

def get_emergency_response():
    return {
        "text": """🚨 **URGENT MEDICAL NOTICE**

The symptoms you mentioned could indicate an acute medical emergency. **Please seek immediate professional medical attention.**

- **United States / Canada**: Call **911** (or 988 for mental health crisis)
- **United Kingdom**: Call **999** or **111**
- **European Union / India**: Call **112** (Ambulance in India: **108**)
- **Australia**: Call **000**

**Immediate Safety Actions:**
1. Stop any strenuous activity and sit or lie down in a safe position.
2. If experiencing severe chest pain, shortness of breath, or sudden weakness/numbness, have someone stay with you and call emergency services right away.
3. If this is a mental health crisis, free confidential help is available 24/7 by calling or texting **988**.

*Do not rely on this app or online advice for emergencies.*""",
        "category": "emergency",
        "suggestions": ["Emergency First Aid Info", "Nearest Hospital Protocol", "Calm Breathing Technique"]
    }

# Comprehensive Knowledge Base
KNOWLEDGE_BASE = [
    {
        "intent": "headache",
        "keywords": ["headache", "migraine", "head ache", "head hurts", "throbbing head", "head pain", "temple pain"],
        "title": "Headache Relief & Care",
        "response": """### 💆 Managing Headaches & Migraines

Headaches are often caused by dehydration, screen fatigue, stress, tension, or lack of sleep.

**Quick Relief Strategies:**
1. **Hydrate immediately**: Drink a tall glass (300-500ml) of cool water or an electrolyte beverage.
2. **Dim lights & reduce screen exposure**: Step away from monitors and smartphones; rest in a dark, quiet room.
3. **Cold or Warm Compress**:
   - *Tension headache*: Apply a warm towel to your neck or shoulders to release muscle tightness.
   - *Migraine/Throbbing*: Place an ice pack wrapped in a cloth on your forehead or temples.
4. **Gentle neck & shoulder stretches**: Roll your shoulders back and gently tilt your head side to side.
5. **Acupressure**: Gently massage the webbing between your thumb and index finger (LI4 point) for 1–2 minutes.

⚠️ **When to see a doctor**: If your headache is sudden and unusually severe ("thunderclap"), accompanied by fever, stiff neck, confusion, vision loss, or follows a head injury.""",
        "suggestions": ["How much water should I drink?", "Tips for better sleep", "Neck and shoulder stretches", "Stress relief methods"]
    },
    {
        "intent": "cold_flu",
        "keywords": ["cold", "flu", "cough", "sore throat", "sneezing", "runny nose", "stuffy nose", "congested", "congestion", "phlegm", "mucus"],
        "title": "Cold, Flu & Sore Throat Care",
        "response": """### 🍵 Soothing Cold, Flu & Throat Irritation

Common colds and flu are viral infections. The primary goal is relieving symptoms and giving your immune system rest.

**Evidence-Based Home Care:**
1. **Warm Saltwater Gargle**: Mix 1/2 teaspoon of salt in warm water and gargle for 30 seconds 3–4 times daily to reduce throat inflammation.
2. **Honey & Warm Fluids**: Drink warm water, chamomile, or ginger tea with 1–2 teaspoons of honey (honey coats and soothes mucosal lining).
3. **Steam Inhalation**: Inhale warm steam over a bowl of hot water or take a warm shower to clear congested nasal passages.
4. **Hydration & Electrolytes**: Aim for 2.5–3 liters of fluids (warm broths, water, herbal teas) to thin mucus.
5. **Elevate Your Head**: Use an extra pillow while sleeping to reduce post-nasal drip and coughing fits.

⚠️ **When to consult a doctor**: If you experience high fever lasting over 3 days, difficulty swallowing, ear pain, or chest tightness.""",
        "suggestions": ["Foods that boost immunity", "Fever management tips", "Herbal teas for wellness", "Sleep tips when sick"]
    },
    {
        "intent": "fever",
        "keywords": ["fever", "high temperature", "chills", "feeling hot", "feverish", "body temperature"],
        "title": "Fever Management & Monitoring",
        "response": """### 🌡️ Fever Management & Care

A fever is your body's natural defense mechanism fighting off infection. 

**Safe Steps to Manage a Mild Fever:**
1. **Stay Well Hydrated**: Fevers increase fluid loss. Drink water, oral rehydration solutions (ORS), coconut water, or clear soups.
2. **Dress in Light Clothing**: Avoid heavy blankets or bundling up, which traps heat and drives body temperature higher.
3. **Rest Actively**: Avoid exercise and strenuous physical work to let your immune system direct energy toward recovery.
4. **Lukewarm Sponge Bath**: If uncomfortable, use a washcloth with lukewarm (not freezing cold) water on your forehead and wrists.
5. **Monitor Temperature**: Keep a log of temperature readings every 3–4 hours.

⚠️ **Medical Advisory**: Seek medical care immediately if adult temperature exceeds 103°F (39.4°C), if fever lasts longer than 3 days, or if accompanied by a rash, severe stiff neck, or difficulty breathing.""",
        "suggestions": ["Hydration guidelines", "Cold and flu remedies", "Healthy foods to eat during fever"]
    },
    {
        "intent": "stomach_digestion",
        "keywords": ["stomach", "stomach ache", "belly", "acidity", "indigestion", "bloating", "bloated", "nausea", "gas", "constipation", "diarrhea", "cramps", "heartburn"],
        "title": "Digestive Health & Stomach Comfort",
        "response": """### 🌿 Calming Digestive Discomfort

Stomach upset, gas, and indigestion are commonly triggered by dietary choices, stress, or fast eating.

**Practical Steps for Relief:**
1. **Sip Herbal Tea**: Peppermint, ginger, or fennel tea naturally relaxes digestive tract muscles and eases bloating/nausea.
2. **Follow the BRAT Diet** (for loose stomach/nausea): Bananas, Rice (white), Applesauce, and Toast. These are gentle and easy to digest.
3. **Avoid Common Irritants**: Cut back on spicy foods, deep-fried snacks, dairy, carbonated sodas, and excess caffeine while your stomach heals.
4. **Stay Upright**: Do not lie flat immediately after eating. Wait at least 2–3 hours after meals before lying down to prevent acid reflux.
5. **Gentle Walking**: A 10-minute slow walk aids gastric motility and relieves gas pressure.
6. **For Constipation**: Increase dietary fiber (chia seeds, oats, prunes, leafy greens) and drink ample warm water.

⚠️ **When to seek medical attention**: Severe persistent abdominal pain, vomiting blood, black/tarry stools, or inability to keep fluids down for 24 hours.""",
        "suggestions": ["Gut-friendly foods and probiotics", "How much water to drink daily", "Healthy meal ideas", "Stress and digestion link"]
    },
    {
        "intent": "water_hydration",
        "keywords": ["water", "hydration", "drink water", "how much water", "dehydration", "thirsty", "fluid intake"],
        "title": "Hydration Guidelines",
        "response": """### 💧 Healthy Hydration Essentials

Proper hydration fuels cognitive performance, joint lubrication, kidney function, and healthy skin.

**Daily Hydration Targets:**
- **General baseline**: 2.5 to 3.5 Liters (approx. 8–12 glasses) daily for adults.
- **Physical activity & warm weather**: Add 500–700 ml for every hour of moderate-to-intense exercise.

**Smart Hydration Tips:**
1. **Morning Kickstart**: Drink a glass of water first thing upon waking to rehydrate after 7-8 hours of sleep.
2. **Check Your Urine**: Pale straw or transparent yellow indicates optimal hydration; dark amber signals you need water.
3. **Infuse for Flavor**: Add lemon, mint leaves, or cucumber slices if plain water feels boring.
4. **Water-Rich Foods**: Watermelon, cucumbers, oranges, tomatoes, and celery contribute up to 20% of your daily fluid intake.

*Use our built-in Water Tracker in the Dashboard tab to monitor your cups today!*""",
        "suggestions": ["Go to Water Tracker", "Calculate daily water needs", "Benefits of green tea", "Electrolyte balance"]
    },
    {
        "intent": "sleep_insomnia",
        "keywords": ["sleep", "insomnia", "can't sleep", "trouble sleeping", "tired", "wake up", "exhausted", "fatigue", "sleep quality", "sleep hygiene"],
        "title": "Sleep Hygiene & Restorative Rest",
        "response": """### 🌙 Blueprint for Better Sleep

Quality sleep (7 to 9 hours nightly) is the cornerstone of cellular repair, hormone balance, and brain function.

**Sleep Hygiene Protocol:**
1. **The 3-2-1 Rule**:
   - **3 hours before bed**: Stop heavy meals and alcohol.
   - **2 hours before bed**: Stop work tasks and intense discussions.
   - **1 hour before bed**: Turn off blue-light screens (phones, TVs, laptops).
2. **Consistent Sleep Schedule**: Go to bed and wake up at the exact same time every day, even on weekends.
3. **Optimize the Sleep Sanctuary**: Keep your bedroom dark, quiet, and cool (around 65°F / 18°C is ideal).
4. **Caffeine Curfew**: Avoid coffee, energy drinks, and black tea after 2:00 PM (caffeine has a 5-6 hour half-life).
5. **Relaxation Ritual**: Try 10 minutes of reading a physical book, progressive muscle relaxation, or gentle breathing exercises.

*Try logging your sleep hours in the Health Dashboard tab to track trends!*""",
        "suggestions": ["4-7-8 Breathing Technique", "Stress relief methods", "Morning routine habits", "Calculate ideal sleep needs"]
    },
    {
        "intent": "stress_anxiety",
        "keywords": ["stress", "stressed", "anxiety", "anxious", "panic", "overwhelmed", "mental health", "nervous", "tension", "worry", "calm"],
        "title": "Stress & Anxiety Relief",
        "response": """### 🧘 Calming Stress & Anxiety in the Moment

When stress strikes, your sympathetic nervous system ("fight or flight") elevates your heart rate and cortisol levels. You can intentionally engage your parasympathetic nervous system to slow down.

**Instant Grounding Techniques:**
1. **The 4-7-8 Breathing Method**:
   - Inhale quietly through your nose for **4 seconds**.
   - Hold your breath gently for **7 seconds**.
   - Exhale completely through your mouth with a whoosh for **8 seconds**.
   - Repeat 4 cycles.
2. **The 5-4-3-2-1 Sensory Grounding**:
   - Acknowledge **5** things you can see around you.
   - Acknowledge **4** things you can physically touch.
   - Acknowledge **3** sounds you hear.
   - Acknowledge **2** things you can smell.
   - Acknowledge **1** positive thing about yourself or what you can taste.
3. **Physical Release**: Go for a brisk 15-minute walk outside in nature or do 5 minutes of gentle stretches.
4. **Expressive Writing**: Write down your worries in a notebook to empty mental clutter.

*Remember: It is okay to ask for professional counseling. Mental health is just as vital as physical health.*""",
        "suggestions": ["Tips for better sleep", "Healthy daily habits", "Desk stretches for tension", "How exercise reduces stress"]
    },
    {
        "intent": "nutrition_diet",
        "keywords": ["diet", "food", "nutrition", "eat healthy", "weight loss", "lose weight", "gain weight", "protein", "carbs", "calories", "sugar", "meal", "breakfast", "lunch", "dinner", "snack"],
        "title": "Healthy Nutrition & Balanced Diet",
        "response": """### 🥗 Foundations of Balanced Nutrition

A sustainable, nourishing diet is built on whole foods rather than restrictive fad diets.

**The Healthy Plate Model:**
- **1/2 Plate Vegetables & Fruits**: Colorful greens, broccoli, carrots, berries, and peppers (rich in antioxidants & fiber).
- **1/4 Plate Lean Protein**: Eggs, lentils, tofu, beans, chicken breast, fish, or Greek yogurt.
- **1/4 Plate Whole Grains**: Quinoa, brown rice, rolled oats, sweet potatoes, or whole-wheat bread.
- **Healthy Fats**: A small thumb-sized portion of olive oil, avocado, chia seeds, almonds, or walnuts.

**Smart Nutritional Rules:**
1. **Prioritize Protein**: 1.2 to 1.8g per kg of body weight if active; protein boosts satiety and maintains lean muscle.
2. **Limit Ultra-Processed Foods**: Minimize sugary beverages, deep-fried snacks, and refined flours.
3. **Eat Mindfully**: Chew thoroughly and eat without screens to register natural fullness cues.

*Check your BMI and daily caloric estimate in the Calculators tab!*""",
        "suggestions": ["Calculate my BMI", "Calculate daily calorie & water needs", "Healthy breakfast ideas", "Gut health foods"]
    },
    {
        "intent": "fitness_exercise",
        "keywords": ["exercise", "workout", "fitness", "gym", "cardio", "weights", "walking", "running", "steps", "active", "sedentary", "stretching", "posture"],
        "title": "Fitness, Movement & Posture",
        "response": """### 🏃 Building an Active & Healthy Body

Regular movement reduces cardiovascular risk, strengthens bones, improves mood, and enhances longevity.

**Weekly Exercise Recommendations:**
- **Aerobic / Cardio**: At least 150 minutes of moderate activity (e.g. brisk walking, cycling, swimming) or 75 minutes of vigorous activity weekly.
- **Strength Training**: 2 to 3 sessions per week targeting major muscle groups (legs, back, chest, core).
- **Daily Steps Target**: Aim for 7,000 to 10,000 steps daily.

**Desk Worker Posture Tips:**
1. **The 20-20-20 Rule**: Every 20 minutes, look at an object 20 feet away for at least 20 seconds to ease eye strain.
2. **Ergonomic Setup**: Keep your monitor at eye level, elbows at 90 degrees, and feet flat on the floor.
3. **Chest Opener Stretch**: Clasp hands behind your back and gently lift your chest upward to reverse slouching.

*Log your steps and activity in the Health Dashboard tab!*""",
        "suggestions": ["Beginner home workout routine", "Neck and back stretches", "How to reach 10,000 steps", "Post-workout recovery tips"]
    },
    {
        "intent": "bp_hypertension",
        "keywords": ["blood pressure", "hypertension", "bp", "systolic", "diastolic", "high blood pressure", "low blood pressure"],
        "title": "Blood Pressure & Heart Health",
        "response": """### ❤️ Understanding Blood Pressure & Cardiovascular Health

Blood pressure measures the force of circulating blood against the walls of your arteries.

**Standard Adult BP Categories (AHA Guidelines):**
- **Normal**: Systolic < 120 AND Diastolic < 80 mm Hg
- **Elevated**: Systolic 120–129 AND Diastolic < 80 mm Hg
- **Stage 1 Hypertension**: Systolic 130–139 OR Diastolic 80–89 mm Hg
- **Stage 2 Hypertension**: Systolic 140+ OR Diastolic 90+ mm Hg
- **Hypertensive Crisis**: Systolic > 180 and/or Diastolic > 120 mm Hg *(Seek emergency care immediately)*

**Lifestyle Measures to Support Healthy BP:**
1. **Reduce Sodium**: Aim for under 2,000 mg of sodium daily; avoid heavily processed foods and salty snacks.
2. **Boost Potassium**: Eat potassium-rich foods like bananas, spinach, avocado, sweet potatoes, and beans.
3. **DASH Diet Principles**: Emphasize fruits, vegetables, whole grains, and lean proteins.
4. **Manage Stress**: Daily deep breathing and moderate walking have proven clinical benefits in lowering resting pressure.

*You can test your reading in the Blood Pressure tool in the Calculators tab!*""",
        "suggestions": ["Go to BP Category Checker", "Heart-healthy diet tips", "Stress reduction techniques", "Benefits of daily walking"]
    },
    {
        "intent": "skin_care",
        "keywords": ["skin", "acne", "sunscreen", "dry skin", "eczema", "rash", "dermatology", "sunburn", "glowing skin"],
        "title": "Daily Skin Health & Protection",
        "response": """### 🧴 Skin Wellness & Protection

Skin is your body's largest organ and protective barrier.

**Core 3-Step Skincare Routine:**
1. **Cleanse**: Wash your face gently with a mild, non-stripping cleanser morning and night.
2. **Moisturize**: Apply a hydrating moisturizer containing ceramides, hyaluronic acid, or glycerin while skin is slightly damp.
3. **Sunscreen (SPF 30+)**: Apply broad-spectrum sunscreen every single morning, rain or shine. UV radiation causes up to 80% of premature skin aging and elevates skin cancer risk.

**Internal Habits for Clear Skin:**
- Drink 2.5+ liters of water daily.
- Limit high-glycemic foods and excess dairy if you notice acne breakouts.
- Change pillowcases weekly and avoid touching your face with unwashed hands.""",
        "suggestions": ["Hydration guidelines", "Antioxidant-rich foods", "Tips for better sleep"]
    },
    {
        "intent": "general_greetings",
        "keywords": ["hello", "hi", "hey", "good morning", "good evening", "good afternoon", "greetings", "how are you", "who are you", "what can you do", "help"],
        "title": "Welcome to CareBot",
        "response": """### 👋 Hello! I'm CareBot, Your Health Companion

I'm here to support your everyday health and wellness journey! You can talk to me about:

- 🩺 **Common Symptoms**: Headaches, sore throat, cold, cough, mild fever, digestion issues.
- 🥗 **Nutrition & Diet**: Balanced meal plans, healthy snacking, weight management.
- 💧 **Hydration & Detox**: Daily water goals, fluid balance, electrolytes.
- 🌙 **Sleep & Rest**: Overcoming insomnia, sleep hygiene, wind-down habits.
- 🧘 **Stress & Mental Wellbeing**: Breathing techniques, anxiety relief, grounding exercises.
- 🏃 **Fitness & Posture**: Home workouts, desk ergonomics, daily step habits.

*How are you feeling today? Tap one of the suggestions below or ask any health question!*""",
        "suggestions": ["Tips for better sleep", "Relief for tension headache", "How much water should I drink?", "Healthy breakfast ideas"]
    },
    {
        "intent": "gratitude",
        "keywords": ["thank you", "thanks", "thank u", "thx", "appreciate it", "great help", "awesome", "good job"],
        "title": "You're Welcome!",
        "response": """### 😊 You're Very Welcome!

I'm always here to help you stay healthy, energized, and informed. 

Remember: small healthy choices made every day—drinking an extra glass of water, taking a 10-minute walk, getting good rest—add up to lifelong vitality!

Feel free to check out the **Dashboard** to log your water and steps, or ask any other health questions!""",
        "suggestions": ["Log daily water intake", "Calculate BMI", "Stress relief techniques", "Foods that boost immunity"]
    }
]

def generate_health_response(user_message: str):
    """
    Intelligently analyzes user query, detects emergency red flags,
    matches health intents, and crafts evidence-backed responses.
    """
    clean_msg = user_message.strip()
    if not clean_msg:
        return {
            "text": "Please share what health or wellness question you'd like to discuss!",
            "category": "prompt",
            "suggestions": ["Tips for better sleep", "How much water should I drink?", "Relief for tension headache", "Healthy diet tips"]
        }
    
    # 1. Emergency check
    if check_emergency(clean_msg):
        return get_emergency_response()
    
    clean_msg_lower = clean_msg.lower()
    
    # 2. Score matching intents
    best_match = None
    highest_score = 0
    
    for item in KNOWLEDGE_BASE:
        score = 0
        for kw in item["keywords"]:
            # Word boundary search
            pattern = r"\b" + re.escape(kw) + r"\b"
            if re.search(pattern, clean_msg_lower):
                score += len(kw.split()) * 3  # multi-word keywords weighted higher
            elif kw in clean_msg_lower:
                score += 1
                
        if score > highest_score:
            highest_score = score
            best_match = item
            
    if best_match and highest_score > 0:
        return {
            "text": best_match["response"],
            "category": best_match["intent"],
            "suggestions": best_match["suggestions"]
        }
        
    # 3. Fallback / General wellness response
    return {
        "text": f"""### 🩺 Wellness Insights on Your Query

Thank you for asking about **"{clean_msg}"**.

While I might not have a specific protocol for that exact phrasing, here are fundamental principles for supporting your body:

1. **Hydration & Nutrition**: Drink plenty of clean water and fuel your body with colorful vegetables, fruits, and lean protein.
2. **Rest & Recovery**: Ensure 7–8 hours of undisturbed sleep; sleep is when your immune system and tissues regenerate.
3. **Listen to Your Body**: Track symptom duration, severity, and any triggers (foods, screen time, stress).
4. **Professional Guidance**: If this is a persistent or worsening condition, speaking with a licensed doctor or healthcare professional is always the safest course of action.

Would you like to explore any of these specific areas?""",
        "category": "general_wellness",
        "suggestions": [
            "Tips for better sleep",
            "Relief for tension headache",
            "How much water should I drink?",
            "Healthy meal ideas",
            "Stress & anxiety relief"
        ]
    }
