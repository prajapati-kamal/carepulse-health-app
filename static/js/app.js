/**
 * CarePulse - Health App & Health Chatbot Frontend Logic
 */

document.addEventListener("DOMContentLoaded", () => {
    initNavigation();
    initCurrentDate();
    loadChatHistory();
    loadTrackerData();
    loadMedications();
    loadWellnessArticles();
});

// ================= NAVIGATION =================

function initNavigation() {
    const navItems = document.querySelectorAll(".nav-item");
    const tabPanes = document.querySelectorAll(".tab-pane");

    navItems.forEach(item => {
        item.addEventListener("click", () => {
            const targetTab = item.getAttribute("data-tab");

            navItems.forEach(n => n.classList.remove("active"));
            tabPanes.forEach(p => p.classList.remove("active"));

            item.classList.add("active");
            const activePane = document.getElementById(`tab-${targetTab}`);
            if (activePane) {
                activePane.classList.add("active");
            }
        });
    });
}

function initCurrentDate() {
    const options = { weekday: "short", month: "short", day: "numeric", year: "numeric" };
    const dateStr = new Date().toLocaleDateString("en-US", options);
    const dateEl = document.getElementById("currentDateDisplay");
    if (dateEl) {
        dateEl.textContent = dateStr;
    }
}

// ================= CHATBOT =================

async function loadChatHistory() {
    try {
        const res = await fetch("/api/chat/history");
        if (!res.ok) return;
        const data = await res.json();
        
        if (data.history && data.history.length > 0) {
            const chatMessages = document.getElementById("chatMessages");
            chatMessages.innerHTML = ""; // Replace default welcome if history exists
            data.history.forEach(item => {
                appendChatMessage(item.role === "user" ? "user" : "bot", item.message, false);
            });
            scrollToBottom();
        }
    } catch (e) {
        console.warn("Could not load chat history:", e);
    }
}

async function handleChatSubmit(e) {
    e.preventDefault();
    const chatInput = document.getElementById("chatInput");
    const message = chatInput.value.trim();
    if (!message) return;

    // Append User Message
    appendChatMessage("user", message);
    chatInput.value = "";

    // Show Typing Indicator
    const typingIndicator = document.getElementById("typingIndicator");
    typingIndicator.style.display = "flex";
    scrollToBottom();

    try {
        const res = await fetch("/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message })
        });

        const data = await res.json();
        typingIndicator.style.display = "none";

        if (res.ok) {
            const isEmergency = data.category === "emergency";
            appendChatMessage("bot", data.reply, true, data.suggestions, isEmergency);
        } else {
            appendChatMessage("bot", "⚠️ Sorry, I encountered an issue processing your request. Please try again.", true);
        }
    } catch (err) {
        typingIndicator.style.display = "none";
        appendChatMessage("bot", "⚠️ Connection error. Please check your connection and try again.", true);
    }

    scrollToBottom();
}

function sendQuickPrompt(promptText) {
    const chatInput = document.getElementById("chatInput");
    chatInput.value = promptText;
    const chatForm = document.getElementById("chatForm");
    chatForm.dispatchEvent(new Event("submit"));
}

function appendChatMessage(sender, text, animate = true, suggestions = [], isEmergency = false) {
    const chatMessages = document.getElementById("chatMessages");
    const msgDiv = document.createElement("div");
    msgDiv.className = `message ${sender === "user" ? "user-msg" : "bot-msg"}`;

    const avatarDiv = document.createElement("div");
    avatarDiv.className = "msg-avatar";
    avatarDiv.textContent = sender === "user" ? "👤" : "🤖";

    const contentDiv = document.createElement("div");
    contentDiv.className = "msg-content";
    if (isEmergency) {
        contentDiv.classList.add("msg-emergency");
    }

    // Format Markdown-like text (headers, bold, bullet points)
    contentDiv.innerHTML = formatMarkdown(text);

    // If bot has suggested quick replies, append them
    if (sender === "bot" && suggestions && suggestions.length > 0) {
        const suggContainer = document.createElement("div");
        suggContainer.className = "msg-suggestions";
        suggestions.forEach(sug => {
            const btn = document.createElement("button");
            btn.className = "suggestion-pill";
            btn.textContent = sug;
            btn.onclick = () => sendQuickPrompt(sug);
            suggContainer.appendChild(btn);
        });
        contentDiv.appendChild(suggContainer);
    }

    msgDiv.appendChild(avatarDiv);
    msgDiv.appendChild(contentDiv);
    chatMessages.appendChild(msgDiv);
}

