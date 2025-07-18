# Insurance Cost Prediction Pipeline

## Project Overview
This repository contains an end-to-end solution for predicting which insurance members will incur high annual healthcare costs (> \$20,000). It follows the CRISP-DM framework to ingest raw data, clean and transform it in SQL Server, perform exploratory data analysis (EDA) and modeling in Python, automate the pipeline, and visualize results in Power BI.

**Key features:**
- SQL Server schemas for staging and production  
- Python scripts for data ingestion, cleaning, modeling, and scoring  
- Random Forest classifier with hyperparameter tuning and calibration  
- Automated daily pipeline via cron (or launchd)  
- Interactive dashboard in Power BI Service (web)  

---

## Tech Stack
- **Data storage & processing:** Microsoft SQL Server (Docker)  
- **Programming:** Python 3.10, pandas, SQLAlchemy, pymssql, scikit-learn, joblib  
- **ETL & automation:** Bash, cron (macOS launchd alternative)  
- **Visualization:** Power BI Service  

---

<details>
<summary><strong>Repository Structure</strong></summary>

```plaintext
insurance-demo/
├── data/                # Raw and exported CSV files
├── docs/                # CRISP-DM plan, data license
├── reports/             # Dashboard screenshots
├── sql/                 # SQL scripts for schemas, staging, and production loads
├── src/                 # Python modules and scripts
│   ├── db_utils.py      # DB connection and loader
│   ├── download_data.py # Download raw CSV
│   ├── load_staging.py  # Script to load CSV into staging
│   └── score.py         # Load model, score data, write results
├── run_pipeline.sh      # Bash wrapper for full ELT + scoring
├── requirements.txt     # Python dependencies
└── README.md            # Project overview and instructions

</details>



⸻

Getting Started
	1.	Clone the repo

git clone https://github.com/dwbango/Data_Science_Misc.git
cd Data_Science_Misc/insurance-demo


	2.	Install dependencies

pip install -r requirements.txt


	3.	Download data

cd src
python download_data.py
cd ..


	4.	Run the full pipeline

./run_pipeline.sh


	5.	View the dashboard
Upload the exported CSVs in the data/ folder to Power BI Service.

⸻

Next Steps
	•	Export model_results and feature_importances to CSV for web reporting.
	•	Build and style the Power BI report in the Power BI Service.

Future Works
	•	Set up an on-premises gateway for live SQL connectivity.


