#Bu kod, bir Flask Blueprint kullanarak temel bir kullanıcı yönetim sistemi 
# API'si oluşturur. API, kullanıcı kaydı, girişi, listeleme, güncelleme ve 
# silme gibi işlevler sunar. Ayrıca JWT (JSON Web Token) kullanarak güvenlik 
# sağlanır. Kodun detaylı açıklaması aşağıda verilmiştir:


from flask import Blueprint,request,jsonify

from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager,create_access_token, jwt_required
from models import db, User

user_routes=Blueprint('user_routes',__name__)

#bir uygulamaya erişim için gerekli olan access token'ı oluşturmak için kullanılan bir standarttır
jwt =JWTManager()

#kullanıcı kaydı
# 
@user_routes.route('/register',methods=['POST'])
def register():
    data=request.json #requestten gelen veriyi alıyoruz
    hashed_password=generate_password_hash(data['password'],method='sha256')
    new_user=User(username=data['username'],email=data['email'],password=hashed_password)
    
    db.session.add(new_user)#db kullanici ekler
    db.session.commit()#kaydet
    return jsonify({"message":"kullanici başariyla oluşturuldu"}),201

# Kullanıcı Girişi
@user_routes.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()

    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({"message": "Geçersiz kullanıcı adı veya şifre"}), 401

    token = create_access_token(identity={"username": user.username, "email": user.email})
    return jsonify({"token": token})

# Kullanıcı Listeleme
@user_routes.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    users = User.query.all()
    return jsonify([{"id": user.id, "username": user.username, "email": user.email} for user in users])

# Kullanıcı Güncelleme
@user_routes.route('/users/<int:id>', methods=['PUT'])
@jwt_required()
def update_user(id):
    data = request.json
    user = User.query.get(id)

    if not user:
        return jsonify({"message": "Kullanıcı bulunamadı!"}), 404

    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)

    db.session.commit()
    return jsonify({"message": "Kullanıcı başarıyla güncellendi!"})

# Kullanıcı Silme
@user_routes.route('/users/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    user = User.query.get(id)

    if not user:
        return jsonify({"message": "Kullanıcı bulunamadı!"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Kullanıcı başarıyla silindi!"})