function formatMarkdown(text) {
    if (!text) return "";
    let formatted = text
        // Headers
        .replace(/^### (.*$)/gim, "<h3>$1</h3>")
        .replace(/^## (.*$)/gim, "<h2>$1</h2>")
        .replace(/^# (.*$)/gim, "<h1>$1</h1>")
        // Bold
        .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
        // Italic
        .replace(/\*(.*?)\*/g, "<em>$1</em>")
        // Newlines
        .replace(/\n\n/g, "</p><p>")
        .replace(/\n/g, "<br>");

    return `<p>${formatted}</p>`;
}

function scrollToBottom() {
    const chatMessages = document.getElementById("chatMessages");
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

async function clearChat() {
    if (!confirm("Are you sure you want to clear the chat history?")) return;
    try {
        await fetch("/api/chat/clear", { method: "POST" });
        const chatMessages = document.getElementById("chatMessages");
        chatMessages.innerHTML = `
            <div class="message bot-msg">
                <div class="msg-avatar">🤖</div>
                <div class="msg-content">
                    <p><strong>Chat cleared!</strong> How can I help you with your health today?</p>
                </div>
            </div>
        `;
        showToast("Chat history cleared");
    } catch (e) {
        showToast("Failed to clear chat");
    }
}

// ================= DAILY TRACKER =================

let currentTracker = {
    water_ml: 0,
    water_goal_ml: 2500,
    steps: 0,
    step_goal: 8000,
    sleep_hours: 7.5,
    mood: "good"
};

async function loadTrackerData() {
    try {
        const res = await fetch("/api/tracker");
        if (!res.ok) return;
        currentTracker = await res.json();
        renderTrackerUI();
    } catch (e) {
        console.warn("Error loading tracker:", e);
    }
}

function renderTrackerUI() {
    // Water
    const waterCount = document.getElementById("waterCount");
    const waterGoal = document.getElementById("waterGoal");
    const waterProgress = document.getElementById("waterProgress");
    
    if (waterCount) waterCount.textContent = currentTracker.water_ml;
    if (waterGoal) waterGoal.textContent = currentTracker.water_goal_ml;
    
    const waterPct = Math.min(100, Math.round((currentTracker.water_ml / currentTracker.water_goal_ml) * 100));
    if (waterProgress) waterProgress.style.width = `${waterPct}%`;

    renderWaterCups();

    // Steps
    const stepCount = document.getElementById("stepCount");
    const stepGoal = document.getElementById("stepGoal");
    const stepProgress = document.getElementById("stepProgress");
    
    if (stepCount) stepCount.textContent = currentTracker.steps.toLocaleString();
    if (stepGoal) stepGoal.textContent = currentTracker.step_goal.toLocaleString();
    
    const stepPct = Math.min(100, Math.round((currentTracker.steps / currentTracker.step_goal) * 100));
    if (stepProgress) stepProgress.style.width = `${stepPct}%`;

    // Sleep
    const sleepDisplay = document.getElementById("sleepDisplay");
    const sleepSlider = document.getElementById("sleepSlider");
    const sliderLabel = document.getElementById("sliderValueLabel");
    
    if (sleepDisplay) sleepDisplay.textContent = currentTracker.sleep_hours.toFixed(1);
    if (sleepSlider) sleepSlider.value = currentTracker.sleep_hours;
    if (sliderLabel) sliderLabel.textContent = `${currentTracker.sleep_hours.toFixed(1)} hrs`;

    // Mood
    highlightMood(currentTracker.mood);
}

function renderWaterCups() {
    const container = document.getElementById("waterCupsVisual");
    if (!container) return;
    container.innerHTML = "";

    const totalCups = Math.ceil(currentTracker.water_goal_ml / 250); // e.g. 10 cups for 2500ml
    const filledCups = Math.floor(currentTracker.water_ml / 250);

    for (let i = 0; i < totalCups; i++) {
        const cup = document.createElement("div");
        cup.className = `cup-item ${i < filledCups ? "filled" : ""}`;
        cup.title = `Cup ${i + 1} (250 ml)`;
        cup.textContent = i < filledCups ? "💧" : `${i + 1}`;
        cup.onclick = () => {
            const targetAmount = (i + 1) * 250;
            saveTrackerUpdate({ water_ml: targetAmount });
        };
        container.appendChild(cup);
    }
}

async function addWater(amount) {
    const newTotal = currentTracker.water_ml + amount;
    await saveTrackerUpdate({ water_ml: newTotal });
    showToast(`Added +${amount} ml water! 💧`);
}

async function resetWater() {
    await saveTrackerUpdate({ water_ml: 0 });
    showToast("Water tracker reset for today");
}

async function saveSteps() {
    const stepInput = document.getElementById("stepInput");
    const val = parseInt(stepInput.value, 10);
    if (isNaN(val) || val < 0) {
        showToast("Please enter a valid step number");
        return;
    }
    await saveTrackerUpdate({ steps: val });
    stepInput.value = "";
    showToast(`Steps updated to ${val.toLocaleString()}! 👟`);
}

async function addSteps(amount) {
    const newSteps = currentTracker.steps + amount;
    await saveTrackerUpdate({ steps: newSteps });
    showToast(`Added +${amount.toLocaleString()} steps! 👟`);
}

function updateSleepSliderLabel(val) {
    const label = document.getElementById("sliderValueLabel");
    if (label) {
        label.textContent = `${parseFloat(val).toFixed(1)} hrs`;
    }
}

async function saveSleep() {
    const sleepSlider = document.getElementById("sleepSlider");
    const val = parseFloat(sleepSlider.value);
    await saveTrackerUpdate({ sleep_hours: val });
    showToast(`Sleep logged: ${val.toFixed(1)} hours! 🌙`);
}

function highlightMood(mood) {
    const moodBtns = document.querySelectorAll(".mood-btn");
    moodBtns.forEach(btn => btn.classList.remove("active"));

    const moodNames = {
        great: "Great 😄",
        good: "Good 🙂",
        tired: "Tired 🥱",
        stressed: "Stressed 😰",
        sick: "Unwell 🤒"
    };

    const tips = {
        great: "You're feeling wonderful! Maintain high energy with nutritious meals and positive vibes.",
        good: "Feeling good today! Keep the steady momentum going with healthy hydration.",
        tired: "Feeling fatigued? Take a 15-minute power nap or wind down earlier tonight.",
        stressed: "High stress detected. Try the 4-7-8 breathing exercise or a calming walk.",
        sick: "Not feeling well? Rest up, drink warm fluids, and monitor your symptoms closely."
    };

    const badge = document.getElementById("currentMoodBadge");
    if (badge && moodNames[mood]) {
        badge.textContent = moodNames[mood];
    }

    const tipEl = document.getElementById("moodTip");
    if (tipEl && tips[mood]) {
        tipEl.textContent = tips[mood];
    }
}

async function selectMood(moodKey, displayName) {
    highlightMood(moodKey);
    await saveTrackerUpdate({ mood: moodKey });
    showToast(`Mood recorded: ${displayName}`);
}

async function saveTrackerUpdate(updateObj) {
    try {
        const res = await fetch("/api/tracker", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(updateObj)
        });
        if (res.ok) {
            currentTracker = await res.json();
            renderTrackerUI();
        }
    } catch (e) {
        console.error("Error saving tracker update:", e);
    }
}

// ================= CALCULATORS =================

async function calculateBMI(e) {
    e.preventDefault();
    const height_cm = document.getElementById("bmiHeight").value;
    const weight_kg = document.getElementById("bmiWeight").value;

    try {
        const res = await fetch("/api/calculator/bmi", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ height_cm, weight_kg })
        });

        const data = await res.json();
        if (!res.ok) {
            showToast(data.error || "Calculation failed");
            return;
        }

        const resultBox = document.getElementById("bmiResult");
        const bmiVal = document.getElementById("bmiVal");
        const bmiCategoryBadge = document.getElementById("bmiCategoryBadge");
        const bmiIdealRange = document.getElementById("bmiIdealRange");
        const bmiAdvice = document.getElementById("bmiAdvice");

        resultBox.style.display = "block";
        bmiVal.textContent = data.bmi;
        bmiCategoryBadge.textContent = data.category;
        bmiCategoryBadge.style.backgroundColor = data.color;
        bmiIdealRange.textContent = `${data.min_ideal_weight} kg – ${data.max_ideal_weight} kg`;
        bmiAdvice.textContent = data.advice;

    } catch (err) {
        showToast("Calculation error");
    }
}

