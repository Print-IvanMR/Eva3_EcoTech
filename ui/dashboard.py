import tkinter as tk
from tkinter import ttk, messagebox

class Dashboard:
    def __init__(self, usuario, auth_service, weather_service, currency_service, history_repository, on_logout):
        self.usuario = usuario
        self.auth_service = auth_service
        self.weather_service = weather_service
        self.currency_service = currency_service
        self.history_repository = history_repository
        self.on_logout = on_logout

        self.root = tk.Tk()
        self.root.title("ecoTech solutions menu")
        self.root.geometry("780x570")
        self.root.minsize(650, 480)
        self._build()
        self.load_history()

    def _build(self):
        main = ttk.Frame(self.root, padding=16)
        main.pack(fill="both", expand=True)

        header = ttk.Frame(main)
        header.pack(fill="x", pady=(0, 14))
        ttk.Label(header, text="panel principal", font=("Arial", 18, "bold")).pack(side="left")
        ttk.Label(header, text=f"usuario: {self.usuario.get('nombre', '')}").pack(side="left", padx=18)
        ttk.Button(header, text="cerrar sesion", command=self.logout).pack(side="right")

        tabs = ttk.Notebook(main)
        tabs.pack(fill="both", expand=True)
        weather_tab = ttk.Frame(tabs, padding=18)
        currency_tab = ttk.Frame(tabs, padding=18)
        history_tab = ttk.Frame(tabs, padding=12)
        tabs.add(weather_tab, text="Clima")
        tabs.add(currency_tab, text="Monedas")
        tabs.add(history_tab, text="Historial")

        self._build_weather(weather_tab)
        self._build_currency(currency_tab)
        self._build_history(history_tab)

    def _build_weather(self, parent):
        ttk.Label(parent, text="consultar condiciones climáticas", font=("Arial", 14, "bold")).pack(anchor="w", pady=(0, 12))
        line = ttk.Frame(parent)
        line.pack(fill="x")
        self.city_entry = ttk.Entry(line)
        self.city_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        ttk.Button(line, text="Consultar clima", command=self.search_weather).pack(side="right")
        self.weather_result = tk.Text(parent, height=9, wrap="word", state="disabled")
        self.weather_result.pack(fill="both", expand=True, pady=16)

    def search_weather(self):
        try:
            data = self.weather_service.get_weather(self.city_entry.get())
            self.history_repository.save_weather(self.usuario["correo"], data)
            text = (
                f"Ciudad: {data['ciudad']}, {data['pais']}\n"
                f"Temperatura: {data['temperatura']} °C\n"
                f"Humedad: {data['humedad']} %\n"
                f"Estado: {data['estado']}\n"
                f"Fecha de consulta: {data['fecha']}"
            )
            self._show_text(self.weather_result, text)
            self.load_history()
        except (ValueError, ConnectionError) as error:
            messagebox.showwarning("consulta de clima", str(error))
        except Exception:
            messagebox.showerror("Error", "no se pudo completar la consulta")

    def _build_currency(self, parent):
        ttk.Label(parent, text="conversión de monedas", font=("Arial", 14, "bold")).pack(anchor="w", pady=(0, 15))
        form = ttk.Frame(parent)
        form.pack(fill="x")

        ttk.Label(form, text="monto").grid(row=0, column=0, sticky="w", padx=5, pady=7)
        self.amount_entry = ttk.Entry(form)
        self.amount_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=7)

        ttk.Label(form, text="moneda de origen").grid(row=1, column=0, sticky="w", padx=5, pady=7)
        self.origin_box = ttk.Combobox(form, values=self.currency_service.CURRENCIES, state="readonly")
        self.origin_box.set("CLP")
        self.origin_box.grid(row=1, column=1, sticky="ew", padx=5, pady=7)

        ttk.Label(form, text="moneda de destino").grid(row=2, column=0, sticky="w", padx=5, pady=7)
        self.destination_box = ttk.Combobox(form, values=self.currency_service.CURRENCIES, state="readonly")
        self.destination_box.set("USD")
        self.destination_box.grid(row=2, column=1, sticky="ew", padx=5, pady=7)

        form.columnconfigure(1, weight=1)
        ttk.Button(parent, text="convertir", command=self.convert_currency).pack(anchor="w", pady=12)
        self.currency_result = tk.Text(parent, height=8, wrap="word", state="disabled")
        self.currency_result.pack(fill="both", expand=True)

    def convert_currency(self):
        try:
            data = self.currency_service.convert(
                self.amount_entry.get(),
                self.origin_box.get(),
                self.destination_box.get()
            )
            self.history_repository.save_currency(self.usuario["correo"], data)
            text = (
                f"monto original: {data['monto']} {data['origen']}\n"
                f"tasa consultada: {data['tasa']}\n"
                f"resultado: {data['total']} {data['destino']}\n"
                f"fecha de referencia: {data['fecha']}\n\n"
                "la tasa puede no coincidir con el valor aplicado por algun banco"
            )
            self._show_text(self.currency_result, text)
            self.load_history()
        except (ValueError, ConnectionError) as error:
            messagebox.showwarning("Conversión", str(error))
        except Exception:
            messagebox.showerror("Error", "no se pudo completar la conversion")

    def _build_history(self, parent):
        columns = ("fecha", "tipo", "detalle")
        self.history_table = ttk.Treeview(parent, columns=columns, show="headings")
        self.history_table.heading("fecha", text="Fecha")
        self.history_table.heading("tipo", text="Tipo")
        self.history_table.heading("detalle", text="Detalle")
        self.history_table.column("fecha", width=175)
        self.history_table.column("tipo", width=90)
        self.history_table.column("detalle", width=400)
        self.history_table.pack(fill="both", expand=True)
        ttk.Button(parent, text="actualizar historial", command=self.load_history).pack(anchor="e", pady=8)

    def load_history(self):
        if not hasattr(self, "history_table"):
            return
        for item in self.history_table.get_children():
            self.history_table.delete(item)
        try:
            records = self.history_repository.get_history(self.usuario["correo"])
            for record in records:
                fecha = record.get("fecha")
                fecha_text = fecha.strftime("%d-%m-%Y %H:%M") if fecha else ""
                result = record.get("resultado", {})
                if record.get("tipo") == "clima":
                    detail = f"{result.get('ciudad', '')}: {result.get('temperatura', '')} °C"
                else:
                    detail = f"{result.get('monto', '')} {result.get('origen', '')} → {result.get('total', '')} {result.get('destino', '')}"
                self.history_table.insert("", "end", values=(fecha_text, record.get("tipo", ""), detail))
        except Exception:
            messagebox.showwarning("historial", "no se pudo cargar el historial")

    @staticmethod
    def _show_text(widget, value):
        widget.configure(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", value)
        widget.configure(state="disabled")

    def logout(self):
        self.auth_service.logout()
        self.root.destroy()
        self.on_logout()

    def run(self):
        self.root.mainloop()
