import csv

from budgetbuddy.core.models import Income, Expense


def export_profile_to_csv(profile, path):
    """
    Export all transactions in a profile to a CSV file.

    Columns: date, amount, category, description, type
    """
    try:
        with open(path, "w", newline="", encoding="utf-8") as f:
            fieldnames = ["date", "amount", "category", "description", "type"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for tx in profile.transactions:
                writer.writerow({
                    "date": tx.date,
                    "amount": tx.amount,
                    "category": tx.category,
                    "description": tx.description,
                    "type": tx.get_type(),  # "income" or "expense"
                })
    except OSError as e:
        # Handle file write errors gracefully (e.g. permission denied, disk full)
        print(f"Error: could not write CSV file '{path}': {e}")


def import_transactions_from_csv(profile, path):
    """
    Load transactions from a CSV file into a profile.

    Lines with invalid numeric amounts are skipped with a warning.
    """
    try:
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Safely parse amount
                try:
                    amount = float(row.get("amount", ""))
                except (TypeError, ValueError):
                    print(f"Warning: skipping row with invalid amount: {row}")
                    continue

                tx_type = (row.get("type") or "").lower()
                date = row.get("date", "")
                category = row.get("category", "")
                description = row.get("description", "")

                if tx_type == "income":
                    tx = Income(date, amount, category, description)
                else:
                    # Treat anything else as an expense
                    tx = Expense(date, amount, category, description)

                profile.add_transaction(tx)

    except FileNotFoundError:
        print(f"Error: CSV file '{path}' not found.")
    except OSError as e:
        print(f"Error: could not read CSV file '{path}': {e}")
