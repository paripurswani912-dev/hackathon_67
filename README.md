# hackathon_67
# koshex
### Inventory Intelligence — Centralized. Real-Time. Effortless.

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat-square)
![Flask](https://img.shields.io/badge/Flask-Backend-lightgrey?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Hackathon%20Build-orange?style=flat-square)

> Built for the hackathon — replacing manual registers, scattered Excel sheets, and fragmented tracking with a single, real-time inventory platform.

---

## What is Koshex?

**Koshex** is a full-stack, modular Inventory Management System (IMS) built with Flask and Python. It gives businesses a centralized hub to manage all stock-related operations — from receiving vendor shipments to dispatching deliveries — with every movement automatically logged in a live stock ledger.

Designed for **Inventory Managers** and **Warehouse Staff**, Koshex supports multi-warehouse environments, real-time KPI dashboards, smart low-stock alerts, and one-click CSV log exports — all wrapped in a branded, interactive UI with your company logo and theme.

---

## Dashboard Preview

> Landing page shows a real-time snapshot of inventory operations with KPI cards, recent operations table, and live stock alerts panel.

---

## Core Features

### 1. Product Management
- Create products with Name, SKU/Code, Category, Unit of Measure, and Initial Stock
- View stock availability per warehouse location
- Set up reordering rules and product categories

### 2. Receipts — Incoming Stock
Used when goods arrive from vendors.
- Create a receipt, add supplier and products
- Input quantities received
- Validate → stock increases automatically
- Example: Receive 50 units of "Steel Rods" → stock +50

### 3. Delivery Orders — Outgoing Stock
Used when stock leaves the warehouse for customers.
- Pick → Pack → Validate workflow
- Validation auto-decrements stock
- Example: Sales order for 10 chairs → Delivery order reduces chairs by 10

### 4. Internal Transfers
Move stock within the company between locations.
- Main Warehouse → Production Floor
- Rack A → Rack B
- Warehouse 1 → Warehouse 2
- Total stock unchanged; location in ledger updated

### 5. Stock Adjustments
Reconcile physical counts against recorded stock.
- Select product and location
- Enter physically counted quantity
- System auto-updates and logs the adjustment with reason

### 6. Dashboard & Smart Alerts
Real-time KPIs on the landing page:
- Total Products in Stock
- Low Stock / Out of Stock Items
- Pending Receipts
- Pending Deliveries
- Internal Transfers Scheduled

Dynamic filters by document type, status, warehouse, and product category.

---

## Inventory Flow — End-to-End Example

```
Step 1 → Receive Goods
  Receipt: 100 kg Steel from vendor
  Stock: +100

Step 2 → Internal Transfer
  Main Store → Production Rack
  Stock total unchanged; location updated in ledger

Step 3 → Deliver Finished Goods
  Delivery Order: 20 kg Steel dispatched
  Stock: -20

Step 4 → Adjust Damaged Items
  3 kg Steel damaged, written off
  Stock: -3  |  Reason logged automatically
```

Every step is immutably written to the **Stock Ledger** and visible under **Move History**.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.x, Flask |
| Database | SQLite / SQLAlchemy |
| Frontend | Jinja2, HTML, CSS, JavaScript |
| Authentication | Session-based login (Flask-Login) |
| Export | CSV log export |
| Branding | Custom logo, company name, theme colors |

---

## Project Structure

```
koshex/
├── app/
│   ├── __init__.py          # App factory
│   ├── models.py            # SQLAlchemy models
│   ├── auth/                # Login & signup
│   ├── dashboard/           # KPI aggregation views
│   ├── products/            # Product CRUD & categories
│   ├── receipts/            # Incoming stock operations
│   ├── delivery/            # Outgoing stock operations
│   ├── transfers/           # Internal warehouse moves
│   ├── adjustments/         # Stock count reconciliation
│   ├── history/             # Full ledger & move history
│   ├── settings/            # Warehouse & profile config
│   ├── exports/             # CSV export logic
│   ├── static/              # CSS, JS, logo assets
│   └── templates/           # Jinja2 HTML templates
├── migrations/              # Flask-Migrate DB migrations
├── requirements.txt
├── .env.example
└── run.py
```

---

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/your-username/koshex.git
cd koshex
```

### 2. Create a virtual environment and install dependencies
```bash
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure environment variables
```bash
cp .env.example .env
# Edit .env — set SECRET_KEY and DATABASE_URI
```

### 4. Initialize the database and run
```bash
flask db upgrade
flask run
```

Open `http://127.0.0.1:5000` in your browser. The first registered account is automatically assigned admin privileges.

---

## Navigation

| Module | Description |
|---|---|
| Dashboard | Real-time KPI snapshot and stock alerts |
| Products | Full catalog with reorder rules |
| Receipts | Log and validate incoming shipments |
| Delivery | Pick, pack, and dispatch outgoing orders |
| Transfers | Move stock between warehouses or locations |
| Adjustments | Reconcile physical counts with system records |
| History | Complete stock ledger and move log |
| Settings | Warehouse configuration and user profile |

---

## Log Export

Export operation logs as CSV directly from the Dashboard or History view.

Exported fields: `Reference ID`, `Type`, `Product`, `Quantity`, `Warehouse`, `Date`, `Status`

Useful for accounting audits, ERP integration, or offline archival.

---

## Branding & Theming

Koshex is built to carry your company's identity:
- Upload your logo via `Settings → Branding`
- Set your company name displayed in the navbar
- Configure primary color palette via CSS variables

```
COMPANY_NAME = "Koshex"
COMPANY_LOGO = /static/assets/logo.png
PRIMARY_COLOR = #2D2B5A
```

---

## Authentication

- Sign up and login with email and password
- Session-based authentication via Flask-Login
- First registered user is auto-assigned admin role
- Profile menu to update name, email, and password

---

## Target Users

- **Inventory Managers** — manage incoming and outgoing stock operations
- **Warehouse Staff** — perform transfers, picking, shelving, and stock counting

---

## License

MIT License — free to use, modify, and distribute.

---

*Koshex — Built at Hackathon 2026*