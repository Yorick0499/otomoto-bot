# OtoMoto Scraper Bot (Development version)
A bot for monitoring and fetching new vehicle offers from OtoMoto.pl.\
*This project is currently under development - some features may be unimplemented or experimental.*

## FEATURES
- scraping offers for the selected brand and model
- downloading basic offer data to a CSV file (model, brand, price, publication date and URL)
- simple CLI interface
- automatic, cyclical checking of offers (time interval can be changed)
- Saving user configuration

## INSTALLATION
```bash
git clone https://github.com/Yorick0499/otomoto-bot.git
cd otomoto-bot
```
It is recommended to create a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```
Then you need to install all the required packages:
```bash
pip install -r requirements.txt
```
It is also necessaryto install the required browsers after installing Playwright
```bash
playwright install
```

## REQUIREMENTS
- Python 3.12.3
