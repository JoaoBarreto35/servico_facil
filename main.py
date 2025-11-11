import tkinter as tk
from tkinter import ttk
from views.client_view import build_client_tab
from views.item_view import build_item_tab
from views.order_view import build_order_tab
from views.order_list_view import build_orders_list_tab
from views.account_view import build_account_tab

# Create the main application window
root = tk.Tk()
root.title("🔧 Sistema de Ordens de Serviço")
root.geometry("1000x700")
root.configure(bg="#f0f0f0")

# Create a Notebook (tabbed interface)
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# Create frames for each tab
tab_clientes = tk.Frame(notebook, bg="#f9f9f9")
tab_itens = tk.Frame(notebook, bg="#f9f9f9")
tab_ordens = tk.Frame(notebook, bg="#f9f9f9")
tab_lista_ordens = tk.Frame(notebook, bg="#f9f9f9")
tab_contas = tk.Frame(notebook, bg="#f9f9f9")

# Add tabs to the notebook
notebook.add(tab_clientes, text="👤 Clientes")
notebook.add(tab_itens, text="🧾 Itens de Serviço")
notebook.add(tab_ordens, text="📦 Cadastro de Ordens")
notebook.add(tab_lista_ordens, text="📋 Lista de Ordens")
notebook.add(tab_contas, text="💰 Contas a Pagar")

# Build each tab interface
build_client_tab(tab_clientes)
build_item_tab(tab_itens)
build_order_tab(tab_ordens)
build_orders_list_tab(tab_lista_ordens)
build_account_tab(tab_contas)

# Start the main loop
root.mainloop()