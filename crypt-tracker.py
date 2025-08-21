import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import time
import csv
import os


# Feature 13: Basic Local User Authentication (scaffold)
USERS = {'user1': 'pass1', 'user2': 'pass2'}


class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login")
        self.geometry("300x150")
        self.resizable(False, False)
        ttk.Label(self, text="Username:").pack()
        self.username_entry = ttk.Entry(self)
        self.username_entry.pack()
        ttk.Label(self, text="Password:").pack()
        self.password_entry = ttk.Entry(self, show='*')
        self.password_entry.pack()
        self.login_btn = ttk.Button(self, text="Login", command=self.check_login)
        self.login_btn.pack(pady=10)


    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if USERS.get(username) == password:
            self.destroy()
            app = CryptoTracker(user=username)
            app.protocol("WM_DELETE_WINDOW", app.on_closing)
            app.mainloop()
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password.")


# Main CryptoTracker app
class CryptoTracker(tk.Tk):
    def __init__(self, user=None):
        super().__init__()
        self.title("Cryptocurrency Price Tracker")
        self.geometry("950x700")
        self.user = user


        # Multiple Crypto Selection (Feature 2)
        self.crypto_choices = ["BTC", "ETH", "DOGE", "XMR"]
        self.currency_choices = ["USD", "EUR", "INR"]
        self.selected_cryptos = []
        self.selected_currency = tk.StringVar(value=self.currency_choices[0])


        ttk.Label(self, text="Select Cryptocurrencies:").pack(pady=5)
        self.crypto_listbox = tk.Listbox(self, selectmode='multiple', exportselection=0)
        for c in self.crypto_choices:
            self.crypto_listbox.insert(tk.END, c)
        self.crypto_listbox.selection_set(0)
        self.crypto_listbox.pack()


        ttk.Label(self, text="Select Fiat Currency:").pack(pady=5)
        currency_menu = ttk.Combobox(self, textvariable=self.selected_currency, values=self.currency_choices, state="readonly")
        currency_menu.pack()


        # Chart Type Selection (Feature 12)
        self.chart_type = tk.StringVar(value="Line")
        ttk.Label(self, text="Chart Type:").pack(pady=5)
        chart_menu = ttk.Combobox(self, textvariable=self.chart_type, values=["Line", "Bar"], state="readonly")
        chart_menu.pack()


        # Theme Toggle (Feature 5)
        self.is_dark = tk.BooleanVar(value=False)
        ttk.Checkbutton(self, text="Dark Mode", variable=self.is_dark, command=self.toggle_theme).pack(pady=5)


        # Refresh Rate Control (Feature 8)
        self.refresh_rate = tk.IntVar(value=10)
        ttk.Label(self, text="Refresh Interval (sec):").pack(pady=5)
        ttk.Spinbox(self, from_=5, to=180, textvariable=self.refresh_rate).pack()


        # Price Alert (Feature 3)
        self.alert_enabled = tk.BooleanVar(value=False)
        self.alert_price = tk.DoubleVar(value=0.0)
        ttk.Checkbutton(self, text="Enable Price Alert", variable=self.alert_enabled).pack(pady=5)
        ttk.Label(self, text="Alert if price above:").pack(pady=2)
        ttk.Entry(self, textvariable=self.alert_price).pack(pady=2)


        # Historical Data Button (Feature 1)
        ttk.Button(self, text="Show Historical Chart", command=self.show_historical_chart).pack(pady=5)


        # Data Export (Feature 4)
        ttk.Button(self, text="Export to CSV", command=self.export_csv).pack(pady=5)


        # Market News (Feature 9)
        ttk.Button(self, text="Show Crypto News", command=self.show_news).pack(pady=5)
        self.news_box = tk.Text(self, height=8, wrap='word')
        self.news_box.pack(fill=tk.BOTH, expand=True, pady=5)


        # Matplotlib Figure
        self.fig = Figure(figsize=(7,4), dpi=100)
        self.ax = self.fig.add_subplot(1,1,1)
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


        self.times = []
        self.prices = {}
        self.track_btn = ttk.Button(self, text="Start Tracking", command=self.start_tracking)
        self.track_btn.pack(pady=10)
        self.stop_event = threading.Event()


    def toggle_theme(self):
        if self.is_dark.get():
            self.style = ttk.Style(self)
            self.style.theme_use('clam')
            self.configure(bg='black')
        else:
            self.style = ttk.Style(self)
            self.style.theme_use('default')
            self.configure(bg='white')


    # Feature 2: Modify to fetch multiple cryptos
    def fetch_price(self):
        selected_indices = self.crypto_listbox.curselection()
        cryptos = [self.crypto_choices[i] for i in selected_indices]
        currency = self.selected_currency.get()
        prices = {}
        for symbol in cryptos:
            url = f"https://min-api.cryptocompare.com/data/price?fsym={symbol}&tsyms={currency}"
            try:
                response = requests.get(url).json()
                prices[symbol] = float(response[currency])
            except Exception as e:
                print(f"Error fetching {symbol}:", e)
                prices[symbol] = None
        return prices


    # Feature 12: Chart type selection
    def update_plot(self):
        self.ax.clear()
        for symbol, price_list in self.prices.items():
            if self.chart_type.get() == "Bar":
                self.ax.bar(self.times, price_list, label=symbol)
            else:
                self.ax.plot(self.times, price_list, marker='o', label=symbol)
        self.ax.set_title("Crypto Prices")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel(f"Price in {self.selected_currency.get()}")
        self.ax.legend()
        self.fig.autofmt_xdate()
        self.canvas.draw()


    # Feature 3: Alert logic
    def check_alert(self, prices):
        if self.alert_enabled.get():
            for symbol, price in prices.items():
                if price and price > self.alert_price.get():
                    messagebox.showinfo("Price Alert", f"{symbol} price crossed {self.alert_price.get()}!")


    def track_prices(self):
        self.times = []
        self.prices = {c: [] for c in self.crypto_choices}
        while not self.stop_event.is_set():
            prices = self.fetch_price()
            self.check_alert(prices)  # Feature 3
            current_time = datetime.now().strftime("%H:%M:%S")
            self.times.append(current_time)
            for symbol in prices:
                self.prices[symbol].append(prices[symbol])
            self.update_plot()
            time.sleep(self.refresh_rate.get())


    def start_tracking(self):
        self.stop_event.clear()
        self.track_btn.config(state=tk.DISABLED)
        track_thread = threading.Thread(target=self.track_prices, daemon=True)
        track_thread.start()


    def show_historical_chart(self):
        # Feature 1: Example for one crypto, can be extended for multiple
        selected_indices = self.crypto_listbox.curselection()
        if not selected_indices:
            messagebox.showerror("Error", "Select at least one cryptocurrency.")
            return
        symbol = self.crypto_choices[selected_indices[0]]
        currency = self.selected_currency.get()
        url = f"https://min-api.cryptocompare.com/data/v2/histoday?fsym={symbol}&tsym={currency}&limit=30"
        try:
            response = requests.get(url).json()
            days = [datetime.fromtimestamp(d['time']).strftime('%d/%m') for d in response['Data']['Data']]
            prices = [d['close'] for d in response['Data']['Data']]
            plt.figure(figsize=(10,5))
            plt.plot(days, prices, marker='o', color='orange', label="daily close")
            plt.title(f"{symbol} Historical Prices")
            plt.xlabel("Date")
            plt.ylabel(f"Price in {currency}")
            plt.xticks(rotation=45)
            plt.legend()
            plt.tight_layout()
            plt.show()
        except Exception as e:
            messagebox.showerror("Error", f"Could not fetch historical data: {e}")


    def export_csv(self):
        file = filedialog.asksaveasfilename(defaultextension=".csv")
        if not file:
            return
        try:
            with open(file, 'w', newline='') as f:
                writer = csv.writer(f)
                header = ['Time'] + self.crypto_choices
                writer.writerow(header)
                for i in range(len(self.times)):
                    row = [self.times[i]]
                    for symbol in self.crypto_choices:
                        price_list = self.prices.get(symbol, [])
                        row.append(price_list[i] if i < len(price_list) else "")
                    writer.writerow(row)
            messagebox.showinfo("Export", f"Data exported to {file}")
        except Exception as e:
            messagebox.showerror("Export Failed", str(e))


    def show_news(self):
        # Feature 9: Fetch news headlines (example using CryptoCompare)
        url = 'https://min-api.cryptocompare.com/data/v2/news/?lang=EN'
        try:
            response = requests.get(url).json()
            news_list = response['Data'][:10]  # Show latest 10
            news_text = ""
            for news in news_list:
                news_text += f"Title: {news['title']}\n{news['body']}\nURL: {news['url']}\n\n"
            self.news_box.delete('1.0', tk.END)
            self.news_box.insert(tk.END, news_text)
        except Exception as e:
            self.news_box.insert(tk.END, f"Error fetching news: {e}")


    def on_closing(self):
        self.stop_event.set()
        self.destroy()


if __name__ == "__main__":
    login = LoginWindow()
    login.mainloop()



