# Install
### 1. Clone the repository

_ssh_
```bash
git clone git@github.com:Sneezy123/weather-stocks-correlation.git
```
_https_
```
git clone https://github.com/Sneezy123/weather-stocks-correlation.git
```

### 2. Go into cloned repo:
```bash
cd weather-stocks-correlation
```

### 3. Install the packages

I recommend setting up a virtual environment
To do this, run:
```bash
python3 -m venv env
```

Activate it:
```
. env/bin/activate
```

Then install, by running
```
pip install -r requirements.txt
```

---

# Usage

Run the program `plotrainaachen.py`:
```bash
python plotrainaachen.py <ARGS>
```
`ARGS`: Stock name or symbol (YFinance will search for it)

## Example
```bash
python plotrainaachen.py Apple
```
```bash
python plotrainaachen.py MSFT
```

Have fun!
