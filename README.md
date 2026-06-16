# Expense Tax Splitter

A simple desktop app for splitting a receipt's sales tax across multiple line items. Built for expense sheets where a vendor gives you a single lump-sum tax amount and a subtotal, but you need to know the tax-inclusive total for each individual item.

## The Problem It Solves

Most receipts show:
- A subtotal
- A single total tax amount
- A grand total

When you're filling out an expense sheet with multiple items, you need each item's total *including* its share of the tax. Doing this by hand for several items is tedious. This app handles it instantly.

## How It Works

The app distributes the total tax proportionally across all items based on each item's share of the subtotal.

**Example:**
| Item | Pre-tax | Tax (proportional) | Total |
|------|---------|-------------------|-------|
| Item 1 | $5.00 | $0.50 | $5.50 |
| Item 2 | $10.00 | $1.00 | $11.00 |
| Item 3 | $15.00 | $1.50 | $16.50 |
| **Total** | **$30.00** | **$3.00** | **$33.00** |

In this example, Item 3 is 50% of the subtotal, so it gets 50% of the tax.

## Features

- Add or remove as many items as you need
- Enter the total tax amount from your receipt
- Results table shows pre-tax, tax share, and final total per item
- Displays the effective tax rate percentage
- Press **Enter** while entering items to jump to the next field (or auto-add a new one)
- **Clear All** button to reset for a new receipt

## Requirements

- Python 3.x
- tkinter (included with standard Python installations)

## Usage

```bash
python tax_calculator.py
```

1. Enter each item's pre-tax amount in the item fields
2. Enter the total sales tax from your receipt
3. Click **Calculate** (or press Enter in the tax field)
4. Read off each item's tax-inclusive total from the results table
