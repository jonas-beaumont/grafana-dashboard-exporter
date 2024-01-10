# Python Grafana Dashboard Exporter

A python script to export grafana dashboard to local filesystem

## Table of Contents

- [About](#about)
- [Why](#why)
- [Getting Started](#getting-started)
- [Usage](#usage)

## About

The Grafana Dashboard Exporter is a Python script designed to simplify the process of exporting Grafana dashboards. It utilizes the grafana_client module to interact with Grafana's API and retrieve dashboard configurations.

## Why

As Grafana users in our engineering teams, we have the privilege of creatig our dashboards. However, the responsibility of preserving and pushing these dashboards to the Grafana repository lies with us. Unfortunately, the occasional oversight of this crucial step has led to the loss of dashboards during Grafana redeployments.

To proactively address this issue and safeguard our dashboards, we incorporated this script into a pipeline. We not only mitigated the risk of losing valuable dashboards but also enhance the efficiency of your workflow. Let automation be our ally.

## Getting Started


**Create a Configuration File:**
* In the same directory as the main.py file, create a config.yaml file.
* Add the following key-value pairs to the config.yaml file, replacing the placeholders with your Grafana instance URL including the admin username and password:
```
---
grafanaURL: https://username:password@grafana.example.com/
```

**Execute setup_virtual_env.sh:**

Run the `setup_virtual_env.sh` script to create a virtual environment and install the necessary dependencies via pip. This will isolate the project's dependencies from your system-wide Python packages.
After completing these steps, you should have a configured environment ready for using your Grafana Dashboard Exporter script. You can then proceed to run the script to export dashboards as described in your project's documentation.

## Usage

Execute the `main.py` script from the virtual environment using Python. This will export Grafana dashboards and save them to the output directory. Later the output directory can be copied to 

```
.venv/bin/python main.py
```

The script will create the output directory if it does not exist in the same directory as main.py.

The contents of the output directory will be flushed with every execution of the script, so it always contains the latest exported dashboards.
