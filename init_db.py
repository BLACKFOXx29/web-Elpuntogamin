from app import app
from models import db, User, Miembro, Evento, Imagen, Mensaje, Producto
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

with app.app_context():
    db.create_all()

    # Crear admin por defecto si no existe
    if not User.query.filter_by(username='BLACKFOXx29').first():
        admin = User(username='BLACKFOXx29', email='misael.garcia.0229@elpuntogaming.local', password_hash=generate_password_hash('252902Ventura@'), is_admin=True)
        db.session.add(admin)
        db.session.commit()

    # Datos de ejemplo
    if not Evento.query.first():
        e1 = Evento(titulo='Torneo Nacional de League of Legends', descripcion='Gran torneo nacional', fecha=datetime.utcnow() + timedelta(days=30))
        e2 = Evento(titulo='Smash Ultimate RD Cup', descripcion='Batallas épicas', fecha=datetime.utcnow() + timedelta(days=60))
        db.session.add_all([e1,e2])
        db.session.commit()

    if not Producto.query.first():
        p1 = Producto(nombre='Camiseta El Punto Gaming', descripcion='Camiseta oficial', precio=15.99, stock=30)
        p2 = Producto(nombre='Mouse Gamer', descripcion='Mouse RGB', precio=49.99, stock=10)
        db.session.add_all([p1,p2])
        db.session.commit()
