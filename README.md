# Intertoys Game Queries Analysis
This project aims to collect data from Intertoys webpage and to analyze and visualize the data. 
Data include: name, price, description. 

## Installation

To be able to run the main scripts, you need to install the packages from the requirements.txt, e.g.:

```
pip install -r requirements.txt
```

## Usage
First, fill in the right value for the configuration in the config.yaml file. To get an idea of the
values needed, look at the config_template.yaml.


Second, run the first main file to run the scraper and write the data to your own database:

```
python 01_run_intertoys.py
```

Third, use the data written to your database, you can generate the analysis using:

```
python 02_visualize_data.py
```

## Issues
You might run into an issue where the emulator does not start in MacOS, because of chromedriver issues. In that case run:

```
xattr -d com.apple.quarantine chromedriver
```
