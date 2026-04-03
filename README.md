# 🌸 Serenity Spa & Wellness — Booking System

A full Django web app with a luxury UI for client spa bookings.
Data is saved to SQLite3 and can be exported to a beautifully formatted Excel file anytime.

---

## 📦 Setup Instructions

### 1. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 2. Run database migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Start the development server
```bash
python manage.py runserver
```

### 4. Open in browser
- **Client Booking Form:** http://127.0.0.1:8000/
- **Admin Dashboard:**     http://127.0.0.1:8000/dashboard/
- **Export to Excel:**     http://127.0.0.1:8000/export/

---

## 📊 How to Get Bookings in Excel / Google Sheets

### Option A — Direct Excel Download (Easiest)
1. Go to http://127.0.0.1:8000/dashboard/
2. Click the **"⬇ Export Excel"** button
3. A `.xlsx` file downloads instantly with ALL bookings
4. Open in **Microsoft Excel** or upload to **Google Sheets** via *File → Import*

### Option B — Upload to Google Sheets
1. Download the `.xlsx` from the export link
2. Open Google Sheets → **File → Import → Upload**
3. Select the downloaded file → **Replace spreadsheet**
4. All data is now live in Google Sheets!

---

## 📋 Excel File Contents

The exported file contains **3 sheets**:

| Sheet | Contents |
|-------|----------|
| **All Bookings** | Complete data for every client booking with color-coded rows |
| **Summary Dashboard** | Booking counts per service + bar chart |
| **Contact List** | Quick reference with name, email, phone, service |

---

## 🌐 Pages

| URL | Description |
|-----|-------------|
| `/` | Client-facing booking form (4-step wizard) |
| `/dashboard/` | Admin view — see all bookings, export button |
| `/export/` | Direct Excel download link |

---

## 🛠 Tech Stack
- **Backend:** Django 4.2 + SQLite3
- **Excel:** openpyxl (styled, multi-sheet)
- **Frontend:** Vanilla HTML/CSS/JS (no frameworks needed)
- **Fonts:** Cormorant Garamond + Jost (Google Fonts)

---

## 📝 Fields Collected

- Full Name, Email, Phone, Date of Birth, Gender
- Service (10 options), Duration (30/60/90/120 min)
- Preferred Date & Time, Therapist Preference
- Health Conditions, Allergies, Pressure Preference
- Special Requests, Consent

---

> **Every time a client submits the form → data is saved to SQLite3 → visit `/export/` or click Export on the dashboard to get the latest Excel file.**
