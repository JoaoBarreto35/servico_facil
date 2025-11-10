import tkinter as tk
from tkinter import messagebox
from utils.db_utils import insert_client, get_all_clients, update_client, delete_client

# Function to build the client tab inside the main notebook
def build_client_tab(parent):
    parent.configure(bg="#f9f9f9")

    # --- Title ---
    tk.Label(parent, text="📇 Cadastro de Clientes", font=("Helvetica", 18, "bold"), bg="#f9f9f9", fg="#333").pack(pady=10)

    # --- Form Frame ---
    form_frame = tk.Frame(parent, bg="#f9f9f9")
    form_frame.pack(pady=10)

    # --- Form fields ---
    tk.Label(form_frame, text="Nome:", font=("Helvetica", 12), bg="#f9f9f9").grid(row=0, column=0, sticky="e", padx=5, pady=5)
    entry_nome = tk.Entry(form_frame, width=40)
    entry_nome.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Telefone:", font=("Helvetica", 12), bg="#f9f9f9").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    entry_telefone = tk.Entry(form_frame, width=40)
    entry_telefone.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Endereço:", font=("Helvetica", 12), bg="#f9f9f9").grid(row=2, column=0, sticky="e", padx=5, pady=5)
    entry_endereco = tk.Entry(form_frame, width=40)
    entry_endereco.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Email:", font=("Helvetica", 12), bg="#f9f9f9").grid(row=3, column=0, sticky="e", padx=5, pady=5)
    entry_email = tk.Entry(form_frame, width=40)
    entry_email.grid(row=3, column=1, padx=5, pady=5)

    selected_id = tk.StringVar()  # Store selected client ID

    # --- Button Frame ---
    button_frame = tk.Frame(parent, bg="#f9f9f9")
    button_frame.pack(pady=10)

    # Function to clear form fields
    def clear_fields():
        entry_nome.delete(0, tk.END)
        entry_telefone.delete(0, tk.END)
        entry_endereco.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        selected_id.set("")
        client_listbox.selection_clear(0, tk.END)

    # Function to register a new client
    def register_client():
        nome = entry_nome.get()
        telefone = entry_telefone.get()
        endereco = entry_endereco.get()
        email = entry_email.get()

        if nome == "":
            messagebox.showwarning("⚠️ Atenção", "O nome é obrigatório.")
            return

        insert_client(nome, telefone, endereco, email)
        messagebox.showinfo("✅ Sucesso", "Cliente cadastrado com sucesso!")
        clear_fields()
        list_clients()

    # Function to update selected client
    def edit_client():
        if not selected_id.get():
            messagebox.showwarning("⚠️ Atenção", "Selecione um cliente para editar.")
            return

        update_client(
            int(selected_id.get()),
            entry_nome.get(),
            entry_telefone.get(),
            entry_endereco.get(),
            entry_email.get()
        )
        messagebox.showinfo("✏️ Atualizado", "Cliente atualizado com sucesso!")
        clear_fields()
        list_clients()

    # Function to delete selected client
    def remove_client():
        if not selected_id.get():
            messagebox.showwarning("⚠️ Atenção", "Selecione um cliente para excluir.")
            return

        confirm = messagebox.askyesno("🗑️ Confirmação", "Tem certeza que deseja excluir este cliente?")
        if confirm:
            delete_client(int(selected_id.get()))
            messagebox.showinfo("🗑️ Excluído", "Cliente excluído com sucesso!")
            clear_fields()
            list_clients()

    # Buttons with emojis and styling
    tk.Button(button_frame, text="➕ Cadastrar", width=15, command=register_client, bg="#4CAF50", fg="white").grid(row=0, column=0, padx=5)
    tk.Button(button_frame, text="✏️ Editar", width=15, command=edit_client, bg="#2196F3", fg="white").grid(row=0, column=1, padx=5)
    tk.Button(button_frame, text="🗑️ Excluir", width=15, command=remove_client, bg="#f44336", fg="white").grid(row=0, column=2, padx=5)
    tk.Button(button_frame, text="🧹 Limpar", width=15, command=clear_fields, bg="#9E9E9E", fg="white").grid(row=0, column=3, padx=5)

    # --- Listbox section ---
    tk.Label(parent, text="📋 Clientes cadastrados:", font=("Helvetica", 14), bg="#f9f9f9").pack(pady=10)
    client_listbox = tk.Listbox(parent, width=80, height=10)
    client_listbox.pack(pady=5)

    # Function to list all clients
    def list_clients():
        clients = get_all_clients()
        client_listbox.delete(0, tk.END)

        for client in clients:
            texto = f"{client[0]} - {client[1]} | {client[2]}"
            client_listbox.insert(tk.END, texto)

    # Function to load selected client into form
    def on_select(event):
        if not client_listbox.curselection():
            return

        index = client_listbox.curselection()[0]
        client = get_all_clients()[index]

        selected_id.set(client[0])
        entry_nome.delete(0, tk.END)
        entry_nome.insert(0, client[1])

        entry_telefone.delete(0, tk.END)
        entry_telefone.insert(0, client[2])

        entry_endereco.delete(0, tk.END)
        entry_endereco.insert(0, client[3])

        entry_email.delete(0, tk.END)
        entry_email.insert(0, client[4])

    client_listbox.bind("<<ListboxSelect>>", on_select)
    list_clients()