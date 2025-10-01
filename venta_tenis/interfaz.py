import sqlite3
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.core.window import Window

DB_VENTAS = "ventas_tenis.db"
DB_CLIENTES = "clientes.db"

# ----------------- Conexiones -----------------
def get_ventas_connection():
    return sqlite3.connect(DB_VENTAS)

def get_clientes_connection():
    return sqlite3.connect(DB_CLIENTES)

# ----------------- Inicializar BD -----------------
def init_db():
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

    conn = get_clientes_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        correo TEXT
    )
    """)
    conn.commit()
    conn.close()

# ----------------- Interfaz -----------------
class AdminTabbed(TabbedPanel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.do_default_tab = False
        self.tab_spacing = 5
        self.tab_height = 40
        self.build_productos_tab()
        self.build_clientes_tab()
        self.build_ventas_tab()

    # -------- PRODUCTOS --------
    def build_productos_tab(self):
        tab = TabbedPanelItem(text="Productos")
        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        self.scroll_prod = ScrollView(size_hint=(1, 1))
        self.table_prod = GridLayout(cols=6, size_hint_y=None, spacing=5, row_default_height=40)
        self.table_prod.bind(minimum_height=self.table_prod.setter("height"))
        self.scroll_prod.add_widget(self.table_prod)
        layout.add_widget(self.scroll_prod)

        tab.add_widget(layout)
        self.add_widget(tab)
        self.refresh_productos()

    def refresh_productos(self):
        self.table_prod.clear_widgets()
        headers = ["ID", "Nombre", "Talla", "Color", "Precio", "Stock"]
        for h in headers:
            self.table_prod.add_widget(Label(text=f"[b]{h}[/b]", markup=True, size_hint_y=None, height=40, color=(0, 0.5, 1, 1)))

        conn = get_ventas_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, talla, color, precio, stock FROM productos")
        for p in cursor.fetchall():
            for item in p:
                self.table_prod.add_widget(Label(text=str(item), size_hint_y=None, height=35))
        conn.close()

    # -------- CLIENTES --------
    def build_clientes_tab(self):
        tab = TabbedPanelItem(text="Clientes")
        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        self.scroll_cli = ScrollView(size_hint=(1, 1))
        self.table_cli = GridLayout(cols=3, size_hint_y=None, spacing=5, row_default_height=40)
        self.table_cli.bind(minimum_height=self.table_cli.setter("height"))
        self.scroll_cli.add_widget(self.table_cli)
        layout.add_widget(self.scroll_cli)

        tab.add_widget(layout)
        self.add_widget(tab)
        self.refresh_clientes()

    def refresh_clientes(self):
        self.table_cli.clear_widgets()
        headers = ["ID", "Nombre", "Correo"]
        for h in headers:
            self.table_cli.add_widget(Label(text=f"[b]{h}[/b]", markup=True, size_hint_y=None, height=40, color=(1, 0.5, 0, 1)))

        conn = get_clientes_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, correo FROM clientes")
        for c in cursor.fetchall():
            for item in c:
                self.table_cli.add_widget(Label(text=str(item), size_hint_y=None, height=35))
        conn.close()

    # -------- VENTAS --------
    def build_ventas_tab(self):
        tab = TabbedPanelItem(text="Ventas")
        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        self.scroll_ventas = ScrollView(size_hint=(1, 1))
        self.table_ventas = GridLayout(cols=5, size_hint_y=None, spacing=5, row_default_height=40)
        self.table_ventas.bind(minimum_height=self.table_ventas.setter("height"))
        self.scroll_ventas.add_widget(self.table_ventas)
        layout.add_widget(self.scroll_ventas)

        tab.add_widget(layout)
        self.add_widget(tab)
        self.refresh_ventas()

    def refresh_ventas(self):
        self.table_ventas.clear_widgets()
        headers = ["ID", "Cliente", "Producto", "Cantidad", "Total"]
        for h in headers:
            self.table_ventas.add_widget(Label(text=f"[b]{h}[/b]", markup=True, size_hint_y=None, height=40, color=(0, 1, 0.5, 1)))

        conn_ventas = get_ventas_connection()
        conn_clientes = get_clientes_connection()
        cursor_ventas = conn_ventas.cursor()
        cursor_clientes = conn_clientes.cursor()
        cursor_ventas.execute("SELECT id, id_cliente, id_producto, cantidad, total FROM ventas")
        ventas = cursor_ventas.fetchall()
        for v in ventas:
            cursor_clientes.execute("SELECT nombre FROM clientes WHERE id=?", (v[1],))
            cliente = cursor_clientes.fetchone()
            cliente_nombre = cliente[0] if cliente else "Desconocido"

            cursor_ventas.execute("SELECT nombre FROM productos WHERE id=?", (v[2],))
            producto = cursor_ventas.fetchone()
            producto_nombre = producto[0] if producto else "Desconocido"

            for item in [v[0], cliente_nombre, producto_nombre, v[3], v[4]]:
                self.table_ventas.add_widget(Label(text=str(item), size_hint_y=None, height=35))
        conn_ventas.close()
        conn_clientes.close()

# ----------------- APP -----------------
class AdminApp(App):
    def build(self):
        init_db()
        Window.size = (1000, 700)  # Tamaño de la ventana
        root = BoxLayout(orientation="vertical", padding=10, spacing=10)

        titulo = Label(
            text="[b][color=ff3333]ADMINISTRACIÓN DE TIENDA DE TENIS[/color][/b]",
            markup=True,
            font_size=32,
            size_hint=(1, 0.1),
            halign="center",
            valign="middle"
        )
        titulo.bind(size=titulo.setter("text_size"))
        root.add_widget(titulo)

        root.add_widget(AdminTabbed())
        return root

if __name__ == "__main__":
    AdminApp().run()
