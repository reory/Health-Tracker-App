# Contributing to the Health Tracker App

Thank you for your interest in contributing to the **Health Tracker** application.  
This project is built with **Python**, **Flet**, and a clean layered architecture designed for clarity, maintainability, and future scalability.  
Contributions of all kinds are welcome — bug fixes, new features, documentation, refactoring, and architectural improvements.

---

## 🧱 Project Architecture Overview

### UI Layer (Flet Views)  
**Location:** `screens/`

- Each screen is a pure function returning an `ft.View`.  
- Navigation is handled via callbacks attached to the `TypedPage` object.  
- UI should remain thin — no business logic.

### TypedPage  
**Location:** `ui_types/typed_page.py`

- A subclass of `ft.Page` that exposes dynamic attributes (repos, services, navigation).  
- Screens rely on these attributes instead of global state.

### Services Layer  
**Location:** `services/`

- Contains business logic: scheduling, reminders, notifications, schedule engine, background scheduler.  
- Services must remain UI‑agnostic except `NotificationService`, which interacts with Flet’s snackbar.

### Repositories Layer  
**Location:** `data/`

- Handles all database operations.  
- Each repository is responsible for CRUD operations on a specific model.

### Models + Validators  
**Location:** `models/` and `validators/`

- Models represent domain entities.  
- Validators enforce correctness before saving/updating.

---

## 🛠️ How to Contribute

### 1. Fork the repository  
Clone your fork locally:

```bash
git clone https://github.com/<your-username>/Health-Tracker-App.git
cd Health-Tracker-App
```

### 2. Create a feature branch

```bash
git checkout -b feature/add-medication-filters
```

### 3. Follow the project’s architecture

- UI → Screens only  
- Logic → Services  
- Data → Repositories  
- Validation → Validators  
- No circular imports  
- No business logic inside UI components  

### 4. Run the app locally

```bash
python main.py
```

### 5. Write clean, typed, documented code

- Use type hints everywhere  
- Keep functions small and intentional  
- Add inline comments when logic is non‑obvious  
- Follow existing naming conventions  
- Avoid introducing global state  

### 6. Add or update tests  
If you add logic to services or validators, include tests where possible.

### 7. Commit with clear messages

```bash
git commit -m "Add schedule validation for duplicate times"
```

### 8. Push and open a Pull Request

```bash
git push origin feature/add-medication-filters
```

Then open a PR on GitHub with:

- A clear description  
- Screenshots (if UI changes)  
- Notes on architectural decisions  

---

## 🧪 Code Style & Quality

### Python

- Use type hints everywhere  
- Keep functions pure where possible  
- Avoid side effects in services unless intentional  
- Prefer dependency injection (as used in `main()`)  

### Flet UI

- Views must be deterministic functions  
- Avoid storing state inside UI components  
- Use `page.update()` sparingly and intentionally  
- Keep navigation callbacks on `TypedPage`  

### Database

- Never access SQLite directly from UI  
- Use repositories only  
- Ensure validators run before saving  

---

## 🧩 Adding New Screens

When adding a new screen:

1. Create a file in `screens/`  
2. Write a function returning an `ft.View`  
3. Accept `page: TypedPage` as the only argument  
4. Use `page.\<repo\>` and `page.\<service\>` for data  
5. Register navigation in `main()` if needed  

---

## 🔔 Adding New Services

Services should:

- Contain business logic only  
- Never import UI components  
- Be stateless where possible  
- Use repositories for data access  
- Include docstrings and type hints  

---

## 🧹 Pull Request Checklist

Before submitting a PR, ensure:

- [ ] Code runs without errors  
- [ ] No linter warnings for obvious issues  
- [ ] Type hints are correct  
- [ ] No business logic inside UI  
- [ ] Validators are used where appropriate  
- [ ] New files follow existing naming conventions  
- [ ] PR description explains the change clearly  

---

## 🤝 Code of Conduct

Be respectful, constructive, and collaborative.  
I welcome contributors of all experience levels.

---

## 📬 Need Help?

If you're unsure where to start, feel free to open a **Discussion** or **Issue**.  
I'd be happy to guide you through your first contribution.
