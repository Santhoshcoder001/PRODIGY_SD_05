import requests
from bs4 import BeautifulSoup
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox

# Function to scrape the website
def scrape_website(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extracting product information (example selectors, update based on the target website)
    products = []
    for item in soup.select('.product-item'):
        name = item.select_one('.product-title').get_text(strip=True)
        price = item.select_one('.product-price').get_text(strip=True)
        rating = item.select_one('.product-rating').get_text(strip=True)
        products.append({'Name': name, 'Price': price, 'Rating': rating})

    return products

# Function to save data to CSV
def save_to_csv(products, filename):
    df = pd.DataFrame(products)
    df.to_csv(filename, index=False)

# Function to start the scraping process
def start_scraping():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Input Error", "Please enter a URL")
        return

    try:
        products = scrape_website(url)
        if products:
            save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if save_path:
                save_to_csv(products, save_path)
                messagebox.showinfo("Success", "Data successfully saved to CSV")
        else:
            messagebox.showinfo("No Data", "No products found on the given URL")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Setting up the GUI
root = tk.Tk()
root.title("Web Scraping Tool")

tk.Label(root, text="Enter e-commerce URL:").grid(row=0, column=0, padx=10, pady=10)
url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=10, pady=10)

scrape_button = tk.Button(root, text="Start Scraping", command=start_scraping)
scrape_button.grid(row=1, column=0, columnspan=2, pady=10)

root.mainloop()