async function calculateWaterCal(e) {
    e.preventDefault();
    const weight_kg = document.getElementById("wcWeight").value;
    const age = document.getElementById("wcAge").value;
    const gender = document.getElementById("wcGender").value;
    const activity = document.getElementById("wcActivity").value;

    try {
        const res = await fetch("/api/calculator/water-calorie", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ weight_kg, age, gender, activity })
        });

        const data = await res.json();
        if (!res.ok) {
            showToast(data.error || "Calculation failed");
            return;
        }

        const wcResult = document.getElementById("wcResult");
        wcResult.style.display = "block";

        document.getElementById("resWater").textContent = `${data.recommended_water_ml} ml`;
        document.getElementById("resCups").textContent = `approx. ${data.recommended_water_cups} glasses (250ml)`;
        document.getElementById("resCalories").textContent = `${data.estimated_daily_calories} kcal`;
        document.getElementById("resBMR").textContent = `Base Metabolic Rate (BMR): ${data.bmr} kcal`;

    } catch (err) {
        showToast("Calculation error");
    }
}

async function calculateBP(e) {
    e.preventDefault();
    const systolic = document.getElementById("bpSystolic").value;
    const diastolic = document.getElementById("bpDiastolic").value;

    try {
        const res = await fetch("/api/calculator/bp", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ systolic, diastolic })
        });

        const data = await res.json();
        if (!res.ok) {
            showToast(data.error || "Calculation failed");
            return;
        }

        const bpResult = document.getElementById("bpResult");
        bpResult.style.display = "block";

        document.getElementById("bpReadingVal").textContent = `${data.systolic} / ${data.diastolic} mm Hg`;
        const badge = document.getElementById("bpCategoryBadge");
        badge.textContent = data.stage;
        badge.style.backgroundColor = data.color;
        document.getElementById("bpAdvice").textContent = data.recommendation;

    } catch (err) {
        showToast("Calculation error");
    }
}

