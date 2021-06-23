import sys

from flask import Flask, request, jsonify
import sqlite3
import json

app = Flask(__name__)


def sqlinjection(keyword):
    if keyword:
        keyword = keyword.replace("/", "//")
        keyword = keyword.replace("'", "''")
        keyword = keyword.replace("[", "/[")
        keyword = keyword.replace("]", "/]")
        keyword = keyword.replace("%", "/%")
        keyword = keyword.replace("&", "/&")
        keyword = keyword.replace("_", "/_")
        keyword = keyword.replace("(", "/(")
        keyword = keyword.replace(")", "/)")
    return keyword


def keywords(q, source, year, page):
    tmp = []

    keywords = []
    operator = []
    
    source = sqlinjection(source)
    year = sqlinjection(year)

    i = 0
    finish_flag = False
    while i <= len(q):
        if i == len(q):
            finish_flag = True
        elif q[i] == "+":
            operator.append("and")
            finish_flag = True
        elif q[i] == "|":
            operator.append("or")
            finish_flag = True
        else:
            tmp.append(q[i])
        if finish_flag:
            tmp_str = "".join(tmp).strip()
            if tmp_str:
                keywords.append(sqlinjection("".join(tmp).strip()))
            tmp = []
            finish_flag = False
        i += 1
    if len(keywords) - len(operator) != 1:
        print("Error")
    # base_query = "SELECT * FROM PAPER WHERE ("
    base_query = "("
    clause = ""
    base_title = "TITLE LIKE'%{0}%'"
    base_abstract = "ABSTRACT LIKE '%{0}%'"
    for i in range(len(operator)):
        try:
            clause += base_title.format(keywords[i],)
            clause += " {0} ".format(operator[i],)
        except IndexError as e:
            print(e)
            return "SELECT * FROM PAPER WHERE YEAR=1900"
    clause += base_title.format(keywords[-1],)

    clause += " OR "

    for i in range(len(operator)):
        clause += base_abstract.format(keywords[i],)
        clause += " {0} ".format(operator[i],)
    clause += base_abstract.format(keywords[-1],) + ")"

    if source is not None:
        clause += (" AND CONFERENCE IN (" + source + ") ")
    if year is not None:
        clause += (" AND YEAR IN (" + year + ") ")

    print(clause)
    return base_query + clause

@app.route('/')
def home():
    return app.send_static_file('index.html')


@app.route('/search')
def get_info():
    q = request.args.get("q")
    source = request.args.get("s")
    year = request.args.get("y")
    page = request.args.get("p")
    conn = sqlite3.connect("./paper.db")
    c = conn.cursor()
    query = keywords(q, source, year, page)
    results = []
    
    # get total count
    try:
        base_q = "SELECT COUNT(*) FROM PAPER WHERE"
        cursor = c.execute(base_q + query)
        total = cursor.fetchone()[0]
    except sqlite3.Error as e:
        total = -1
    
    # get real data
    try:
        query = "SELECT * FROM PAPER WHERE" +  query
        query += " ORDER BY YEAR DESC "
        try:
            page = int(page) - 1
        except:
            page = 0
        query += "LIMIT 10 OFFSET {0}".format(page * 10)
        cursor = c.execute(query)
        for item in cursor:
            results.append(item)
        msg = {"code": 0, "msg": "success", "data": results, "count": total}
    except sqlite3.OperationalError as e:
        msg = {"code": 1, "msg": e, "data": query}
    except sqlite3.IntegrityError as e:
        msg = {"code": 1, "msg": e, "data": query}
    finally:
        conn.close()
    return json.dumps(msg)


@app.route('/abstract/<q>')
def get_abs(q):
    conn = sqlite3.connect("./paper.db")
    c = conn.cursor()
    query = "SELECT title,abstract FROM PAPER WHERE id=" + str(int(q))
    results = []
    try:
        cursor = c.execute(query)
        for item in cursor:
            results.append(item)
        msg = {"code": 0, "msg": "success", "data": results}
    except sqlite3.OperationalError as e:
        msg = {"code": 1, "msg": e, "data": query}
    except sqlite3.IntegrityError as e:
        msg = {"code": 1, "msg": e, "data": query}
    finally:
        conn.close()

    return json.dumps(msg)


if __name__ == '__main__':
    app.run(host=sys.argv[1], port=sys.argv[2], debug=True)
