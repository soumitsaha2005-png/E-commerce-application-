"""
=============================================================
SmartShop – E-Commerce Application
=============================================================
A simplified Amazon-like E-Commerce system built with Tkinter.

Demonstrates real-world usage of DAA concepts:
  • Linear Search  – for product search/filtering
  • Sorting         – for price-based ordering
  • Recommendation  – category + price-range similarity

Author : SmartShop Team
Python : 3.8+
=============================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox
import math

# ───────────────────────────────────────────────────────────
# COLOUR PALETTE  (Amazon-inspired)
# ───────────────────────────────────────────────────────────
COLORS = {
    "bg":            "#EAEDED",   # light grey page background
    "navbar":        "#131921",   # dark navy top bar
    "navbar_text":   "#FFFFFF",
    "accent":        "#FF9900",   # Amazon orange
    "accent_hover":  "#E68A00",
    "card_bg":       "#FFFFFF",
    "card_border":   "#D5D9D9",
    "text_primary":  "#0F1111",
    "text_secondary":"#565959",
    "price":         "#B12704",   # Amazon price red
    "button_blue":   "#FFD814",   # Amazon yellow button
    "button_blue_h": "#F7CA00",
    "cart_bg":       "#FFFFFF",
    "cart_header":   "#232F3E",
    "recommend_bg":  "#FFF8E7",   # warm highlight for recs
    "search_bg":     "#FFFFFF",
    "star":          "#FFA41C",
}

# ───────────────────────────────────────────────────────────
# PRODUCT DATA  (10 products, 4 categories)
# ───────────────────────────────────────────────────────────
PRODUCTS = [
    {"id": 1,  "name": "Wireless Bluetooth Headphones",   "price": 2499,  "category": "Electronics",  "rating": 4.5,
     "desc": "Premium noise-cancelling wireless headphones with 30-hour battery life and deep bass."},
    {"id": 2,  "name": "Smartphone Stand Holder",         "price": 399,   "category": "Electronics",  "rating": 4.2,
     "desc": "Adjustable aluminium phone stand compatible with all smartphones and tablets."},
    {"id": 3,  "name": "Running Shoes – Men",             "price": 1899,  "category": "Fashion",      "rating": 4.7,
     "desc": "Lightweight breathable mesh running shoes with cushioned sole for maximum comfort."},
    {"id": 4,  "name": "Cotton T-Shirt – Unisex",         "price": 499,   "category": "Fashion",      "rating": 4.0,
     "desc": "100% organic cotton crew-neck t-shirt available in multiple colours."},
    {"id": 5,  "name": "Stainless Steel Water Bottle",    "price": 699,   "category": "Home",         "rating": 4.6,
     "desc": "Double-wall vacuum insulated bottle – keeps drinks cold 24 hrs / hot 12 hrs."},
    {"id": 6,  "name": "Non-Stick Frying Pan",            "price": 899,   "category": "Home",         "rating": 4.3,
     "desc": "PFOA-free ceramic coated frying pan with ergonomic heat-resistant handle."},
    {"id": 7,  "name": "Python Programming Book",         "price": 599,   "category": "Books",        "rating": 4.8,
     "desc": "Comprehensive guide to Python 3 – from basics to advanced topics with 200+ exercises."},
    {"id": 8,  "name": "Data Structures & Algorithms",    "price": 749,   "category": "Books",        "rating": 4.9,
     "desc": "Master DSA concepts with clear explanations, diagrams and interview problems."},
    {"id": 9,  "name": "USB-C Charging Cable (3-Pack)",   "price": 349,   "category": "Electronics",  "rating": 4.1,
     "desc": "Braided nylon USB-C cables (1m, 1.5m, 2m) with fast-charge support."},
    {"id": 10, "name": "Desk Organiser – Bamboo",         "price": 1299,  "category": "Home",         "rating": 4.4,
     "desc": "Eco-friendly bamboo desk organiser with compartments for pens, phone and stationery."},
]


# ═══════════════════════════════════════════════════════════
# ALGORITHM IMPLEMENTATIONS
# ═══════════════════════════════════════════════════════════

def linear_search(products, query):
    """
    LINEAR SEARCH  – O(n)
    --------------------------------------------------
    Scans every product and checks if the query string
    appears in the product name OR category (case-insensitive).

    This is the simplest search algorithm and works well
    for small catalogues. For very large datasets a hash-based
    index or trie would be faster, but linear search clearly
    demonstrates the concept.
    --------------------------------------------------
    """
    query = query.strip().lower()
    if not query:
        return list(products)          # empty query → return all

    results = []
    for product in products:           # iterate every item – O(n)
        # Check if query matches name or category
        if (query in product["name"].lower() or
                query in product["category"].lower()):
            results.append(product)
    return results


def sort_products(products, order="low_to_high"):
    """
    SORTING  – Selection Sort variant  – O(n²)
    --------------------------------------------------
    We use a simple selection-sort-style approach so the
    algorithm is easy to understand and demonstrate.

    'order' can be:
        "low_to_high"  → ascending price
        "high_to_low"  → descending price
    --------------------------------------------------
    """
    arr = list(products)               # work on a copy
    n = len(arr)

    for i in range(n):
        selected = i
        for j in range(i + 1, n):      # find min/max in unsorted part
            if order == "low_to_high":
                if arr[j]["price"] < arr[selected]["price"]:
                    selected = j
            else:  # high_to_low
                if arr[j]["price"] > arr[selected]["price"]:
                    selected = j
        arr[i], arr[selected] = arr[selected], arr[i]   # swap

    return arr


def recommend_products(selected_product, all_products, max_results=4):
    """
    RECOMMENDATION SYSTEM  – Similarity Score  – O(n)
    --------------------------------------------------
    For each candidate product we compute a simple
    similarity score based on two factors:

      1. Category Match  → +50 points if same category
      2. Price Proximity → up to 50 points, inversely
         proportional to the absolute price difference

    Products are then sorted by descending score and the
    top 'max_results' are returned.

    This mirrors collaborative / content-based filtering
    used by real e-commerce platforms, simplified for
    classroom demonstration.
    --------------------------------------------------
    """
    scores = []

    for product in all_products:
        if product["id"] == selected_product["id"]:
            continue                     # skip the selected product itself

        score = 0

        # --- Factor 1 : Category match (0 or 50) ---
        if product["category"] == selected_product["category"]:
            score += 50

        # --- Factor 2 : Price proximity (0 – 50) ---
        price_diff = abs(product["price"] - selected_product["price"])
        max_price  = max(p["price"] for p in all_products)
        # Normalise so that identical price gives 50, max diff gives 0
        proximity  = max(0, 1 - price_diff / max_price) * 50
        score += proximity

        scores.append((product, round(score, 1)))

    # Sort by score descending (highest similarity first)
    scores.sort(key=lambda x: x[1], reverse=True)

    return [item[0] for item in scores[:max_results]]


# ═══════════════════════════════════════════════════════════
# MAIN APPLICATION CLASS
# ═══════════════════════════════════════════════════════════

class SmartShopApp:
    """Root application – assembles all UI components."""

    def __init__(self, root):
        self.root = root
        self.root.title("SmartShop – E-Commerce Application")
        self.root.geometry("1200x780")
        self.root.configure(bg=COLORS["bg"])
        self.root.minsize(1000, 600)

        # ── State ──
        self.cart = []                         # list of product dicts
        self.displayed_products = list(PRODUCTS)
        self.selected_product = None

        # ── Build UI ──
        self._build_navbar()
        self._build_body()
        self._render_products(self.displayed_products)

    # ───────────────────────────────────────────────────────
    #  NAVBAR
    # ───────────────────────────────────────────────────────
    def _build_navbar(self):
        nav = tk.Frame(self.root, bg=COLORS["navbar"], height=60)
        nav.pack(fill="x", side="top")
        nav.pack_propagate(False)

        # Logo
        logo = tk.Label(nav, text="🛒 SmartShop", font=("Segoe UI", 18, "bold"),
                        bg=COLORS["navbar"], fg=COLORS["accent"])
        logo.pack(side="left", padx=20)

        # Tagline
        tag = tk.Label(nav, text="DAA-Powered E-Commerce", font=("Segoe UI", 10),
                       bg=COLORS["navbar"], fg="#999999")
        tag.pack(side="left", padx=(0, 30))

        # Search bar
        search_frame = tk.Frame(nav, bg=COLORS["navbar"])
        search_frame.pack(side="left", expand=True, fill="x", padx=10)

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self._on_search)

        search_entry = tk.Entry(search_frame, textvariable=self.search_var,
                                font=("Segoe UI", 12), bg=COLORS["search_bg"],
                                fg=COLORS["text_primary"], relief="flat",
                                insertbackground=COLORS["text_primary"])
        search_entry.pack(side="left", fill="x", expand=True, ipady=6)

        search_btn = tk.Label(search_frame, text=" 🔍 ", font=("Segoe UI", 14),
                              bg=COLORS["accent"], fg="white", cursor="hand2")
        search_btn.pack(side="left")
        search_btn.bind("<Button-1>", lambda e: self._on_search())

        # Sort dropdown
        sort_frame = tk.Frame(nav, bg=COLORS["navbar"])
        sort_frame.pack(side="right", padx=20)

        tk.Label(sort_frame, text="Sort:", font=("Segoe UI", 10),
                 bg=COLORS["navbar"], fg="#CCCCCC").pack(side="left", padx=(0, 5))

        self.sort_var = tk.StringVar(value="Default")
        sort_combo = ttk.Combobox(sort_frame, textvariable=self.sort_var,
                                  values=["Default", "Price: Low to High", "Price: High to Low"],
                                  state="readonly", width=18, font=("Segoe UI", 10))
        sort_combo.pack(side="left")
        sort_combo.bind("<<ComboboxSelected>>", self._on_sort)

        # Cart icon in navbar
        self.cart_label = tk.Label(nav, text="🛒 Cart (0)", font=("Segoe UI", 11, "bold"),
                                   bg=COLORS["navbar"], fg=COLORS["accent"], cursor="hand2")
        self.cart_label.pack(side="right", padx=20)

    # ───────────────────────────────────────────────────────
    #  BODY  (product grid + cart sidebar)
    # ───────────────────────────────────────────────────────
    def _build_body(self):
        body = tk.Frame(self.root, bg=COLORS["bg"])
        body.pack(fill="both", expand=True)

        # --- Left: scrollable product area ---
        left = tk.Frame(body, bg=COLORS["bg"])
        left.pack(side="left", fill="both", expand=True)

        # Section header
        header_frame = tk.Frame(left, bg=COLORS["bg"])
        header_frame.pack(fill="x", padx=15, pady=(12, 0))
        self.section_title = tk.Label(header_frame, text="All Products",
                                      font=("Segoe UI", 14, "bold"),
                                      bg=COLORS["bg"], fg=COLORS["text_primary"])
        self.section_title.pack(side="left")
        self.result_count = tk.Label(header_frame, text="",
                                     font=("Segoe UI", 10),
                                     bg=COLORS["bg"], fg=COLORS["text_secondary"])
        self.result_count.pack(side="left", padx=10)

        # Canvas + scrollbar for scrollable grid
        canvas_frame = tk.Frame(left, bg=COLORS["bg"])
        canvas_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.canvas = tk.Canvas(canvas_frame, bg=COLORS["bg"],
                                highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical",
                                  command=self.canvas.yview)
        self.scroll_frame = tk.Frame(self.canvas, bg=COLORS["bg"])

        self.scroll_frame.bind("<Configure>",
                               lambda e: self.canvas.configure(
                                   scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Mouse-wheel scrolling
        self.canvas.bind_all("<MouseWheel>",
                             lambda e: self.canvas.yview_scroll(
                                 int(-1 * (e.delta / 120)), "units"))

        # --- Recommendation section (below products) ---
        self.rec_outer = tk.Frame(left, bg=COLORS["bg"])
        self.rec_outer.pack(fill="x", padx=15, pady=(0, 10))

        # --- Right: Cart sidebar ---
        right = tk.Frame(body, bg=COLORS["cart_bg"], width=300,
                         relief="flat", bd=0)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        cart_header = tk.Frame(right, bg=COLORS["cart_header"], height=44)
        cart_header.pack(fill="x")
        cart_header.pack_propagate(False)
        tk.Label(cart_header, text="🛒  Shopping Cart",
                 font=("Segoe UI", 13, "bold"),
                 bg=COLORS["cart_header"], fg="white").pack(side="left", padx=14, pady=8)

        # Cart items area (scrollable)
        cart_canvas_frame = tk.Frame(right, bg=COLORS["cart_bg"])
        cart_canvas_frame.pack(fill="both", expand=True)

        self.cart_canvas = tk.Canvas(cart_canvas_frame, bg=COLORS["cart_bg"],
                                     highlightthickness=0)
        cart_sb = ttk.Scrollbar(cart_canvas_frame, orient="vertical",
                                command=self.cart_canvas.yview)
        self.cart_inner = tk.Frame(self.cart_canvas, bg=COLORS["cart_bg"])
        self.cart_inner.bind("<Configure>",
                             lambda e: self.cart_canvas.configure(
                                 scrollregion=self.cart_canvas.bbox("all")))
        self.cart_canvas.create_window((0, 0), window=self.cart_inner, anchor="nw")
        self.cart_canvas.configure(yscrollcommand=cart_sb.set)

        self.cart_canvas.pack(side="left", fill="both", expand=True)
        cart_sb.pack(side="right", fill="y")

        self.cart_empty_label = tk.Label(self.cart_inner,
                                         text="\n\n  Your cart is empty.\n  Browse and add items!",
                                         font=("Segoe UI", 10),
                                         bg=COLORS["cart_bg"],
                                         fg=COLORS["text_secondary"],
                                         justify="left")
        self.cart_empty_label.pack(padx=14, pady=20, anchor="w")

        # Cart footer (total + clear)
        cart_footer = tk.Frame(right, bg="#F7F7F7", height=100)
        cart_footer.pack(fill="x", side="bottom")
        cart_footer.pack_propagate(False)

        sep = tk.Frame(cart_footer, bg=COLORS["card_border"], height=1)
        sep.pack(fill="x")

        self.total_label = tk.Label(cart_footer, text="Total: ₹0",
                                    font=("Segoe UI", 14, "bold"),
                                    bg="#F7F7F7", fg=COLORS["price"])
        self.total_label.pack(pady=(12, 6))

        btn_frame = tk.Frame(cart_footer, bg="#F7F7F7")
        btn_frame.pack()

        checkout_btn = tk.Label(btn_frame, text="  Checkout  ",
                                font=("Segoe UI", 11, "bold"),
                                bg=COLORS["accent"], fg="white",
                                cursor="hand2", padx=12, pady=4)
        checkout_btn.pack(side="left", padx=4)
        checkout_btn.bind("<Button-1>", self._checkout)
        checkout_btn.bind("<Enter>", lambda e: e.widget.config(bg=COLORS["accent_hover"]))
        checkout_btn.bind("<Leave>", lambda e: e.widget.config(bg=COLORS["accent"]))

        clear_btn = tk.Label(btn_frame, text="  Clear  ",
                             font=("Segoe UI", 11),
                             bg="#D5D9D9", fg=COLORS["text_primary"],
                             cursor="hand2", padx=12, pady=4)
        clear_btn.pack(side="left", padx=4)
        clear_btn.bind("<Button-1>", self._clear_cart)
        clear_btn.bind("<Enter>", lambda e: e.widget.config(bg="#C0C4C4"))
        clear_btn.bind("<Leave>", lambda e: e.widget.config(bg="#D5D9D9"))

    # ───────────────────────────────────────────────────────
    #  PRODUCT CARD RENDERING
    # ───────────────────────────────────────────────────────
    def _render_products(self, products):
        """Clears the grid and redraws product cards."""
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        if not products:
            tk.Label(self.scroll_frame, text="No products found.",
                     font=("Segoe UI", 12), bg=COLORS["bg"],
                     fg=COLORS["text_secondary"]).grid(row=0, column=0,
                                                        padx=20, pady=40)
            self.result_count.config(text="(0 results)")
            return

        self.result_count.config(text=f"({len(products)} products)")

        cols = 3  # 3 cards per row
        for idx, product in enumerate(products):
            row, col = divmod(idx, cols)
            self._create_card(self.scroll_frame, product, row, col)

        # Update canvas scroll region after rendering
        self.scroll_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _create_card(self, parent, product, row, col, is_rec=False):
        """Creates a single product card widget."""
        bg = COLORS["recommend_bg"] if is_rec else COLORS["card_bg"]
        border_color = COLORS["accent"] if is_rec else COLORS["card_border"]

        card = tk.Frame(parent, bg=bg, bd=1, relief="solid",
                        highlightbackground=border_color,
                        highlightthickness=2 if is_rec else 1)
        card.grid(row=row, column=col, padx=10, pady=8, sticky="nsew")
        parent.columnconfigure(col, weight=1)

        # Category badge
        cat_colors = {
            "Electronics": "#0066C0",
            "Fashion":     "#C7511F",
            "Home":        "#007600",
            "Books":       "#8B6914",
        }
        cat_bg = cat_colors.get(product["category"], "#555555")
        badge = tk.Label(card, text=f" {product['category']} ",
                         font=("Segoe UI", 8, "bold"), bg=cat_bg, fg="white")
        badge.pack(anchor="w", padx=10, pady=(10, 2))

        if is_rec:
            rec_badge = tk.Label(card, text="⭐ Recommended",
                                 font=("Segoe UI", 8, "bold"),
                                 bg=COLORS["accent"], fg="white")
            rec_badge.pack(anchor="w", padx=10, pady=(2, 0))

        # Product name
        name = tk.Label(card, text=product["name"],
                        font=("Segoe UI", 12, "bold"), bg=bg,
                        fg=COLORS["text_primary"], wraplength=220,
                        justify="left")
        name.pack(anchor="w", padx=10, pady=(6, 2))

        # Stars
        full = int(product["rating"])
        half = 1 if product["rating"] - full >= 0.5 else 0
        stars = "★" * full + "½" * half + "☆" * (5 - full - half)
        rating_label = tk.Label(card, text=f"{stars}  {product['rating']}",
                                font=("Segoe UI", 10), bg=bg,
                                fg=COLORS["star"])
        rating_label.pack(anchor="w", padx=10)

        # Price
        price = tk.Label(card, text=f"₹{product['price']:,}",
                         font=("Segoe UI", 16, "bold"), bg=bg,
                         fg=COLORS["price"])
        price.pack(anchor="w", padx=10, pady=(4, 2))

        # Description snippet
        desc_text = product["desc"][:80] + ("…" if len(product["desc"]) > 80 else "")
        desc = tk.Label(card, text=desc_text, font=("Segoe UI", 9),
                        bg=bg, fg=COLORS["text_secondary"],
                        wraplength=220, justify="left")
        desc.pack(anchor="w", padx=10, pady=(0, 6))

        # Buttons row
        btn_row = tk.Frame(card, bg=bg)
        btn_row.pack(fill="x", padx=10, pady=(0, 10))

        # "View Details" button
        view_btn = tk.Label(btn_row, text="View Details",
                            font=("Segoe UI", 9, "bold"),
                            bg="#E3E6E6", fg=COLORS["text_primary"],
                            cursor="hand2", padx=8, pady=3)
        view_btn.pack(side="left", padx=(0, 6))
        view_btn.bind("<Button-1>", lambda e, p=product: self._view_details(p))
        view_btn.bind("<Enter>", lambda e: e.widget.config(bg="#D5D9D9"))
        view_btn.bind("<Leave>", lambda e: e.widget.config(bg="#E3E6E6"))

        # "Add to Cart" button
        add_btn = tk.Label(btn_row, text="Add to Cart 🛒",
                           font=("Segoe UI", 9, "bold"),
                           bg=COLORS["button_blue"], fg=COLORS["text_primary"],
                           cursor="hand2", padx=8, pady=3)
        add_btn.pack(side="left")
        add_btn.bind("<Button-1>", lambda e, p=product: self._add_to_cart(p))
        add_btn.bind("<Enter>", lambda e: e.widget.config(bg=COLORS["button_blue_h"]))
        add_btn.bind("<Leave>", lambda e: e.widget.config(bg=COLORS["button_blue"]))

    # ───────────────────────────────────────────────────────
    #  SEARCH  (uses linear_search)
    # ───────────────────────────────────────────────────────
    def _on_search(self, *_args):
        query = self.search_var.get()
        # --- Call the Linear Search algorithm ---
        results = linear_search(PRODUCTS, query)

        # Re-apply current sort on search results
        sort_val = self.sort_var.get()
        if sort_val == "Price: Low to High":
            results = sort_products(results, "low_to_high")
        elif sort_val == "Price: High to Low":
            results = sort_products(results, "high_to_low")

        self.displayed_products = results
        self.section_title.config(
            text="Search Results" if query.strip() else "All Products")
        self._render_products(results)

    # ───────────────────────────────────────────────────────
    #  SORT  (uses sort_products)
    # ───────────────────────────────────────────────────────
    def _on_sort(self, _event=None):
        sort_val = self.sort_var.get()

        if sort_val == "Price: Low to High":
            sorted_list = sort_products(self.displayed_products, "low_to_high")
        elif sort_val == "Price: High to Low":
            sorted_list = sort_products(self.displayed_products, "high_to_low")
        else:
            # Default order – re-run search to restore original order
            sorted_list = linear_search(PRODUCTS, self.search_var.get())

        self.displayed_products = sorted_list
        self._render_products(sorted_list)

    # ───────────────────────────────────────────────────────
    #  VIEW DETAILS  +  RECOMMENDATIONS
    # ───────────────────────────────────────────────────────
    def _view_details(self, product):
        """Opens a detail popup and shows recommendations."""
        self.selected_product = product

        # --- Detail popup ---
        popup = tk.Toplevel(self.root)
        popup.title(f"SmartShop – {product['name']}")
        popup.geometry("500x420")
        popup.configure(bg=COLORS["card_bg"])
        popup.resizable(False, False)
        popup.grab_set()

        # Header bar
        hdr = tk.Frame(popup, bg=COLORS["navbar"], height=50)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(hdr, text="📦  Product Details",
                 font=("Segoe UI", 14, "bold"),
                 bg=COLORS["navbar"], fg="white").pack(side="left", padx=16)

        content = tk.Frame(popup, bg=COLORS["card_bg"])
        content.pack(fill="both", expand=True, padx=24, pady=18)

        # Category badge
        cat_colors = {"Electronics": "#0066C0", "Fashion": "#C7511F",
                      "Home": "#007600", "Books": "#8B6914"}
        tk.Label(content, text=f"  {product['category']}  ",
                 font=("Segoe UI", 9, "bold"),
                 bg=cat_colors.get(product["category"], "#555"),
                 fg="white").pack(anchor="w", pady=(0, 8))

        tk.Label(content, text=product["name"],
                 font=("Segoe UI", 18, "bold"),
                 bg=COLORS["card_bg"], fg=COLORS["text_primary"],
                 wraplength=440, justify="left").pack(anchor="w")

        full = int(product["rating"])
        half = 1 if product["rating"] - full >= 0.5 else 0
        stars = "★" * full + "½" * half + "☆" * (5 - full - half)
        tk.Label(content, text=f"{stars}  {product['rating']} / 5.0",
                 font=("Segoe UI", 12), bg=COLORS["card_bg"],
                 fg=COLORS["star"]).pack(anchor="w", pady=(6, 0))

        tk.Label(content, text=f"₹{product['price']:,}",
                 font=("Segoe UI", 26, "bold"),
                 bg=COLORS["card_bg"], fg=COLORS["price"]).pack(anchor="w", pady=(10, 4))

        tk.Label(content, text=product["desc"],
                 font=("Segoe UI", 11), bg=COLORS["card_bg"],
                 fg=COLORS["text_secondary"], wraplength=440,
                 justify="left").pack(anchor="w", pady=(6, 16))

        # Add to cart button in popup
        add_btn = tk.Label(content, text="   Add to Cart 🛒   ",
                           font=("Segoe UI", 12, "bold"),
                           bg=COLORS["button_blue"],
                           fg=COLORS["text_primary"], cursor="hand2",
                           padx=14, pady=6)
        add_btn.pack(anchor="w")
        add_btn.bind("<Button-1>", lambda e, p=product: (self._add_to_cart(p), popup.destroy()))
        add_btn.bind("<Enter>", lambda e: e.widget.config(bg=COLORS["button_blue_h"]))
        add_btn.bind("<Leave>", lambda e: e.widget.config(bg=COLORS["button_blue"]))

        # --- Show recommendations below the product grid ---
        self._show_recommendations(product)

    def _show_recommendations(self, product):
        """Displays recommended products section using the recommendation algorithm."""
        # Clear previous recommendations
        for w in self.rec_outer.winfo_children():
            w.destroy()

        recs = recommend_products(product, PRODUCTS, max_results=4)
        if not recs:
            return

        sep = tk.Frame(self.rec_outer, bg=COLORS["accent"], height=3)
        sep.pack(fill="x", pady=(6, 0))

        tk.Label(self.rec_outer,
                 text=f"✨ Recommended for you  (based on \"{product['name'][:30]}…\")",
                 font=("Segoe UI", 13, "bold"),
                 bg=COLORS["bg"], fg=COLORS["text_primary"]).pack(anchor="w", pady=(8, 4))

        tk.Label(self.rec_outer,
                 text="Products from the same category and similar price range",
                 font=("Segoe UI", 9),
                 bg=COLORS["bg"], fg=COLORS["text_secondary"]).pack(anchor="w", pady=(0, 6))

        rec_grid = tk.Frame(self.rec_outer, bg=COLORS["bg"])
        rec_grid.pack(fill="x")

        for idx, rec in enumerate(recs):
            self._create_card(rec_grid, rec, row=0, col=idx, is_rec=True)

    # ───────────────────────────────────────────────────────
    #  CART OPERATIONS
    # ───────────────────────────────────────────────────────
    def _add_to_cart(self, product):
        self.cart.append(product)
        self._refresh_cart()
        # Quick flash on the navbar cart label
        self.cart_label.config(fg="white")
        self.root.after(200, lambda: self.cart_label.config(fg=COLORS["accent"]))

    def _remove_from_cart(self, index):
        if 0 <= index < len(self.cart):
            self.cart.pop(index)
            self._refresh_cart()

    def _clear_cart(self, _event=None):
        self.cart.clear()
        self._refresh_cart()

    def _checkout(self, _event=None):
        if not self.cart:
            messagebox.showinfo("SmartShop", "Your cart is empty!")
            return
        total = sum(p["price"] for p in self.cart)
        messagebox.showinfo(
            "SmartShop – Checkout",
            f"🎉 Order placed successfully!\n\n"
            f"Items: {len(self.cart)}\n"
            f"Total: ₹{total:,}\n\n"
            f"Thank you for shopping with SmartShop!")
        self.cart.clear()
        self._refresh_cart()

    def _refresh_cart(self):
        """Redraws the cart sidebar."""
        for w in self.cart_inner.winfo_children():
            w.destroy()

        self.cart_label.config(text=f"🛒 Cart ({len(self.cart)})")

        if not self.cart:
            self.cart_empty_label = tk.Label(
                self.cart_inner,
                text="\n\n  Your cart is empty.\n  Browse and add items!",
                font=("Segoe UI", 10), bg=COLORS["cart_bg"],
                fg=COLORS["text_secondary"], justify="left")
            self.cart_empty_label.pack(padx=14, pady=20, anchor="w")
            self.total_label.config(text="Total: ₹0")
            return

        for idx, item in enumerate(self.cart):
            row = tk.Frame(self.cart_inner, bg=COLORS["cart_bg"])
            row.pack(fill="x", padx=10, pady=4)

            # Item info
            info = tk.Frame(row, bg=COLORS["cart_bg"])
            info.pack(side="left", fill="x", expand=True)

            tk.Label(info, text=item["name"],
                     font=("Segoe UI", 9, "bold"), bg=COLORS["cart_bg"],
                     fg=COLORS["text_primary"], wraplength=180,
                     justify="left", anchor="w").pack(anchor="w")
            tk.Label(info, text=f"₹{item['price']:,}",
                     font=("Segoe UI", 9), bg=COLORS["cart_bg"],
                     fg=COLORS["price"]).pack(anchor="w")

            # Remove button
            rm = tk.Label(row, text=" ✕ ", font=("Segoe UI", 10, "bold"),
                          bg="#FFEAEA", fg="#B12704", cursor="hand2")
            rm.pack(side="right", padx=4)
            rm.bind("<Button-1>", lambda e, i=idx: self._remove_from_cart(i))
            rm.bind("<Enter>", lambda e: e.widget.config(bg="#FFD4D4"))
            rm.bind("<Leave>", lambda e: e.widget.config(bg="#FFEAEA"))

            # Separator
            tk.Frame(self.cart_inner, bg=COLORS["card_border"],
                     height=1).pack(fill="x", padx=10)

        total = sum(p["price"] for p in self.cart)
        self.total_label.config(text=f"Total: ₹{total:,}")


# ═══════════════════════════════════════════════════════════
#  ENTRY POINT
# ═══════════════════════════════════════════════════════════
if __name__ == "__main__":
    root = tk.Tk()

    # Apply a modern ttk theme if available
    style = ttk.Style()
    available = style.theme_names()
    for theme in ("clam", "vista", "xpnative", "alt"):
        if theme in available:
            style.theme_use(theme)
            break

    app = SmartShopApp(root)
    root.mainloop()
