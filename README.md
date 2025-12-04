

# **Global Life Expectancy Analysis**

Understanding global health trends from **1990–2019**

---

## **1. Project Overview**

This project explores how **health**, **demographics**, **economics**, and **nutrition** shape life expectancy across countries.
The dataset spans **281 countries/regions**, **30 years**, and **80+ variables**.

### **Objectives**

* Clean and preprocess a large multi-source dataset
* Perform Exploratory Data Analysis (EDA)
* Build a predictive life expectancy model
* Identify key contributors using feature importance + SHAP
* Cluster countries into development groups
* Predict future life expectancy for selected nations

---

## **2. Dataset & Preprocessing**

### **Key preprocessing steps**

* Standardized column names
* Removed features with excessive missing values
* Country-wise median imputation for numeric fields
* Converted non-numeric cells into numeric format
* Verified the completeness of year-wise records

### **Final cleaned dataset**

* **Rows:** 22,050
* **Columns:** 80

---

## **3. Exploratory Data Analysis (EDA)**

### **Major insights**

* Global life expectancy shows a **steady upward trend**
* Strong negative correlations:

  * Infant mortality
  * Under-5 mortality
  * Maternal mortality
* Strong positive associations:

  * GDP per capita
  * Healthcare access (doctors, nurses, skilled birth attendance)
* Diet composition and age demographics also influence longevity

---

## **4. Predictive Modeling**

A **Random Forest Regressor** was trained to model life expectancy.

### **Model performance**

* **R² score:** **0.93**
* Reliable predictions across countries and years

### **Most influential features**

* Maternal Mortality Ratio
* Infant Mortality Rate
* Under-5 Mortality Rate
* GDP per Capita / Income per Capita
* Doctors per 1,000 population
* Birth Rate
* Death Rate
* Diet composition features

---

## **5. Country Clustering**

K-Means clustering grouped countries into **four clusters**:

| Cluster | Description                                              |
| ------- | -------------------------------------------------------- |
| **1**   | High-income, high-life-expectancy nations                |
| **2**   | Middle-income improving nations (e.g., China, Sri Lanka) |
| **3**   | Developing nations with moderate progress                |
| **4**   | Low-income nations with high mortality                   |

---

## **6. Future Life Expectancy Predictions**

Using forward-projected features and the trained model:

| Country       | **2025** | **2030** |
| ------------- | -------- | -------- |
| **India**     | 72.02    | 72.33    |
| **China**     | 77.19    | 77.87    |
| **Sri Lanka** | 77.70    | 77.86    |

> These predictions are analytic estimates — not official demographic forecasts.

---

## **7. Repository Structure**

```
global-life-expectancy-analysis/
│
├── data/                 # Dataset
├── notebooks/            # Jupyter notebooks for analysis
├── scripts/              # Python scripts for cleaning, modeling, clustering
├── results/              # Graphs, feature importance, SHAP values
├── README.md             # Project documentation
└── REPORT.md             # Full detailed report
```

---

## **8. Technologies Used**

* Python
* Pandas, NumPy
* Scikit-Learn
* Matplotlib, Seaborn
* SHAP
* K-Means Clustering
* Jupyter Notebook
* Git & GitHub

---

## **9. Author**

**Siddharth Chawla**

IIT Jodhpur

Global Health & Data Science Research Project

---

