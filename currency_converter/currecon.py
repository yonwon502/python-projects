import requests
import tkinter as tk    
from tkinter import ttk, messagebox
from datetime import datetime

# Using a free API (ExchangeRate-API) that requires no API key for latest rates
URL = "https://open.er-api.com/v6/latest/USD"

history = []

def get_rates():
    """Fetches latest currency rates relative to USD from a free API."""
    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()
        data = response.json()

        
        if data.get("result") == "success":
            return data.get("rates", {})
        else:
            raise Exception("API returned unsuccessful result")
            
    except Exception as e:
        print(f"[DEBUG] API Fetch failed: {e}")
        # Return fallback rates so the application can start
        return {"USD": 1.0, "EUR": 0.9, "GBP": 0.8, "JPY": 110.0, "ETB": 57.0}


def update_history():
    history_text.delete(1.0, tk.END)
    for record in history:
        amt, f_cur, t_cur, c_amt, dt = record
        history_text.insert(tk.END, f"{dt.strftime('%H:%M:%S')} - {amt} {f_cur} = {c_amt:.2f} {t_cur}\n")

def convert():
    rates = get_rates()
    if not rates:
        return
    
    try: 
        amount = float(amount_entry.get())
        from_cur = from_currency.get()
        to_cur = to_currency.get()

        if from_cur == to_cur:
            converted_amount = amount
            result_label.config(text=f"{amount:.2f} {to_cur}")
        elif from_cur == "USD":
            converted_amount = amount * rates[to_cur]
        elif to_cur == "USD":
            converted_amount = amount / rates[from_cur]
        else:
            converted_amount = amount * rates[to_cur] / rates[from_cur]

        result_label.config(text=f"{converted_amount:.2f} {to_cur}")
        history.append((amount, from_cur, to_cur, converted_amount, datetime.now()))
        update_history()

    except ValueError:
        messagebox.showerror("Error", "Please enter a valid amount")
    except KeyError:
        messagebox.showerror("Error", "Invalid currency")
    except Exception as e:
        messagebox.showerror("Error", f"Conversion failed: {e}")

def clear_history():
    global history
    history = []
    update_history()

# GUI setup
root = tk.Tk()
root.title("Currency Converter")
root.geometry("400x500")
root.resizable(False, False)

# Fetch rates for menus
rates_data = get_rates()
currency_list = list(rates_data.keys()) if rates_data else ["USD", "EUR", "GBP", "JPY", "ETB"]

# Amount input
amount_label = tk.Label(root, text="Amount:")
amount_label.pack(pady=5)
amount_entry = tk.Entry(root)
amount_entry.pack()

# From currency
from_currency = tk.StringVar(root)
from_currency.set("USD")
from_currency_label = tk.Label(root, text="From:")
from_currency_label.pack(pady=5)
from_currency_menu = tk.OptionMenu(root, from_currency, *currency_list)
from_currency_menu.pack()

# To currency
to_currency = tk.StringVar(root)
to_currency.set("USD")
to_currency_label = tk.Label(root, text="To:")
to_currency_label.pack(pady=5)
to_currency_menu = tk.OptionMenu(root, to_currency, *currency_list)
to_currency_menu.pack()

# Convert button
convert_button = tk.Button(root, text="Convert", command=convert)
convert_button.pack(pady=10)

# Result
result_label = tk.Label(root, text="", font=("Helvetica", 12, "bold"))
result_label.pack(pady=5)

# History
history_label = tk.Label(root, text="History:")
history_label.pack()
history_text = tk.Text(root, height=10, width=45)
history_text.pack(pady=5)

# Clear history button
clear_history_button = tk.Button(root, text="Clear History", command=clear_history)
clear_history_button.pack(pady=5)

# Run the app
root.mainloop()