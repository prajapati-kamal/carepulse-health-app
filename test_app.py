import unittest
import json
import os
import database
import chatbot_engine
from app import app

class TestHealthApp(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        database.init_db()

    # --- CHATBOT TESTS ---
    def test_chatbot_engine_headache(self):
        res = chatbot_engine.generate_health_response("I have a bad headache, what can I do?")
        self.assertIn("Headache", res["text"])
        self.assertEqual(res["category"], "headache")
        self.assertGreater(len(res["suggestions"]), 0)

    def test_chatbot_engine_cold(self):
        res = chatbot_engine.generate_health_response("I am coughing and have a sore throat")
        self.assertIn("Cold", res["text"])
        self.assertEqual(res["category"], "cold_flu")

    def test_chatbot_engine_water(self):
        res = chatbot_engine.generate_health_response("How much water should I drink daily?")
        self.assertIn("Hydration", res["text"])
        self.assertEqual(res["category"], "water_hydration")

    def test_chatbot_engine_emergency(self):
        res = chatbot_engine.generate_health_response("I am having severe chest pain and cannot breathe")
        self.assertEqual(res["category"], "emergency")
        self.assertIn("URGENT MEDICAL NOTICE", res["text"])
        self.assertIn("911", res["text"])

    # --- CALCULATOR TESTS ---
    def test_bmi_calculator(self):
        # 175cm, 70kg -> BMI ~ 22.9 (Normal)
        response = self.client.post("/api/calculator/bmi", json={
            "height_cm": 175,
            "weight_kg": 70
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertAlmostEqual(data["bmi"], 22.9, places=1)
        self.assertEqual(data["category"], "Normal / Healthy Weight")

    def test_water_calorie_calculator(self):
        response = self.client.post("/api/calculator/water-calorie", json={
            "weight_kg": 70,
            "age": 28,
            "gender": "male",
            "activity": "moderate"
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertGreater(data["recommended_water_ml"], 2000)
        self.assertGreater(data["estimated_daily_calories"], 1500)

    def test_blood_pressure_calculator(self):
        # Normal BP
        res_normal = self.client.post("/api/calculator/bp", json={"systolic": 118, "diastolic": 76})
        self.assertEqual(res_normal.status_code, 200)
        self.assertEqual(res_normal.get_json()["stage"], "Normal Blood Pressure")

        # Stage 2 Hypertension
        res_stage2 = self.client.post("/api/calculator/bp", json={"systolic": 145, "diastolic": 92})
        self.assertEqual(res_stage2.status_code, 200)
        self.assertEqual(res_stage2.get_json()["stage"], "Stage 2 Hypertension")

    # --- TRACKER API TESTS ---
    def test_tracker_api(self):
        # GET tracker
        res_get = self.client.get("/api/tracker")
        self.assertEqual(res_get.status_code, 200)
        
        # POST update water and steps
        res_post = self.client.post("/api/tracker", json={
            "water_ml": 1250,
            "steps": 4500,
            "sleep_hours": 8.0,
            "mood": "great"
        })
        self.assertEqual(res_post.status_code, 200)
        data = res_post.get_json()
        self.assertEqual(data["water_ml"], 1250)
        self.assertEqual(data["steps"], 4500)
        self.assertEqual(data["sleep_hours"], 8.0)
        self.assertEqual(data["mood"], "great")

    # --- MEDICATION API TESTS ---
    def test_medication_crud(self):
        # Add medication
        res_add = self.client.post("/api/medications", json={
            "name": "Vitamin C",
            "dosage": "500mg",
            "time": "09:00"
        })
        self.assertEqual(res_add.status_code, 201)
        med_id = res_add.get_json()["id"]

        # Toggle medication
        res_toggle = self.client.post(f"/api/medications/{med_id}/toggle")
        self.assertEqual(res_toggle.status_code, 200)
        self.assertEqual(res_toggle.get_json()["is_taken"], 1)

        # Delete medication
        res_del = self.client.delete(f"/api/medications/{med_id}")
        self.assertEqual(res_del.status_code, 200)

    # --- CHAT API TESTS ---
    def test_chat_api(self):
        res = self.client.post("/api/chat", json={"message": "What should I eat for breakfast?"})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue("reply" in data)
        self.assertTrue(len(data["suggestions"]) > 0)

        # Chat history
        hist_res = self.client.get("/api/chat/history")
        self.assertEqual(hist_res.status_code, 200)
        self.assertGreater(len(hist_res.get_json()["history"]), 0)

    # --- INDEX PAGE TEST ---
    def test_index_page(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"CarePulse", res.data)

if __name__ == "__main__":
    unittest.main()
