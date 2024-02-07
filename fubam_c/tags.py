from .optHelper import *
# Config:
Performance= True
SEO = True
Accessibility = True

InjectCSS = False
InjectJS = False

MinifyStyleTags = True
MinifyScriptTags = True

# Helpers:
tagIterarions = 0
titlebool = False

if SEO:
    SEOtags = {
        "meta":[{"name":["viewport",True,'<meta name="viewport" content="width=device-width, initial-scale=1.0">']},
        {"name":["description",True,'<meta name="description" content="This is a descriptio with random text to maintain your seo level">']},
        {"http-equiv":["X-UA-Compatible",True,'<meta http-equiv="X-UA-Compatible" content="ie=edge">']},
        {"name":["keywords",True,'<meta name="keywords" content="some,random,keywords">']},
        {"http-equiv":["Content-Type",True,'<meta http-equiv="Content-Type" content="text/html;charset=UTF-8">']}]
       }

def initTags(attributes,body,phyla,closings,*args):
 try:
    global tagIterarions
    if(phyla == "html"):
        body = body
        body += makeSEOtags()
    y = False
    scriptsy = False
    skipper = False
    if phyla == "link":
        href = ""
    if phyla == "script":
        src = ""
    for arg in args:
        if isinstance(arg, dict):
            if(SEO and phyla in SEOtags):
                for key, value in arg.items():
                    attributes += f" {key}=\"{value}\""
                    for t in SEOtags[phyla]:
                        if key in t:
                            if value == t[key][0]:
                                t[key][1] = False
            else:
                for key, value in arg.items():
                    attributes += f" {key}=\"{value}\""
                    if phyla == "img" and not "alt" in  attributes and Accessibility:
                        attributes += f" alt=\"There was an image\""
                    if key == "href":
                        href = value
                    if key == "src":
                        src = value
                    if phyla == "link" and key == "rel":
                        if value == "stylesheet":
                            print(value,href,key)
                            y = True        
                    if phyla == "script":
                        print(value,src,key)
                        scriptsy = True        
        elif isinstance(arg, str) or isinstance(arg,int) or isinstance(arg,float):
            body += f"{cssmin(arg) if phyla == 'style' and MinifyStyleTags else jsmin(arg) if phyla == 'script' and MinifyScriptTags else arg}"
        elif isinstance(arg,list):
            for ar in arg:
                body += f"{cssmin(ar) if phyla == 'style' and MinifyStyleTags else jsmin(ar) if phyla == 'script' and MinifyScriptTags else ar}"
        elif isinstance(arg,iterationSkipper):
            skipper = True
        else:
            TypeError(f"{arg} of type `{type(arg)}` is not useable!")
    if(not skipper):
        tagIterarions += 1
    global InjectCSS
    if(y) and  InjectCSS:
            return "<style>" + (open(href).read() if not MinifyStyleTags else cssmin(open(href).read()))+ "</style>"
    global InjectJS
    if(scriptsy) and  InjectJS:
            return "<script>" + (open(src).read() if not MinifyScriptTags else jsmin(open(src).read()))+ "</script>"
    return f'{"<!DOCTYPE html>" if phyla == "html" and Accessibility else "" }<{phyla}{attributes}>{body}{f"</{phyla}>" if closings else ""}'     
 except Exception as e:
    print(e)
    return "Exception at element " + phyla

def a(*args):
    return initTags( "", "", "a", True,*args)
def abbr(*args):
    return initTags( "", "", "abbr", True,*args)

def address(*args):
    return initTags( "", "", "address", True,*args)
   
def area(*args):
    return initTags( "", "", "area", True,*args)

def article(*args):
    return initTags( "", "", "article", True,*args)
   
def aside(*args):
    return initTags( "", "", "aside", True,*args)
 
def audio(*args):
    return initTags( "", "", "audio", True,*args)
 
def b(*args):
    return initTags( "", "", "b", True,*args)
def base(*args):
    return initTags( "", "", "base", True,*args)

def bdi(*args):
    return initTags( "", "", "bdi", True,*args)
def bdo(*args):
    return initTags( "", "", "bdo", True,*args)
