from db import db
from flask import *
from cryptography.fernet import Fernet
key = bytes('1BtO6rcED37HjLiKI5BiYBuWK77C_C8B5Kz2S7GYcK8=', encoding='utf-8')
cipher_suite = Fernet(key)

#from Cryptodome.Cipher import AES
#key = bytes("gx3nwpl03Ffdo8NPhTSZHfTXML9n7WXa", encoding='utf-8')
#cipher_suite = AES.new(key, AES.MODE_EAX)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    company = db.Column(db.String, nullable=False)

    def __init__(self, email, password, company):
        self.email = email
        self.password = password
        self.company = company

    @classmethod
    def get_by_email(cls, email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def login_valid(email, password):
        user = User.get_by_email(email)
        if user is not None:
            encrypted_pass = cipher_suite.decrypt(bytes(user.password, encoding='utf-8'))
            decrypted_pass = str(encrypted_pass, encoding='utf-8')
            return decrypted_pass == password
        return False

    @classmethod
    def create_user(cls, email, password, company):
        cipher_text = cipher_suite.encrypt(bytes(password, encoding='utf-8'))
        passwordtostore = str(cipher_text, encoding='utf-8')
        try:
            usertoadd = cls(email, passwordtostore, company)
            usertoadd.save_to_db()
            return True
        except:
            return False

    @staticmethod
    def login(user_email):
        session['email'] = user_email

    @staticmethod
    def logout():
        session['email'] = None

    def json(self):
        return {
            "email": self.email,
            "password": self.password
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
