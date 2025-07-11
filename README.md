# Assignment-3-SQL-Database-Design-Flask-Web-API
*CMPT 354 – Summer 2025*  
## 📄 Overview

This assignment has two major components:
1. **SQL Database Creation & Constraints**  
   Implement a secure, robust PostgreSQL schema for the "Pie-in-the-Sky Security Corp." (PITS) trading system, enforcing business logic via constraints and triggers.
2. **Flask Web API Programming**  
   Develop a minimal web API in Python (Flask) to support account/stock queries and trading operations on the PITS database.

---

## 🗂️ Directory Structure
```
A3/
├── p1/
│ ├── create.sql # SQL schema and triggers
│ ├── load.sql # Provided initial data
│ ├── f.sql–l.sql # Test SQL for constraints/triggers
├── p2/
│ ├── app.py # Flask web API (Python)
│ └── flask_mini_example.py # Provided starter/example
└── A3.ipynb # Assignment instructions
```
## Problem 1: SQL Database Design

**Goal:**  
Model the PITS trading platform with 6 main tables, and enforce all required integrity constraints using PostgreSQL features (PKs, FKs, triggers).

### 📊 Schema Overview

- **Person** (`pid`, name, address)
- **Broker** (`pid`, license, phone, manager)
- **Account** (`aid`, brokerpid)
- **Owns** (`pid`, aid)
- **Stock** (`sym`, price)
- **Trade** (`aid`, seq, type, timestamp, sym, shares, price)

### 🔒 Constraints & Triggers

- Enforce primary/foreign keys
- **Trade type** must be `'buy'` or `'sell'`
- **Trade** is append-only: no UPDATE/DELETE allowed (use trigger)
- **Trade sequencing**: each new trade for an account must have strictly increasing `seq` and non-decreasing `timestamp`
- **Broker-Account**: brokers may *not* own accounts (directly or jointly) — trigger enforced
- **Holds view**: compute current account holdings from `Trade` (for later checks)
- **Oversell protection**: do not allow selling more shares than an account currently holds

### 🧪 Testing

Test your schema/triggers by running provided SQL statements in files `f.sql`–`l.sql`, each of which attempts to violate a specific constraint (should throw an error).

**Sample command:**
```bash
psql pits -U <your-username> -af f.sql
```
# Problem 2: Basic Flask Web API
Goal:
Build a web service in Python using Flask and SQLAlchemy to interface with your database.
🧩 API Endpoints to Implement

   -``` /getOwner?aid=<aid>```
    → Returns the owner(s) of a given account as JSON (```[{"pid": ...}]``` or ```[{"pid": -1}]```)

   -``` /getHoldings?aid=<aid>&sym=<symbol>```
    → Returns holdings as JSON (```{"shares": total_share}```), with specific rules for error/zero cases

  -```  /trade?aid=<aid>&sym=<symbol>&type=buy|sell&shares=<amount>&price=<price>```
    → Completes a trade; returns ```{'res': seq}``` on success, or ```{'res': 'fail'}``` on failure (invalid/oversell)

# Constraints:

  -  Use only the provided Python files (do not add extra files/libraries)

  -  Implement using Flask, SQLAlchemy, and psycopg2-binary as specified

   - Use explicit SQL transactions where necessary

💻 Environment Setup

Recommended Python: 3.9+
Required libraries: Flask, Flask-SQLAlchemy, psycopg2-binary
```bash
pip install flask==3.1.1 flask-sqlalchemy==3.1.1 psycopg2-binary==2.9.9
```
To run the server:
```bash
cd A3/p2/
python app.py

```
🧪 API Example Usage

Test your endpoints in your browser or with curl:

- [Get owner(s) of account 800](http://127.0.0.1:5000/getOwner?aid=800)
- [Get holdings for account 150, symbol AAPL](http://127.0.0.1:5000/getHoldings?aid=150&sym=AAPL)
- [Attempt trade (buy/sell)](http://127.0.0.1:5000/trade?aid=300&sym=GOOGL&type=buy&shares=100.00&price=99.99)# 👨‍💻 Author

Utsav Patel

Email:usp@sfu.ca

Simon Fraser University
## Credits

This project is adapted from the CMPT 354 (Database Systems I ) assignment at Simon Fraser University, Summer 2025.
Code structure and assignment specification provided by course instructors.
# License

This project is open for educational and demonstration purposes. Attribution is appreciated!
<p align="center"> <b>🌟 If you like this project, please star the repo! 🌟</b> </p> 
