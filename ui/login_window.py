import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class LoginWindow:
    def __init__(self, auth_service, on_success):
        self.auth_service = auth_service
        self.on_success = on_success
        self.root = tk.Tk()
        self.root.title("EcoTech solutions login")
        self.root.geometry("430x370")
        self.root.resizable(False, False)
        self._build()

    def _build(self):
        frame = ttk.Frame(self.root, padding=28)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="ECOTECH SOLUTIONS", font=("Arial", 18, "bold")).pack(pady=(5, 5))
        ttk.Label(frame, text="sistema de consultas operativas y financieras").pack(pady=(0, 22))

        ttk.Label(frame, text="correo electronico").pack(anchor="w")
        self.email_entry = ttk.Entry(frame)
        self.email_entry.pack(fill="x", pady=(4, 13))

        ttk.Label(frame, text="Contraseña").pack(anchor="w")
        self.password_entry = ttk.Entry(frame, show="*")
        self.password_entry.pack(fill="x", pady=(4, 18))

        ttk.Button(frame, text="iniciar sesion", command=self.login).pack(fill="x", pady=4)
        ttk.Button(frame, text="crear primer administrador", command=self.register_admin).pack(fill="x", pady=4)
        ttk.Label(frame, text="wl registro inicial se habilita solo cuando no hay usuarios").pack(pady=12)

    def login(self):
        try:
            usuario = self.auth_service.login(self.email_entry.get(), self.password_entry.get())
            self.root.destroy()
            self.on_success(usuario)
        except ValueError as error:
            messagebox.showerror("Acceso", str(error))

    def register_admin(self):
        nombre = simpledialog.askstring("registro", "nombre del administrador:", parent=self.root)
        if not nombre:
            return
        try:
            self.auth_service.register_admin(
                nombre, self.email_entry.get(), self.password_entry.get()
            )
            usuario = self.auth_service.login(
                self.email_entry.get(), self.password_entry.get()
            )
            self.root.destroy()
            self.on_success(usuario)
        except ValueError as error:
            messagebox.showerror("Registro", str(error))

    def run(self):
        self.root.mainloop()
