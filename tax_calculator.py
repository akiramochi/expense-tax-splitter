import tkinter as tk
from tkinter import ttk, messagebox


class TaxCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Expense Tax Calculator")
        self.resizable(False, False)
        self.configure(padx=16, pady=16)

        self._build_input_section()
        self._build_results_section()

    # ── Input section ──────────────────────────────────────────────────────

    def _build_input_section(self):
        input_frame = ttk.LabelFrame(self, text="Items", padding=10)
        input_frame.grid(row=0, column=0, sticky="ew")

        self.item_entries = []
        self.item_frame = ttk.Frame(input_frame)
        self.item_frame.grid(row=0, column=0, columnspan=3)

        self._add_item_row()

        ttk.Button(input_frame, text="+ Add Item", command=self._add_item_row).grid(
            row=1, column=0, sticky="w", pady=(8, 0)
        )
        ttk.Button(input_frame, text="− Remove Last", command=self._remove_item_row).grid(
            row=1, column=1, sticky="w", pady=(8, 0), padx=4
        )

        tax_frame = ttk.LabelFrame(self, text="Sales Tax", padding=10)
        tax_frame.grid(row=1, column=0, sticky="ew", pady=(10, 0))

        ttk.Label(tax_frame, text="Total tax amount:  $").grid(row=0, column=0, sticky="w")
        self.tax_var = tk.StringVar()
        tax_entry = ttk.Entry(tax_frame, textvariable=self.tax_var, width=12)
        tax_entry.grid(row=0, column=1, sticky="w")
        tax_entry.bind("<Return>", lambda e: self._calculate())

        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=2, column=0, pady=(12, 0), sticky="ew")
        ttk.Button(btn_frame, text="Calculate", command=self._calculate).pack(side="left")
        ttk.Button(btn_frame, text="Clear All", command=self._clear).pack(side="left", padx=6)

    def _add_item_row(self):
        row = len(self.item_entries)
        ttk.Label(self.item_frame, text=f"Item {row + 1}:  $").grid(
            row=row, column=0, sticky="w", pady=2
        )
        var = tk.StringVar()
        entry = ttk.Entry(self.item_frame, textvariable=var, width=12)
        entry.grid(row=row, column=1, sticky="w", pady=2)
        entry.bind("<Return>", self._item_enter)
        self.item_entries.append((var, entry))
        entry.focus_set()

    def _remove_item_row(self):
        if len(self.item_entries) <= 1:
            return
        var, entry = self.item_entries.pop()
        entry.master.children  # silence
        # destroy all widgets in the last row
        for widget in self.item_frame.grid_slaves(row=len(self.item_entries)):
            widget.destroy()

    def _item_enter(self, event):
        current = event.widget
        for i, (var, entry) in enumerate(self.item_entries):
            if entry is current:
                if i + 1 < len(self.item_entries):
                    self.item_entries[i + 1][1].focus_set()
                else:
                    self._add_item_row()
                return

    # ── Results section ────────────────────────────────────────────────────

    def _build_results_section(self):
        self.results_frame = ttk.LabelFrame(self, text="Results", padding=10)
        self.results_frame.grid(row=3, column=0, sticky="ew", pady=(12, 0))

        cols = ("item", "pretax", "tax", "total")
        self.tree = ttk.Treeview(
            self.results_frame,
            columns=cols,
            show="headings",
            height=8,
        )
        headers = {"item": "Item", "pretax": "Pre-tax", "tax": "Tax", "total": "Total"}
        widths  = {"item": 60,     "pretax": 100,       "tax": 100,   "total": 110}
        for col in cols:
            self.tree.heading(col, text=headers[col])
            self.tree.column(col, width=widths[col], anchor="e" if col != "item" else "center")

        self.tree.grid(row=0, column=0)

        self.summary_var = tk.StringVar()
        ttk.Label(self.results_frame, textvariable=self.summary_var, font=("", 9, "bold")).grid(
            row=1, column=0, sticky="w", pady=(6, 0)
        )

    # ── Logic ──────────────────────────────────────────────────────────────

    def _calculate(self):
        # Parse items
        items = []
        for i, (var, _) in enumerate(self.item_entries, 1):
            raw = var.get().strip()
            if not raw:
                continue
            try:
                val = float(raw)
                if val < 0:
                    raise ValueError
                items.append(val)
            except ValueError:
                messagebox.showerror("Invalid input", f"Item {i} has an invalid amount.")
                return

        if not items:
            messagebox.showerror("No items", "Please enter at least one item amount.")
            return

        raw_tax = self.tax_var.get().strip()
        try:
            tax = float(raw_tax)
            if tax < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a valid tax amount.")
            return

        subtotal = sum(items)
        tax_rate = (tax / subtotal) * 100 if subtotal else 0
        grand_total = subtotal + tax

        # Populate table
        for row in self.tree.get_children():
            self.tree.delete(row)

        for i, amount in enumerate(items, 1):
            proportion = amount / subtotal
            item_tax = tax * proportion
            item_total = amount + item_tax
            self.tree.insert("", "end", values=(
                f"Item {i}",
                f"${amount:.2f}",
                f"${item_tax:.2f}",
                f"${item_total:.2f}",
            ))

        # Totals row
        self.tree.insert("", "end", values=("TOTAL", f"${subtotal:.2f}", f"${tax:.2f}", f"${grand_total:.2f}"),
                         tags=("total",))
        self.tree.tag_configure("total", font=("", 9, "bold"))

        self.summary_var.set(f"Tax rate: {tax_rate:.2f}%   |   Subtotal: ${subtotal:.2f}   |   Grand total: ${grand_total:.2f}")

    def _clear(self):
        # Reset to one blank item row
        for var, entry in self.item_entries:
            for widget in self.item_frame.grid_slaves():
                widget.destroy()
        self.item_entries.clear()
        self._add_item_row()
        self.tax_var.set("")
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.summary_var.set("")


if __name__ == "__main__":
    app = TaxCalculator()
    app.mainloop()
