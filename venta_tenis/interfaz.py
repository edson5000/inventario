import sqlite3
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

DB_VENTAS = "ventas_tenis.db"
DB_CLIENTES = "clientes.db"

# ----------------- Conexiones -----------------
def get_ventas_connection():
    return sqlite3.connect(DB_VENTAS)

def get_clientes_connection():
    return sqlite3.connect(DB_CLIENTES)

# ----------------- Inicializar BD -----------------
def init_db():
    # Productos y ventas
    conn = get_ventas_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        talla REAL,
        color TEXT,
        precio REAL,
        stock INTEGER
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ventas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_cliente INTEGER,
        id_producto INTEGER,
        cantidad INTEGER,
        total REAL,
        FOREIGN KEY (id_cliente) REFERENCES clientes(id),
        FOREIGN KEY (id_producto) REFERENCES productos(id)
    )
    """)
    conn.commit()
    conn.close()

    # Clientes
    conn = get_clientes_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT
    )
    """)
    # Asegurar columna correo
    cursor.execute("PRAGMA table_info(clientes)")
    columnas = [col[1] for col in cursor.fetchall()]
    if "correo" not in columnas:
        cursor.execute("ALTER TABLE clientes ADD COLUMN correo TEXT")
    conn.commit()
    conn.close()

