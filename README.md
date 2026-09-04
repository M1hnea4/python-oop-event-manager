# 📅 OOP Event Management System - Enterprise Architecture

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OOP](https://img.shields.io/badge/OOP-Strict-4CAF50?style=for-the-badge)
![Architecture](https://img.shields.io/badge/Architecture-Layered_Design-blue8A2BE2?style=for-the-badge)

A complex Object-Oriented Python application built to manage event registrations, applying strict software engineering principles including Layered Architecture, Dependency Injection, and Test-Driven Development (TDD).

### 🏗️ System Architecture
The application is strictly decoupled into distinct layers to ensure high cohesion and low coupling:
* **Domain Layer:** Encapsulates core business entities (`Person`, `Event`, `Registration`).
* **Validation Layer:** Custom validator classes and exception handling (`ValidationException`) isolating data integrity rules from business logic.
* **Repository Layer:** Abstracted data access logic featuring both in-memory and persistent file-based storage (`PersonFileRepository`).
* **Service/Controller Layer (`MainController`):** The Business Logic Layer (BLL) that coordinates repositories and validators to execute complex operations and generate statistical reports.
* **UI Layer:** A console-based interface completely completely agnostic of data storage or business rules.

### ⚙️ Core Engineering Features
* **Dependency Injection:** The application wire-up injects specific repository and validator instances into the controller at runtime, demonstrating Inversion of Control (IoC).
* **Data Persistence:** Implemented custom file I/O operations to maintain state across application sessions without relying on external database engines.
* **Referential Integrity:** The registration system strictly enforces relational constraints between Persons and Events before allowing state mutations.
* **Advanced Analytics:** Dynamic reporting features calculating top 20% most popular events and sorting participant histories using custom lambda functions.

### 🧪 Quality Assurance
Developed using standard Feature-Driven and Test-Driven Development methodologies. The `tests.py` suite explicitly covers domain integrity, validation boundary cases, repository CRUD operations (both memory and file-based), and complex service-level integration testing.
