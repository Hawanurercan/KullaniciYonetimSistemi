from flask import Flask
from models import db
from routes import user_routes
from config import Config

#flask uygulamasını baslatır
app=Flask(__name__)
app.config.from_object(Config)

#databasi baslatır
db.init_app(app)

#register_blueprint: Uygulamaya bir blueprint ekler. Blueprint, rotaları 
# (URL yolları) organize etmek için kullanılan bir Flask özelliğidir. 
# Burada user_routes, kullanıcılarla ilgili rotaları içeren bir Blueprint'tir.
app.register_blueprint(user_routes)


#veritabanini baslat
with app.app_context():
    db.create_all()
    
if __name__=='__main__':
    app.run(debug=True)
        
    
    
    
    
    
    
    
    
    
    
    
    
    