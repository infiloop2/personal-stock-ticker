# Interactive Brokers

Interactive brokers has nice APIs (<https://interactivebrokers.github.io/cpwebapi/>) but the authentication mechanism is slightly painful. It doesn't officially support headless authentication and requires login through a browser.
While a browser can be automated, if you have 2-fac on, automatic login is unfeasible.

There's a workaround by creating a new IBKR user which has read only permissions on your account. To do this

-   go to IBKR -> Settings -> Account Settings
-   Click on Configure 'Users & Access Rights'
-   Create a new user. In Access rights give access to all parts under 'Statements Access' and 'PortfolioAnalyst' headings.
-   It will take some time for IBKR to setup the user, once it is done you will have a new set of credentials which does not have 2fac and only has read-only access to your account. Use it in ```config.json```
-   You'll also need to add Account number in ```config.json```. It's of the form of a Letter followed by 7 digits.

## Additional Setup

-   Download java 8 or higher: (<https://www.digitalocean.com/community/tutorials/how-to-install-java-with-apt-on-ubuntu-18-04>)
-   Download the 'Gateway: Latest' in 'Client Portal API'. (<https://www.interactivebrokers.com/en/index.php?f=5041>) and replace ```clientportal``` folder with the latest version. (This step is not strictly necessary since a version is already included in this repo but it will get outdated)
-   Install jq CLI : `sudo apt-get install jq`

## Script Structure

IBKR script works in the following way:

-   First a java server is started and a new login session is initiated using browser
-   Periodic API reads using this session. You need to do at-least one call per 60 sec so that the session doesn't auto-timeout
-   The session auto-closes 2-3 times a day randomly. If this is detected then step 1 is repeated programatically

All this logic is included in `fetch_latest.py` which is meant to run indefinitely. Note this script uses some bash commands and has been written for Ubuntu 18.04