// ================= MEDICATIONS =================

async function loadMedications() {
    try {
        const res = await fetch("/api/medications");
        if (!res.ok) return;
        const data = await res.json();
        renderMedications(data.medications || []);
    } catch (e) {
        console.warn("Error loading medications:", e);
    }
}

function renderMedications(meds) {
    const medList = document.getElementById("medList");
    const progressCount = document.getElementById("medProgressCount");
    if (!medList) return;

    if (meds.length === 0) {
        medList.innerHTML = '<div class="empty-state">No medications or vitamins scheduled for today. Add one above!</div>';
        if (progressCount) progressCount.textContent = "0 of 0 taken";
        return;
    }

    const takenCount = meds.filter(m => m.is_taken === 1).length;
    if (progressCount) {
        progressCount.textContent = `${takenCount} of ${meds.length} taken`;
    }

    medList.innerHTML = "";
    meds.forEach(med => {
        const item = document.createElement("div");
        item.className = `med-item ${med.is_taken === 1 ? "taken" : ""}`;

        item.innerHTML = `
            <div class="med-item-left">
                <input type="checkbox" class="med-checkbox" ${med.is_taken === 1 ? "checked" : ""} onchange="toggleMed(${med.id})">
                <div class="med-info">
                    <h4>${escapeHtml(med.name)}</h4>
                    <span class="med-details">Dosage: ${escapeHtml(med.dosage || "Standard")} • Scheduled: ${formatTime(med.time)}</span>
                </div>
            </div>
            <button class="btn-delete-med" onclick="deleteMed(${med.id})" title="Delete Reminder">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M3 6h18"/>
                    <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/>
                    <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/>
                </svg>
            </button>
        `;
        medList.appendChild(item);
    });
}

