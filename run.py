import argparse
import yaml
import pandas as pd
import numpy as np
import json
import logging
import time
import sys

# Setup logging
def setup_logger(log_file):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

# Error handler
def write_error(output, version, message):
    error_json = {
        "version": version if version else "unknown",
        "status": "error",
        "error_message": message
    }
    with open(output, "w") as f:
        json.dump(error_json, f, indent=4)
    print(json.dumps(error_json, indent=4))
    sys.exit(1)

def main(args):
    start_time = time.time()

    setup_logger(args.log_file)
    logging.info("Job started")

    # STEP 1: Load config
    try:
        with open(args.config, "r") as f:
            config = yaml.safe_load(f)

        seed = config["seed"]
        window = config["window"]
        version = config["version"]

        np.random.seed(seed)
        logging.info(f"Config loaded: {config}")

    except Exception as e:
        write_error(args.output, None, f"Config error: {str(e)}")

    # STEP 2: Load data
    try:
        df = pd.read_csv(args.input)

        if df.empty:
            raise ValueError("Empty dataset")

        if "close" not in df.columns:
            raise ValueError("Missing 'close' column")

        logging.info(f"Rows loaded: {len(df)}")

    except Exception as e:
        write_error(args.output, version, f"Data error: {str(e)}")

    try:
        # STEP 3: Rolling mean
        df["rolling_mean"] = df["close"].rolling(window=window).mean()

        # STEP 4: Signal generation
        df["signal"] = (df["close"] > df["rolling_mean"]).astype(int)

        # Remove first rows (NaN)
        df = df.dropna()

        # STEP 5: Metrics
        rows_processed = len(df)
        signal_rate = df["signal"].mean()

        latency_ms = int((time.time() - start_time) * 1000)

        metrics = {
            "version": version,
            "rows_processed": rows_processed,
            "metric": "signal_rate",
            "value": round(signal_rate, 4),
            "latency_ms": latency_ms,
            "seed": seed,
            "status": "success"
        }

        # Save metrics
        with open(args.output, "w") as f:
            json.dump(metrics, f, indent=4)

        logging.info(f"Metrics: {metrics}")
        logging.info("Job completed successfully")

        print(json.dumps(metrics, indent=4))

    except Exception as e:
        write_error(args.output, version, f"Processing error: {str(e)}")

# CLI arguments
if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--input", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--log-file", required=True)

    args = parser.parse_args()

    main(args)