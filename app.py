from flask import Flask, render_template
from models import db, Producto, Cliente, Venta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ventas_tenis.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# --- Ruta principal ---
@app.route('/')
def index():
    productos = Producto.query.all()
    clientes = Cliente.query.all()
    ventas = Venta.query.all()
    return render_template('index.html', productos=productos, clientes=clientes, ventas=ventas)

# --- Ejecutar app ---
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Solo crea tablas si no existen
    app.run(debug=True)
