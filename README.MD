# **Machine Learning Crash Course: Cost of Living Prediction in Nairobi**

## **Lesson I: Building and Exposing Machine Learning Models via API**

## **📌 Overview**
This project is a machine learning crash course designed to teach you how to build a **time-series forecasting model** using **Random Forest Regressor** in Scikit-Learn. The model predicts the **monthly cost of living** in different areas of Nairobi, Kenya.

You'll learn how to:
- Run a machine learning model for time-series forecasting 📊
- Load and use the model via **FastAPI** 🌐
- Access the API in the browser and test endpoints 🖥️

📺 **Full Video Course**: [Watch here](https://youtu.be/N_F-Hw6RbVw?si=M9TeJj0n-vJX0LsH)

---

## **📂 Dataset Source**
The dataset is available on **Kaggle**:
📥 [Download Here](https://www.kaggle.com/datasets/yacooti/cost-of-living-in-nairobi)

---

## **📦 Project Setup**

### **1️⃣ Clone the Repository**
```sh
git clone git@github.com:yacooti/cost-of-living-forecaster.git
cd cost-of-living-forecaster
```

### **2️⃣ Install Dependencies**
Ensure you have **Python 3.8+** installed.
```sh
pip install pandas numpy scikit-learn joblib fastapi uvicorn xgboost 
```

### **3️⃣ Run the FastAPI Application**
```sh
uvicorn entrypoint:application --reload
```

### **4️⃣ Access the API Documentation**
Once the FastAPI server is running, open your browser and go to:

🔹 **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
🔹 **Redoc UI**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

This will allow you to test the prediction endpoint interactively.

### **5️⃣ Make a Prediction Request**
You can use **cURL**, Postman, or your browser to send a request:
```sh
curl -X POST "http://127.0.0.1:8000/predict?year=2025&area=Westlands"
```

---

## **🚀 Next Steps: Docker Deployment (Coming Soon!)**
