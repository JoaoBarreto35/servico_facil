import tkinter as tk
from tkinter import messagebox
from utils.db_utils import insert_item, get_all_items, update_item, delete_item

# Function to build the service items tab inside the main notebook
def build_item_tab(parent):
    parent.configure(bg="#f9f9f9")

    # --- Title ---
    tk.Label(parent, text="🧾 Itens de Serviço", font=("Helvetica", 18, "bold"), bg="#f9f9f9", fg="#333").pack(pady=10)

    # --- Form Frame ---
    form_frame = tk.Frame(parent, bg="#f9f9f9")
    form_frame.pack(pady=10)

    # --- Form fields ---
    tk.Label(form_frame, text="Nome do Serviço:", font=("Helvetica", 12), bg="#f9f9f9").grid(row=0, column=0, sticky="e", padx=5, pady=5)
    entry_name = tk.Entry(form_frame, width=40)
    entry_name.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Preço (R$):", font=("Helvetica", 12), bg="#f9f9f9").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    entry_price = tk.Entry(form_frame, width=40)
    entry_price.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Observações:", font=("Helvetica", 12), bg="#f9f9f9").grid(row=2, column=0, sticky="ne", padx=5, pady=5)
    entry_notes = tk.Text(form_frame, width=30, height=4)
    entry_notes.grid(row=2, column=1, padx=5, pady=5)

    selected_id = tk.StringVar()  # Store selected item ID

    # --- Button Frame ---
    button_frame = tk.Frame(parent, bg="#f9f9f9")
    button_frame.pack(pady=10)

    # Function to clear form fields
    def clear_fields():
        entry_name.delete(0, tk.END)
        entry_price.delete(0, tk.END)
        entry_notes.delete("1.0", tk.END)
        selected_id.set("")
        item_listbox.selection_clear(0, tk.END)

    # Function to register a new item
    def register_item():
        name = entry_name.get()
        price = entry_price.get()
        notes = entry_notes.get("1.0", tk.END).strip()

        if name == "":
            messagebox.showwarning("⚠️ Atenção", "O nome do serviço é obrigatório.")
            return

        try:
            price_float = float(price)
        except ValueError:
            messagebox.showwarning("⚠️ Atenção", "Preço inválido.")
            return

        insert_item(name, price_float, notes)
        messagebox.showinfo("✅ Sucesso", "Item cadastrado com sucesso!")
        clear_fields()
        list_items()

    # Function to update selected item
    def edit_item():
        if not selected_id.get():
            messagebox.showwarning("⚠️ Atenção", "Selecione um item para editar.")
            return

        name = entry_name.get()
        price = entry_price.get()
        notes = entry_notes.get("1.0", tk.END).strip()

        try:
            price_float = float(price)
        except ValueError:
            messagebox.showwarning("⚠️ Atenção", "Preço inválido.")
            return

        update_item(int(selected_id.get()), name, price_float, notes)
        messagebox.showinfo("✏️ Atualizado", "Item atualizado com sucesso!")
        clear_fields()
        list_items()

    # Function to delete selected item
    def remove_item():
        if not selected_id.get():
            messagebox.showwarning("⚠️ Atenção", "Selecione um item para excluir.")
            return

        confirm = messagebox.askyesno("🗑️ Confirmação", "Tem certeza que deseja excluir este item?")
        if confirm:
            delete_item(int(selected_id.get()))
            messagebox.showinfo("🗑️ Excluído", "Item excluído com sucesso!")
            clear_fields()
            list_items()

    # Buttons with emojis and styling
    tk.Button(button_frame, text="➕ Cadastrar", width=15, command=register_item, bg="#4CAF50", fg="white").grid(row=0, column=0, padx=5)
    tk.Button(button_frame, text="✏️ Editar", width=15, command=edit_item, bg="#2196F3", fg="white").grid(row=0, column=1, padx=5)
    tk.Button(button_frame, text="🗑️ Excluir", width=15, command=remove_item, bg="#f44336", fg="white").grid(row=0, column=2, padx=5)
    tk.Button(button_frame, text="🧹 Limpar", width=15, command=clear_fields, bg="#9E9E9E", fg="white").grid(row=0, column=3, padx=5)

    # --- Listbox section ---
    tk.Label(parent, text="📋 Itens cadastrados:", font=("Helvetica", 14), bg="#f9f9f9").pack(pady=10)
    item_listbox = tk.Listbox(parent, width=80, height=10)
    item_listbox.pack(pady=5)

    # Function to list all items
    def list_items():
        items = get_all_items()
        item_listbox.delete(0, tk.END)

        for item in items:
            texto = f"{item[0]} - {item[1]} | R$ {item[2]:.2f}"
            item_listbox.insert(tk.END, texto)

    # Function to load selected item into form
    def on_select(event):
        if not item_listbox.curselection():
            return

        index = item_listbox.curselection()[0]
        item = get_all_items()[index]

        selected_id.set(item[0])
        entry_name.delete(0, tk.END)
        entry_name.insert(0, item[1])

        entry_price.delete(0, tk.END)
        entry_price.insert(0, str(item[2]))

        entry_notes.delete("1.0", tk.END)
        entry_notes.insert("1.0", item[3])

    item_listbox.bind("<<ListboxSelect>>", on_select)
    list_items()