import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from typing import List, Tuple
from utils.db_utils import (
    get_all_orders, get_all_clients, get_order_items,
    get_all_items, delete_order, delete_order_item
)


class OrdersListTab:
    """Classe para gerenciar a aba de lista e filtros de ordens"""

    def __init__(self, parent):
        self.parent = parent
        self.parent.configure(bg="#f9f9f9")

        self.client_list = get_all_clients()
        self.item_list = get_all_items()
        self.all_orders = []

        self._setup_ui()
        self.load_orders()

    def _setup_ui(self):
        """Configura a interface do usuário"""
        # --- Título ---
        title_label = tk.Label(
            self.parent,
            text="📋 Lista de Ordens de Serviço",
            font=("Helvetica", 18, "bold"),
            bg="#f9f9f9"
        )
        title_label.pack(pady=10)

        # --- Filtros ---
        self._create_filters_section()

        # --- Treeview para ordens ---
        self._create_orders_treeview()

        # --- Detalhes da ordem selecionada ---
        self._create_order_details_section()

        # --- Botões de Ação ---
        self._create_action_buttons()

    def _create_filters_section(self):
        """Cria a seção de filtros"""
        filter_frame = tk.LabelFrame(
            self.parent, text="🔍 Filtros",
            bg="#f9f9f9", padx=10, pady=10
        )
        filter_frame.pack(fill="x", padx=20, pady=10)

        # Filtro por cliente
        tk.Label(filter_frame, text="Cliente:", bg="#f9f9f9").grid(row=0, column=0, sticky="w", padx=5)
        self.client_filter_var = tk.StringVar()
        client_options = ["Todos"] + [f"{c[0]} - {c[1]}" for c in self.client_list]
        client_combo = ttk.Combobox(
            filter_frame, textvariable=self.client_filter_var,
            values=client_options, state="readonly", width=30
        )
        client_combo.grid(row=0, column=1, padx=5, pady=2)
        client_combo.set("Todos")

        # Filtro por status
        tk.Label(filter_frame, text="Status:", bg="#f9f9f9").grid(row=0, column=2, sticky="w", padx=5)
        self.status_filter_var = tk.StringVar()
        status_options = ["Todos", "Pendente", "Em Andamento", "Concluído", "Cancelado"]
        status_combo = ttk.Combobox(
            filter_frame, textvariable=self.status_filter_var,
            values=status_options, state="readonly", width=20
        )
        status_combo.grid(row=0, column=3, padx=5, pady=2)
        status_combo.set("Todos")

        # Filtro por data
        tk.Label(filter_frame, text="Data Início:", bg="#f9f9f9").grid(row=1, column=0, sticky="w", padx=5)
        self.start_date_var = tk.StringVar()
        start_date_entry = tk.Entry(filter_frame, textvariable=self.start_date_var, width=12)
        start_date_entry.grid(row=1, column=1, padx=5, pady=2)
        start_date_entry.insert(0, (datetime.now() - timedelta(days=30)).strftime("%d/%m/%Y"))

        tk.Label(filter_frame, text="Data Fim:", bg="#f9f9f9").grid(row=1, column=2, sticky="w", padx=5)
        self.end_date_var = tk.StringVar()
        end_date_entry = tk.Entry(filter_frame, textvariable=self.end_date_var, width=12)
        end_date_entry.grid(row=1, column=3, padx=5, pady=2)
        end_date_entry.insert(0, datetime.now().strftime("%d/%m/%Y"))

        # Botões de filtro
        button_frame = tk.Frame(filter_frame, bg="#f9f9f9")
        button_frame.grid(row=0, column=4, rowspan=2, padx=10)

        tk.Button(
            button_frame, text="🔍 Aplicar Filtros",
            command=self.apply_filters, bg="#2196F3", fg="white",
            width=15
        ).pack(pady=2)

        tk.Button(
            button_frame, text="🧹 Limpar Filtros",
            command=self.clear_filters, bg="#FF9800", fg="white",
            width=15
        ).pack(pady=2)

    def _create_orders_treeview(self):
        """Cria a treeview para exibir as ordens"""
        tree_frame = tk.Frame(self.parent, bg="#f9f9f9")
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Treeview com scrollbar
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Cliente", "Data", "Status", "Entrega", "Total"),
            show="headings",
            height=12
        )

        # Configurar colunas
        columns = {
            "ID": 60,
            "Cliente": 200,
            "Data": 100,
            "Status": 120,
            "Entrega": 120,
            "Total": 100
        }

        for col, width in columns.items():
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor="center" if col in ["ID", "Total"] else "w")

        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind selection event
        self.tree.bind("<<TreeviewSelect>>", self.on_order_select)

    def _create_order_details_section(self):
        """Cria a seção de detalhes da ordem"""
        details_frame = tk.LabelFrame(
            self.parent, text="📄 Detalhes da Ordem Selecionada",
            bg="#f9f9f9", padx=10, pady=10
        )
        details_frame.pack(fill="x", padx=20, pady=10)

        # Frame para informações básicas
        info_frame = tk.Frame(details_frame, bg="#f9f9f9")
        info_frame.pack(fill="x", pady=5)

        # Labels de informações
        self.info_labels = {}
        fields = [
            ("ID:", "id"),
            ("Cliente:", "client"),
            ("Data:", "date"),
            ("Status:", "status"),
            ("Entrega:", "delivery"),
            ("Observações:", "notes")
        ]

        for i, (label, key) in enumerate(fields):
            tk.Label(info_frame, text=label, bg="#f9f9f9", font=("Helvetica", 9, "bold")).grid(
                row=i // 2, column=(i % 2) * 2, sticky="w", padx=5, pady=2
            )
            self.info_labels[key] = tk.Label(
                info_frame, text="", bg="#f9f9f9", wraplength=300
            )
            self.info_labels[key].grid(
                row=i // 2, column=(i % 2) * 2 + 1, sticky="w", padx=5, pady=2
            )

        # Treeview para itens da ordem
        items_frame = tk.Frame(details_frame, bg="#f9f9f9")
        items_frame.pack(fill="x", pady=5)

        tk.Label(items_frame, text="Itens da Ordem:", bg="#f9f9f9", font=("Helvetica", 10, "bold")).pack(anchor="w")

        self.items_tree = ttk.Treeview(
            items_frame,
            columns=("Item", "Quantidade", "Preço Unit.", "Subtotal"),
            show="headings",
            height=4
        )

        items_columns = {
            "Item": 250,
            "Quantidade": 80,
            "Preço Unit.": 100,
            "Subtotal": 100
        }

        for col, width in items_columns.items():
            self.items_tree.heading(col, text=col)
            self.items_tree.column(col, width=width, anchor="center" if col != "Item" else "w")

        self.items_tree.pack(fill="x", pady=5)

        # Label do total
        self.total_label = tk.Label(
            details_frame, text="💰 Total da Ordem: R$ 0.00",
            bg="#f9f9f9", font=("Helvetica", 12, "bold")
        )
        self.total_label.pack(pady=5)

    def _create_action_buttons(self):
        """Cria os botões de ação"""
        button_frame = tk.Frame(self.parent, bg="#f9f9f9")
        button_frame.pack(pady=10)

        tk.Button(
            button_frame, text="🔄 Atualizar Lista",
            command=self.load_orders, bg="#4CAF50", fg="white",
            width=15
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame, text="🗑️ Excluir Ordem",
            command=self.delete_selected_order, bg="#f44336", fg="white",
            width=15
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame, text="📊 Relatório",
            command=self.generate_report, bg="#9C27B0", fg="white",
            width=15
        ).pack(side="left", padx=5)

    def load_orders(self):
        """Carrega todas as ordens"""
        self.all_orders = get_all_orders()
        self.apply_filters()

    def apply_filters(self):
        """Aplica os filtros selecionados"""
        filtered_orders = self.all_orders.copy()

        # Filtro por cliente
        client_filter = self.client_filter_var.get()
        if client_filter != "Todos":
            client_id = int(client_filter.split(" - ")[0])
            filtered_orders = [o for o in filtered_orders if o[1] == client_id]

        # Filtro por status
        status_filter = self.status_filter_var.get()
        if status_filter != "Todos":
            filtered_orders = [o for o in filtered_orders if o[3] == status_filter]

        # Filtro por data
        try:
            start_date = self._parse_date(self.start_date_var.get())
            end_date = self._parse_date(self.end_date_var.get())

            if start_date and end_date:
                filtered_orders = [
                    o for o in filtered_orders
                    if start_date <= self._parse_date(o[2]) <= end_date
                ]
        except:
            pass  # Ignora erros de data

        # 🔥 CORREÇÃO: Mudar para display_orders (sem o 'y')
        self.display_orders(filtered_orders)

    def _parse_date(self, date_str):
        """Converte string de data para objeto datetime"""
        try:
            return datetime.strptime(date_str, "%d/%m/%Y")
        except:
            try:
                return datetime.strptime(date_str, "%Y-%m-%d")
            except:
                return None

    def display_order_details(self, order):
        """Exibe os detalhes da ordem selecionada"""
        # Informações básicas
        client_name = next((c[1] for c in self.client_list if c[0] == order[1]), "Desconhecido")

        self.info_labels["id"].config(text=order[0])
        self.info_labels["client"].config(text=client_name)
        self.info_labels["date"].config(text=order[2])
        self.info_labels["status"].config(text=order[3])
        self.info_labels["delivery"].config(text=order[4])
        self.info_labels["notes"].config(text=order[5] or "Nenhuma")

        # Itens da ordem
        for item in self.items_tree.get_children():
            self.items_tree.delete(item)

        order_items = get_order_items(order[0])
        total_order = 0

        # 🔥 CORREÇÃO: Usar a ordem correta das colunas
        for item in order_items:
            registro_id = item[0]  # Não usado
            item_id = item[1]  # ID do item
            qty = item[2]  # Quantidade
            unit_price = item[3]  # Preço unitário

            item_name = next((i[1] for i in self.item_list if i[0] == item_id), "Desconhecido")
            subtotal = qty * unit_price
            total_order += subtotal

            self.items_tree.insert("", "end", values=(
                item_name,
                qty,
                f"R$ {unit_price:.2f}",
                f"R$ {subtotal:.2f}"
            ))

        self.total_label.config(text=f"💰 Total da Ordem: R$ {total_order:.2f}")

    def clear_filters(self):
        """Limpa todos os filtros"""
        self.client_filter_var.set("Todos")
        self.status_filter_var.set("Todos")
        self.start_date_var.set((datetime.now() - timedelta(days=30)).strftime("%d/%m/%Y"))
        self.end_date_var.set(datetime.now().strftime("%d/%m/%Y"))
        self.load_orders()

    def on_order_select(self, event):
        """Manipula a seleção de uma ordem"""
        selection = self.tree.selection()
        if not selection:
            return

        item = self.tree.item(selection[0])
        order_id = item['values'][0]

        # Encontra a ordem completa
        order = next((o for o in self.all_orders if o[0] == order_id), None)
        if not order:
            return

        self.display_order_details(order)

    def display_orders(self, orders):
        """Exibe as ordens na treeview"""
        # Limpa a treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        client_dict = {c[0]: c[1] for c in self.client_list}

        for order in orders:
            # Calcula o total da ordem
            order_items = get_order_items(order[0])
            total = sum(qty * price for _, _, qty, price in order_items)

            self.tree.insert("", "end", values=(
                order[0],  # ID
                client_dict.get(order[1], "Desconhecido"),  # Cliente
                order[2],  # Data
                order[3],  # Status
                order[4],  # Método de entrega
                f"R$ {total:.2f}"  # Total
            ))

    def delete_selected_order(self):
        """Exclui a ordem selecionada"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("⚠️", "Selecione uma ordem para excluir.")
            return

        item = self.tree.item(selection[0])
        order_id = item['values'][0]
        client_name = item['values'][1]

        if messagebox.askyesno(
                "🗑️ Confirmar Exclusão",
                f"Tem certeza que deseja excluir a ordem {order_id} do cliente {client_name}?\n"
                "Esta ação não pode ser desfeita."
        ):
            try:
                # Remove os itens da ordem primeiro
                order_items = get_order_items(order_id)
                for item_id, _, _, _ in order_items:
                    delete_order_item(item_id)

                # Remove a ordem
                delete_order(order_id)

                messagebox.showinfo("✅", "Ordem excluída com sucesso!")
                self.load_orders()

                # Limpa os detalhes
                for label in self.info_labels.values():
                    label.config(text="")
                for item in self.items_tree.get_children():
                    self.items_tree.delete(item)
                self.total_label.config(text="💰 Total da Ordem: R$ 0.00")

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir ordem: {str(e)}")

    def generate_report(self):
        """Gera um relatório simples das ordens"""
        total_orders = len(self.tree.get_children())
        if total_orders == 0:
            messagebox.showinfo("📊 Relatório", "Nenhuma ordem para gerar relatório.")
            return

        # Calcula totais
        total_value = 0
        status_count = {}

        for item in self.tree.get_children():
            order_data = self.tree.item(item)['values']
            total_value += float(order_data[5].replace("R$ ", "").replace(",", ""))
            status = order_data[3]
            status_count[status] = status_count.get(status, 0) + 1

        report = f"""
📊 RELATÓRIO DE ORDENS

📈 Total de Ordens: {total_orders}
💰 Valor Total: R$ {total_value:.2f}

📋 Distribuição por Status:
"""
        for status, count in status_count.items():
            report += f"   • {status}: {count} ordens\n"

        messagebox.showinfo("📊 Relatório de Ordens", report)


def build_orders_list_tab(parent):
    """Função principal para construir a aba de lista de ordens"""
    return OrdersListTab(parent)