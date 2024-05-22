# Fubam
### Best python frontend generator 

- **Version** : 1.3 stable release
- **Release** : 05 February 2024
- **Author** : Aman Ali

FUBAM: Functions based markup for python is a ligth weight python library, which helps you make complex design in pure python even with components!

# Setup
## Installation
### Using git
```bash
$ git clone https://github.com/DeveloperAmanAli/fubam.git
```

## Server Config
Import the module first!
```python
from fubam import *
```
Return the **HTML**


Render pmx for a route "x"
```python
return html(
    head(
        title("titlefor fubamproject"),
        link({"rel":"stylesheet","href":"bootstrap.css"})
        ),
    body(
        div({"class":"container"},h1("Hello, world!"))
    )
    )
```

Or use template

```python
context = {'message':"Hello, world!"}
return render_pythonMarkup("page",resources=context)
```
In `templates/page.pmx`

```python

from fubam import *

HTML = html(
    head(
        title("titlefor fubamproject"),
        link({"rel":"stylesheet","href":"bootstrap.css"})
        ),
    body(
        div({"class":"container"},h1(message))
    )
    )
```




### __Note!__  Everything possible in python is possible here. 
### __Precaution!__  Never use input function in pmx file.

Before we go on tutorials first we'll learn the way how fubam works!

## Working
When you render a fubam template or call some fubam functions, it returns a string, in normal frameworks like django and flask. There are different logics, as flask ask for a string on a route, whereas django asks for a httpResponse, which takes a string argument. So, in both cases, fubam is able to work with as it returns a simple python string!
### How to write a template
When you write a .pmx template with fubam actually you're writting simple python with some extra functions.
#### Only two things for boilerplate

1. Write
```python
 from fubam import *
```
2. secondly we must need to declare a HTML variable, which contains the desired fubam code, e.g
```python
from fubam import *
HTML = html(
        head(
            title("Title")
        ),
        body(
            div({"class":"container"},
                h1(
                    "Success"
                )
            )
        )
)
```

# Tutorials
## Comparision with normal HTML
In HTML most common terminologies are
- Tag
- Children Tags
- Attribute
- Content 

### Tag
In HTML `<div></div>` is a tag, but in fubam `div()` is a tag.
### Children Tags
Nothing new just `div(div())` for `<div><div></div></div>`
## Attribute
`<div class="mydiv"></div>` in this code `class="mydiv"` is an attribute whereas, in fubam `div({"class":"mydiv"})` is a tag with an class attribute!
## __Note!__ in fubam tags, between everything commas "," are used for sepration!
e.g div({"tag":"tags"},div("another tag"),"Text")


### Content
In fubam "" are used to describe text nodes!
**HTML**
```HTML
<p>Fubam is a good templating engine</p>
```
**Fubam-Python equivalent**
```python
HTML = p(
    "Fubam is a good templating engine"
)
```
You can also use
```python
HTML = '<p>Fubam is a good templating engine</p>'
```
# Pros of fubam
- Provides all powers of python within HTML code generation.

- Decrease the file size more than you can imagine.

- Free
- Supports HTML within '' (quotes)
- Very light framework!
- Provides a good command over SEO and performance
- Significantly fast
- Provides code reusibilty

# Tutorials again

As, fubam use builtin string you can use each string method, you can also methods like replace, join, e.t.c.
## Tricks to blow your mind
### Components
components.py
```python
Footer = footer(
    div(
        "links"
    ),
    div(
        "copyrigth &copy; 2023"
    )
)
```

page.pmx
```python
from fubam import *
import components as comp
HTML = body(
    "This is a body"
) + footer
```
**conclusion:** Reuseable code using variables like components

### loops
Suppose with a server we fetch some persons or services with server and then render it with fubam
Server
```python
dbResult = [{"name":"Aman","age":"17"},{"name":"Lorem","age":"27"},{"name":"someone","age":"12"}]

return render_pythonMarkup("page", resources={"persons":dbResult})
```
Then in page
```python
from fubam import *
def card(name,age):
    return div(
        h1(
            f"Username: {name}"
        ),
        p(
            f'age: {age}'
        )
    )

HTML = body(
    div(
        [card(p.name,p.age) for p in persons]
    )
)
```
**conclusion:** Loops support as an example of python integrity

### Conditional operations
Suppose a home page, when shows the index page else asks for login
```python
return render_pythonMarkup("page", resources={"loggedin":loggedIn})
```
Then in page, This will show login page content
```python
from fubam import *
HTML = <page content> if loggedin else render_pythonMarkup("../templates/login") # if login.pmx in same dir
```
This will redirect to login page
Server
```python
    return render_pythonMarkup("indexpage", resources={"redirect":redirect})
```
Index page
```python
from fubam import *
HTML = <page content> if loggedin else redirect("login") # flask server method redirect is used, used what your respective server provides
```
**Conclusion:** Fubam is best!

## Component Files
Another good approach of rendering dynamic HTML is using *render_component* function.
It takes a relative to cwd (current working directory) and render the file as a single component, there is also a optional resources arguments. Returns the main HTML variable.

# SEO and Performance updates
## ``if SEO is True``
To boost your SEO within the time of site development fubam will automatically handle SEO and maintain your site's score! Let's have a closer look what you'll if SEO is turned on:
- Title tag "Page Title" will automatically added
- These SEO opt tags will be added 
    1. ``<meta name="viewport" content="width=device-width, initial-scale=1.0">``
    2. ``<meta name="description" content="This is a descriptio with random text to maintain your seo level">``
    3. ``<meta http-equiv="X-UA-Compatible" content="ie=edge">``
    4. ``<meta name="keywords" content="some,random,keywords">``
    5. ``<meta http-equiv="Content-Type" content="text/html;charset=UTF-8">``

## ``if Performance``

- Images will automatically get lazy loading attribute

## ``if Accessibility``

- Images will have alt attribute with content "There was an image"
- ``<!DOCTYPE html>`` will be the start of the code so browsers can easily understood the HTML version 5 also if you don't wrote it on the code
- lang en attr is added onto html tag
## Sub Performance features
## InjectCSS & InjectJS
 If enabled will assert the content of your CSS/JS file into HTML code and minimizes the requests
## MinifyStyleTags & MinifyScriptTags
This features is built to minize the code inside Style/Script tag and save request size
# Config
### **By default these is the config**

- Performance= True
- SEO = True
- Accessibility = True
- InjectCSS = False
- InjectJS = False
- MinifyStyleTags = True
- MinifyScriptTags = True


# Pre - serving compression
As fubam uses cssmin and rjsmin libraries you can compress your CSS/JS files from fubam.

```python
compressCSSFile("style.css")
compressJSFile("script.js")
```
The first function will in result make a file with name style.min.css and the other function will outputs a file with name script.min.js within the same directory you can specify directory and name as an argument e.g.

```python
compressCSSFile("style.css","dist/main.css")
```
