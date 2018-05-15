# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, g, redirect, session, escape  #라이브러리 몇만개중 한개만 실행
import hashlib #비밀번호를 평문으로 저장하지 않고 해시화 된 형태로 저장해줌.
import sqlite3 

DATABASE = 'test.db'

app = Flask(__name__)
app.secret_key = 'fefaef098efaw0efeawfaef'

def get_db():
    db = getattr(g, '_test', None)
    if db is None:
        db = g._test = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(Exception):
    db = getattr(g, '_test', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False, modify=False):
    cur = get_db().execute(query, args)
    if modify:
        try:
            get_db().commit()
            cur.close()
        except:
            return False
        return True
    rv= cur.fetchall()

    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.route("/") # / 라는 경로에 사용자가 접근하면. hello world가 출력
def hello():
    if 'id' in session:
        return u'로그인 완료 %s <a href="/logout">logout</a>' % escape(session['id'])
    return render_template("login.html")


@app.route("/name") # 127.0.0.1:5000/name 경로에 kkt가 출력
def name():
    return "kkt"

@app.route("/logout")
def logout():
    session.pop('id', None)
    return redirect('/login')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        id = request.form['id'].strip() #id라는 값을 POST로 부터 받아 올 것임.
        pw = hashlib.sha1(request.form['pw'].strip()).hexdigest()

        sql = "select * from user where id ='%s' and password='%s'" % (id,pw) 
        if query_db(sql, one =True):
            #로그인이 성공한 경우
            session['id'] = id
            return redirect('/')
        #로그인이 실패한 경우
        else:
            return "<script>alert('login fail');history.back(-1);</script>"

    if 'id' in session:
        return redirect('/')

    return render_template("login.html")

@app.route("/join", methods=['GET', 'POST']) #POST와 GET의 차이, POST는 직접 주소창에 입력하였을 때 /join을 입력하면 GET이 Retrun
def join():  #POST는 아이디와 비밀번호를 치고 로그인하였을 때 화면이 넘어가면 POST가 Retrun
    if request.method == 'POST':
        id = request.form['id'].strip() #id라는 값을 POST로 부터 받아 올 것임.
        pw = hashlib.sha1(request.form['pw'].strip()).hexdigest()

        sql = "select * from user where id ='%s'" % id
        if query_db(sql, one=True):
            return "<script>alert('join fail');history.back(-1);</script>"

        sql = "insert into user(id, password) values('%s', '%s')" % (id, pw)
        query_db(sql, modify=True)
        return redirect("/login")

    if 'id' in session:
        return redirect('/')

    return render_template("join.html")





@app.route("/add")
@app.route("/add/<int:num1>")
@app.route("/add/<int:num1>/<int:num2>")
def add(num1=None, num2=None):
    if num1 is None or num2 is None:
        return "add/num1/num2"
    return str(num1+num2)

@app.route("/sub/<int:num1>/<int:num2>")    
def sub(num1, num2):
    return str(num1-num2)

@app.route("/mul/<int:num1>/<int:num2>")    
def mul(num1, num2):
    return str(num1*num2)

@app.route("/div/<int:num1>/<int:num2>")
def div(num1, num2):
    if num2==0:
        return "0으로 나눌 수 없습니다."
    return str(num1/num2)

