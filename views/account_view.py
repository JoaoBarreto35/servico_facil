import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from typing import List, Tuple
from utils.db_utils import (
    insert_account, get_all_accounts, update_account, delete_account
)


class AccountsTab:
    """Classe para gerenciar a aba de contas a pagar"""

    def __init__(self, parent):
        self.parent = parent
        self.parent.configure(bg="#f9f9f9")

        self.selected_id = tk.StringVar()
        self.all_accounts = []

        self._setup_ui()
        self.load_accounts()

    def _setup_ui(self):
        """Configura a interface do usuário"""
        # --- Título ---
        title_label = tk.Label(
            self.parent,
            text="💰 Contas a Pagar",
            font=("Helvetica", 18, "bold"),
            bg="#f9f9f9"
        )
        title_label.pack(pady=10)

        # --- Formulário ---
        self._create_form_section()

        # --- Filtros ---
        self._create_filters_section()

        # --- Treeview para contas ---
        self._create_accounts_treeview()

        # --- Botões de Ação ---
        self._create_action_buttons()

    def _create_form_section(self):
        """Cria a seção do formulário"""
        form_frame = tk.LabelFrame(
            self.parent, text="📝 Nova Conta",
            bg="#f9f9f9", padx=10, pady=10
        )
        form_frame.pack(fill="x", padx=20, pady=10)

        # Descrição
        tk.Label(form_frame, text="Descrição:", bg="#f9f9f9").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry_descricao = tk.Entry(form_frame, width=40)
        self.entry_descricao.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Valor
        tk.Label(form_frame, text="Valor (R$):", bg="#f9f9f9").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.entry_valor = tk.Entry(form_frame, width=15)
        self.entry_valor.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        # Data de Vencimento
        tk.Label(form_frame, text="Vencimento (DD/MM/AAAA):", bg="#f9f9f9").grid(row=1, column=0, sticky="w", padx=5,
                                                                                 pady=5)
        self.entry_vencimento = tk.Entry(form_frame, width=15)
        self.entry_vencimento.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        # Preenche com data de hoje + 30 dias
        data_padrao = (datetime.now() + timedelta(days=30)).strftime("%d/%m/%Y")
        self.entry_vencimento.insert(0, data_padrao)

        # Recorrente
        self.var_recorrente = tk.BooleanVar()
        self.check_recorrente = tk.Checkbutton(
            form_frame, text="Conta Recorrente",
            variable=self.var_recorrente, bg="#f9f9f9"
        )
        self.check_recorrente.grid(row=1, column=2, padx=5, pady=5, sticky="w")

        # Pago
        self.var_pago = tk.BooleanVar()
        self.check_pago = tk.Checkbutton(
            form_frame, text="Pago",
            variable=self.var_pago, bg="#f9f9f9"
        )
        self.check_pago.grid(row=1, column=3, padx=5, pady=5, sticky="w")

    def _create_filters_section(self):
        """Cria a seção de filtros"""
        filter_frame = tk.LabelFrame(
            self.parent, text="🔍 Filtros",
            bg="#f9f9f9", padx=10, pady=10
        )
        filter_frame.pack(fill="x", padx=20, pady=10)

        # Filtro por status
        tk.Label(filter_frame, text="Status:", bg="#f9f9f9").grid(row=0, column=0, sticky="w", padx=5)
        self.status_filter_var = tk.StringVar()
        status_options = ["Todos", "Pendentes", "Pagas", "Atrasadas"]
        status_combo = ttk.Combobox(
            filter_frame, textvariable=self.status_filter_var,
            values=status_options, state="readonly", width=15
        )
        status_combo.grid(row=0, column=1, padx=5, pady=2)
        status_combo.set("Todos")

        # Filtro por data
        tk.Label(filter_frame, text="Vencimento Início:", bg="#f9f9f9").grid(row=0, column=2, sticky="w", padx=5)
        self.start_date_var = tk.StringVar()
        start_date_entry = tk.Entry(filter_frame, textvariable=self.start_date_var, width=12)
        start_date_entry.grid(row=0, column=3, padx=5, pady=2)
        start_date_entry.insert(0, datetime.now().strftime("%d/%m/%Y"))

        tk.Label(filter_frame, text="Vencimento Fim:", bg="#f9f9f9").grid(row=0, column=4, sticky="w", padx=5)
        self.end_date_var = tk.StringVar()
        end_date_entry = tk.Entry(filter_frame, textvariable=self.end_date_var, width=12)
        end_date_entry.grid(row=0, column=5, padx=5, pady=2)
        end_date_entry.insert(0, (datetime.now() + timedelta(days=60)).strftime("%d/%m/%Y"))

        # Botões de filtro
        button_frame = tk.Frame(filter_frame, bg="#f9f9f9")
        button_frame.grid(row=0, column=6, padx=10)

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

    def _create_accounts_treeview(self):
        """Cria a treeview para exibir as contas"""
        tree_frame = tk.Frame(self.parent, bg="#f9f9f9")
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Treeview com scrollbar
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Descrição", "Valor", "Vencimento", "Recorrente", "Pago", "Status"),
            show="headings",
            height=12
        )

        # Configurar colunas
        columns = {
            "ID": 60,
            "Descrição": 200,
            "Valor": 100,
            "Vencimento": 100,
            "Recorrente": 80,
            "Pago": 80,
            "Status": 100
        }

        for col, width in columns.items():
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor="center")

        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind selection event
        self.tree.bind("<<TreeviewSelect>>", self.on_account_select)

    def _create_action_buttons(self):
        """Cria os botões de ação"""
        button_frame = tk.Frame(self.parent, bg="#f9f9f9")
        button_frame.pack(pady=10)

        buttons = [
            ("➕ Adicionar", self.add_account, "#4CAF50"),
            ("✏️ Editar", self.edit_account, "#2196F3"),
            ("✅ Marcar como Paga", self.mark_as_paid, "#FF9800"),
            ("🗑️ Excluir", self.delete_account, "#f44336"),
            ("🧹 Limpar", self.clear_fields, "#9C27B0")
        ]

        for text, command, color in buttons:
            tk.Button(
                button_frame, text=text, command=command,
                bg=color, fg="white", width=15
            ).pack(side="left", padx=5)

    def load_accounts(self):
        """Carrega todas as contas"""
        self.all_accounts = get_all_accounts()
        self.apply_filters()

    def apply_filters(self):
        """Aplica os filtros selecionados"""
        filtered_accounts = self.all_accounts.copy()

        # Filtro por status
        status_filter = self.status_filter_var.get()
        if status_filter != "Todos":
            if status_filter == "Pendentes":
                filtered_accounts = [a for a in filtered_accounts if not a[5]]  # paid = False
            elif status_filter == "Pagas":
                filtered_accounts = [a for a in filtered_accounts if a[5]]  # paid = True
            elif status_filter == "Atrasadas":
                hoje = datetime.now().date()
                filtered_accounts = [
                    a for a in filtered_accounts
                    if not a[5] and self._parse_date(a[3]) < hoje
                ]

        # Filtro por data de vencimento
        try:
            start_date = self._parse_date(self.start_date_var.get())
            end_date = self._parse_date(self.end_date_var.get())

            if start_date and end_date:
                filtered_accounts = [
                    a for a in filtered_accounts
                    if start_date <= self._parse_date(a[3]) <= end_date
                ]
        except:
            pass  # Ignora erros de data

        self.display_accounts(filtered_accounts)

    def _parse_date(self, date_str):
        """Converte string de data para objeto datetime"""
        try:
            return datetime.strptime(date_str, "%d/%m/%Y").date()
        except:
            try:
                return datetime.strptime(date_str, "%Y-%m-%d").date()
            except:
                return None

    def display_accounts(self, accounts):
        """Exibe as contas na treeview"""
        # Limpa a treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        hoje = datetime.now().date()

        for account in accounts:
            # Determina o status
            vencimento = self._parse_date(account[3])
            if account[5]:  # Se está pago
                status = "Pago"
                status_color = "green"
            elif vencimento and vencimento < hoje:
                status = "Atrasado"
                status_color = "red"
            else:
                status = "Pendente"
                status_color = "orange"

            self.tree.insert("", "end", values=(
                account[0],  # ID
                account[1],  # Descrição
                f"R$ {account[2]:.2f}",  # Valor
                account[3],  # Vencimento
                "Sim" if account[4] else "Não",  # Recorrente
                "Sim" if account[5] else "Não",  # Pago
                status  # Status
            ))

    def clear_filters(self):
        """Limpa todos os filtros"""
        self.status_filter_var.set("Todos")
        self.start_date_var.set(datetime.now().strftime("%d/%m/%Y"))
        self.end_date_var.set((datetime.now() + timedelta(days=60)).strftime("%d/%m/%Y"))
        self.load_accounts()

    def on_account_select(self, event):
        """Manipula a seleção de uma conta"""
        selection = self.tree.selection()
        if not selection:
            return

        item = self.tree.item(selection[0])
        account_id = item['values'][0]

        # Encontra a conta completa
        account = next((a for a in self.all_accounts if a[0] == account_id), None)
        if not account:
            return

        self.selected_id.set(account[0])
        self.entry_descricao.delete(0, tk.END)
        self.entry_descricao.insert(0, account[1])
        self.entry_valor.delete(0, tk.END)
        self.entry_valor.insert(0, str(account[2]))
        self.entry_vencimento.delete(0, tk.END)
        self.entry_vencimento.insert(0, account[3])
        self.var_recorrente.set(bool(account[4]))
        self.var_pago.set(bool(account[5]))

    def validate_form(self):
        """Valida os dados do formulário"""
        if not self.entry_descricao.get().strip():
            messagebox.showwarning("⚠️", "Informe a descrição da conta.")
            return False

        if not self.entry_valor.get().replace('.', '').replace(',', '').isdigit():
            messagebox.showwarning("⚠️", "Informe um valor válido.")
            return False

        if not self.entry_vencimento.get():
            messagebox.showwarning("⚠️", "Informe a data de vencimento.")
            return False

        return True

    def format_date_br_to_iso(self, date_str):
        """Converte data do formato BR para ISO"""
        try:
            d, m, y = date_str.split("/")
            return f"{y}-{m}-{d}"
        except ValueError:
            messagebox.showerror("Erro", "Formato de data inválido. Use DD/MM/AAAA")
            return None

    def add_account(self):
        """Adiciona uma nova conta"""
        if not self.validate_form():
            return

        vencimento_iso = self.format_date_br_to_iso(self.entry_vencimento.get())
        if not vencimento_iso:
            return

        try:
            descricao = self.entry_descricao.get().strip()
            valor = float(self.entry_valor.get().replace(',', '.'))
            recorrente = self.var_recorrente.get()
            pago = self.var_pago.get()

            insert_account(descricao, valor, vencimento_iso, recorrente, pago)

            self.load_accounts()
            self.clear_fields()
            messagebox.showinfo("✅", "Conta adicionada com sucesso!")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar conta: {str(e)}")

    def edit_account(self):
        """Edita uma conta existente"""
        if not self.selected_id.get():
            messagebox.showwarning("⚠️", "Selecione uma conta para editar.")
            return

        if not self.validate_form():
            return

        vencimento_iso = self.format_date_br_to_iso(self.entry_vencimento.get())
        if not vencimento_iso:
            return

        try:
            account_id = int(self.selected_id.get())
            descricao = self.entry_descricao.get().strip()
            valor = float(self.entry_valor.get().replace(',', '.'))
            recorrente = self.var_recorrente.get()
            pago = self.var_pago.get()

            update_account(account_id, descricao, valor, vencimento_iso, recorrente, pago)

            self.load_accounts()
            self.clear_fields()
            messagebox.showinfo("✏️", "Conta atualizada com sucesso!")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao editar conta: {str(e)}")

    def mark_as_paid(self):
        """Marca a conta selecionada como paga"""
        if not self.selected_id.get():
            messagebox.showwarning("⚠️", "Selecione uma conta para marcar como paga.")
            return

        try:
            account_id = int(self.selected_id.get())

            # Encontra a conta atual
            account = next((a for a in self.all_accounts if a[0] == account_id), None)
            if not account:
                messagebox.showerror("Erro", "Conta não encontrada.")
                return

            # Atualiza apenas o status de pago
            update_account(
                account_id,
                account[1],  # descricao
                account[2],  # valor
                account[3],  # vencimento
                account[4],  # recorrente
                True  # pago
            )

            self.load_accounts()
            self.clear_fields()
            messagebox.showinfo("✅", "Conta marcada como paga!")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao marcar conta como paga: {str(e)}")

    def delete_account(self):
        """Exclui a conta selecionada"""
        if not self.selected_id.get():
            messagebox.showwarning("⚠️", "Selecione uma conta para excluir.")
            return

        if messagebox.askyesno(
                "🗑️ Confirmar Exclusão",
                "Tem certeza que deseja excluir esta conta?\nEsta ação não pode ser desfeita."
        ):
            try:
                delete_account(int(self.selected_id.get()))
                self.load_accounts()
                self.clear_fields()
                messagebox.showinfo("🗑️", "Conta excluída com sucesso.")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir conta: {str(e)}")

    def clear_fields(self):
        """Limpa todos os campos do formulário"""
        self.entry_descricao.delete(0, tk.END)
        self.entry_valor.delete(0, tk.END)
        self.entry_vencimento.delete(0, tk.END)
        # Preenche com data de hoje + 30 dias
        data_padrao = (datetime.now() + timedelta(days=30)).strftime("%d/%m/%Y")
        self.entry_vencimento.insert(0, data_padrao)
        self.var_recorrente.set(False)
        self.var_pago.set(False)
        self.selected_id.set("")
        self.tree.selection_remove(self.tree.selection())

    def generate_report(self):
        """Gera um relatório das contas"""
        total_contas = len(self.tree.get_children())
        if total_contas == 0:
            messagebox.showinfo("📊 Relatório", "Nenhuma conta para gerar relatório.")
            return

        # Calcula totais
        total_pendente = 0
        total_pago = 0
        contas_atrasadas = 0

        for item in self.tree.get_children():
            account_data = self.tree.item(item)['values']
            valor = float(account_data[2].replace("R$ ", "").replace(",", ""))
            status = account_data[6]

            if status == "Pago":
                total_pago += valor
            else:
                total_pendente += valor
                if status == "Atrasado":
                    contas_atrasadas += 1

        report = f"""
📊 RELATÓRIO DE CONTAS A PAGAR

📈 Total de Contas: {total_contas}
💰 Total Pendente: R$ {total_pendente:.2f}
💰 Total Pago: R$ {total_pago:.2f}
💰 Valor Total: R$ {total_pendente + total_pago:.2f}

⚠️  Contas Atrasadas: {contas_atrasadas}
"""

        messagebox.showinfo("📊 Relatório de Contas", report)


def build_account_tab(parent):
    """Função principal para construir a aba de contas a pagar"""
    return AccountsTab(parent)