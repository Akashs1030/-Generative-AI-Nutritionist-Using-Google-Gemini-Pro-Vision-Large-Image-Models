# 🥗 Calories Advisor App

An AI-powered **food image analysis application** that uses Google Gemini Vision to identify food items from a meal image and provide estimated calories and nutritional insights.

## 🚀 Features

* 📸 Upload meal images (`JPG`, `JPEG`, `PNG`)
* 🤖 AI-powered food recognition using Google Gemini
* 🔢 Estimated calories for individual food items
* 📊 Nutrition breakdown including carbohydrates, fats, sugar, and fibre
* 🥗 Healthiness assessment of the meal
* 🎨 Interactive Streamlit interface
* ⚡ Instant AI-generated nutrition report

## 🛠️ Tech Stack

* **Python**
* **Streamlit**
* **Google Gemini Vision**
* **PIL (Pillow)**
* **python-dotenv**

## 🔄 Workflow

```text
Meal Image
    ↓
Image Upload
    ↓
Gemini Vision Model
    ↓
Food Recognition
    ↓
Calorie & Nutrition Analysis
    ↓
Nutrition Report
```

## ⚙️ Installation

```bash
git clone <YOUR_REPOSITORY_URL>
cd Calories-Advisor-App
pip install -r requirements.txt
```

Create a `.env` file:

```env
GOOGLE_API_KEY=your_api_key
```

## ▶️ Run

```bash
streamlit run app.py
```

## 📌 Output

The application provides:

* Individual food items
* Estimated calories
* Overall calorie information
* Carbohydrate, fat, sugar & fibre split
* General healthiness assessment

> ⚠️ **Disclaimer:** AI-generated calorie and nutrition estimates are approximate and should not be considered professional medical or dietary advice.

## 🔮 Future Improvements

* Meal history tracking
* Daily calorie tracking
* Personalized meal recommendations
* Nutrition goal tracking
* Multiple meal comparison
* Improved nutritional database integration
