import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class Huesped:
    def __init__(self, nombre, apellidos, documento, fecha_ingreso):
        self.nombre = nombre
        self.apellidos = apellidos
        self.documento = documento
        self.fecha_ingreso = fecha_ingreso


class Habitacion:
    def __init__(self, numero, precio):
        self.numero = numero
        self.precio = precio
        self.disponible = True
        self.huesped = None

    def registrar_huesped(self, huesped):
        if not self.disponible:
            raise ValueError("La habitación no está disponible.")
        self.huesped = huesped
        self.disponible = False

    def calcular_pago(self, fecha_salida):
        if self.disponible or self.huesped is None:
            raise ValueError("La habitación no tiene un huésped alojado.")
        ingreso = datetime.strptime(
            self.huesped.fecha_ingreso, "%d/%m/%Y").date()
        salida = datetime.strptime(fecha_salida, "%d/%m/%Y").date()
        if salida <= ingreso:
            raise ValueError("La salida debe ser posterior al ingreso.")
        dias = (salida - ingreso).days
        return dias, dias * self.precio

    def registrar_salida(self):
        if self.disponible:
            raise ValueError("La habitación ya está disponible.")
        self.huesped = None
        self.disponible = True


class Hotel:
    def __init__(self):
        self.habitaciones = [
            Habitacion(n, 120000 if n <= 5 else 160000)
            for n in range(1, 11)
        ]

    def obtener_habitacion(self, numero):
        for habitacion in self.habitaciones:
            if habitacion.numero == numero:
                return habitacion
        raise ValueError("La habitación no existe.")

    def habitaciones_disponibles(self):
        return [h for h in self.habitaciones if h.disponible]

    def habitaciones_ocupadas(self):
        return [h for h in self.habitaciones if not h.disponible]


class HotelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión Hotelera")
        self.root.geometry("780x520")
        self.hotel = Hotel()
        self.crear_menu()
        self.crear_inicio()

    def crear_menu(self):
        barra = tk.Menu(self.root)
        menu_h = tk.Menu(barra, tearoff=0)
        menu_h.add_command(label="Consultar habitaciones",
                           command=self.ventana_habitaciones)
        barra.add_cascade(label="Habitaciones", menu=menu_h)
        menu_s = tk.Menu(barra, tearoff=0)
        menu_s.add_command(label="Salida de huéspedes",
                           command=self.ventana_salida)
        barra.add_cascade(label="Salidas", menu=menu_s)
        self.root.config(menu=barra)

    def crear_inicio(self):
        marco = ttk.Frame(self.root, padding=30)
        marco.pack(expand=True)
        ttk.Label(marco, text="SISTEMA DE GESTIÓN HOTELERA",
                  font=("Arial", 21, "bold")).pack(pady=25)
        self.lbl_resumen = ttk.Label(marco, font=("Arial", 12))
        self.lbl_resumen.pack(pady=12)
        ttk.Label(marco, text="Consulte las habitaciones o registre "
                  "la salida de un huésped desde el menú superior.",
                  wraplength=500, justify="center").pack(pady=10)
        self.actualizar_resumen()

    def actualizar_resumen(self):
        self.lbl_resumen.config(
            text=f"Disponibles: {len(self.hotel.habitaciones_disponibles())}  |  "
                 f"Ocupadas: {len(self.hotel.habitaciones_ocupadas())}")

    def ventana_habitaciones(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Consultar habitaciones")
        ventana.geometry("700x510")
        marco = ttk.Frame(ventana, padding=18)
        marco.pack(fill="both", expand=True)
        ttk.Label(marco, text="HABITACIONES DEL HOTEL",
                  font=("Arial", 16, "bold")).pack(pady=10)
        contenedor = ttk.Frame(marco)
        contenedor.pack(fill="both", expand=True)

        def actualizar():
            for widget in contenedor.winfo_children():
                widget.destroy()
            for h in self.hotel.habitaciones:
                fila, col = (h.numero - 1) // 2, (h.numero - 1) % 2
                estado = "Disponible" if h.disponible else "No disponible"
                texto = (f"Habitación {h.numero}\nPrecio diario: ${h.precio:,}"
                         f"\nEstado: {estado}")
                boton = ttk.Button(
                    contenedor, text=texto, width=34,
                    command=lambda n=h.numero: self.ventana_ingreso(
                        ventana, n, actualizar))
                boton.grid(row=fila, column=col, padx=10, pady=8, sticky="nsew")
                if not h.disponible:
                    boton.state(["disabled"])
            for c in range(2):
                contenedor.columnconfigure(c, weight=1)

        actualizar()

    def ventana_ingreso(self, padre, numero, actualizar):
        habitacion = self.hotel.obtener_habitacion(numero)
        ventana = tk.Toplevel(padre)
        ventana.title(f"Ingreso habitación {numero}")
        ventana.geometry("420x350")
        ventana.transient(padre)
        ventana.grab_set()
        marco = ttk.Frame(ventana, padding=20)
        marco.pack(fill="both", expand=True)
        ttk.Label(marco, text=f"REGISTRO DE HUÉSPED - HABITACIÓN {numero}",
                  font=("Arial", 13, "bold")).grid(
                      row=0, column=0, columnspan=2, pady=12)

        campos = {}
        for fila, campo in enumerate(
                ["Nombre", "Apellidos", "Documento", "Fecha de ingreso (DD/MM/AAAA)"],
                start=1):
            ttk.Label(marco, text=campo + ":").grid(
                row=fila, column=0, sticky="w", pady=8)
            variable = tk.StringVar()
            campos[campo] = variable
            ttk.Entry(marco, textvariable=variable, width=25).grid(
                row=fila, column=1, sticky="ew", pady=8)

        def registrar():
            valores = {k: v.get().strip() for k, v in campos.items()}
            if any(not v for v in valores.values()):
                messagebox.showerror("Datos incompletos",
                                     "Todos los campos son obligatorios.",
                                     parent=ventana)
                return
            if not valores["Documento"].isdigit():
                messagebox.showerror("Documento inválido",
                                     "El documento debe contener solo números.",
                                     parent=ventana)
                return
            try:
                datetime.strptime(
                    valores["Fecha de ingreso (DD/MM/AAAA)"], "%d/%m/%Y")
                huesped = Huesped(
                    valores["Nombre"], valores["Apellidos"],
                    valores["Documento"],
                    valores["Fecha de ingreso (DD/MM/AAAA)"])
                habitacion.registrar_huesped(huesped)
            except ValueError as error:
                messagebox.showerror("No se pudo registrar", str(error),
                                     parent=ventana)
                return
            messagebox.showinfo("Registro", "Huésped registrado correctamente.",
                                parent=ventana)
            ventana.destroy()
            actualizar()
            self.actualizar_resumen()

        ttk.Button(marco, text="Registrar ingreso",
                   command=registrar).grid(
                       row=5, column=0, columnspan=2, pady=15)
        marco.columnconfigure(1, weight=1)

    def ventana_salida(self):
        ocupadas = self.hotel.habitaciones_ocupadas()
        if not ocupadas:
            messagebox.showwarning("Sin huéspedes",
                                   "No hay habitaciones ocupadas.")
            return

        seleccion = tk.Toplevel(self.root)
        seleccion.title("Seleccionar habitación")
        seleccion.geometry("370x190")
        marco = ttk.Frame(seleccion, padding=20)
        marco.pack(fill="both", expand=True)
        ttk.Label(marco, text="Seleccione la habitación ocupada:").pack(anchor="w")
        numero = tk.StringVar()
        combo = ttk.Combobox(
            marco, textvariable=numero, state="readonly",
            values=[str(h.numero) for h in ocupadas])
        combo.pack(fill="x", pady=10)

        def continuar():
            if not numero.get():
                messagebox.showwarning("Selección", "Seleccione una habitación.",
                                       parent=seleccion)
                return
            n = int(numero.get())
            seleccion.destroy()
            self.ventana_detalle_salida(n)

        ttk.Button(marco, text="Continuar", command=continuar).pack(pady=8)

    def ventana_detalle_salida(self, numero):
        habitacion = self.hotel.obtener_habitacion(numero)
        huesped = habitacion.huesped
        ventana = tk.Toplevel(self.root)
        ventana.title(f"Salida habitación {numero}")
        ventana.geometry("520x390")
        marco = ttk.Frame(ventana, padding=20)
        marco.pack(fill="both", expand=True)

        ttk.Label(marco, text=f"SALIDA - HABITACIÓN {numero}",
                  font=("Arial", 15, "bold")).pack(pady=10)
        ttk.Label(
            marco,
            text=(f"Huésped: {huesped.nombre} {huesped.apellidos}\n"
                  f"Documento: {huesped.documento}\n"
                  f"Fecha de ingreso: {huesped.fecha_ingreso}\n"
                  f"Precio diario: ${habitacion.precio:,}"),
            justify="left").pack(anchor="w", pady=10)

        ttk.Label(marco, text="Fecha de salida (DD/MM/AAAA):").pack(anchor="w")
        fecha = tk.StringVar()
        ttk.Entry(marco, textvariable=fecha, width=30).pack(anchor="w", pady=8)
        lbl_dias = ttk.Label(marco, text="Días de alojamiento: -")
        lbl_dias.pack(anchor="w", pady=5)
        lbl_total = ttk.Label(marco, text="Total a pagar: -",
                              font=("Arial", 13, "bold"))
        lbl_total.pack(anchor="w", pady=5)
        calculo = {"total": None}

        def calcular():
            try:
                dias, total = habitacion.calcular_pago(fecha.get())
                calculo["total"] = total
                lbl_dias.config(text=f"Días de alojamiento: {dias}")
                lbl_total.config(text=f"Total a pagar: ${total:,}")
            except ValueError as error:
                messagebox.showerror("Error de fecha", str(error),
                                     parent=ventana)

        def registrar_salida():
            if calculo["total"] is None:
                messagebox.showwarning("Falta calcular",
                                       "Primero calcule el alojamiento.",
                                       parent=ventana)
                return
            if not messagebox.askyesno(
                    "Confirmar",
                    f"¿Registrar la salida?\nTotal: ${calculo['total']:,}",
                    parent=ventana):
                return
            habitacion.registrar_salida()
            messagebox.showinfo("Salida", "Salida registrada. "
                                "La habitación está disponible nuevamente.",
                                parent=ventana)
            ventana.destroy()
            self.actualizar_resumen()

        botones = ttk.Frame(marco)
        botones.pack(pady=18)
        ttk.Button(botones, text="Calcular alojamiento",
                   command=calcular).pack(side="left", padx=5)
        ttk.Button(botones, text="Registrar salida",
                   command=registrar_salida).pack(side="left", padx=5)


if __name__ == "__main__":
    root = tk.Tk()
    app = HotelApp(root)
    root.mainloop()