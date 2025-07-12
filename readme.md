# Fubam

### 🧩 Best Python Frontend Generator — Lightweight, Fast & Pure Python

- **Version**: 0.1.0 (Stable)
- **Release**: 12 July 2025  
- **Author**: Aman Ali  
- **License**: MIT  

**Fubam** — *Functions-based Markup for Python* — is a minimal, fast, and flexible HTML frontend builder using only Python.  
It supports layouts, components, conditionals, and SEO optimizations — **without writing a single line of raw HTML.**

---

## 🔧 Setup

### 📦 Installation

```bash
git clone https://github.com/DeveloperAmanAli/fubam.git
````

> Fubam is framework-independent and works with **Flask**, **Django**, or **any Python web server**.

---

## ⚙️ Usage

### Basic Folder Structure

```
project/
│
├── templates/
│   ├── layout.pmx
│   ├── page.pmx
│   └── component.pmx
├── main.py
└── fubam/
```

---

### `main.py`

```python
import fubam
fubam = fubam.Fubam(template_dir="./templates", SEO=True, Accessibility=True)

output = fubam.compile("page", resources={"username": "Aman", "time": "4:05 PM"})
print(output)
```

---

### `layout.pmx`

```python
Export = html(
    head(title("Layout File")),
    body(
        div({"class": "container"},
            __extend__,  # Inject child page here
            h6(_time)
        )
    )
)
```

---

### `components.pmx`

```python
Export = div(
    h4("Reusable Footer Component"),
    p("© 2025 Fubam Inc.")
)
```

---

### `page.pmx`

```python
p = div(
    h2(f"Hello, {username}"),
    useComponent("components"),  # Imported component
    img({"src": "/profile.png"})
)

Export = useLayout("layout", wrapper(p), resources={"_time": time})
```

---

## 🧠 How It Works

Fubam templates are **just Python files** that use `fubam`'s built-in tag functions (`div()`, `p()`, `img()`...).

Fubam will:

* Parse your `.pmx` file
* Build a complete HTML string
* Inject SEO/Accessibility/meta/layout enhancements (based on config)

---

## 🧪 Template Syntax Basics

| Concept      | HTML                     | Fubam Equivalent                     |
| ------------ | ------------------------ | ------------------------------------ |
| Tag          | `<div></div>`            | `div()`                              |
| Attribute    | `<div class="box">`      | `div({"class": "box"})`              |
| Nesting      | `<div><h1>Hi</h1></div>` | `div(h1("Hi"))`                      |
| Text Content | `<p>Hello</p>`           | `p("Hello")`                         |
| Loops        | —                        | `[div(user.name) for user in users]` |
| Conditionals | —                        | `HTML = comp1 if cond else comp2`    |

---

## ⚡ Features

* 🔁 Component-based structure with `useComponent`
* 🧱 Layout system with `useLayout`
* 🧠 Full Python logic (loops, conditionals, variables)
* 🔍 Built-in SEO tag injection (title, meta)
* 🌐 Accessibility enhancements (alt, doctype, lang)
* 🚀 JS/CSS auto inlining (optional)
* 🧼 Minification for styles/scripts (optional)
* 📁 Static pre-compilers: `compressJSFile()` & `compressCSSFile()`

---

## 🧩 Advanced: Components

`components.py`:

```python
Footer = footer(
    div("Links Section"),
    div("© 2024 Fubam Inc.")
)
```

In your page:

```python
comp = useComponent("component")
Export = body(
    div("Main Content"),
    comp
)
```

---

## 🧪 Loops Example

```python
def userCard(name, age):
    return div(
        h2(f"Name: {name}"),
        p(f"Age: {age}")
    )

Export = div(
    [userCard(p["name"], p["age"]) for p in persons]
)
```

---

## 🔄 Conditionals Example

```python
Export = page_content if loggedin else render_component("login")
```

---

## 🌟 SEO & Performance

### SEO Mode (`SEO=True`)

* Adds `<title>` if missing
* Injects standard SEO meta tags:

  * `viewport`, `description`, `keywords`, `charset`, `X-UA-Compatible`

### Accessibility Mode (`Accessibility=True`)

* Adds `alt="..."` to images
* Forces `<!DOCTYPE html>`
* Adds `lang="en"` to `<html>`

### Performance Mode (`Performance=True`)

* Adds `loading="lazy"` to `<img>` by default

---

## 📦 Static Minification

Fubam includes tools to **minify CSS and JS** before deployment.

```python
compressCSSFile("style.css")
compressJSFile("script.js")
```

Output will be:

* `style.min.css`
* `script.min.js`

You can also pass custom output paths.

---

## ⚙️ Default Configs

```python
Fubam(
  template_dir="templates",
  SEO=True,
  Accessibility=True,
  Performance=True,
  InjectCSS=False,
  InjectJS=False,
  MinifyStyleTags=True,
  MinifyScriptTags=True
)
```

---

## ✅ Precautions
* `<input />` is defined as `inp()` not `input()`
* ⚠️ Do **not** use `input()` or interactive logic in `.pmx` templates.
* Always define `Export = ...` in your templates.
* You can use `Export = ...` in components if they’re used with `useComponent`.

---

## ❤️ Why Fubam?

* Zero learning curve if you know Python
* Full control: loops, conditions, variables
* Clean & structured frontend without markup
* No external dependencies
* Works anywhere Python runs

---

## 🔗 Links

* [Homepage](https://amanalimon.github.io/fubam)
* [Repository](https://github.com/amanalimon/fubam)

---

## 📜 License

[MIT License](LICENSE) — © Aman Ali

```