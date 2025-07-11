from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
import time, datetime

app = Flask(__name__)
# Update the below configuration with your existing PostgreSQL database details
psql_user = 'postgres'
psql_password = 'Utsav@2208'
db_name = 'pits'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Utsav%402208@localhost:5433/pits'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route('/')
def index():
    # Execute a raw SQL query directly
    connection = db.engine.raw_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Stock WHERE sym = 'AAPL';")
    query_result = cursor.fetchall()
    if len(query_result) > 0:
        res = query_result[0]
    else:
        res = []
    return jsonify(res)

# @app.route('/')
# def index():
#     """
#         an alternative implementation of the index() function
#         with query parameter and placeholder
#     """
#     res = []
#     with db.engine.begin() as conn:
#         query_result = conn.execute(text("SELECT * FROM Stock WHERE sym = :sym ;"), 
#                                     dict(sym='AAPL'))
#         for sym, price in query_result:
#             res.append([sym, price])
#     return jsonify(res[0])

@app.route('/getOwner')
def getOwner():
    """
        This HTTP method takes aid as input, and returns all owner's pid in a list
        If the account does not exist, return [{'pid': -1}]
    """
    aid = int(request.args.get('aid', -1))
    # complete the function by replacing the line below with your code
    with db.engine.begin() as conn:
        result = conn.execute(text("SELECT aid FROM Account WHERE aid = :aid"), {'aid': aid}).fetchone()
        if not result:
            return jsonify([{'pid': -1}])
        # Get all owners
        result = conn.execute(text("SELECT pid FROM Owns WHERE aid = :aid"), {'aid': aid}).fetchall()
        owners = [{'pid': row[0]} for row in result]
        return jsonify(owners)

@app.route('/getHoldings')
def getHoldings():
    """
        This HTTP method takes aid and sym as input, 
        and returns the total share of holdings for a stock sym of an account
        If the stock does not exist or the account does not exist, return {'shares': -1};
        If the account does not hold any share of the stock, return {'shares': 0}
        DO NOT USE the view you create in P1
    """
    aid = int(request.args.get('aid', -1))
    sym = request.args.get('sym', '')
    # complete the function by replacing the line below with your code
    with db.engine.begin() as conn:
        # Check if account and stock exist
        acc = conn.execute(text("SELECT 1 FROM Account WHERE aid = :aid"), {'aid': aid}).fetchone()
        stk = conn.execute(text("SELECT 1 FROM Stock WHERE sym = :sym"), {'sym': sym}).fetchone()
        if not acc or not stk:
            return jsonify({'shares': -1})
        # Calculate holdings (buys - sells)
        result = conn.execute(text("""
            SELECT COALESCE(SUM(
                CASE WHEN type = 'buy' THEN shares
                     WHEN type = 'sell' THEN -shares
                     ELSE 0 END), 0)
            FROM Trade WHERE aid = :aid AND sym = :sym
        """), {'aid': aid, 'sym': sym}).fetchone()
        shares = result[0] if result else 0
        return jsonify({'shares': shares})

def currentTime():
    ts = time.time()
    return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    
@app.route('/trade')
def trade():
    """
        This HTTP method takes the information of a trade as input: aid, sym, type, shares, price 
        You need to retrieve the current maximum seq numer (max_seq) for aid and 
        then insert with max_seq+1 and the current timestamp.
        It returns {'res' : 'fail'} if there is an oversell or other errors like aid/sym/type does not exist;
        Otherwise, it returns {'res': the current seq} and also updates the database accordingly.
        You should implement the check of the violation in the Python function 
        and DO NOT use the view you implemented in P1.
        You will need to finish a multi statement transaction in this function.
        
        Ideally, you need to send a HTTP POST request for such editing requests, 
        but we just choose GET for easier test
    """
    aid = int(request.args.get('aid', -1))
    sym = request.args.get('sym', '')
    type_= request.args.get('type', '')
    shares = float(request.args.get('shares', -1))
    price = float(request.args.get('price', -1))

    # complete the function by replacing the line below with your code
    if type_ not in ('buy', 'sell') or shares <= 0 or price < 0:
        return jsonify({'res': 'fail'})

    try:
        with db.engine.begin() as conn:
            # Check account and stock existence
            acc = conn.execute(text("SELECT 1 FROM Account WHERE aid = :aid"), {'aid': aid}).fetchone()
            stk = conn.execute(text("SELECT 1 FROM Stock WHERE sym = :sym"), {'sym': sym}).fetchone()
            if not acc or not stk:
                return jsonify({'res': 'fail'})

            # Get current holdings
            res = conn.execute(text("""
                SELECT COALESCE(SUM(
                    CASE WHEN type = 'buy' THEN shares
                         WHEN type = 'sell' THEN -shares
                         ELSE 0 END), 0)
                FROM Trade WHERE aid = :aid AND sym = :sym
            """), {'aid': aid, 'sym': sym}).fetchone()
            held = res[0] if res else 0

            if type_ == 'sell' and held < shares:
                return jsonify({'res': 'fail'})

            # Get current max seq
            max_seq = conn.execute(text("SELECT COALESCE(MAX(seq), 0) FROM Trade WHERE aid = :aid"), {'aid': aid}).fetchone()[0]
            new_seq = max_seq + 1
            now = currentTime()

            # Insert trade
            conn.execute(text("""
                INSERT INTO Trade(aid, seq, type, timestamp, sym, shares, price)
                VALUES (:aid, :seq, :type, :timestamp, :sym, :shares, :price)
            """), {'aid': aid, 'seq': new_seq, 'type': type_, 'timestamp': now, 'sym': sym, 'shares': shares, 'price': price})

            return jsonify({'res': new_seq})

    except Exception as e:
        return jsonify({'res': 'fail'})

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5000)