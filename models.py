# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Producto(db.Model):
    __tablename__ = "productos"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    talla = db.Column(db.Float, nullable=True)
    precio = db.Column(db.Float, nullable=True)
    stock = db.Column(db.Integer, nullable=True)

    ventas = db.relationship("Venta", backref="producto", lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Producto {self.nombre} - Talla {self.talla}>"


class Cliente(db.Model):
    __tablename__ = "clientes"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), nullable=True)

    ventas = db.relationship("Venta", backref="cliente", lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Cliente {self.nombre}>"


class Venta(db.Model):
    __tablename__ = "ventas"
    id = db.Column(db.Integer, primary_key=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey("clientes.id"), nullable=False)
    id_producto = db.Column(db.Integer, db.ForeignKey("productos.id"), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Venta {self.id}: Cliente {self.id_cliente}, Producto {self.id_producto}, Cantidad {self.cantidad}>"