def blockquote(*args):
    return initTags( "", "", "blockquote", True,*args)
   
def body(*args):
    return initTags( "", "", "body", True,*args)

def br(*args):
    return initTags( "", "", "br", False,*args)
def button(*args):
    return initTags( "", "", "button", True,*args)
  
def canvas(*args):
    return initTags( "", "", "canvas", True,*args)
  
def caption(*args):
    return initTags( "", "", "caption", True,*args)
   
def cite(*args):
    return initTags( "", "", "cite", True,*args)

def code(*args):
    return initTags( "", "", "code", True,*args)

def col(*args):
    return initTags( "", "", "col", True,*args)
def colgroup(*args):
    return initTags( "", "", "colgroup", True,*args)
   
def data(*args):
    return initTags( "", "", "data", True,*args)

def datalist(*args):
    return initTags( "", "", "datalist", True,*args)
   
def dd(*args):
    return initTags( "", "", "dd", True,*args)
def details(*args):
    return initTags( "", "", "details", True,*args)
   
def dfn(*args):
    return initTags( "", "", "dfn", True,*args)
def dialog(*args):
    return initTags( "", "", "dialog", True,*args)
  
def div(*args):
    return initTags( "", "", "div", True,*args)
def dl(*args):
    return initTags( "", "", "dl", True,*args)
def dt(*args):
    return initTags( "", "", "dt", True,*args)
def em(*args):
    return initTags( "", "", "em", True,*args)
def embed(*args):
    return initTags( "", "", "embed", True,*args)
 
def fieldset(*args):
    return initTags( "", "", "fieldset", True,*args)
   
def figcaption(*args):
    return initTags( "", "", "figcaption", True,*args)
   
def figure(*args):
    return initTags( "", "", "figure", True,*args)
  
def footer(*args):
    return initTags( "", "", "footer", True,*args)
  
def form(*args):
    return initTags( "", "", "form", True,*args)

def h1(*args):
    return initTags( "", "", "h1", True,*args)
def h2(*args):
    return initTags( "", "", "h2", True,*args)
def h3(*args):
    return initTags( "", "", "h3", True,*args)
def h4(*args):
    return initTags( "", "", "h4", True,*args)
def h5(*args):
    return initTags( "", "", "h5", True,*args)
def h6(*args):
    return initTags( "", "", "h6", True,*args)
def head(*args):
    return initTags( "", "", "head", True,*args,iterationSkipper())

def header(*args):
    return initTags( "", "", "header", True,*args)
  
def hgroup(*args):
    return initTags( "", "", "hgroup", True,*args)
  
def hr(*args):
    return initTags( "", "", "hr", False,*args)
def html(*args):
    return initTags( "", "", "html", True,*args,{"lang":"en"} if Accessibility else "",iterationSkipper())

def i(*args):
    return initTags( "", "", "i", True,*args)
def iframe(*args):
    return initTags( "", "", "iframe", True,*args)
  
def img(*args):
    return initTags( "" if not Performance else " loading=\"lazy\"", "", "img", False,*args)
def inp(*args):
    return initTags( "", "", "input", True,*args)
def ins(*args):
    return initTags( "", "", "ins", True,*args)
def kbd(*args):
    return initTags( "", "", "kbd", True,*args)
def keygen(*args):
    return initTags( "", "", "keygen", True,*args)
  
def label(*args):
    return initTags( "", "", "label", True,*args)
 
def legend(*args):
    return initTags( "", "", "legend", True,*args)
  
def li(*args):
    return initTags( "", "", "li", True,*args)
def link(*args):
    return initTags( "", "", "link", False,*args)
def main(*args):
    return initTags( "", "", "main", True,*args)

def _map(*args):
    return initTags( "", "", "map", True,*args)

def mark(*args):
    return initTags( "", "", "mark", True,*args)

def menu(*args):
    return initTags( "", "", "menu", True,*args)

def menuitem(*args):
    return initTags( "", "", "menuitem", True,*args)
   
def meta(*args):
    return initTags( "", "", "meta", False,*args,iterationSkipper())

def meter(*args):
    return initTags( "", "", "meter", True,*args)
 
