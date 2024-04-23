# OpenBB Open Metrics

This is a simple implementation that collects metrics on OpenBB across several platforms such as
YouTube, Discord, PyPi, and more. The metrics are collected and stored in the `metrics.json` file.

This is currently running as a GitHub Action at minute 0 past every 12th hour.

To run the metrics collection, make sure you have the required dependencies installed by running:

```bash
pip install -r requirements.txt
```

You will also need to have a `.env` file in the root directory with the variables shown inside the `utilities/config.py` file.

Then, run the following command to collect the metrics:

```bash
python main.py
```