async function handleAddMedication(e) {
    e.preventDefault();
    const nameInput = document.getElementById("medName");
    const dosageInput = document.getElementById("medDosage");
    const timeInput = document.getElementById("medTime");

    const name = nameInput.value.trim();
    const dosage = dosageInput.value.trim();
    const time = timeInput.value.trim();

    if (!name || !time) return;

    try {
        const res = await fetch("/api/medications", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, dosage, time })
        });

        if (res.ok) {
            nameInput.value = "";
            dosageInput.value = "";
            timeInput.value = "";
            loadMedications();
            showToast(`Added ${name} to schedule! 💊`);
        } else {
            showToast("Failed to add medication");
        }
    } catch (err) {
        showToast("Error adding medication");
    }
}

async function toggleMed(medId) {
    try {
        const res = await fetch(`/api/medications/${medId}/toggle`, { method: "POST" });
        if (res.ok) {
            loadMedications();
        }
    } catch (e) {
        showToast("Failed to update status");
    }
}

async function deleteMed(medId) {
    if (!confirm("Delete this medication reminder?")) return;
    try {
        const res = await fetch(`/api/medications/${medId}`, { method: "DELETE" });
        if (res.ok) {
            loadMedications();
            showToast("Medication deleted");
        }
    } catch (e) {
        showToast("Error deleting medication");
    }
}

function formatTime(time24) {
    if (!time24) return "";
    const [h, m] = time24.split(":");
    const hour = parseInt(h, 10);
    const ampm = hour >= 12 ? "PM" : "AM";
    const formattedHour = hour % 12 || 12;
    return `${formattedHour}:${m} ${ampm}`;
}

// ================= WELLNESS ARTICLES =================

async function loadWellnessArticles() {
    try {
        const res = await fetch("/api/wellness/articles");
        if (!res.ok) return;
        const data = await res.json();
        const container = document.getElementById("articlesGrid");
        if (!container) return;

        container.innerHTML = "";
        data.articles.forEach(art => {
            const card = document.createElement("div");
            card.className = "article-card";
            card.innerHTML = `
                <div class="article-top">
                    <span class="article-icon">${art.icon}</span>
                    <span class="article-cat">${escapeHtml(art.category)}</span>
                </div>
                <h4>${escapeHtml(art.title)}</h4>
                <p>${escapeHtml(art.summary)}</p>
                <div class="article-details">
                    💡 <strong>Action Tip:</strong> ${escapeHtml(art.details)}
                </div>
            `;
            container.appendChild(card);
        });
    } catch (e) {
        console.warn("Could not load wellness articles:", e);
    }
}

// ================= EMERGENCY MODAL & TOAST =================

function openEmergencyModal() {
    const modal = document.getElementById("emergencyModal");
    if (modal) modal.style.display = "flex";
}

function closeEmergencyModal() {
    const modal = document.getElementById("emergencyModal");
    if (modal) modal.style.display = "none";
}

document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeEmergencyModal();
});

let toastTimeout;
function showToast(message) {
    const toast = document.getElementById("toast");
    if (!toast) return;
    toast.textContent = message;
    toast.classList.add("show");
    clearTimeout(toastTimeout);
    toastTimeout = setTimeout(() => {
        toast.classList.remove("show");
    }, 2800);
}

function escapeHtml(text) {
    if (!text) return "";
    return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}
