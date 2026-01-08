System Health Monitoring and Alerting (Python)
Overview

This project is a Python-based system health monitoring tool designed to simulate real-world IT support and Tier 1/Tier 2 troubleshooting tasks. It collects real-time system performance metrics and logs them for analysis and documentation.

Features

Monitors CPU usage, memory (RAM) utilization, and disk free space

Implements threshold-based alerting for performance and storage issues

Logs system health data to both text and CSV files

Supports continuous monitoring with configurable intervals

Technologies Used

Python

System and process utilities for system metrics collection

File-based logging using TXT and CSV formats

Git and GitHub

How to Run

Install the required dependency:

pip install psutil


Run the script:

python health_monitor.py


Stop execution at any time using:

Ctrl + C
