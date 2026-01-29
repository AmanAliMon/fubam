# Fubam

### The Lightweight Python Frontend Generator

* **Version**: 1.0 Stable Release
* **Release Date**: 29 January 2026
* **Author**: Aman Ali
* **Documentation**: [https://fubam.mdadsolutions.com/docs/](https://fubam.mdadsolutions.com/docs/)

**FUBAM** (Functions-Based Markup for Python) is a lightweight Python library for generating HTML using pure Python. It enables complex UI designs with components, loops, conditional rendering, and automated SEO/performance enhancements.

---

## Table of Contents

- [Fubam](#fubam)
    - [The Lightweight Python Frontend Generator](#the-lightweight-python-frontend-generator)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
    - [Using Git](#using-git)
    - [Importing Fubam](#importing-fubam)
  - [Basic Usage](#basic-usage)
    - [Using Templates](#using-templates)
  - [How Fubam Works](#how-fubam-works)
  - [Templates \& Components](#templates--components)
    - [Components](#components)
    - [Layouts](#layouts)
  - [Loops](#loops)
  - [Conditionals](#conditionals)
  - [SEO, Performance, and Accessibility](#seo-performance-and-accessibility)
    - [SEO](#seo)
    - [Performance](#performance)
    - [Accessibility](#accessibility)
  - [Configuration](#configuration)
  - [Pre-serving Compression](#pre-serving-compression)
  - [CLI Entry Point](#cli-entry-point)
    - [Usage](#usage)
    - [Options](#options)
    - [Examples](#examples)
      - [Compile a single template](#compile-a-single-template)
      - [Compile a directory recursively](#compile-a-directory-recursively)
      - [Compile to a custom output directory](#compile-to-a-custom-output-directory)
      - [Compile with template resources from JSON](#compile-with-template-resources-from-json)
  - [Pros \& Highlights](#pros--highlights)
  - [Advanced Tips](#advanced-tips)

---

## Installation

### Using Git

```bash
git clone https://github.com/amanalimon/fubam.git
```

### Importing Fubam

```python
from fubam import Fubam
```

Fubam functions return plain HTML strings compatible with frameworks like Flask (`return string`) or Django (`HttpResponse(string)`).

---

## Basic Usage

### Using Templates

`templates/page.pmx`:

```python
Export = html(
    head(
        title("My Fubam Project"),
        link({"rel":"stylesheet","href":"bootstrap.css"})
    ),
    body(
        div({"class":"container"}, h1(message))
    )
)
```

Server-side:

```python
from fubam import Fubam

compiler = Fubam(templates_dir="templates")
context = {"message": "Hello, world!"}
return compiler.renderTemplate("page", resources=context)
```

---

## How Fubam Works

* **HTML representation**: Each function corresponds to an HTML tag.
* **Children & Attributes**: `div({"class":"mydiv"}, "Text")` → `<div class="mydiv">Text</div>`.
* **Text Content**: Strings represent text nodes.

```python
Export = p("Fubam is a lightweight Python templating engine")
```

---

## Templates & Components

### Components

Define reusable HTML blocks in a separate file (`components.pmx`):

```python
Footer = footer(
    div("Links"),
    div("Copyright &copy; 2023")
)
```

Use in template:

```python
HTML = wrapper(body("This is a body") , useComponent("Footer")) # `wrapper` is use for combining tags/modules
```

---

### Layouts

Layouts provide a reusable page structure across multiple templates. They define common elements like headers, footers, and main containers, while letting templates inject content into placeholders.

`layout.pmx`:

```python
Export = HTML(
    head(
        title(page_title if "page_title" in globals() else "My Fubam Site"),
        meta(charset="UTF-8")
    ),
    body(
        header(
            h1("Site Header"),
            nav(
                a("Home", href="/"),
                a("About", href="/about")
            )
        ),
        main(__content__),  # Placeholder for page-specific content
        footer(
            p("© 2025 Fubam")
        )
    )
)
```

`template.pmx`:

```python
page_title = "Home Page"
Export = useLayout("layout.pmx", content=wrapper(
    h2("Welcome to Fubam!"),
    p("This page uses a layout for consistent structure.")
))
```

**Notes:**

* `__content__` is where page template content is injected.
* You can define multiple placeholders for flexibility (e.g., `content.var1`, `content.var2`).
* Layouts can use Python logic to dynamically adjust content.

---

## Loops

Dynamic rendering with Python loops:

```python
dbResult = [{"name": "Aman", "age": 17}, {"name": "Lorem", "age": 27}]
return render_pythonMarkup("page", resources={"persons": dbResult})
```

Template:

```python
def card(name, age):
    return div(
        h1(f"Username: {name}"),
        p(f"Age: {age}")
    )

Export = body(
    div([card(p["name"], p["age"]) for p in persons])
)
```

---

## Conditionals

Render content based on a condition:

```python
return render_pythonMarkup("page", resources={"loggedin": loggedIn})
```

Template:

```python
HTML = "<homepage content>" if loggedin else render_pythonMarkup("../templates/login")
```

---

## SEO, Performance, and Accessibility

### SEO

If `SEO=True`:

* Automatic `<title>` tag.
* Meta tags for `viewport`, `description`, `keywords`, `Content-Type`, `X-UA-Compatible`.

### Performance

* Images automatically receive `loading="lazy"`.
* Optional CSS/JS inlining (`InjectCSS`/`InjectJS`).
* Minifies `<style>` and `<script>` tags.

### Accessibility

* Images receive default `alt="There was an image"`.
* Automatic `<!DOCTYPE html>` and `lang="en"` on `<html>`.

---

## Configuration

Default settings:

```python
Performance = True
SEO = True
Accessibility = True
InjectCSS = False
InjectJS = False
MinifyStyleTags = True
MinifyScriptTags = True
```

---

## Pre-serving Compression

```python
compressCSSFile("style.css")                   # outputs style.min.css
compressJSFile("script.js")                    # outputs script.min.js
compressCSSFile("style.css", "dist/main.css")  # custom path
```



## CLI Entry Point

Fubam provides a command-line interface for compiling `.pmx` templates without writing Python code.

### Usage

```bash
python3 -m fubam <files_or_directories> [options]
```

### Options

| Flag                | Description                                  |
| ------------------- | -------------------------------------------- |
| `-r`, `--recursive` | Process directories recursively              |
| `--ext`             | Set output file extension (e.g., `html`)     |
| `--ref`             | Load a JSON file with template resources     |
| `-o`, `--out`       | Set the output directory (default: `./`) |

### Examples

#### Compile a single template

```bash
python3 -m fubam templates/page.pmx --ext=html
```

#### Compile a directory recursively

```bash
python3 -m fubam templates/ -r --ext=html
```

#### Compile to a custom output directory

```bash
python3 -m fubam templates/ -r --ext=html --out=build
```

#### Compile with template resources from JSON

```bash
python3 -m fubam templates/ -r --ext=html --ref=ref.json
```


## Pros & Highlights

* Full Python integration within HTML.
* Lightweight and fast.
* Supports reusable components.
* SEO, accessibility, and performance optimizations included.
* Minimal boilerplate.
* Ideal for rapid prototyping, teaching, and lightweight production.

---

## Advanced Tips

* Use Python string methods (`replace`, `join`, etc.) directly in templates.
* `useComponent()` allows rendering reusable blocks dynamically.

---

**Official Documentation:** [https://fubam.mdadsolutions.com/docs/](https://fubam.mdadsolutions.com/docs/)