def nav(*args):
    return initTags( "", "", "nav", True,*args)
def noscript(*args):
    return initTags( "", "", "noscript", True,*args)
   
def obj(*args):
    return initTags( "", "", "obj", True,*args)
def ol(*args):
    return initTags( "", "", "ol", True,*args)
def optgroup(*args):
    return initTags( "", "", "optgroup", True,*args)
   
def option(*args):
    return initTags( "", "", "option", True,*args)
  
def output(*args):
    return initTags( "", "", "output", True,*args)
  
def p(*args):
    return initTags( "", "", "p", True,*args)
def param(*args):
    return initTags( "", "", "param", True,*args)
 
def picture(*args):
    return initTags( "", "", "picture", True,*args)
   
def pre(*args):
    return initTags( "", "", "pre", True,*args)
def progress(*args):
    return initTags( "", "", "progress", True,*args)
   
def q(*args):
    return initTags( "", "", "q", True,*args)
def rb(*args):
    return initTags( "", "", "rb", True,*args)
def rp(*args):
    return initTags( "", "", "rp", True,*args)
def rt(*args):
    return initTags( "", "", "rt", True,*args)
def rtc(*args):
    return initTags( "", "", "rtc", True,*args)
def ruby(*args):
    return initTags( "", "", "ruby", True,*args)

def s(*args):
    return initTags( "", "", "s", True,*args)
def samp(*args):
    return initTags( "", "", "samp", True,*args)

def script(*args):
    return initTags( "", "", "script", True,*args)
  
def section(*args):
    return initTags( "", "", "section", True,*args)
   
def select(*args):
    return initTags( "", "", "select", True,*args)
  
def small(*args):
    return initTags( "", "", "small", True,*args)
 
def source(*args):
    return initTags( "", "", "source", True,*args)
  
def span(*args):
    return initTags( "", "", "span", True,*args)

def strong(*args):
    return initTags( "", "", "strong", True,*args)
  
def style(*args):
    return initTags( "", "", "style", True,*args)
 
def sub(*args):
    return initTags( "", "", "sub", True,*args)
def summary(*args):
    return initTags( "", "", "summary", True,*args)
   
def sup(*args):
    return initTags( "", "", "sup", True,*args)
def table(*args):
    return initTags( "", "", "table", True,*args)
 
def tbody(*args):
    return initTags( "", "", "tbody", True,*args)
 
def td(*args):
    return initTags( "", "", "td", True,*args)
def template(*args):
    return initTags( "", "", "template", True,*args)
   
def textarea(*args):
    return initTags( "", "", "textarea", True,*args)
   
def tfoot(*args):
    return initTags( "", "", "tfoot", True,*args)
def th(*args):
    return initTags( "", "", "th", True,*args)
def thead(*args):
    return initTags( "", "", "thead", True,*args)
def time(*args):
    return initTags( "", "", "time", True,*args)
def title(*args):
    global titlebool
    titlebool = True
    return initTags( "", "", "title", True,*args,iterationSkipper())
def tr(*args):
    return initTags( "", "", "tr", True,*args)
def track(*args):
    return initTags( "", "", "track", True,*args)
def u(*args):
    return initTags( "", "", "u", True,*args)
def ul(*args):
    return initTags( "", "", "ul", True,*args)
def video(*args):
    return initTags( "", "", "video", True,*args)
def wbr(*args):
    return initTags( "", "", "wbr", True,*args)
def wrapper(*args):
    for arg in args:
        body = ""
        if isinstance(arg, str) or isinstance(arg,int) or isinstance(arg,float):
            body += f"{cssmin(arg)}"
        elif isinstance(arg,list):
            for ar in arg:
                body += f"{cssmin(ar)}"
        else:
            TypeError(f"{arg} of type `{type(arg)}` is not useable!")
    return body
def makeSEOtags():
    returntags  = ""
    for i in SEOtags.keys():
        for attr in SEOtags[i]:
            for obj in attr.values():
                if obj[1]:
                    returntags += obj[2]
    if not titlebool:
        returntags += "<title>Page Title</title>"
    return returntags
