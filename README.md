# OtoMoto Scraper Bot
![Release](https://img.shields.io/github/v/release/Yorick0499/otomoto-bot?color=blue)
![Python](https://img.shields.io/badge/python-3.12.3-blue)
![Last Commit](https://img.shields.io/github/last-commit/Yorick0499/otomoto-bot)
![Maintenance](https://img.shields.io/maintenance/yes/2025)\
A bot for monitoring and fetching new vehicle offers from OtoMoto.pl.\
*This project is currently under development - some features may be unimplemented or experimental.*

## FEATURES
- scraping offers for the selected brand and model
- downloading basic offer data to a CSV file (model, brand, price, publication date and URL)
- simple CLI for easy interaction
- automatic, cyclical checking of offers (time interval can be changed)
- Saving user configuration

## INSTALLATION
1. Clone the repository:
```bash
git clone https://github.com/Yorick0499/otomoto-bot.git
cd otomoto-bot
```
2. Create a virtual environment (recommended):
```bash
python3 -m venv .venv
source .venv/bin/activate
```
3. Install required packages:
```bash
pip install -r requirements.txt
```
4. Install required browsers with Playwright (first-time setup or after Playwright update):
```bash
playwright install
```

## USAGE
1. Activate virtual environment:
```bash
source .venv/bin/activate
```
2. Run the scraper:
```bash
python3 main.py
```
3. Follow the instructions displayed in the CLI.

## DISCLAIMER
This project is for educational purposes only. 
Please use responsibly and respect the target website's terms of service.

## REQUIREMENTS
- Python 3.12.3 (or compatible)
- pip packages from requirements.txt
