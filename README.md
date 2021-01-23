# personal-stock-ticker

These are the scripts powering a personal stock ticker. To learn more about the concept visit https://infiloop.io/personalstockticker

Currently supported brokers are:

- Interactive Brokers (https://www.interactivebrokers.com/en/home.php)
- Coinbase (https://www.coinbase.com)
- IG UK (https://www.ig.com/uk)
- Fixed portfolio tracking using yahoo finance

## Dependencies

All of the scripts are written in python3. To install python3 follow: https://realpython.com/installing-python/

You'll need to install the following libraries for these scripts. To install a library use:
`python3 -m pip install library`

- selenium (used for browser automation)
- yahoo_fin
- coinbase (only needed for coinbase)

Additionally for selenium you'll need to install firefox browser drivers: https://github.com/mozilla/geckodriver/releases

## Overall Setup

Each broker has its own folder which has the following files:

- fetch_latest.py : Use `python3 fetch_latest.py` to fetch the latest price and print it to terminal.
- config_sample.json : Sample of the config file needed to fetch the price. Copy it to config.json and replace the config with actual secrets. Remember not to commit config.json (It's already in .gitignore)
- README.md : Broker specific instructions to setup the config

## Setting up the ticker in production

- You'll need to configure the script for each broker you use. If your broker is not in the supported list, please consider adding support for it and contributing to this repo.
- Choose a DB and configure scripts to write the value to the DB instead of printing it. [AWS Dynamo DB](https://aws.amazon.com/dynamodb/) might be a good choice. This is not natively supported in this repo yet.
- Configure a machine to run these scripts periodically. [AWS EC2](https://aws.amazon.com/ec2/) might be a good choice.
- Configure aggregation of this data. This can be done via another script which periodically reads from the DB or you can use [stream processing](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Streams.Lambda.html).
