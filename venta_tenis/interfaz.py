import sqlite3
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

DB_NAME = "ventas_tenis.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        talla REAL,
        precio REAL,
        stock INTEGER
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        correo TEXT
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

# -------- TAB PANEL --------
class VentasTabbed(TabbedPanel):
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

        form = GridLayout(cols=4, spacing=5, size_hint=(1, None), height=40)
        self.txt_prod_nombre = TextInput(hint_text="Nombre")
        self.txt_prod_talla = TextInput(hint_text="Talla", input_filter="float")
        self.txt_prod_precio = TextInput(hint_text="Precio", input_filter="float")
        self.txt_prod_stock = TextInput(hint_text="Stock", input_filter="int")
        for w in [self.txt_prod_nombre, self.txt_prod_talla, self.txt_prod_precio, self.txt_prod_stock]:
            form.add_widget(w)
        layout.add_widget(form)

        btn_add = Button(text="Agregar Producto", size_hint=(1, None), height=40)
        btn_add.bind(on_press=self.agregar_producto)
        layout.add_widget(btn_add)

        self.scroll_prod = ScrollView(size_hint=(1, 1))
        self.table_prod = GridLayout(cols=5, size_hint_y=None, spacing=5)
        self.table_prod.bind(minimum_height=self.table_prod.setter("height"))
        self.scroll_prod.add_widget(self.table_prod)
        layout.add_widget(self.scroll_prod)

        tab.add_widget(layout)
        self.add_widget(tab)
        self.refresh_productos()

    def agregar_producto(self, instance):
        if not (self.txt_prod_nombre.text and self.txt_prod_talla.text and self.txt_prod_precio.text and self.txt_prod_stock.text):
            return
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO productos (nombre, talla, precio, stock) VALUES (?, ?, ?, ?)",
                (self.txt_prod_nombre.text, float(self.txt_prod_talla.text),
                 float(self.txt_prod_precio.text), int(self.txt_prod_stock.text))
            )
            conn.commit()
            conn.close()
            self.txt_prod_nombre.text = self.txt_prod_talla.text = self.txt_prod_precio.text = self.txt_prod_stock.text = ""
            self.refresh_productos()
        except:
            pass

    def refresh_productos(self):
        self.table_prod.clear_widgets()
        header = ["ID", "Nombre", "Talla", "Precio (Bs)", "Stock"]
        for h in header:
            self.table_prod.add_widget(Label(text=f"[b]{h}[/b]", markup=True, size_hint_y=None, height=30))

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, talla, precio, stock FROM productos")
        for p in cursor.fetchall():
            for item in p:
                self.table_prod.add_widget(Label(text=str(item) if item else "", size_hint_y=None, height=30))
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
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO clientes (nombre, correo) VALUES (?, ?)",
                       (self.txt_cli_nombre.text, self.txt_cli_correo.text))
        conn.commit()
        conn.close()
        self.txt_cli_nombre.text = self.txt_cli_correo.text = ""
        self.refresh_clientes()

    def refresh_clientes(self):
        self.table_cli.clear_widgets()
        header = ["ID", "Nombre", "Correo"]
        for h in header:
            self.table_cli.add_widget(Label(text=f"[b]{h}[/b]", markup=True, size_hint_y=None, height=30))

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, correo FROM clientes")
        for c in cursor.fetchall():
            for item in c:
                self.table_cli.add_widget(Label(text=str(item) if item else "", size_hint_y=None, height=30))
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
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT precio, stock FROM productos WHERE id=?", (int(self.txt_id_producto.text),))
            prod = cursor.fetchone()
            if prod:
                precio, stock = prod
                cantidad = int(self.txt_cantidad.text)
                if cantidad <= stock:
                    total = precio * cantidad
                    cursor.execute(
                        "INSERT INTO ventas (id_cliente, id_producto, cantidad, total) VALUES (?, ?, ?, ?)",
                        (int(self.txt_id_cliente.text), int(self.txt_id_producto.text), cantidad, total)
                    )
                    cursor.execute(
                        "UPDATE productos SET stock=? WHERE id=?",
                        (stock - cantidad, int(self.txt_id_producto.text))
                    )
                    conn.commit()
            conn.close()
            self.txt_id_cliente.text = self.txt_id_producto.text = self.txt_cantidad.text = ""
            self.refresh_ventas()
            self.refresh_productos()
        except:
            pass

    def refresh_ventas(self):
        self.table_ventas.clear_widgets()
        header = ["ID", "Cliente", "Producto", "Cantidad", "Total (Bs)"]
        for h in header:
            self.table_ventas.add_widget(Label(text=f"[b]{h}[/b]", markup=True, size_hint_y=None, height=30))

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT v.id, c.nombre, p.nombre, v.cantidad, v.total
            FROM ventas v
            JOIN clientes c ON v.id_cliente = c.id
            JOIN productos p ON v.id_producto = p.id
        """)
        for v in cursor.fetchall():
            for item in v:
                self.table_ventas.add_widget(Label(text=str(item) if item else "", size_hint_y=None, height=30))
        conn.close()


# -------- APP --------
class VentasApp(App):
    def build(self):
        init_db()
        root = BoxLayout(orientation="vertical")
        root.add_widget(Label(text="INTERFAZ DE LA TIENDA", size_hint=(1, 0.1), font_size=30, bold=True))
        root.add_widget(VentasTabbed())
        return root

if __name__ == "__main__":
    VentasApp().run()
