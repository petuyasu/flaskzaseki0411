from flask import Flask,render_template,session,request,redirect,url_for
import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from werkzeug.utils import secure_filename
from tkinter import messagebox

#インスタンスの作成
app = Flask(__name__)

#暗号鍵の作成
key =os.urandom(21)
app.secret_key = key 

#idとパスワードの設定（ローカルの）
id_pwd ={'watanabe': 'a'}

#データベース設定（ローカルの）
URI = 'postgresql://postgres:zasekites@localhost/flasktest'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = URI
db = SQLAlchemy(app)

#テーブル内容の設定
class Data(db.Model):
    name_r = db.Column(db.String(50), primary_key=True)
    name_k = db.Column(db.String(60))
    group = db.Column(db.String(20))
    tel = db.Column(db.String(4))
    floor = db.Column(db.String(3))
    area = db.Column(db.String(1))
    status = db.Column(db.String(20))
    dt = db.Column(db.DateTime,nullable=False,default=datetime.now)

#テーブルの初期化
@app.cli.command('initdb')
def initdb():
    db.create_all()

#メイン
@app.route('/')
def index():
    if not session.get('login'):
        return redirect(url_for('login'))
    else:
        data = Data.query.order_by(desc(Data.dt)).all()
        return render_template('index.html',data=data)

#ログイン
@app.route('/login')
def login():
    return render_template('login.html')

#ログインの認証
@app.route('/logincheck', methods=['POST'])
def logincheck():
    user_id = request.form['user_id']
    password = request.form['password']

    if user_id in id_pwd:
        if password == id_pwd[user_id]:
            session['login'] = True
        else:
            session['login'] = False
    else:
        session['login'] = False
    
    if session['login']:    
        return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))

#ログアウト
@app.route('/logout')
def logout():
    session.pop('login',None)
    return redirect(url_for('index'))

#status変更
@app.route('/uopdate/<string:key>/<string:st>', methods=['GET'])
def update(key,st):
    data = Data.query.get(key)
    data.status = st
    data.dt = datetime.now().isoformat(timespec='seconds')
    db.session.commit()
    return redirect(url_for('index'))

#アプリケーションの起動
if __name__ == '__main__' :
    app.run(debug=True)


