# 💰 Finance Management App

A **simple finance management application** written entirely in **Python**, featuring both the **backend** and **frontend**.

---

## 🚀 Features (Work in Progress)

- **Backend**
  - Built with [FastAPI](https://fastapi.tiangolo.com/)  
  - Runs on a **Uvicorn** server  
  - **PostgreSQL** database server for storing:
    - User data  
    - Sessions (stateful server)  
  - REST API endpoints

- **Frontend**
  - Developed with [PyQt6](https://doc.qt.io/qtforpython/)  
  - Provides a **desktop GUI** for interacting with the backend  
  - Currently in **active development**  

---

## 📌 Project Status

- ✅ Basic backend functionality completed + with simple testig
- ⚙️ Frontend (GUI) under development  

---

## 🛠️ Tech Stack

- **Python**
- **FastAPI** + **SQLAlchemy**
- **PostgreSQL**
- **PyQt6**

---

## 📷 Architecture Overview

The backend follows a **4-layer architecture** for clean separation of concerns:

1. **Routes Layer**  
   - Exposes endpoints via **FastAPI**.  
   - Handles HTTP requests/responses and delegates business logic to the service layer.  

2. **Service Layer**  
   - Implements application logic.  
   - Orchestrates workflows, validation, and business rules.  
   - Uses the *Unit of Work* to ensure operations are executed in a transactional context.  

3. **Unit of Work Layer**  
   - Manages **database transactions**.  
   - Ensures atomicity and consistency across multiple operations.  
   - Provides a clear commit/rollback mechanism.  

4. **Repository Layer**  
   - Encapsulates **data access logic**.  
   - Provides a clean interface for querying and persisting entities in **PostgreSQL**.  
   - Keeps SQL/ORM details hidden from higher layers.  

---

MIT License © 2025  


 
