import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

class CTkTreeview(ttk.Treeview):
    """
    Treeview widget personalizado que combina ttk.Treeview con el estilo de customtkinter.
    """
    def __init__(self, master, **kwargs):
        # Configurar el estilo
        self.style = ttk.Style()
        self.style.configure("Treeview", 
                             background=master._fg_color if hasattr(master, "_fg_color") else "#f0f0f0",
                             foreground="#333333",
                             rowheight=25,
                             fieldbackground=master._fg_color if hasattr(master, "_fg_color") else "#f0f0f0")
        
        self.style.configure("Treeview.Heading", 
                             background="#4a4d50",
                             foreground="#ffffff",
                             relief="flat")
        
        self.style.map("Treeview", 
                       background=[("selected", "#1f6aa5")],
                       foreground=[("selected", "#ffffff")])
        
        # Inicializar el Treeview
        super().__init__(master, **kwargs)
