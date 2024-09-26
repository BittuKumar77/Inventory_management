# Inventory Management System API


## **Project Setup Instructions**

### **1. Clone the Repository**

git clone <your-repo-url>
cd inventory-management-system

python -m venv venv
source venv/bin/activate   # For Linux/macOS
venv\Scripts\activate      # For Windows

pip install -r requirements.txt

psql -U postgres
CREATE DATABASE inventory_db;
\q
