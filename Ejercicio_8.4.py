import tkinter as tk
from tkinter import ttk, messagebox, filedialog


class Empleado:
    def __init__(self, nombre, apellidos, cargo, genero, sueldo_dia,
                 dias, otros_ingresos, salud, pension):
        self.nombre = nombre
        self.apellidos = apellidos
        self.cargo = cargo
        self.genero = genero
        self.sueldo_dia = sueldo_dia
        self.dias = dias
        self.otros_ingresos = otros_ingresos
        self.salud = salud
        self.pension = pension

    def calcular_salario_mensual(self):
        return (self.sueldo_dia * self.dias + self.otros_ingresos
                - self.salud - self.pension)


class Nomina:
    def __init__(self):
        self.empleados = []

    def agregar_empleado(self, empleado):
        self.empleados.append(empleado)

    def calcular_total(self):
        return sum(e.calcular_salario_mensual() for e in self.empleados)


class NominaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Nómina")
        self.root.geometry("700x460")
        self.nomina = Nomina()
        self.crear_menu()
        self.crear_inicio()

    def crear_menu(self):
        barra = tk.Menu(self.root)

        menu_empleados = tk.Menu(barra, tearoff=0)
        menu_empleados.add_command(label="Agregar empleado",
                                   command=self.ventana_agregar)
        barra.add_cascade(label="Empleados", menu=menu_empleados)

        menu_nomina = tk.Menu(barra, tearoff=0)
        menu_nomina.add_command(label="Calcular nómina",
                                command=self.ventana_nomina)
        barra.add_cascade(label="Nómina", menu=menu_nomina)

        menu_archivo = tk.Menu(barra, tearoff=0)
        menu_archivo.add_command(label="Guardar archivo",
                                 command=self.guardar_archivo)
        barra.add_cascade(label="Archivo", menu=menu_archivo)
        self.root.config(menu=barra)

    def crear_inicio(self):
        marco = ttk.Frame(self.root, padding=30)
        marco.pack(expand=True)
        ttk.Label(marco, text="SISTEMA DE NÓMINA",
                  font=("Arial", 22, "bold")).pack(pady=25)
        self.lbl_cantidad = ttk.Label(marco, font=("Arial", 12))
        self.lbl_cantidad.pack(pady=10)
        ttk.Label(marco, text="Utilice el menú superior para administrar "
                  "los empleados y calcular la nómina.",
                  wraplength=480, justify="center").pack(pady=10)
        self.actualizar_cantidad()

    def actualizar_cantidad(self):
        self.lbl_cantidad.config(
            text=f"Empleados registrados: {len(self.nomina.empleados)}")

    @staticmethod
    def numero(valor, campo):
        try:
            resultado = float(valor)
            if resultado < 0:
                raise ValueError
            return resultado
        except ValueError:
            raise ValueError(f"{campo} debe ser un número mayor o igual a cero.")

    def ventana_agregar(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Agregar empleado")
        ventana.geometry("440x550")
        ventana.transient(self.root)
        ventana.grab_set()

        marco = ttk.Frame(ventana, padding=18)
        marco.pack(fill="both", expand=True)
        ttk.Label(marco, text="DATOS DEL EMPLEADO",
                  font=("Arial", 15, "bold")).grid(
                      row=0, column=0, columnspan=2, pady=10)

        variables = {
            "Nombre": tk.StringVar(),
            "Apellidos": tk.StringVar(),
            "Sueldo por día": tk.StringVar(),
            "Otros ingresos": tk.StringVar(value="0"),
            "Pagos por salud": tk.StringVar(value="0"),
            "Aporte a pensiones": tk.StringVar(value="0")
        }

        for fila, (campo, variable) in enumerate(variables.items(), start=1):
            ttk.Label(marco, text=campo + ":").grid(
                row=fila, column=0, sticky="w", pady=6)
            ttk.Entry(marco, textvariable=variable, width=27).grid(
                row=fila, column=1, sticky="ew", pady=6)

        ttk.Label(marco, text="Cargo:").grid(row=7, column=0, sticky="w", pady=6)
        cargo = tk.StringVar(value="Directivo")
        ttk.Combobox(marco, textvariable=cargo,
                     values=["Directivo", "Estratégico", "Operativo"],
                     state="readonly", width=25).grid(
                         row=7, column=1, sticky="ew", pady=6)

        ttk.Label(marco, text="Género:").grid(row=8, column=0, sticky="w", pady=6)
        genero = tk.StringVar(value="Masculino")
        opciones = ttk.Frame(marco)
        opciones.grid(row=8, column=1, sticky="w")
        ttk.Radiobutton(opciones, text="Masculino", variable=genero,
                        value="Masculino").pack(side="left")
        ttk.Radiobutton(opciones, text="Femenino", variable=genero,
                        value="Femenino").pack(side="left")

        ttk.Label(marco, text="Días trabajados (1-31):").grid(
            row=9, column=0, sticky="w", pady=6)
        dias = tk.StringVar(value="1")
        tk.Spinbox(marco, from_=1, to=31, textvariable=dias,
                   width=25).grid(row=9, column=1, sticky="ew", pady=6)

        def registrar():
            try:
                nombre = variables["Nombre"].get().strip()
                apellidos = variables["Apellidos"].get().strip()
                if not nombre or not apellidos:
                    raise ValueError("Nombre y apellidos son obligatorios.")
                dias_num = int(dias.get())
                if not 1 <= dias_num <= 31:
                    raise ValueError("Los días deben estar entre 1 y 31.")

                empleado = Empleado(
                    nombre, apellidos, cargo.get(), genero.get(),
                    self.numero(variables["Sueldo por día"].get(), "Sueldo por día"),
                    dias_num,
                    self.numero(variables["Otros ingresos"].get(), "Otros ingresos"),
                    self.numero(variables["Pagos por salud"].get(), "Pagos por salud"),
                    self.numero(variables["Aporte a pensiones"].get(), "Aporte a pensiones")
                )
                self.nomina.agregar_empleado(empleado)
                self.actualizar_cantidad()
                messagebox.showinfo("Registro", "Empleado agregado correctamente.",
                                    parent=ventana)
                ventana.destroy()
            except ValueError as error:
                messagebox.showerror("Datos inválidos", str(error), parent=ventana)

        botones = ttk.Frame(marco)
        botones.grid(row=10, column=0, columnspan=2, pady=15)
        ttk.Button(botones, text="Guardar empleado",
                   command=registrar).pack(side="left", padx=5)
        ttk.Button(botones, text="Cancelar",
                   command=ventana.destroy).pack(side="left", padx=5)
        marco.columnconfigure(1, weight=1)

    def ventana_nomina(self):
        if not self.nomina.empleados:
            messagebox.showwarning("Sin empleados", "Primero agregue empleados.")
            return

        ventana = tk.Toplevel(self.root)
        ventana.title("Nómina")
        ventana.geometry("850x420")
        marco = ttk.Frame(ventana, padding=15)
        marco.pack(fill="both", expand=True)

        columnas = ("nombre", "apellidos", "cargo", "salario")
        tabla = ttk.Treeview(marco, columns=columnas, show="headings")
        for col, titulo in zip(columnas,
                               ["Nombre", "Apellidos", "Cargo", "Salario mensual"]):
            tabla.heading(col, text=titulo)
        tabla.column("nombre", width=140)
        tabla.column("apellidos", width=170)
        tabla.column("cargo", width=130)
        tabla.column("salario", width=150, anchor="e")

        for empleado in self.nomina.empleados:
            tabla.insert("", "end", values=(
                empleado.nombre, empleado.apellidos, empleado.cargo,
                f"${empleado.calcular_salario_mensual():,.2f}"
            ))
        tabla.pack(fill="both", expand=True)
        ttk.Label(marco, text=f"TOTAL NÓMINA: ${self.nomina.calcular_total():,.2f}",
                  font=("Arial", 13, "bold")).pack(anchor="e", pady=12)

    def guardar_archivo(self):
        if not self.nomina.empleados:
            messagebox.showwarning("Sin empleados", "No hay empleados para guardar.")
            return
        carpeta = filedialog.askdirectory(title="Seleccione la carpeta")
        if not carpeta:
            return
        ruta = carpeta + "/Nómina.txt"
        try:
            with open(ruta, "w", encoding="utf-8") as archivo:
                archivo.write("NÓMINA DE EMPLEADOS\n" + "=" * 45 + "\n\n")
                for i, e in enumerate(self.nomina.empleados, start=1):
                    archivo.write(
                        f"EMPLEADO {i}\nNombre: {e.nombre}\n"
                        f"Apellidos: {e.apellidos}\nCargo: {e.cargo}\n"
                        f"Género: {e.genero}\nSueldo por día: ${e.sueldo_dia:,.2f}\n"
                        f"Días trabajados: {e.dias}\nOtros ingresos: ${e.otros_ingresos:,.2f}\n"
                        f"Salud: ${e.salud:,.2f}\nPensión: ${e.pension:,.2f}\n"
                        f"Salario mensual: ${e.calcular_salario_mensual():,.2f}\n\n"
                    )
                archivo.write(f"TOTAL NÓMINA: ${self.nomina.calcular_total():,.2f}\n")
            messagebox.showinfo("Guardado", f"Archivo guardado en:\n{ruta}")
        except OSError as error:
            messagebox.showerror("Error", str(error))


if __name__ == "__main__":
    root = tk.Tk()
    app = NominaApp(root)
    root.mainloop()
