MLOps Task – Data Processing Pipeline

Overview:
This project implements a complete MLOps pipeline that processes financial time-series data from a CSV file and computes a metric called signal rate.
The application supports CLI execution, logging, error handling, and Docker containerization.

Features:
Reads CSV data (OHLC format)
Validates required columns
Computes signal rate
Outputs results in JSON
Docker support
CLI-based execution

Project Structure:
mlops-task/
│── run.py
│── config.yaml
│── data.csv
│── requirements.txt
│── Dockerfile
│── metrics.json
│── run.log
│── README.md

Run With Docker

###  Build Docker Image
docker build -t mlops-app .

###  Run Docker Container
docker run mlops-app --input data.csv --config config.yaml --output metrics.json --log-file run.log

Sample Output:
{
  "version": "v1",
  "rows_processed": 9996,
  "metric": "signal_rate",
  "value": 0.4991,
  "latency_ms": 33,
  "seed": 42,
  "status": "success"
}

Error Handling Handles:
Missing files
Invalid config
Missing columns
Runtime errors

Conclusion:
This project demonstrates a complete MLOps workflow including development, containerization, and deployment using GitHub.