# ----------------- Interfaz -----------------
class AdminTabbed(TabbedPanel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.do_default_tab = False
        self.build_productos_tab()
        self.build_clientes_tab()
        self.build_ventas_tab()

    # -------- PRODUCTOS --------
    def build_productos_tab(self):
        tab = TabbedPanelItem(text="Productos")
        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        # Formulario agregar producto
        form = GridLayout(cols=5, spacing=5, size_hint=(1, None), height=40)
        self.txt_prod_nombre = TextInput(hint_text="Nombre")
        self.txt_prod_talla = TextInput(hint_text="Talla", input_filter="float")
        self.txt_prod_color = TextInput(hint_text="Color")
        self.txt_prod_precio = TextInput(hint_text="Precio", input_filter="float")
        self.txt_prod_stock = TextInput(hint_text="Stock", input_filter="int")
        for w in [self.txt_prod_nombre, self.txt_prod_talla, self.txt_prod_color, self.txt_prod_precio, self.txt_prod_stock]:
            form.add_widget(w)
        layout.add_widget(form)

        btn_add = Button(text="Agregar Producto", size_hint=(1, None), height=40)
        btn_add.bind(on_press=self.agregar_producto)
        layout.add_widget(btn_add)

        # Tabla de productos
        self.scroll_prod = ScrollView(size_hint=(1, 1))
        self.table_prod = GridLayout(cols=6, size_hint_y=None, spacing=5)
        self.table_prod.bind(minimum_height=self.table_prod.setter("height"))
        self.scroll_prod.add_widget(self.table_prod)
        layout.add_widget(self.scroll_prod)

        tab.add_widget(layout)
        self.add_widget(tab)
        self.refresh_productos()

    def agregar_producto(self, instance):
        if not (self.txt_prod_nombre.text and self.txt_prod_talla.text and self.txt_prod_color.text
                and self.txt_prod_precio.text and self.txt_prod_stock.text):
            return
        try:
            conn = get_ventas_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO productos (nombre, talla, color, precio, stock) VALUES (?, ?, ?, ?, ?)",
                (self.txt_prod_nombre.text, float(self.txt_prod_talla.text),
                 self.txt_prod_color.text, float(self.txt_prod_precio.text), int(self.txt_prod_stock.text))
            )
            conn.commit()
            conn.close()
            # Limpiar inputs
            self.txt_prod_nombre.text = self.txt_prod_talla.text = self.txt_prod_color.text = ""
            self.txt_prod_precio.text = self.txt_prod_stock.text = ""
            self.refresh_productos()
        except Exception as e:
            print("Error:", e)

    def refresh_productos(self):
        self.table_prod.clear_widgets()
        headers = ["ID", "Nombre", "Talla", "Color", "Precio", "Stock"]
        for h in headers:
            self.table_prod.add_widget(Label(text=f"[b]{h}[/b]", markup=True, size_hint_y=None, height=30))

        conn = get_ventas_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, talla, color, precio, stock FROM productos")
        for p in cursor.fetchall():
            for item in p:
                self.table_prod.add_widget(Label(text=str(item), size_hint_y=None, height=30))
        conn.close()

    # -------- CLIENTES --------
    def build_clientes_tab(self):
        tab = TabbedPanelItem(text="Clientes")
        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        form = GridLayout(cols=2, spacing=5, size_hint=(1, None), height=40)
        self.txt_cli_nombre = TextInput(hint_text="Nombre")
        self.txt_cli_correo = TextInput(hint_text="Correo")
        form.add_widget(self.txt_cli_nombre)
        form.add_widget(self.txt_cli_correo)
        layout.add_widget(form)

        btn_add = Button(text="Agregar Cliente", size_hint=(1, None), height=40)
        btn_add.bind(on_press=self.agregar_cliente)
        layout.add_widget(btn_add)

        self.scroll_cli = ScrollView(size_hint=(1, 1))
        self.table_cli = GridLayout(cols=3, size_hint_y=None, spacing=5)
        self.table_cli.bind(minimum_height=self.table_cli.setter("height"))
        self.scroll_cli.add_widget(self.table_cli)
        layout.add_widget(self.scroll_cli)

        tab.add_widget(layout)
        self.add_widget(tab)
        self.refresh_clientes()

    def agregar_cliente(self, instance):
        if not (self.txt_cli_nombre.text and self.txt_cli_correo.text):
            return
        conn = get_clientes_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO clientes (nombre, correo) VALUES (?, ?)",
                       (self.txt_cli_nombre.text, self.txt_cli_correo.text))
        conn.commit()
        conn.close()
        self.txt_cli_nombre.text = self.txt_cli_correo.text = ""
        self.refresh_clientes()

    def refresh_clientes(self):
        self.table_cli.clear_widgets()
        headers = ["ID", "Nombre", "Correo"]
        for h in headers:
            self.table_cli.add_widget(Label(text=f"[b]{h}[/b]", markup=True, size_hint_y=None, height=30))

        conn = get_clientes_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, correo FROM clientes")
        for c in cursor.fetchall():
            for item in c:
                self.table_cli.add_widget(Label(text=str(item), size_hint_y=None, height=30))
        conn.close()

    # -------- VENTAS --------
    def build_ventas_tab(self):
        tab = TabbedPanelItem(text="Ventas")
        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        form = GridLayout(cols=3, spacing=5, size_hint=(1, None), height=40)
        self.txt_id_cliente = TextInput(hint_text="ID Cliente", input_filter="int")
        self.txt_id_producto = TextInput(hint_text="ID Producto", input_filter="int")
        self.txt_cantidad = TextInput(hint_text="Cantidad", input_filter="int")
        form.add_widget(self.txt_id_cliente)
        form.add_widget(self.txt_id_producto)
        form.add_widget(self.txt_cantidad)
        layout.add_widget(form)

        btn_add = Button(text="Registrar Venta", size_hint=(1, None), height=40)
        btn_add.bind(on_press=self.agregar_venta)
        layout.add_widget(btn_add)

        self.scroll_ventas = ScrollView(size_hint=(1, 1))
        self.table_ventas = GridLayout(cols=5, size_hint_y=None, spacing=5)
        self.table_ventas.bind(minimum_height=self.table_ventas.setter("height"))
        self.scroll_ventas.add_widget(self.table_ventas)
        layout.add_widget(self.scroll_ventas)

        tab.add_widget(layout)
        self.add_widget(tab)
        self.refresh_ventas()

    def agregar_venta(self, instance):
        if not (self.txt_id_cliente.text and self.txt_id_producto.text and self.txt_cantidad.text):
            return
        try:
            conn_ventas = get_ventas_connection()
            cursor_ventas = conn_ventas.cursor()
            cursor_ventas.execute("SELECT precio, stock FROM productos WHERE id=?", (int(self.txt_id_producto.text),))
            prod = cursor_ventas.fetchone()
            if prod:
                precio, stock = prod
                cantidad = int(self.txt_cantidad.text)
                if cantidad <= stock:
                    total = precio * cantidad
                    cursor_ventas.execute(
                        "INSERT INTO ventas (id_cliente, id_producto, cantidad, total) VALUES (?, ?, ?, ?)",
                        (int(self.txt_id_cliente.text), int(self.txt_id_producto.text), cantidad, total)
                    )
                    cursor_ventas.execute(
                        "UPDATE productos SET stock=? WHERE id=?",
                        (stock - cantidad, int(self.txt_id_producto.text))
                    )
                    conn_ventas.commit()
            conn_ventas.close()
            self.txt_id_cliente.text = self.txt_id_producto.text = self.txt_cantidad.text = ""
            self.refresh_ventas()
            self.refresh_productos()
        except Exception as e:
            print("Error:", e)

    def refresh_ventas(self):
        self.table_ventas.clear_widgets()
        headers = ["ID", "Cliente", "Producto", "Cantidad", "Total"]
        for h in headers:
            self.table_ventas.add_widget(Label(text=f"[b]{h}[/b]", markup=True, size_hint_y=None, height=30))

        conn_ventas = get_ventas_connection()
        conn_clientes = get_clientes_connection()
        cursor_ventas = conn_ventas.cursor()
        cursor_clientes = conn_clientes.cursor()
        cursor_ventas.execute("SELECT id, id_cliente, id_producto, cantidad, total FROM ventas")
        ventas = cursor_ventas.fetchall()
        for v in ventas:
            # Obtener nombre cliente
            cursor_clientes.execute("SELECT nombre FROM clientes WHERE id=?", (v[1],))
            cliente = cursor_clientes.fetchone()
            cliente_nombre = cliente[0] if cliente else "Desconocido"
            # Obtener nombre producto
            cursor_ventas.execute("SELECT nombre FROM productos WHERE id=?", (v[2],))
            producto = cursor_ventas.fetchone()
            producto_nombre = producto[0] if producto else "Desconocido"
            for item in [v[0], cliente_nombre, producto_nombre, v[3], v[4]]:
                self.table_ventas.add_widget(Label(text=str(item), size_hint_y=None, height=30))
        conn_ventas.close()
        conn_clientes.close()


# ----------------- APP -----------------
class AdminApp(App):
    def build(self):
        init_db()
        root = BoxLayout(orientation="vertical")
        titulo = Label(
            text="[b][color=ff3333]ADMINISTRACIÓN DE TIENDA DE TENIS[/color][/b]",
            markup=True,
            font_size=40,
            size_hint=(1, 0.15),
            halign="center",
            valign="middle"
        )
        titulo.bind(size=titulo.setter("text_size"))
        root.add_widget(titulo)

        root.add_widget(AdminTabbed())
        return root

if __name__ == "__main__":
    AdminApp().run()
