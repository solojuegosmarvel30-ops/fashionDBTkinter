
from datetime import datetime
import os
import re
from pathlib import Path
from tkinter import messagebox, simpledialog, ttk
import tkinter as tk
from bson.objectid import ObjectId
from pymongo import MongoClient
from tkcalendar import Calendar

# Configuración de conexión a MongoDB
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "fashiondb"


def conectar_db():
  try:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    client.admin.command("ping")
    return db
  except Exception as e:
    messagebox.showerror(
        "Error de Conexión",
        f"No se pudo conectar a MongoDB:\n{e}\n\nVerifica que el servicio"
        " esté encendido.",
    )
    return None


class FashionApp:

  def __init__(self, root):
    self.root = root
    self.root.title(
        "FashionDB | Suite Ejecutiva de Lujo & Inteligencia Comercial"
    )
    self.root.geometry("1420x820")
    self.root.minsize(1200, 720)

    # Paleta de Colores de Lujo (Modo Oscuro Ejecutivo)
    self.c_bg_main = "#0b0f19"
    self.c_sidebar = "#111827"
    self.c_sidebar_hover = "#1f2937"
    self.c_card = "#1f2937"
    self.c_primary = "#3b82f6"
    self.c_accent = "#10b981"
    self.c_danger = "#ef4444"
    self.c_gold = "#d97706"
    self.c_text_light = "#f9fafb"
    self.c_text_muted = "#9ca3af"
    self.c_zebra = "#253245"

    self.root.config(bg=self.c_bg_main)
    self.orden_estados = {}

    self.configurar_favicon()
    self.configurar_estilos_ttk()
    self.crear_sidebar()
    self.crear_panel_principal()

    self.listar_prendas()

  def configurar_favicon(self):
    """Carga el icono principal de FashionDB."""

    # Obtener la ubicación de la carpeta del proyecto
    carpeta_proyecto = Path(__file__).resolve().parent

    # Ubicación del archivo del icono
    icon_path = carpeta_proyecto / "fashion_icon.ico"

    try:
      # Comprobar si existe el archivo
      if icon_path.exists():
        # Colocar el icono en la ventana principal
        self.root.iconbitmap(str(icon_path))
        print("Icono FashionDB cargado correctamente.")
      else:
        print("No se encontró el archivo fashion_icon.ico")
    except Exception as e:
      print(f"No se pudo cargar el icono: {e}")

  def configurar_estilos_ttk(self):
    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        "Custom.Treeview",
        background=self.c_card,
        foreground=self.c_text_light,
        rowheight=36,
        fieldbackground=self.c_card,
        borderwidth=0,
        font=("Segoe UI", 10),
    )
    style.configure(
        "Custom.Treeview.Heading",
        background="#374151",
        foreground="#f3f4f6",
        relief="flat",
        font=("Segoe UI", 10, "bold"),
        padding=(10, 8),
    )
    style.map("Custom.Treeview.Heading", background=[("active", "#4b5563")])
    style.map(
        "Custom.Treeview",
        background=[("selected", "#2563eb")],
        foreground=[("selected", "#ffffff")],
    )

  def crear_boton_menu(self, parent, texto, comando, icono="▸"):
    btn = tk.Button(
        parent,
        text=f"  {icono}   {texto}",
        font=("Segoe UI", 10),
        bg=self.c_sidebar,
        fg="#d1d5db",
        activebackground=self.c_sidebar_hover,
        activeforeground="#ffffff",
        bd=0,
        anchor="w",
        cursor="hand2",
        padx=15,
        pady=9,
        command=comando,
    )
    btn.pack(fill=tk.X, padx=10, pady=2)
    btn.bind(
        "<Enter>", lambda e: btn.config(bg=self.c_sidebar_hover, fg="#60a5fa")
    )
    btn.bind("<Leave>", lambda e: btn.config(bg=self.c_sidebar, fg="#d1d5db"))
    return btn

  def crear_sidebar(self):
    self.sidebar = tk.Frame(self.root, bg=self.c_sidebar, width=315)
    self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
    self.sidebar.pack_propagate(False)

    brand_frame = tk.Frame(self.sidebar, bg=self.c_sidebar)
    brand_frame.pack(fill=tk.X, pady=(20, 15), padx=20)

    tk.Label(
        brand_frame,
        text="✨ FASHION DB",
        font=("Segoe UI", 18, "bold"),
        bg=self.c_sidebar,
        fg="#60a5fa",
    ).pack(anchor="w")
    tk.Label(
        brand_frame,
        text="Enterprise Fashion Suite",
        font=("Segoe UI", 9),
        bg=self.c_sidebar,
        fg=self.c_text_muted,
    ).pack(anchor="w")

    tk.Frame(self.sidebar, bg="#374151", height=1).pack(
        fill=tk.X, padx=20, pady=5
    )

    # Reportes Oficiales
    tk.Label(
        self.sidebar,
        text="REPORTES OFICIALES",
        font=("Segoe UI", 8, "bold"),
        bg=self.c_sidebar,
        fg="#9ca3af",
    ).pack(anchor="w", padx=25, pady=(10, 4))

    self.crear_boton_menu(
        self.sidebar, "Ingresos por Colección", self.reporte_1, "📊"
    )
    self.crear_boton_menu(
        self.sidebar, "Existencias por Talla", self.reporte_2, "📏"
    )
    self.crear_boton_menu(
        self.sidebar, "Prendas por Diseñador", self.reporte_3, "✂️"
    )

    # Catálogo y Entidades
    tk.Label(
        self.sidebar,
        text="GESTIÓN Y COLECCIONES",
        font=("Segoe UI", 8, "bold"),
        bg=self.c_sidebar,
        fg="#9ca3af",
    ).pack(anchor="w", padx=25, pady=(15, 4))

    self.crear_boton_menu(
        self.sidebar, "Inventario General (Prendas)", self.listar_prendas, "👗"
    )
    self.crear_boton_menu(
        self.sidebar, "Directorio de Vendedores", self.listar_vendedores, "👤"
    )
    self.crear_boton_menu(
        self.sidebar, "Red de Tiendas Oficiales", self.listar_tiendas, "🏬"
    )
    self.crear_boton_menu(
        self.sidebar, "Talleres de Confección", self.listar_talleres, "🏭"
    )
    self.crear_boton_menu(
        self.sidebar,
        "Prendas Gama Alta (> $200k)",
        self.consulta_precio_alto,
        "💎",
    )
    self.crear_boton_menu(
        self.sidebar,
        "Diseñadores por Ciudad",
        self.consulta_disenadores_ciudad,
        "📍",
    )

    # Inteligencia Comercial
    tk.Label(
        self.sidebar,
        text="INTELIGENCIA COMERCIAL",
        font=("Segoe UI", 8, "bold"),
        bg=self.c_sidebar,
        fg=self.c_gold,
    ).pack(anchor="w", padx=25, pady=(15, 4))

    self.crear_boton_menu(
        self.sidebar,
        "Ventas por Tienda (con Fecha)",
        self.consultar_ventas_por_tienda_dialogo,
        "🏢",
    )
    self.crear_boton_menu(
        self.sidebar,
        "Ventas por Vendedor (con Fecha)",
        self.consultar_ventas_por_vendedor_dialogo,
        "👨‍💼",
    )
    self.crear_boton_menu(
        self.sidebar,
        "Calendario de Nuevas Prendas",
        self.abrir_panel_calendario,
        "📅",
    )

    footer = tk.Label(
        self.sidebar,
        text="MongoDB • Conectado 2026",
        font=("Segoe UI", 8),
        bg=self.c_sidebar,
        fg="#4b5563",
    )
    footer.pack(side=tk.BOTTOM, pady=10)

  def crear_panel_principal(self):
    self.main = tk.Frame(self.root, bg=self.c_bg_main)
    self.main.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=25, pady=20)

    top_card = tk.Frame(
        self.main,
        bg=self.c_card,
        highlightbackground="#374151",
        highlightthickness=1,
    )
    top_card.pack(fill=tk.X, pady=(0, 15))

    title_box = tk.Frame(top_card, bg=self.c_card)
    title_box.pack(side=tk.LEFT, padx=20, pady=18)

    self.lbl_titulo = tk.Label(
        title_box,
        text="Inventario General de Prendas",
        font=("Segoe UI", 16, "bold"),
        bg=self.c_card,
        fg=self.c_text_light,
    )
    self.lbl_titulo.pack(anchor="w")

    self.lbl_subtitulo = tk.Label(
        title_box,
        text=(
            "Haz clic en cualquier título de columna para ordenar (Asc / Desc)"
        ),
        font=("Segoe UI", 9),
        bg=self.c_card,
        fg=self.c_text_muted,
    )
    self.lbl_subtitulo.pack(anchor="w")

    actions_box = tk.Frame(top_card, bg=self.c_card)
    actions_box.pack(side=tk.RIGHT, padx=20, pady=18)

    tk.Button(
        actions_box,
        text="🔍 Buscar Ref",
        font=("Segoe UI", 9, "bold"),
        bg="#475569",
        fg="#ffffff",
        activebackground="#64748b",
        activeforeground="white",
        bd=0,
        cursor="hand2",
        padx=12,
        pady=8,
        command=self.buscar_por_referencia_dialogo,
    ).pack(side=tk.LEFT, padx=6)

    tk.Button(
        actions_box,
        text="+ Nueva Prenda",
        font=("Segoe UI", 9, "bold"),
        bg=self.c_accent,
        fg="#ffffff",
        activebackground="#059669",
        activeforeground="white",
        bd=0,
        cursor="hand2",
        padx=14,
        pady=8,
        command=self.abrir_ventana_crear,
    ).pack(side=tk.LEFT, padx=6)

    tk.Button(
        actions_box,
        text="✎ Editar",
        font=("Segoe UI", 9, "bold"),
        bg=self.c_primary,
        fg="#ffffff",
        activebackground="#2563eb",
        activeforeground="white",
        bd=0,
        cursor="hand2",
        padx=14,
        pady=8,
        command=self.abrir_ventana_actualizar,
    ).pack(side=tk.LEFT, padx=6)

    tk.Button(
        actions_box,
        text="🗑 Eliminar",
        font=("Segoe UI", 9, "bold"),
        bg=self.c_danger,
        fg="#ffffff",
        activebackground="#dc2626",
        activeforeground="white",
        bd=0,
        cursor="hand2",
        padx=14,
        pady=8,
        command=self.eliminar_prenda,
    ).pack(side=tk.LEFT, padx=(6, 0))

    table_card = tk.Frame(
        self.main,
        bg=self.c_card,
        highlightbackground="#374151",
        highlightthickness=1,
    )
    table_card.pack(fill=tk.BOTH, expand=True)

    self.tree = ttk.Treeview(
        table_card, show="headings", style="Custom.Treeview"
    )
    self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=1, pady=1)

    self.tree.tag_configure("evenrow", background=self.c_card)
    self.tree.tag_configure("oddrow", background=self.c_zebra)

    scrollbar = ttk.Scrollbar(
        table_card, orient=tk.VERTICAL, command=self.tree.yview
    )
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    self.tree.configure(yscrollcommand=scrollbar.set)

    self.status_bar = tk.Label(
        self.main,
        text="Listo • 0 registros mostrados",
        font=("Segoe UI", 9),
        bg=self.c_bg_main,
        fg=self.c_text_muted,
        anchor="w",
    )
    self.status_bar.pack(fill=tk.X, pady=(8, 0))

  def limpiar_tabla(self):
    for item in self.tree.get_children():
      self.tree.delete(item)
    self.tree["columns"] = ()
    self.orden_estados.clear()

  def configurar_columnas(self, columnas):
    self.tree["columns"] = columnas
    for col in columnas:
      self.tree.heading(
          col,
          text=f"{col} ↕",
          command=lambda c=col: self.ordenar_por_columna_especifica(c),
      )
      self.tree.column(col, anchor=tk.CENTER, width=170)
      self.orden_estados[col] = False

  def insertar_filas_estilizadas(self, filas, texto_estado_extra=""):
    for idx, fila in enumerate(filas):
      tag = "evenrow" if idx % 2 == 0 else "oddrow"
      self.tree.insert("", tk.END, values=fila, tags=(tag,))

    base_msg = f"Mostrando {len(filas)} registro(s)"
    if texto_estado_extra:
      base_msg += f" • {texto_estado_extra}"
    self.status_bar.config(text=base_msg)

  def _extraer_valor_ordenamiento(self, texto):
    s = str(texto).strip()
    limpio = re.sub(r"[\$,\.]", "", s)
    if limpio.isdigit() or (limpio.startswith("-") and limpio[1:].isdigit()):
      return (0, float(limpio))
    return (1, s.lower())

  def ordenar_por_columna_especifica(self, col):
    columnas = list(self.tree["columns"])
    idx = columnas.index(col)
    items = self.tree.get_children("")
    if not items:
      return

    descendente = not self.orden_estados[col]
    self.orden_estados[col] = descendente

    for c in columnas:
      flecha = " ↕"
      if c == col:
        flecha = " ⬇" if descendente else " ⬆"
      self.tree.heading(
          c,
          text=f"{c}{flecha}",
          command=lambda x=c: self.ordenar_por_columna_especifica(x),
      )

    datos = [(self.tree.item(item, "values")[idx], item) for item in items]
    datos.sort(
        key=lambda x: self._extraer_valor_ordenamiento(x[0]),
        reverse=descendente,
    )

    for index, (_, item) in enumerate(datos):
      self.tree.move(item, "", index)
      tag = "evenrow" if index % 2 == 0 else "oddrow"
      self.tree.item(item, tags=(tag,))

    sentido_txt = "Mayor a Menor" if descendente else "Menor a Mayor"
    self.status_bar.config(
        text=f"Ordenado por '{col}' ({sentido_txt})"
    )

  # ================= BÚSQUEDA ESPECÍFICA POR REFERENCIA =================
  def buscar_por_referencia_dialogo(self):
    ref_buscada = simpledialog.askstring(
        "Consultar por Referencia",
        "Ingresa la referencia de la prenda (ej. REF001):",
    )
    if not ref_buscada:
      return

    db = conectar_db()
    if db is None:
      return

    self.limpiar_tabla()
    self.configurar_columnas((
        "ID",
        "Referencia",
        "Nombre Prenda",
        "Diseñador",
        "Existencias",
        "Precio Unitario",
    ))

    try:
      query = {"referencia": {"$regex": ref_buscada.strip(), "$options": "i"}}
      filas = []
      for doc in db.prendas.find(query):
        disenador_nombre = doc.get("disenador", {}).get("nombre", "Sin asignar")
        tallas_lista = doc.get("tallas", [])
        total_stock = sum(
            t.get("existencias", 0)
            for t in tallas_lista
            if isinstance(t, dict)
        )
        filas.append((
            str(doc.get("_id")),
            doc.get("referencia", "N/A"),
            doc.get("nombre", ""),
            disenador_nombre,
            total_stock,
            f"${doc.get('precio', 0):,.0f}".replace(",", "."),
        ))

      self.lbl_titulo.config(
          text=f"Búsqueda por Referencia: '{ref_buscada}'"
      )
      self.lbl_subtitulo.config(
          text=f"Resultados coincidentes en catálogo de prendas"
      )
      self.insertar_filas_estilizadas(
          filas, f"Coincidencias para '{ref_buscada}'"
      )
    except Exception as e:
      messagebox.showerror("Error", str(e))

  # ================= CONSULTAR VENTAS POR TIENDA Y FECHA =================
  def consultar_ventas_por_tienda_dialogo(self):
    db = conectar_db()
    if db is None:
      return

    tiendas_docs = list(db.tiendas.find())
    if not tiendas_docs:
      messagebox.showwarning(
          "Aviso", "No hay tiendas registradas en la colección 'tiendas'."
      )
      return

    mapa_tiendas = {}
    lista_opciones = []
    for t in tiendas_docs:
      etiqueta = f"{t.get('_id')} - {t.get('nombre')} ({t.get('ciudad', '')})"
      lista_opciones.append(etiqueta)
      mapa_tiendas[etiqueta] = t.get("_id")

    ven_tienda = tk.Toplevel(self.root)
    ven_tienda.title("Ventas por Tienda y Fecha")
    ven_tienda.geometry("460x520")
    ven_tienda.config(bg=self.c_card)
    ven_tienda.resizable(False, False)

    tk.Label(
        ven_tienda,
        text="🏬 Ventas por Tienda Oficial",
        font=("Segoe UI", 14, "bold"),
        bg=self.c_card,
        fg=self.c_text_light,
    ).pack(pady=(18, 5))

    tk.Label(
        ven_tienda,
        text="Selecciona la tienda y una fecha específica (o consulta general):",
        font=("Segoe UI", 9),
        bg=self.c_card,
        fg=self.c_text_muted,
    ).pack(pady=(0, 10))

    cb_tienda = ttk.Combobox(
        ven_tienda,
        values=lista_opciones,
        state="readonly",
        font=("Segoe UI", 10),
        width=45,
    )
    if lista_opciones:
      cb_tienda.current(0)
    cb_tienda.pack(pady=5)

    tk.Label(
        ven_tienda,
        text="Selecciona Fecha de Filtrado:",
        font=("Segoe UI", 9, "bold"),
        bg=self.c_card,
        fg=self.c_text_light,
    ).pack(anchor="w", padx=30, pady=(10, 2))

    cal = Calendar(
        ven_tienda,
        selectmode="day",
        year=2026,
        month=9,
        day=18,
        background="#374151",
        foreground="white",
        selectbackground="#3b82f6",
        normalbackground="#1f2937",
        headersbackground="#111827",
        headersforeground="white",
    )
    cal.pack(padx=25, pady=5)

    def ejecutar_calculo(filtrar_por_fecha=True):
      sel = cb_tienda.get()
      tienda_id = mapa_tiendas.get(sel)
      if not tienda_id:
        return

      fecha_sel = (
          cal.selection_get().strftime("%Y-%m-%d")
          if filtrar_por_fecha
          else None
      )
      ven_tienda.destroy()
      self.limpiar_tabla()
      self.configurar_columnas((
          "ID Venta",
          "Fecha / Canal",
          "Cliente",
          "Vendedor",
          "Total Transacción",
      ))

      total_recaudado = 0
      total_transacciones = 0
      total_unidades = 0
      filas = []

      for v in db.ventas.find():
        v_tienda = v.get("tienda_id") or v.get("tienda")
        if v_tienda == tienda_id or v.get("tienda_id") == tienda_id:
          f_mongo = v.get("fecha_hora")
          if isinstance(f_mongo, dict) and "$date" in f_mongo:
            f_str = f_mongo["$date"][:10]
          elif isinstance(f_mongo, datetime):
            f_str = f_mongo.strftime("%Y-%m-%d")
          else:
            f_str = "N/A"

          if filtrar_por_fecha and f_str != fecha_sel:
            continue

          total_transacciones += 1
          monto = v.get("total", 0)
          total_recaudado += monto
          total_unidades += v.get("cantidad", 0)

          filas.append((
              str(v.get("_id")),
              f"{f_str} ({v.get('canal', 'tienda')})",
              v.get("cliente", "N/A"),
              v.get("vendedor", "N/A"),
              f"${monto:,.0f}".replace(",", "."),
          ))

      sub_txt = (
          f"Fecha: {fecha_sel}"
          if filtrar_por_fecha
          else "Histórico Global de la Tienda"
      )
      self.lbl_titulo.config(text=f"Ventas Sucursal: {sel}")
      self.lbl_subtitulo.config(
          text=f"{sub_txt} • Recaudo Total: ${total_recaudado:,.0f}".replace(
              ",", "."
          )
      )

      resumen_txt = (
          f"Transacciones: {total_transacciones} | Unidades: {total_unidades} |"
          f" Recaudado: ${total_recaudado:,.0f}".replace(",", ".")
      )
      self.insertar_filas_estilizadas(filas, resumen_txt)

    btn_box = tk.Frame(ven_tienda, bg=self.c_card)
    btn_box.pack(fill=tk.X, padx=30, pady=10)

    tk.Button(
        btn_box,
        text="📅 Filtrar por Fecha Seleccionada",
        bg=self.c_primary,
        fg="white",
        font=("Segoe UI", 9, "bold"),
        bd=0,
        cursor="hand2",
        pady=8,
        command=lambda: ejecutar_calculo(True),
    ).pack(fill=tk.X, pady=3)

    tk.Button(
        btn_box,
        text="📊 Ver Histórico Total de la Tienda",
        bg=self.c_gold,
        fg="white",
        font=("Segoe UI", 9, "bold"),
        bd=0,
        cursor="hand2",
        pady=8,
        command=lambda: ejecutar_calculo(False),
    ).pack(fill=tk.X, pady=3)

  # ================= CONSULTAR VENTAS POR VENDEDOR Y FECHA =================
  def consultar_ventas_por_vendedor_dialogo(self):
    db = conectar_db()
    if db is None:
      return

    vendedores_docs = list(db.vendedores.find())
    if not vendedores_docs:
      messagebox.showwarning(
          "Aviso", "No hay vendedores registrados en la colección 'vendedores'."
      )
      return

    mapa_vendedores = {}
    lista_opciones = []
    for vend in vendedores_docs:
      etiqueta = (
          f"{vend.get('_id')} - {vend.get('nombre')} ({vend.get('ciudad', '')})"
      )
      lista_opciones.append(etiqueta)
      mapa_vendedores[etiqueta] = vend.get("nombre")

    ven_vendedor = tk.Toplevel(self.root)
    ven_vendedor.title("Ventas por Vendedor y Fecha")
    ven_vendedor.geometry("460x520")
    ven_vendedor.config(bg=self.c_card)
    ven_vendedor.resizable(False, False)

    tk.Label(
        ven_vendedor,
        text="👨‍💼 Ventas por Vendedor Comercial",
        font=("Segoe UI", 14, "bold"),
        bg=self.c_card,
        fg=self.c_text_light,
    ).pack(pady=(18, 5))

    tk.Label(
        ven_vendedor,
        text=(
            "Selecciona el vendedor y una fecha específica (o consulta"
            " general):"
        ),
        font=("Segoe UI", 9),
        bg=self.c_card,
        fg=self.c_text_muted,
    ).pack(pady=(0, 10))

    cb_vendedor = ttk.Combobox(
        ven_vendedor,
        values=lista_opciones,
        state="readonly",
        font=("Segoe UI", 10),
        width=45,
    )
    if lista_opciones:
      cb_vendedor.current(0)
    cb_vendedor.pack(pady=5)

    tk.Label(
        ven_vendedor,
        text="Selecciona Fecha de Filtrado:",
        font=("Segoe UI", 9, "bold"),
        bg=self.c_card,
        fg=self.c_text_light,
    ).pack(anchor="w", padx=30, pady=(10, 2))

    cal = Calendar(
        ven_vendedor,
        selectmode="day",
        year=2026,
        month=9,
        day=18,
        background="#374151",
        foreground="white",
        selectbackground="#3b82f6",
        normalbackground="#1f2937",
        headersbackground="#111827",
        headersforeground="white",
    )
    cal.pack(padx=25, pady=5)

    def ejecutar_calculo_vendedor(filtrar_por_fecha=True):
      sel = cb_vendedor.get()
      nombre_vendedor = mapa_vendedores.get(sel)
      if not nombre_vendedor:
        return

      fecha_sel = (
          cal.selection_get().strftime("%Y-%m-%d")
          if filtrar_por_fecha
          else None
      )
      ven_vendedor.destroy()
      self.limpiar_tabla()
      self.configurar_columnas((
          "ID Venta",
          "Fecha / Canal",
          "Cliente",
          "Tienda",
          "Total Transacción",
      ))

      total_recaudado = 0
      total_transacciones = 0
      total_unidades = 0
      filas = []

      for v in db.ventas.find():
        v_vend = v.get("vendedor")
        if v_vend == nombre_vendedor or v_vend == sel.split(" - ")[0]:
          f_mongo = v.get("fecha_hora")
          if isinstance(f_mongo, dict) and "$date" in f_mongo:
            f_str = f_mongo["$date"][:10]
          elif isinstance(f_mongo, datetime):
            f_str = f_mongo.strftime("%Y-%m-%d")
          else:
            f_str = "N/A"

          if filtrar_por_fecha and f_str != fecha_sel:
            continue

          total_transacciones += 1
          monto = v.get("total", 0)
          total_recaudado += monto
          total_unidades += v.get("cantidad", 0)

          filas.append((
              str(v.get("_id")),
              f"{f_str} ({v.get('canal', 'tienda')})",
              v.get("cliente", "N/A"),
              v.get("tienda_id", "N/A"),
              f"${monto:,.0f}".replace(",", "."),
          ))

      sub_txt = (
          f"Fecha: {fecha_sel}"
          if filtrar_por_fecha
          else "Histórico Global del Vendedor"
      )
      self.lbl_titulo.config(text=f"Ventas Vendedor: {sel.split(' - ')[1]}")
      self.lbl_subtitulo.config(
          text=f"{sub_txt} • Recaudo Total: ${total_recaudado:,.0f}".replace(
              ",", "."
          )
      )

      resumen_txt = (
          f"Transacciones: {total_transacciones} | Unidades: {total_unidades} |"
          f" Recaudado: ${total_recaudado:,.0f}".replace(",", ".")
      )
      self.insertar_filas_estilizadas(filas, resumen_txt)

    btn_box = tk.Frame(ven_vendedor, bg=self.c_card)
    btn_box.pack(fill=tk.X, padx=30, pady=10)

    tk.Button(
        btn_box,
        text="📅 Filtrar por Fecha Seleccionada",
        bg=self.c_accent,
        fg="white",
        font=("Segoe UI", 9, "bold"),
        bd=0,
        cursor="hand2",
        pady=8,
        command=lambda: ejecutar_calculo_vendedor(True),
    ).pack(fill=tk.X, pady=3)

    tk.Button(
        btn_box,
        text="📊 Ver Histórico Total del Vendedor",
        bg=self.c_gold,
        fg="white",
        font=("Segoe UI", 9, "bold"),
        bd=0,
        cursor="hand2",
        pady=8,
        command=lambda: ejecutar_calculo_vendedor(False),
    ).pack(fill=tk.X, pady=3)

  # ================= MÓDULO CALENDARIO EXCLUSIVO DE NUEVAS PRENDAS =================
  def abrir_panel_calendario(self):
    cal_ven = tk.Toplevel(self.root)
    cal_ven.title("📅 Calendario de Nuevas Prendas")
    cal_ven.geometry("440x500")
    cal_ven.config(bg=self.c_card)
    cal_ven.resizable(False, False)

    tk.Label(
        cal_ven,
        text="Selecciona una Fecha",
        font=("Segoe UI", 14, "bold"),
        bg=self.c_card,
        fg=self.c_text_light,
    ).pack(pady=(18, 5))

    cal = Calendar(
        cal_ven,
        selectmode="day",
        year=2026,
        month=9,
        day=18,
        background="#374151",
        foreground="white",
        selectbackground="#3b82f6",
        normalbackground="#1f2937",
        headersbackground="#111827",
        headersforeground="white",
    )
    cal.pack(padx=25, pady=10)

    def consultar_prendas_por_fecha():
      fecha_str = cal.selection_get().strftime("%Y-%m-%d")

      db = conectar_db()
      if db is None:
        return

      self.limpiar_tabla()
      self.lbl_titulo.config(
          text=f"Prendas Ingresadas en la Fecha: {fecha_str}"
      )
      self.lbl_subtitulo.config(
          text="Nuevos lanzamientos registrados en el sistema este día"
      )
      self.configurar_columnas(
          ("ID Prenda", "Referencia", "Nombre", "Categoría", "Precio")
      )

      filas = []
      for p in db.prendas.find():
        f_reg = p.get("fecha_registro") or p.get("fecha_creacion")
        if isinstance(f_reg, dict) and "$date" in f_reg:
          f_reg_str = f_reg["$date"][:10]
        elif isinstance(f_reg, datetime):
          f_reg_str = f_reg.strftime("%Y-%m-%d")
        else:
          continue

        if f_reg_str == fecha_str:
          filas.append((
              str(p.get("_id")),
              p.get("referencia", "N/A"),
              p.get("nombre", "Sin nombre"),
              p.get("categoria", "General"),
              f"${p.get('precio', 0):,.0f}".replace(",", "."),
          ))

      self.insertar_filas_estilizadas(
          filas, f"Lanzamientos encontrados: {len(filas)}"
      )
      cal_ven.destroy()

    tk.Button(
        cal_ven,
        text="👗 Consultar Prendas de esta Fecha",
        bg="#8b5cf6",
        fg="white",
        font=("Segoe UI", 10, "bold"),
        bd=0,
        cursor="hand2",
        pady=10,
        command=consultar_prendas_por_fecha,
    ).pack(fill=tk.X, padx=35, pady=15)

  # ================= REPORTES OFICIALES CON TOTALES =================
  def reporte_1(self):
    self.lbl_titulo.config(text="Reporte 1: Ventas e Ingresos por Colección")
    self.lbl_subtitulo.config(
        text="Consolidado financiero agrupado por colección de moda"
    )
    db = conectar_db()
    if db is None:
      return
    self.limpiar_tabla()
    self.configurar_columnas((
        "ID Colección",
        "Nombre Colección",
        "Unidades Vendidas",
        "Ingresos Totales",
    ))

    pipeline = [
        {
            "$group": {
                "_id": "$coleccion_id",
                "total_unidades": {"$sum": "$cantidad"},
                "total_ingresos": {"$sum": "$total"},
            }
        },
        {
            "$lookup": {
                "from": "colecciones",
                "localField": "_id",
                "foreignField": "_id",
                "as": "c_info",
            }
        },
        {"$unwind": {"path": "$c_info", "preserveNullAndEmptyArrays": True}},
        {
            "$project": {
                "nombre_coleccion": {
                    "$ifNull": ["$c_info.nombre", "Desconocida"]
                },
                "total_unidades": 1,
                "total_ingresos": 1,
            }
        },
    ]

    try:
      filas = []
      gran_total_ingresos = 0
      gran_total_unidades = 0
      for doc in db.ventas.aggregate(pipeline):
        ingresos = doc.get("total_ingresos", 0)
        unidades = doc.get("total_unidades", 0)
        gran_total_ingresos += ingresos
        gran_total_unidades += unidades
        filas.append((
            doc.get("_id", "N/A"),
            doc.get("nombre_coleccion"),
            unidades,
            f"${ingresos:,.0f}".replace(",", "."),
        ))

      resumen = (
          f"Total Unidades Vendidas: {gran_total_unidades} | Ingresos Globales:"
          f" ${gran_total_ingresos:,.0f}".replace(",", ".")
      )
      self.insertar_filas_estilizadas(filas, resumen)
    except Exception as e:
      messagebox.showerror("Error", str(e))

  def reporte_2(self):
    self.lbl_titulo.config(text="Reporte 2: Existencias Totales por Talla")
    self.lbl_subtitulo.config(
        text="Inventario físico desenrollando el arreglo de tallas ($unwind)"
    )
    db = conectar_db()
    if db is None:
      return
    self.limpiar_tabla()
    self.configurar_columnas(("Talla", "Existencias Totales"))

    pipeline = [
        {"$unwind": "$tallas"},
        {
            "$group": {
                "_id": "$tallas.talla",
                "total_existencias": {"$sum": "$tallas.existencias"},
            }
        },
        {"$sort": {"_id": 1}},
    ]

    try:
      filas = []
      stock_general = 0
      for doc in db.prendas.aggregate(pipeline):
        talla = doc.get("_id")
        existencias = doc.get("total_existencias", 0)
        stock_general += existencias
        filas.append((talla, existencias))

      self.insertar_filas_estilizadas(
          filas, f"Stock Total en Almacén: {stock_general} unidades"
      )
    except Exception as e:
      messagebox.showerror("Error", str(e))

  def reporte_3(self):
    self.lbl_titulo.config(text="Reporte 3: Prendas por Diseñador")
    self.lbl_subtitulo.config(
        text="Catálogo de creaciones agrupadas por autoría"
    )
    db = conectar_db()
    if db is None:
      return
    self.limpiar_tabla()
    self.configurar_columnas((
        "ID Diseñador",
        "Nombre Diseñador",
        "Total Prendas",
        "Prendas Asignadas",
    ))

    pipeline = [
        {
            "$group": {
                "_id": {
                    "id": "$disenador.id",
                    "nombre": "$disenador.nombre",
                },
                "lista": {"$push": "$nombre"},
                "cantidad": {"$sum": 1},
            }
        }
    ]

    try:
      filas = []
      total_prendas_catalogo = 0
      for doc in db.prendas.aggregate(pipeline):
        _id_info = doc.get("_id", {})
        cant = doc.get("cantidad", 0)
        total_prendas_catalogo += cant
        filas.append((
            _id_info.get("id", "N/A"),
            _id_info.get("nombre", "Sin Nombre"),
            cant,
            ", ".join(doc.get("lista", [])),
        ))
      self.insertar_filas_estilizadas(
          filas, f"Total Diseñadores / Creaciones: {total_prendas_catalogo}"
      )
    except Exception as e:
      messagebox.showerror("Error", str(e))

  # ================= LISTADOS Y CONSULTAS GENERALES =================
  def listar_vendedores(self):
    self.lbl_titulo.config(text="Directorio de Vendedores")
    self.lbl_subtitulo.config(
        text="Gestión de personal comercial y asignación de tiendas"
    )
    db = conectar_db()
    if db is None:
      return
    self.limpiar_tabla()
    self.configurar_columnas(
        ("ID", "Nombre", "Documento", "Ciudad", "Teléfono", "Correo")
    )

    try:
      filas = []
      for doc in db.vendedores.find():
        filas.append((
            str(doc.get("_id")),
            doc.get("nombre", ""),
            doc.get("documento", ""),
            doc.get("ciudad", ""),
            doc.get("telefono", ""),
            doc.get("correo", ""),
        ))
      self.insertar_filas_estilizadas(
          filas, f"Total Vendedores Activos: {len(filas)}"
      )
    except Exception as e:
      messagebox.showerror("Error", str(e))

  def listar_tiendas(self):
    self.lbl_titulo.config(text="Red de Tiendas Oficiales")
    self.lbl_subtitulo.config(
        text="Ubicaciones físicas y centros comerciales de FashionDB"
    )
    db = conectar_db()
    if db is None:
      return
    self.limpiar_tabla()
    self.configurar_columnas(
        ("ID", "Nombre Tienda", "Ciudad", "Departamento", "Dirección")
    )

    try:
      filas = []
      for doc in db.tiendas.find():
        filas.append((
            str(doc.get("_id")),
            doc.get("nombre", ""),
            doc.get("ciudad", ""),
            doc.get("departamento", ""),
            doc.get("direccion", ""),
        ))
      self.insertar_filas_estilizadas(
          filas, f"Total Tiendas Operativas: {len(filas)}"
      )
    except Exception as e:
      messagebox.showerror("Error", str(e))

  def listar_talleres(self):
    self.lbl_titulo.config(text="Talleres de Confección")
    self.lbl_subtitulo.config(
        text="Directorio de talleres asociados, capacidad y especialidad"
    )
    db = conectar_db()
    if db is None:
      return
    self.limpiar_tabla()
    self.configurar_columnas(
        ("ID", "Nombre Taller", "Especialidad", "Capacidad", "Teléfono")
    )

    try:
      filas = []
      capacidad_total = 0
      for doc in db.talleres.find():
        cap = doc.get("capacidad_produccion", 0)
        capacidad_total += cap
        filas.append((
            str(doc.get("_id")),
            doc.get("nombre", ""),
            doc.get("especialidad", ""),
            cap,
            doc.get("telefono", ""),
        ))
      self.insertar_filas_estilizadas(
          filas, f"Capacidad Conjunta de Producción: {capacidad_total} unidades"
      )
    except Exception as e:
      messagebox.showerror("Error", str(e))

  def listar_prendas(self):
    self.lbl_titulo.config(text="Inventario General de Prendas")
    self.lbl_subtitulo.config(
        text=(
            "Selecciona cualquier fila para editar o eliminar • Con totales en"
            " tiempo real"
        )
    )
    db = conectar_db()
    if db is None:
      return
    self.limpiar_tabla()
    self.configurar_columnas((
        "ID",
        "Referencia",
        "Nombre Prenda",
        "Diseñador",
        "Existencias",
        "Precio Unitario",
    ))

    try:
      filas = []
      total_stock_global = 0
      valor_total_inventario = 0

      for doc in db.prendas.find():
        disenador_nombre = doc.get("disenador", {}).get("nombre", "Sin asignar")
        tallas_lista = doc.get("tallas", [])
        total_stock_prenda = sum(
            t.get("existencias", 0)
            for t in tallas_lista
            if isinstance(t, dict)
        )
        precio_unit = doc.get("precio", 0)

        total_stock_global += total_stock_prenda
        valor_total_inventario += total_stock_prenda * precio_unit

        filas.append((
            str(doc.get("_id")),
            doc.get("referencia", "N/A"),
            doc.get("nombre", ""),
            disenador_nombre,
            total_stock_prenda,
            f"${precio_unit:,.0f}".replace(",", "."),
        ))

      resumen_total = (
          f"Stock Total: {total_stock_global} unidades | Valor del Inventario:"
          f" ${valor_total_inventario:,.0f}".replace(",", ".")
      )
      self.insertar_filas_estilizadas(filas, resumen_total)
    except Exception as e:
      messagebox.showerror("Error", str(e))

  def consulta_precio_alto(self):
    self.lbl_titulo.config(text="Prendas Gama Alta (Precio > $200.000)")
    self.lbl_subtitulo.config(
        text="Filtro de artículos premium con mayor margen unitario"
    )
    db = conectar_db()
    if db is None:
      return
    self.limpiar_tabla()
    self.configurar_columnas(("Nombre", "Categoría", "Temporada", "Precio"))

    try:
      filas = []
      for doc in db.prendas.find({"precio": {"$gt": 200000}}):
        filas.append((
            doc.get("nombre"),
            doc.get("categoria"),
            doc.get("temporada", "N/A"),
            f"${doc.get('precio', 0):,.0f}".replace(",", "."),
        ))
      self.insertar_filas_estilizadas(
          filas, f"Artículos Premium Encontrados: {len(filas)}"
      )
    except Exception as e:
      messagebox.showerror("Error", str(e))

  def consulta_disenadores_ciudad(self):
    self.lbl_titulo.config(text="Diseñadores por Ciudad")
    self.lbl_subtitulo.config(
        text="Distribución geográfica del equipo creativo"
    )
    db = conectar_db()
    if db is None:
      return
    self.limpiar_tabla()
    self.configurar_columnas(("Ciudad", "Total Diseñadores", "Nombres"))

    pipeline = [
        {
            "$group": {
                "_id": "$ciudad",
                "total": {"$sum": 1},
                "nombres": {"$push": "$nombre"},
            }
        }
    ]
    try:
      filas = [
          (
              doc.get("_id", "Desconocida"),
              doc.get("total", 0),
              ", ".join(doc.get("nombres", [])),
          )
          for doc in db.disenadores.aggregate(pipeline)
      ]
      self.insertar_filas_estilizadas(
          filas, f"Ciudades con Cobertura: {len(filas)}"
      )
    except Exception as e:
      messagebox.showerror("Error", str(e))

  # ================= GESTIÓN CRUD =================
  def _buscar_documento_por_id(self, db, id_str):
    doc = db.prendas.find_one({"_id": id_str})
    if not doc and ObjectId.is_valid(id_str):
      doc = db.prendas.find_one({"_id": ObjectId(id_str)})
    return doc

  def abrir_ventana_crear(self):
    db = conectar_db()
    if db is None:
      return

    self.mapa_disenadores = {}
    lista_disenadores = []
    for d in db.disenadores.find():
      etiqueta = f"{d.get('_id')} - {d.get('nombre')} ({d.get('ciudad', '')})"
      lista_disenadores.append(etiqueta)
      self.mapa_disenadores[etiqueta] = {
          "id": d.get("_id"),
          "nombre": d.get("nombre"),
          "ciudad": d.get("ciudad", "Medellín"),
      }

    self.mapa_colecciones = {}
    lista_colecciones = []
    for c in db.colecciones.find():
      etiqueta = f"{c.get('_id')} - {c.get('nombre')}"
      lista_colecciones.append(etiqueta)
      self.mapa_colecciones[etiqueta] = {
          "id": c.get("_id"),
          "nombre": c.get("nombre"),
      }

    self.ven_form = tk.Toplevel(self.root)
    self.ven_form.title("Nueva Prenda")
    self.ven_form.geometry("540x640")
    self.ven_form.config(bg=self.c_card)
    self.ven_form.resizable(False, False)

    tk.Label(
        self.ven_form,
        text="✨ Registrar Nueva Prenda",
        font=("Segoe UI", 15, "bold"),
        bg=self.c_card,
        fg=self.c_text_light,
    ).pack(pady=(18, 3))
    tk.Label(
        self.ven_form,
        text="Completa la ficha técnica, diseñador e inventario inicial",
        font=("Segoe UI", 9),
        bg=self.c_card,
        fg=self.c_text_muted,
    ).pack(pady=(0, 12))

    form = tk.Frame(self.ven_form, bg=self.c_card)
    form.pack(padx=30, fill=tk.BOTH)
    form.columnconfigure(0, weight=1)
    form.columnconfigure(1, weight=1)

    def crear_input(parent, label, row, col, colspan=1, default=""):
      frame_item = tk.Frame(parent, bg=self.c_card)
      frame_item.grid(
          row=row,
          column=col,
          columnspan=colspan,
          sticky="ew",
          padx=6,
          pady=6,
      )
      tk.Label(
          frame_item,
          text=label,
          font=("Segoe UI", 9, "bold"),
          bg=self.c_card,
          fg=self.c_text_light,
      ).pack(anchor="w")
      ent = tk.Entry(
          frame_item,
          font=("Segoe UI", 10),
          bg="#374151",
          fg="white",
          insertbackground="white",
          relief="solid",
          bd=1,
      )
      if default:
        ent.insert(0, default)
      ent.pack(fill=tk.X, pady=(3, 0), ipady=4)
      return ent

    def crear_combo(parent, label, valores, row, col, colspan=1, default_idx=0):
      frame_item = tk.Frame(parent, bg=self.c_card)
      frame_item.grid(
          row=row,
          column=col,
          columnspan=colspan,
          sticky="ew",
          padx=6,
          pady=6,
      )
      tk.Label(
          frame_item,
          text=label,
          font=("Segoe UI", 9, "bold"),
          bg=self.c_card,
          fg=self.c_text_light,
      ).pack(anchor="w")
      cb = ttk.Combobox(
          frame_item, values=valores, state="readonly", font=("Segoe UI", 10)
      )
      if valores:
        cb.current(default_idx)
      cb.pack(fill=tk.X, pady=(3, 0), ipady=3)
      return cb

    self.e_ref = crear_input(form, "Referencia * (ej. REF016):", 0, 0)
    self.e_precio = crear_input(form, "Precio Unitario ($) *:", 0, 1)
    self.e_nom = crear_input(form, "Nombre de la Prenda *:", 1, 0, colspan=2)
    self.e_cat = crear_input(
        form, "Categoría (ej. Vestido, Blusa):", 2, 0, default="Vestido"
    )
    self.cb_temp = crear_combo(
        form,
        "Temporada:",
        ["Primavera-Verano", "Otoño-Invierno", "Todo el año"],
        2,
        1,
    )
    self.cb_disenador = crear_combo(
        form, "Diseñador Asignado:", lista_disenadores, 3, 0, colspan=2
    )
    self.cb_coleccion = crear_combo(
        form, "Colección:", lista_colecciones, 4, 0, colspan=2
    )

    sub_stock = tk.Frame(form, bg=self.c_card)
    sub_stock.grid(row=5, column=0, columnspan=2, sticky="ew", pady=4)
    sub_stock.columnconfigure(0, weight=1)
    sub_stock.columnconfigure(1, weight=1)
    sub_stock.columnconfigure(2, weight=1)

    self.cb_talla = crear_combo(
        sub_stock,
        "Talla Inicial:",
        ["XS", "S", "M", "L", "XL", "32"],
        0,
        0,
        default_idx=2,
    )
    self.e_color = crear_input(sub_stock, "Color:", 0, 1, default="Negro")
    self.e_cantidad = crear_input(
        sub_stock, "Cantidad (Existencias) *:", 0, 2, default="10"
    )

    self.e_materiales = crear_input(
        form,
        "Materiales (separados por coma):",
        6,
        0,
        colspan=2,
        default="Algodón, Lino",
    )

    tk.Button(
        self.ven_form,
        text="✔ Guardar Prenda Completa",
        bg=self.c_accent,
        fg="white",
        font=("Segoe UI", 10, "bold"),
        bd=0,
        cursor="hand2",
        pady=11,
        command=self.guardar_nueva_prenda,
    ).pack(fill=tk.X, padx=36, pady=(15, 20))

  def guardar_nueva_prenda(self):
    ref = self.e_ref.get().strip()
    nombre = self.e_nom.get().strip()
    cat = self.e_cat.get().strip() or "General"
    temp = self.cb_temp.get().strip()
    precio_str = self.e_precio.get().strip()
    cantidad_str = self.e_cantidad.get().strip()
    talla_sel = self.cb_talla.get().strip()
    color_sel = self.e_color.get().strip() or "Único"
    materiales_raw = self.e_materiales.get().strip()

    if not ref or not nombre or not precio_str:
      messagebox.showwarning(
          "Regla de Validación",
          "Referencia, nombre y precio son obligatorios.",
      )
      return

    try:
      precio = float(precio_str)
      if precio <= 0:
        raise ValueError()
    except ValueError:
      messagebox.showerror(
          "Regla de Validación",
          "El precio debe ser un número mayor que cero.",
      )
      return

    try:
      cantidad = int(cantidad_str)
      if cantidad < 0:
        raise ValueError()
    except ValueError:
      messagebox.showerror(
          "Validación de Inventario",
          "La cantidad de existencias debe ser un número entero válido (0 o"
          " mayor).",
      )
      return

    dis_key = self.cb_disenador.get()
    disenador_obj = self.mapa_disenadores.get(
        dis_key, {"id": "DIS001", "nombre": "Laura Martínez", "ciudad": "Medellín"}
    )

    col_key = self.cb_coleccion.get()
    coleccion_obj = self.mapa_colecciones.get(
        col_key, {"id": "COL001", "nombre": "Elegancia Natural"}
    )

    lista_materiales = [
        m.strip() for m in materiales_raw.split(",") if m.strip()
    ]

    db = conectar_db()
    if db is None:
      return

    nuevo_documento = {
        "referencia": ref,
        "nombre": nombre,
        "categoria": cat,
        "temporada": temp,
        "precio": precio,
        "colecciones": [coleccion_obj],
        "disenador": disenador_obj,
        "tallas": [
            {
                "talla": talla_sel,
                "color": color_sel,
                "existencias": cantidad,
            }
        ],
        "materiales": lista_materiales,
        "fecha_registro": datetime.utcnow(),
    }

    try:
      db.prendas.insert_one(nuevo_documento)
      messagebox.showinfo(
          "Éxito",
          f"Prenda '{nombre}' registrada con {cantidad} unidades en talla"
          f" {talla_sel}.",
      )
      self.ven_form.destroy()
      self.listar_prendas()
    except Exception as e:
      messagebox.showerror("Error", f"No se pudo guardar: {e}")

  def abrir_ventana_actualizar(self):
    seleccion = self.tree.selection()
    if not seleccion:
      messagebox.showwarning(
          "Selección requerida",
          "Primero ve a 'Inventario General' y selecciona la prenda que deseas"
          " editar.",
      )
      return

    id_registro = str(self.tree.item(seleccion[0], "values")[0])
    db = conectar_db()
    if db is None:
      return

    self.prenda_actual = self._buscar_documento_por_id(db, id_registro)
    if not self.prenda_actual:
      messagebox.showwarning(
          "Aviso",
          "Este registro no corresponde a una prenda editable. Ve a"
          " 'Inventario General'.",
      )
      return

    self.ven_act = tk.Toplevel(self.root)
    self.ven_act.title("Editar Prenda")
    self.ven_act.geometry("440x460")
    self.ven_act.config(bg=self.c_card)
    self.ven_act.resizable(False, False)

    tk.Label(
        self.ven_act,
        text=f"Editando: {self.prenda_actual.get('_id')}",
        font=("Segoe UI", 14, "bold"),
        bg=self.c_card,
        fg=self.c_text_light,
    ).pack(pady=(20, 15))

    f2 = tk.Frame(self.ven_act, bg=self.c_card)
    f2.pack(padx=35, fill=tk.BOTH)

    for label_txt, attr, key in [
        ("Nombre:", "e_act_nom", "nombre"),
        ("Categoría:", "e_act_cat", "categoria"),
        ("Precio ($):", "e_act_precio", "precio"),
    ]:
      tk.Label(
          f2,
          text=label_txt,
          font=("Segoe UI", 9, "bold"),
          bg=self.c_card,
          fg=self.c_text_light,
      ).pack(anchor="w")
      ent = tk.Entry(
          f2,
          font=("Segoe UI", 10),
          bg="#374151",
          fg="white",
          insertbackground="white",
          relief="solid",
          bd=1,
      )
      ent.insert(0, str(self.prenda_actual.get(key, "")))
      ent.pack(fill=tk.X, pady=(3, 12), ipady=4)
      setattr(self, attr, ent)

    tallas = self.prenda_actual.get("tallas", [])
    stock_actual = (
        tallas[0].get("existencias", 0)
        if tallas and isinstance(tallas[0], dict)
        else 0
    )
    talla_nombre = (
        tallas[0].get("talla", "M")
        if tallas and isinstance(tallas[0], dict)
        else "M"
    )

    tk.Label(
        f2,
        text=f"Existencias (Talla {talla_nombre}):",
        font=("Segoe UI", 9, "bold"),
        bg=self.c_card,
        fg=self.c_text_light,
    ).pack(anchor="w")
    self.e_act_stock = tk.Entry(
        f2,
        font=("Segoe UI", 10),
        bg="#374151",
        fg="white",
        insertbackground="white",
        relief="solid",
        bd=1,
    )
    self.e_act_stock.insert(0, str(stock_actual))
    self.e_act_stock.pack(fill=tk.X, pady=(3, 12), ipady=4)

    tk.Button(
        self.ven_act,
        text="Guardar Cambios",
        bg=self.c_primary,
        fg="white",
        font=("Segoe UI", 10, "bold"),
        bd=0,
        cursor="hand2",
        pady=10,
        command=self.ejecutar_actualizacion,
    ).pack(fill=tk.X, padx=35, pady=10)

  def ejecutar_actualizacion(self):
    nombre = self.e_act_nom.get().strip()
    cat = self.e_act_cat.get().strip()
    precio_str = self.e_act_precio.get().strip()
    stock_str = self.e_act_stock.get().strip()

    if not nombre or not precio_str:
      messagebox.showwarning("Validación", "Nombre y precio son obligatorios.")
      return

    try:
      precio = float(precio_str)
      if precio <= 0:
        raise ValueError()
      nuevo_stock = int(stock_str)
      if nuevo_stock < 0:
        raise ValueError()
    except ValueError:
      messagebox.showerror(
          "Validación",
          "Verifica que el precio sea > 0 y las existencias sean un entero"
          " válido.",
      )
      return

    db = conectar_db()
    if db is None:
      return

    update_fields = {"nombre": nombre, "categoria": cat, "precio": precio}
    tallas = self.prenda_actual.get("tallas", [])
    if tallas and isinstance(tallas[0], dict):
      tallas[0]["existencias"] = nuevo_stock
      update_fields["tallas"] = tallas
    else:
      update_fields["tallas"] = [
          {"talla": "M", "color": "Único", "existencias": nuevo_stock}
      ]

    try:
      db.prendas.update_one(
          {"_id": self.prenda_actual["_id"]},
          {"$set": update_fields},
      )
      messagebox.showinfo("Éxito", "Prenda actualizada correctamente.")
      self.ven_act.destroy()
      self.listar_prendas()
    except Exception as e:
      messagebox.showerror("Error", f"No se pudo actualizar: {e}")

  def eliminar_prenda(self):
    seleccion = self.tree.selection()
    if not seleccion:
      messagebox.showwarning(
          "Selección requerida",
          "Primero ve a 'Inventario General' y selecciona la prenda que deseas"
          " eliminar.",
      )
      return

    id_registro = str(self.tree.item(seleccion[0], "values")[0])
    db = conectar_db()
    if db is None:
      return

    doc = self._buscar_documento_por_id(db, id_registro)
    if not doc:
      messagebox.showwarning(
          "Aviso",
          "Este registro no corresponde a una prenda eliminable. Ve a"
          " 'Inventario General'.",
      )
      return

    if not messagebox.askyesno(
        "Confirmar Eliminación",
        f"¿Estás seguro de eliminar '{doc.get('nombre')}' ({id_registro})?",
    ):
      return

    try:
      db.prendas.delete_one({"_id": doc["_id"]})
      messagebox.showinfo("Éxito", "Prenda eliminada correctamente.")
      self.listar_prendas()
    except Exception as e:
      messagebox.showerror("Error", f"No se pudo eliminar: {e}")


if __name__ == "__main__":
  root = tk.Tk()
  app = FashionApp(root)
  root.mainloop()
