import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from typing import List, Tuple, Optional
from utils.db_utils import (
    insert_order, get_all_orders, update_order, delete_order,
    get_all_clients, get_all_items, get_order_items,
    insert_order_item, delete_order_item
)
from utils.constants import ORDER_STATUS, DELIVERY_METHODS

class OrderTab:
    """Classe para gerenciar a aba de cadastro de ordens de serviço"""

    def __init__(self, parent):
        self.parent = parent
        self.parent.configure(bg="#f9f9f9")

        self.selected_id = tk.StringVar()
        self.temp_items: List[Tuple[int, int, float]] = []

        # Carregar dados
        self.client_list = get_all_clients()
        self.item_list = get_all_items()

        # Debug detalhado dos itens
        print("=== CARREGAMENTO DE ITENS ===")
        print(f"Total de clientes: {len(self.client_list)}")
        print(f"Total de itens: {len(self.item_list)}")

        if not self.item_list:
            print("⚠️ AVISO: Lista de itens está VAZIA!")
        else:
            print("Itens carregados:")
            for i, item in enumerate(self.item_list):
                print(
                    f"  {i + 1:2d}. ID: {item[0]:3d} | Nome: '{item[1]:20}' | Preço: R$ {item[2]:8.2f} | Notas: '{item[3]}'")

        # Debug dos clientes
        if not self.client_list:
            print("⚠️ AVISO: Lista de clientes está VAZIA!")
        else:
            print("Clientes carregados:")
            for i, client in enumerate(self.client_list[:3]):  # Mostrar só os 3 primeiros
                print(f"  {i + 1:2d}. ID: {client[0]:3d} | Nome: '{client[1]:20}'")

        self._setup_ui()
        self.list_orders()

    def _setup_ui(self):
        """Configura a interface do usuário"""
        # --- Título ---
        title_label = tk.Label(
            self.parent,
            text="📦 Cadastro de Ordens de Serviço",
            font=("Helvetica", 18, "bold"),
            bg="#f9f9f9"
        )
        title_label.pack(pady=10)

        # --- Formulário Principal ---
        self._create_main_form()

        # --- Painel de Itens ---
        self._create_items_panel()

        # --- Botões de Ação ---
        self._create_action_buttons()

        # --- Lista de Ordens ---
        self._create_orders_list()

    def _create_main_form(self):
        """Cria o formulário principal de dados da ordem"""
        form_frame = tk.Frame(self.parent, bg="#f9f9f9")
        form_frame.pack(pady=10, fill="x", padx=20)

        # Cliente
        client_options = [f"{c[0]} - {c[1]}" for c in self.client_list]
        self.client_var = tk.StringVar()
        self._create_form_field(
            form_frame, "Cliente:", 0,
            ttk.Combobox(form_frame, textvariable=self.client_var,
                         values=client_options, state="readonly", width=40)
        )

        # Data
        self.entry_date = tk.Entry(form_frame, width=40)
        self._create_form_field(form_frame, "Data (DD/MM/AAAA):", 1, self.entry_date)
        self.entry_date.insert(0, datetime.now().strftime("%d/%m/%Y"))

        # Status
        self.status_var = tk.StringVar()
        status_combo = ttk.Combobox(
            form_frame, textvariable=self.status_var,
            values=ORDER_STATUS, state="readonly", width=40
        )
        self._create_form_field(form_frame, "Status:", 2, status_combo)
        if ORDER_STATUS:
            status_combo.set(ORDER_STATUS[0])

        # Método de Entrega
        self.delivery_var = tk.StringVar()
        delivery_combo = ttk.Combobox(
            form_frame, textvariable=self.delivery_var,
            values=DELIVERY_METHODS, state="readonly", width=40
        )
        self._create_form_field(form_frame, "Entrega:", 3, delivery_combo)
        if DELIVERY_METHODS:
            delivery_combo.set(DELIVERY_METHODS[0])

        # Observações
        tk.Label(form_frame, text="Observações:", bg="#f9f9f9").grid(
            row=4, column=0, sticky="ne", padx=5, pady=5
        )
        self.entry_notes = tk.Text(form_frame, width=30, height=4)
        self.entry_notes.grid(row=4, column=1, columnspan=2, padx=5, pady=5, sticky="w")

    def _create_form_field(self, parent, label, row, widget):
        """Cria um campo do formulário com label"""
        tk.Label(parent, text=label, bg="#f9f9f9").grid(
            row=row, column=0, sticky="e", padx=5, pady=5
        )
        widget.grid(row=row, column=1, padx=5, pady=5, sticky="w")
        return widget

    def _create_items_panel(self):
        """Cria o painel para adicionar itens à ordem"""
        item_frame = tk.LabelFrame(
            self.parent, text="🧾 Itens da Ordem",
            bg="#f9f9f9", padx=10, pady=10
        )
        item_frame.pack(pady=10, fill="x", padx=20)

        # Seleção de item
        item_options = [f"{i[0]} - {i[1]} (R${i[2]:.2f})" for i in self.item_list]
        self.item_var = tk.StringVar()

        tk.Label(item_frame, text="Item de Serviço:", bg="#f9f9f9").grid(
            row=0, column=0, sticky="w", padx=5
        )
        self.item_combo = ttk.Combobox(
            item_frame, textvariable=self.item_var,
            values=item_options, state="readonly", width=40
        )
        self.item_combo.grid(row=0, column=1, padx=5)
        if item_options:
            self.item_combo.set(item_options[0])

        # Quantidade
        tk.Label(item_frame, text="Quantidade:", bg="#f9f9f9").grid(
            row=0, column=2, sticky="w", padx=5
        )
        self.entry_qty = tk.Entry(item_frame, width=10)
        self.entry_qty.grid(row=0, column=3, padx=5)
        self.entry_qty.insert(0, "1")

        # Lista de itens adicionados
        self.item_listbox = tk.Listbox(item_frame, width=80, height=6)
        self.item_listbox.grid(row=1, column=0, columnspan=4, pady=10, padx=5)

        # Label do total
        self.total_label = tk.Label(
            item_frame, text="💰 Total: R$ 0.00",
            bg="#f9f9f9", font=("Helvetica", 12, "bold")
        )
        self.total_label.grid(row=2, column=0, columnspan=4)

        # Botões de itens
        button_frame = tk.Frame(item_frame, bg="#f9f9f9")
        button_frame.grid(row=0, column=4, rowspan=2, padx=10, sticky="n")

        tk.Button(
            button_frame, text="➕ Adicionar Item",
            command=self.add_item_to_temp, bg="#4CAF50", fg="white",
            width=18
        ).pack(pady=2)

        tk.Button(
            button_frame, text="🗑️ Remover Item",
            command=self.remove_item_from_temp, bg="#f44336", fg="white",
            width=18
        ).pack(pady=2)

    def _create_action_buttons(self):
        """Cria os botões de ação principais"""
        button_frame = tk.Frame(self.parent, bg="#f9f9f9")
        button_frame.pack(pady=10)

        buttons = [
            ("➕ Cadastrar", self.register_order, "#4CAF50"),
            ("✏️ Editar", self.edit_order, "#2196F3"),
            ("🗑️ Excluir", self.remove_order, "#f44336"),
            ("🧹 Limpar", self.clear_fields, "#FF9800")
        ]

        for text, command, color in buttons:
            tk.Button(
                button_frame, text=text, command=command,
                bg=color, fg="white", width=15
            ).pack(side="left", padx=5)

    def _create_orders_list(self):
        """Cria a lista de ordens cadastradas"""
        tk.Label(
            self.parent, text="📋 Ordens cadastradas (clique para editar):",
            bg="#f9f9f9", font=("Helvetica", 10, "bold")
        ).pack(pady=(20, 5))

        self.order_listbox = tk.Listbox(self.parent, width=80, height=8)
        self.order_listbox.pack(pady=5, padx=20)
        self.order_listbox.bind("<<ListboxSelect>>", self.on_select)

    def format_date_br_to_iso(self, date_str: str) -> Optional[str]:
        """Converte data do formato BR para ISO"""
        try:
            d, m, y = date_str.split("/")
            return f"{y}-{m}-{d}"
        except ValueError:
            messagebox.showerror("Erro", "Formato de data inválido. Use DD/MM/AAAA")
            return None

    def validate_form(self) -> bool:
        """Valida os dados do formulário"""
        if not self.client_var.get():
            messagebox.showwarning("⚠️", "Selecione um cliente.")
            return False

        if not self.entry_date.get():
            messagebox.showwarning("⚠️", "Informe a data da ordem.")
            return False

        if not self.temp_items:
            messagebox.showwarning("⚠️", "Adicione pelo menos um item.")
            return False

        return True

    def list_temp_items(self):
        """Atualiza a lista de itens temporários e calcula o total"""
        self.item_listbox.delete(0, tk.END)
        total = 0.0

        print(f"=== LISTANDO ITENS TEMPORÁRIOS ===")  # Debug
        print(f"Total de itens na temp_items: {len(self.temp_items)}")  # Debug
        print(f"Total de itens na item_list: {len(self.item_list)}")  # Debug

        for i, item in enumerate(self.item_list):
            print(f"Item {i}: ID={item[0]}, Nome='{item[1]}', Preço={item[2]}")  # Debug

        for item_id, qtd, preco in self.temp_items:
            print(f"Buscando item ID {item_id}...")  # Debug

            # Buscar o nome do item
            nome = "Desconhecido"
            for item in self.item_list:
                if item[0] == item_id:
                    nome = item[1]
                    print(f"Item encontrado: {nome}")  # Debug
                    break
            else:
                print(f"Item ID {item_id} NÃO encontrado!")  # Debug

            subtotal = qtd * preco
            total += subtotal
            texto = f"{nome} | Qtd: {qtd} | Unit: R${preco:.2f} | Subtotal: R${subtotal:.2f}"
            self.item_listbox.insert(tk.END, texto)
            print(f"Item listado: {texto}")  # Debug

        self.total_label.config(text=f"💰 Total: R$ {total:.2f}")
        print(f"Total calculado: R$ {total:.2f}")  # Debug

    def add_item_to_temp(self):
        """Adiciona item à lista temporária"""
        print("=== INICIANDO ADIÇÃO DE ITEM ===")

        if not self.item_var.get():
            messagebox.showwarning("⚠️", "Selecione um item da lista.")
            return

        qtd_text = self.entry_qty.get().strip()
        if not qtd_text or not qtd_text.isdigit():
            messagebox.showwarning("⚠️", "Informe uma quantidade válida (número inteiro).")
            return

        try:
            # Extrair ID do item
            item_text = self.item_var.get()
            print(f"Texto do item selecionado: '{item_text}'")

            # Verificar se o texto tem o formato esperado
            if " - " not in item_text:
                messagebox.showerror("Erro", "Formato do item inválido.")
                return

            item_id_str = item_text.split(" - ")[0]
            print(f"ID extraído como string: '{item_id_str}'")

            item_id = int(item_id_str)
            qtd = int(qtd_text)

            print(f"Item ID: {item_id}, Quantidade: {qtd}")

            if qtd <= 0:
                messagebox.showwarning("⚠️", "A quantidade deve ser maior que zero.")
                return

            # Buscar preço e nome do item para verificação
            preco = 0
            nome_item = "Não encontrado"
            item_encontrado = False

            for item in self.item_list:
                if item[0] == item_id:
                    preco = item[2]
                    nome_item = item[1]
                    item_encontrado = True
                    print(f"Item encontrado na base: '{nome_item}' - R$ {preco:.2f}")
                    break

            if not item_encontrado:
                # Tentar encontrar por nome (fallback)
                nome_procurado = item_text.split(" - ")[1].split(" (R$")[0]
                for item in self.item_list:
                    if item[1] == nome_procurado:
                        item_id = item[0]  # Corrigir o ID
                        preco = item[2]
                        nome_item = item[1]
                        item_encontrado = True
                        print(f"Item encontrado por nome: '{nome_item}' - ID: {item_id} - R$ {preco:.2f}")
                        break

            if not item_encontrado:
                messagebox.showerror("Erro", f"Item não encontrado na base de dados. ID: {item_id}")
                return

            # Adicionar à lista temporária
            novo_item = (item_id, qtd, preco)
            self.temp_items.append(novo_item)
            print(f"Item adicionado à lista: ID={item_id}, Nome='{nome_item}', Qtd={qtd}, Preço={preco}")

            # Resetar campos
            self.entry_qty.delete(0, tk.END)
            self.entry_qty.insert(0, "1")

            # Atualizar lista visual
            self.list_temp_items()

            print("=== ITEM ADICIONADO COM SUCESSO ===")

        except ValueError as e:
            error_msg = f"Erro ao processar dados: {str(e)}"
            print(f"ERRO: {error_msg}")
            messagebox.showerror("Erro", error_msg)
        except Exception as e:
            error_msg = f"Erro inesperado: {str(e)}"
            print(f"ERRO INESPERADO: {error_msg}")
            messagebox.showerror("Erro", error_msg)

    def remove_item_from_temp(self):
        """Remove item selecionado da lista temporária"""
        if not self.item_listbox.curselection():
            messagebox.showwarning("⚠️", "Selecione um item para remover.")
            return

        index = self.item_listbox.curselection()[0]
        self.temp_items.pop(index)
        self.list_temp_items()

    def clear_fields(self):
        """Limpa todos os campos do formulário"""
        self.client_var.set("")
        self.entry_date.delete(0, tk.END)
        self.entry_date.insert(0, datetime.now().strftime("%d/%m/%Y"))
        self.status_var.set(ORDER_STATUS[0] if ORDER_STATUS else "")
        self.delivery_var.set(DELIVERY_METHODS[0] if DELIVERY_METHODS else "")
        self.entry_notes.delete("1.0", tk.END)
        self.selected_id.set("")
        self.temp_items.clear()
        self.item_listbox.delete(0, tk.END)
        self.total_label.config(text="💰 Total: R$ 0.00")
        self.order_listbox.selection_clear(0, tk.END)

    def register_order(self):
        """Cadastra uma nova ordem"""
        if not self.validate_form():
            return

        date_iso = self.format_date_br_to_iso(self.entry_date.get())
        if not date_iso:
            return

        try:
            client_id = int(self.client_var.get().split(" - ")[0])
            status = self.status_var.get()
            delivery = self.delivery_var.get()
            notes = self.entry_notes.get("1.0", tk.END).strip()

            # 🔥 INSERE A ORDEM E PEGA O ID
            ordem_id = insert_order(client_id, date_iso, status, delivery, notes)
            print(f"Ordem criada com ID: {ordem_id}")  # Debug

            # 🔥 INSERE OS ITENS DA ORDEM
            for item_id, qtd, preco in self.temp_items:
                print(f"Adicionando item: {item_id}, qtd: {qtd}, preco: {preco}")  # Debug
                insert_order_item(ordem_id, item_id, qtd, preco)

            self.list_orders()
            self.clear_fields()
            messagebox.showinfo("✅", "Ordem cadastrada com sucesso!")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar ordem: {str(e)}")
            print(f"Erro detalhado: {e}")  # Debug

    def edit_order(self):
        """Edita uma ordem existente"""
        if not self.selected_id.get():
            messagebox.showwarning("⚠️", "Selecione uma ordem para editar.")
            return

        if not self.validate_form():
            return

        date_iso = self.format_date_br_to_iso(self.entry_date.get())
        if not date_iso:
            return

        try:
            ordem_id = int(self.selected_id.get())
            client_id = int(self.client_var.get().split(" - ")[0])
            status = self.status_var.get()
            delivery = self.delivery_var.get()
            notes = self.entry_notes.get("1.0", tk.END).strip()

            # Atualiza ordem
            update_order(ordem_id, client_id, date_iso, status, delivery, notes)

            # 🔥 CORREÇÃO: Remove os itens antigos corretamente
            order_items = get_order_items(ordem_id)
            for item in order_items:
                item_id = item[0]  # 🔥 Aqui é o ID do order_item, não do item!
                delete_order_item(item_id)

            # Adiciona os novos itens
            for item_id, qtd, preco in self.temp_items:
                insert_order_item(ordem_id, item_id, qtd, preco)

            self.list_orders()
            self.clear_fields()
            messagebox.showinfo("✏️", "Ordem e itens atualizados com sucesso!")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao editar ordem: {str(e)}")

    def remove_order(self):
        """Remove uma ordem"""
        if not self.selected_id.get():
            messagebox.showwarning("⚠️", "Selecione uma ordem para excluir.")
            return

        if messagebox.askyesno(
                "🗑️ Confirmar Exclusão",
                "Tem certeza que deseja excluir esta ordem?\nEsta ação não pode ser desfeita."
        ):
            try:
                delete_order(int(self.selected_id.get()))
                self.list_orders()
                self.clear_fields()
                messagebox.showinfo("🗑️", "Ordem excluída com sucesso.")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir ordem: {str(e)}")

    def list_orders(self):
        """Lista todas as ordens cadastradas"""
        orders = get_all_orders()
        self.order_listbox.delete(0, tk.END)

        client_dict = {c[0]: c[1] for c in self.client_list}

        for order in orders:
            texto = f"{order[0]} - {client_dict.get(order[1], 'Desconhecido')} | {order[2]} | {order[3]} | {order[4]}"
            self.order_listbox.insert(tk.END, texto)

    def on_select(self, event):
        """Manipula a seleção de uma ordem na lista - AGORA MOSTRA OS ITENS CORRETAMENTE"""
        if not self.order_listbox.curselection():
            return

        try:
            index = self.order_listbox.curselection()[0]
            orders = get_all_orders()

            if index >= len(orders):
                messagebox.showerror("Erro", "Índice da ordem inválido.")
                return

            order = orders[index]

            print(f"=== SELECIONANDO ORDEM ===")
            print(f"Ordem ID: {order[0]}")
            print(f"Cliente ID: {order[1]}")
            print(f"Data: {order[2]}")
            print(f"Status: {order[3]}")

            self.selected_id.set(order[0])

            # Preenche dados do cliente
            client_name = next(
                (c[1] for c in self.client_list if c[0] == order[1]),
                "Desconhecido"
            )
            self.client_var.set(f"{order[1]} - {client_name}")

            # Preenche outros campos
            self.entry_date.delete(0, tk.END)
            self.entry_date.insert(0, order[2])
            self.status_var.set(order[3])
            self.delivery_var.set(order[4])
            self.entry_notes.delete("1.0", tk.END)
            self.entry_notes.insert("1.0", order[5] or "")

            # 🔥🔥🔥 CORREÇÃO PRINCIPAL: Carrega itens da ordem selecionada
            self.temp_items.clear()
            order_items = get_order_items(order[0])  # order[0] é o ID da ordem

            print(f"Carregando {len(order_items)} itens da ordem {order[0]}:")
            for i, item in enumerate(order_items):
                # 🔥 ORDEM CORRETA: (id_do_registro, item_id, quantity, unit_price)
                registro_id = item[0]  # ID do registro na tabela order_items (não usamos)
                item_id = item[1]  # ID do item de serviço
                qtd = item[2]  # Quantidade
                preco = item[3]  # Preço unitário

                print(f"  Item {i + 1}: Registro_ID={registro_id}, Item_ID={item_id}, Qtd={qtd}, Preço={preco}")
                self.temp_items.append((item_id, qtd, preco))

            print(f"Total de itens carregados: {len(self.temp_items)}")
            self.list_temp_items()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar ordem: {str(e)}")
            import traceback
            print(f"Erro detalhado: {traceback.format_exc()}")

def build_order_tab(parent):
    """Função principal para construir a aba de cadastro de ordens"""
    return OrderTab(parent)