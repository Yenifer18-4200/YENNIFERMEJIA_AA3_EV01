# Software Requirements Specification (SRS)
**Project:** Virtual Store: Customer Order Management System  
**Architecture:** Decoupled RESTful API (FastAPI / SQLite3)  
**Target Portfolio:** SENA Software Analysis and Development (ADSO)

---

## 1. Introduction
This document defines the formal Functional and Non-Functional requirements for the enterprise-grade Virtual Store Backend. It serves as the baseline for system evaluation, automated Pydantic schema validation, and architectural compliance for project defenses.

---

## 2. System Scope
The application manages a modular backend ecosystem capable of orchestrating user profiles, relational product inventories, and multi-table order transactions. It exposes secure, cross-origin endpoints mapped to a localized SQLite relational database, enabling frictionless future frontend consumption.

---

## 3. Functional Requirements (FR)
Functional requirements define the explicit behaviors, endpoints, calculations, and data mutation tasks that the backend ecosystem executes.

| Requirement ID | System Module | Technical Description | Mapped Database Target |
| :--- | :--- | :--- | :--- |
| **FR1** | User Registry | The system shall maintain persistent profiles for users, tracking distinct relational properties including Name, Email, Password, and System Role (`customer`, `admin`). | `User` Table |
| **FR2** | Inventory Ingestion | The system shall allow administrators to register new products via HTTP `POST` requests, establishing records containing Product Name, Unit Price, and Stock Level. | `Product` Table |
| **FR3** | Data Presentation | The system shall query and serve comprehensive, decoupled JSON catalogs of all available inventory metrics via scalable `GET /products` endpoints. | `Product` Table |
| **FR4** | Order Initialization | The system shall process unique order transaction headers, tracking timestamps via Python's `datetime` module and binding them structurally to a ordering `user_id`. | `Order` Table |
| **FR5** | Relational Line Items | The system shall link active transactions to distinct products via a normalized junction table (`Order_items`), evaluating real-time stock deficits before processing deductions. | `Order_items` Table |
| **FR6** | Administrative CRUD | The system shall expose secure administrative HTTP `PUT` and `DELETE` endpoints to dynamic-update catalog pricing, restock items, or purge products from active storage. | `Product` Table |
| **FR7** | Business Intelligence | The system shall compile detailed, cross-referenced business invoices using optimized relational SQL `JOIN` statements across 4 target tables simultaneously via `GET /orders`. | Multi-Table Join |

---

## 4. Non-Functional Requirements (NFR)

### 🔒 NFR1: Data Security, Isolation & Integrity
* **Local Isolation:** The backend configuration shall completely isolate transactional database binaries (`*.db`) locally using project rules (`.gitignore`) to avoid exposing sensitive data on public repositories.
* **Referential Constraints:** The schema script shall enforce relational integrity across tables using explicit `FOREIGN KEY` declarations, linking items securely to parents.
* **Case Normalization:** To prevent data duplication, the product engine shall map input string names to lowercase variants before writing entries to disk.

### 🎨 NFR2: API Usability & Interface Contract
* **Interactive Contract:** The system shall auto-generate an OpenAPI-compliant documentation interface (Swagger UI at `/docs`) for interactive route verification and test pipelines.
* **Defensive Schema Parsing:** The application shall utilize robust Pydantic data models (`BaseModel`) to intercept malformed body structures, negative integers, or missing keys, returning standardized `422 Validation Error` payloads instead of throwing application exceptions.

### ⚡ NFR3: Reliability, Performance & Atomicity
* **Throughput Optimization:** The engine shall execute complex, multi-table structural queries, mutations, and database lookups within a responsive latency window of under 2 seconds.
* **Transactional State Consistency:** The transactional components shall invoke atomic database routines (`conn.commit()`), ensuring any mid-flight operational failure triggers isolation safety to keep table relationships intact.