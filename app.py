from flask import Flask,render_template,request,session,make_response, jsonify,redirect,url_for
import mysql.connector
import bitcoin
import numpy as np
import pandas as pd
from datetime import datetime
global loadedmodel
global forecast
import pickle
import pandas_ta as pta
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
import marshal, types
import requests



db=mysql.connector.connect(user='root',password='',database='bitcoin',port=3307)
cur=db.cursor()

app=Flask(__name__)
app.secret_key="!@wehjbeywe5425c456scjsuywiydbwbqwgdq)(U#*(WJh8uchQ&*Y*)3jnchdsbc"
df = pd.read_csv('DATASET/bitcoin_class.csv', index_col=False)


# def regr(time):
#     dbfile = open('regr', 'rb')
#     code = marshal.loads(dbfile.read())
#     func = types.FunctionType(code, globals(), "some_func_name")
#     ans = func(time)
#     return ans


global model
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signin',methods=['POST','GET'])


def signin():
    if request.method=='POST':
        email=request.form['email']
        session['useremail']=email
        password=request.form['password']
        sql="select name,password from bitcoinreg where email='%s' and password='%s'"%(email,password)
        cur.execute(sql)
        data=cur.fetchall()
        db.commit()
        print(data)
        if data!=[]:
            return render_template('userhome.html')
        else:
            msg = "Invalid Credentials"
            return render_template('signin.html', msg=msg)

    return render_template('signin.html')


@app.route("/main")
def main():
    return render_template("main.html")







@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        password=request.form['password']
        confirmpassword=request.form['confirmpassword']
        contact=request.form['contact']
        pancard=request.form['txtPANCard']
        if password == confirmpassword:
            sq="select * from bitcoinreg where email='%s'"%(email)
            cur.execute(sq)
            data=cur.fetchall()
            db.commit()
            if data==[]:
                sql="insert into bitcoinreg(name,email,password,contactNumber,PANCARD)values(%s,%s,%s,%s,%s)"
                val=(name,email,password,contact,pancard)
                cur.execute(sql,val)
                db.commit()
                msg="Data Inserted Successfully"
                return render_template('signup.html',mag=msg)
            elif data !=[]:
                msg="Details already exist"
                return render_template('signup.html',msg=msg)
    return render_template('signup.html')

@app.route('/userprofile')
def userprofile():
    sql="select * from bitcoinreg where email='%s'"%(session['useremail'])
    cur.execute(sql)
    data=cur.fetchall()
    db.commit()
    data=[j for i in data for j in i]
    val=data[0]
    name=data[1]
    session['username']=name
    email=data[2]
    contact=data[5]
    Pancard=data[-1]
    Bitcoins=data[3]
    return render_template('userprofile.html',id=val,name=name,email=email,Bitcoins=Bitcoins,contact=contact,Pan=Pancard)

@app.route('/dashboard')
def dashboard():
    price = df.iloc[:, -4]
    time = df.iloc[:,1]
    # regr(time)
    data = {'time': time.to_dict(), 'price': price.to_dict()}
    return jsonify(data)



@app.route('/storebitcoin')
def storebitcoin():
    buy = request.args.get('buy')
    sell = request.args.get('sell')
    bitcoin = int(float(sell)) - int(float(buy))
    sql="select * from bitcoinreg where email='%s'"%(session['useremail'])
    cur.execute(sql)
    data=cur.fetchall()
    db.commit()
    print(data)
    coins=data[0][3]
    username=data[0][1]
    email=data[0][2]
    contact=data[0][5]
    pancard=data[0][6]
    coins=int(coins)
    totalcoins=coins + bitcoin
    sql="update bitcoinreg set bitcoins='%s' where email='%s'"%(totalcoins,session['useremail'])
    cur.execute(sql)
    db.commit()
    sql = "insert into bitcointransaction(Username,Email,Bitcoins,Contact,PANCARD)values(%s,%s,%s,%s,%s)"
    val = (username, email, coins, contact, pancard)
    cur.execute(sql, val)
    db.commit()
    return 'hello'

@app.route('/dashboard1')
def dashboard1():
    data = pd.read_csv('DATASET/bitcoin.csv')
    rsi = pta.rsi(data['Close'], length=10)
    data['rsi'] = rsi
    data['ma'] = data.Close.rolling(window=11).mean()
    l = []
    for x in range(data.shape[0]):
        if x >= 10:
            d1 = data.iloc[x, 5]
            d2 = data.iloc[x - 10, 5]
            if d1 > d2:
                l.append('uptrend')
            else:
                l.append('downtrend')
        else:
            l.append('0')
    data['trend'] = pd.DataFrame({'col': l})
    df = data.iloc[10:, :]
    df1 = df.drop('ID', axis=1)
    df1.to_csv('bitcoin_class.csv')
    X = df1.iloc[:, :-1]
    y = df1.iloc[:, -1]
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.7, random_state=42)
    classifier_rf = RandomForestClassifier(random_state=42, n_jobs=-1, max_depth=5, n_estimators=100, oob_score=True)
    classifier_rf.fit(X_train, y_train)
    y_pred = classifier_rf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    key = "https://api.binance.com/api/v3/ticker/price?symbol="
    # Making list for multiple crypto's
    currencies = ["BTCUSDT", "DOGEUSDT", "LTCUSDT","ETHBUSD"]
    j = 0
    # running loop to print all crypto prices
    l = []
    for i in currencies:
        # completing API for request
        url = key + currencies[j]
        data = requests.get(url)
        data = data.json()
        j = j + 1

        price= data['symbol'] ," " +  data['price']
        a=price
        l.append(a)

    x=l
    print(x)




    sql="select * from bitcointransaction"
    data=pd.read_sql_query(sql,db)

    return render_template("dashboard1.html", email=session['username'], accuracy=acc,cols=data.columns.values,rows=data.values.tolist(),price=x)



@app.route('/prediction')
def prediction():
    global forecast
    pred = int(request.args.get('sell'))
    newdata=df.iloc[pred,1:-1]
    newdata = [newdata]
    model = pickle.load(open('finalized_model.sav', 'rb'))
    y_pred = model.predict(newdata)
    print(pred)
    w = bitcoin.b_predict(pred)
    w = str(w)
    # print(df.loc[df.loc['Timestamp'] == newdata.loc['Timestamp']])
    return jsonify({'pred': y_pred[0], 'value': w})



@app.route('/logout')
def logout():
    try:
        session.pop('useremail',None)
        session.clear()
        return redirect(url_for('index'))
    except:
        return redirect(url_for('index'))


if __name__=='__main__':
    app.run(debug=True,port='8000')
