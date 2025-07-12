import os
from .optHelper import *

class iterationSkipper:
    def __init__(self):
        pass


class Fubam:
    def __init__(
        self,
        template_dir="templates",
        *,
        SEO=False,
        Accessibility=False,
        Performance=False,
        InjectCSS=False,
        InjectJS=False,
        MinifyStyleTags=True,
        MinifyScriptTags=True,
    ):
        # Template rendering
        self.FUBAM_TEMPLATES_DIR = template_dir
        self.titlebool = False
        # Optimization settings
        self.SEO = SEO
        self.Accessibility = Accessibility
        self.Performance = Performance

        self.InjectCSS = InjectCSS
        self.InjectJS = InjectJS
        self.MinifyStyleTags = MinifyStyleTags
        self.MinifyScriptTags = MinifyScriptTags

        self.SEOtags = {
            "meta": [
                {
                    "name": [
                        "viewport",
                        True,
                        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
                    ]
                },
                {
                    "name": [
                        "description",
                        True,
                        '<meta name="description" content="Default SEO Description">',
                    ]
                },
                {
                    "http-equiv": [
                        "X-UA-Compatible",
                        True,
                        '<meta http-equiv="X-UA-Compatible" content="ie=edge">',
                    ]
                },
                {
                    "name": [
                        "keywords",
                        True,
                        '<meta name="keywords" content="default,keywords,here">',
                    ]
                },
                {
                    "http-equiv": [
                        "Content-Type",
                        True,
                        '<meta http-equiv="Content-Type" content="text/html;charset=UTF-8">',
                    ]
                },
            ]
        }



    def makeSEOtags(self):
        if not self.SEO:
            return ""  # <-- Nothing is injected if SEO is disabled
    
        __tags = ""
        for tagtype in self.SEOtags:
            for entry in self.SEOtags[tagtype]:
                for rule in entry.values():
                    if rule[1]:
                        __tags += rule[2]
        if not self.titlebool:
            __tags += "<title>Page Title</title>"
        return __tags


    def initTags(self, attributes, body, phyla, closings, *args):
        tagIterarions = 0
        try:
            if phyla == "html":
                body += self.makeSEOtags()

            y = False
            scriptsy = False
            skipper = False
            href = ""
            src = ""

            for arg in args:
                if isinstance(arg, dict):
                    if self.SEO and phyla in self.SEOtags:
                        for key, value in arg.items():
                            attributes += f' {key}="{value}"'
                            for t in self.SEOtags[phyla]:
                                if key in t and value == t[key][0]:
                                    t[key][1] = False
                    else:
                        for key, value in arg.items():
                            attributes += f' {key}="{value}"'
                            if (
                                phyla == "img"
                                and "alt" not in attributes
                                and self.Accessibility
                            ):
                                attributes += ' alt="There was an image"'
                            if key == "href":
                                href = value
                            if key == "src":
                                src = value
                            if (
                                phyla == "link"
                                and key == "rel"
                                and value == "stylesheet"
                            ):
                                y = True
                            if phyla == "script" and key == "src":
                                scriptsy = True

                elif isinstance(arg, (str, int, float)):
                     if phyla == "style" and self.MinifyStyleTags:
                         body += cssmin(str(arg))
                     elif phyla == "script" and self.MinifyScriptTags:
                         body += jsmin(str(arg))
                     else:
                        body += str(arg)

                elif isinstance(arg, list):
                    for ar in arg:
                             if phyla == "style" and self.MinifyStyleTags:
                                 body += cssmin(str(ar))
                             elif phyla == "script" and self.MinifyScriptTags:
                                 body += jsmin(str(ar))
                             else:
                               body += str(ar)

                elif isinstance(arg, iterationSkipper):
                    skipper = True

                else:
                    raise TypeError(f"{arg} of type `{type(arg)}` is not usable!")

            if not skipper:
                tagIterarions += 1

            if y and self.InjectCSS:
                 with open(href) as f:
                     content = f.read()
                 return f"<style>{cssmin(content) if self.MinifyStyleTags else content}</style>"

            if scriptsy and self.InjectJS:
                with open(src) as f:
                     content = f.read()
                return f"<script>{jsmin(content) if self.MinifyScriptTags else content}</script>"

            return (
                f'{"<!DOCTYPE html>" if phyla == "html" and self.Accessibility else ""}'
                f"<{phyla}{attributes}{f'' if closings else '/'}>{body if closings else ''}{f'</{phyla}>' if closings else ''}"
            )

        except Exception as e:
            print(e)
            return f"Exception at element <{phyla}>"
    
    def tags(self):
        return {
            "a" : lambda *args: self.initTags( "", "", "a", True,*args),
            "abbr" : lambda *args: self.initTags( "", "", "abbr", True,*args),

            "address" : lambda *args: self.initTags( "", "", "address", True,*args),
   
            "area" : lambda *args: self.initTags( "", "", "area", True,*args),

            "article" : lambda *args: self.initTags( "", "", "article", True,*args),
   
            "aside" : lambda *args: self.initTags( "", "", "aside", True,*args),
 
            "audio" : lambda *args: self.initTags( "", "", "audio", True,*args),
 
            "b" : lambda *args: self.initTags( "", "", "b", True,*args),
            "base" : lambda *args: self.initTags( "", "", "base", True,*args),

            "bdi" : lambda *args: self.initTags( "", "", "bdi", True,*args),
            "bdo" : lambda *args: self.initTags( "", "", "bdo", True,*args),
            "blockquote" : lambda *args: self.initTags( "", "", "blockquote", True,*args),
   
            "body" : lambda *args: self.initTags( "", "", "body", True,*args),

            "br" : lambda *args: self.initTags( "", "", "br", False,*args),
            "button" : lambda *args: self.initTags( "", "", "button", True,*args),
  
            "canvas" : lambda *args: self.initTags( "", "", "canvas", True,*args),
  
            "caption" : lambda *args: self.initTags( "", "", "caption", True,*args),
   
            "cite" : lambda *args: self.initTags( "", "", "cite", True,*args),

            "code" : lambda *args: self.initTags( "", "", "code", True,*args),

            "col" : lambda *args: self.initTags( "", "", "col", True,*args),
            "colgroup" : lambda *args: self.initTags( "", "", "colgroup", True,*args),
   
            "data" : lambda *args: self.initTags( "", "", "data", True,*args),

            "datalist" : lambda *args: self.initTags( "", "", "datalist", True,*args),
   
            "dd" : lambda *args: self.initTags( "", "", "dd", True,*args),
            "details" : lambda *args: self.initTags( "", "", "details", True,*args),
   
            "dfn" : lambda *args: self.initTags( "", "", "dfn", True,*args),
            "dialog" : lambda *args: self.initTags( "", "", "dialog", True,*args),
  
            "div" : lambda *args: self.initTags( "", "", "div", True,*args),
            "dl" : lambda *args: self.initTags( "", "", "dl", True,*args),
            "dt" : lambda *args: self.initTags( "", "", "dt", True,*args),
            "em" : lambda *args: self.initTags( "", "", "em", True,*args),
            "embed" : lambda *args: self.initTags( "", "", "embed", True,*args),
 
            "fieldset" : lambda *args: self.initTags( "", "", "fieldset", True,*args),
   
            "figcaption" : lambda *args: self.initTags( "", "", "figcaption", True,*args),
   
            "figure" : lambda *args: self.initTags( "", "", "figure", True,*args),
  
            "footer" : lambda *args: self.initTags( "", "", "footer", True,*args),
  
            "form" : lambda *args: self.initTags( "", "", "form", True,*args),

            "h1" : lambda *args: self.initTags( "", "", "h1", True,*args),
            "h2" : lambda *args: self.initTags( "", "", "h2", True,*args),
            "h3" : lambda *args: self.initTags( "", "", "h3", True,*args),
            "h4" : lambda *args: self.initTags( "", "", "h4", True,*args),
            "h5" : lambda *args: self.initTags( "", "", "h5", True,*args),
            "h6" : lambda *args: self.initTags( "", "", "h6", True,*args),
            "head" : lambda *args: self.initTags( "", "", "head", True,*args,iterationSkipper()),

            "header" : lambda *args: self.initTags( "", "", "header", True,*args),
  
            "hgroup" : lambda *args: self.initTags( "", "", "hgroup", True,*args),
  
            "hr" : lambda *args: self.initTags( "", "", "hr", False,*args),
            "html" : lambda *args: self.initTags( "", "", "html", True,*args,{"lang":"en"} if self.Accessibility else "",iterationSkipper()),

            "i" : lambda *args: self.initTags( "", "", "i", True,*args),
            "iframe" : lambda *args: self.initTags( "", "", "iframe", True,*args),
  
            "img" : lambda *args: self.initTags( "" if not self.Performance else " loading=\"lazy\"", "", "img", False,*args),
            "inp" : lambda *args: self.initTags( "", "", "input", False,*args),
            "ins" : lambda *args: self.initTags( "", "", "ins", True,*args),
            "kbd" : lambda *args: self.initTags( "", "", "kbd", True,*args),
            "keygen" : lambda *args: self.initTags( "", "", "keygen", True,*args),
  
            "label" : lambda *args: self.initTags( "", "", "label", True,*args),
 
            "legend" : lambda *args: self.initTags( "", "", "legend", True,*args),
  
            "li" : lambda *args: self.initTags( "", "", "li", True,*args),
            "link" : lambda *args: self.initTags( "", "", "link", False,*args),
            "main" : lambda *args: self.initTags( "", "", "main", True,*args),

            "_map" : lambda *args: self.initTags( "", "", "map", True,*args),

            "mark" : lambda *args: self.initTags( "", "", "mark", True,*args),

            "menu" : lambda *args: self.initTags( "", "", "menu", True,*args),

            "menuitem" : lambda *args: self.initTags( "", "", "menuitem", True,*args),
   
            "meta" : lambda *args: self.initTags( "", "", "meta", False,*args,iterationSkipper()),

            "meter" : lambda *args: self.initTags( "", "", "meter", True,*args),
 
            "nav" : lambda *args: self.initTags( "", "", "nav", True,*args),
            "noscript" : lambda *args: self.initTags( "", "", "noscript", True,*args),
   
            "obj" : lambda *args: self.initTags( "", "", "obj", True,*args),
            "ol" : lambda *args: self.initTags( "", "", "ol", True,*args),
            "optgroup" : lambda *args: self.initTags( "", "", "optgroup", True,*args),
   
            "option" : lambda *args: self.initTags( "", "", "option", True,*args),
  
            "output" : lambda *args: self.initTags( "", "", "output", True,*args),
  
            "p" : lambda *args: self.initTags( "", "", "p", True,*args),
            "param" : lambda *args: self.initTags( "", "", "param", True,*args),
 
            "picture" : lambda *args: self.initTags( "", "", "picture", True,*args),
   
            "pre" : lambda *args: self.initTags( "", "", "pre", True,*args),
            "progress" : lambda *args: self.initTags( "", "", "progress", True,*args),
   
            "q" : lambda *args: self.initTags( "", "", "q", True,*args),
            "rb" : lambda *args: self.initTags( "", "", "rb", True,*args),
            "rp" : lambda *args: self.initTags( "", "", "rp", True,*args),
            "rt" : lambda *args: self.initTags( "", "", "rt", True,*args),
            "rtc" : lambda *args: self.initTags( "", "", "rtc", True,*args),
            "ruby" : lambda *args: self.initTags( "", "", "ruby", True,*args),

            "s" : lambda *args: self.initTags( "", "", "s", True,*args),
            "samp" : lambda *args: self.initTags( "", "", "samp", True,*args),

            "script" : lambda *args: self.initTags( "", "", "script", True,*args),
  
            "section" : lambda *args: self.initTags( "", "", "section", True,*args),
   
            "select" : lambda *args: self.initTags( "", "", "select", True,*args),
  
            "small" : lambda *args: self.initTags( "", "", "small", True,*args),
 
            "source" : lambda *args: self.initTags( "", "", "source", True,*args),
  
            "span" : lambda *args: self.initTags( "", "", "span", True,*args),

            "strong" : lambda *args: self.initTags( "", "", "strong", True,*args),
  
            "style" : lambda *args: self.initTags( "", "", "style", True,*args),
 
            "sub" : lambda *args: self.initTags( "", "", "sub", True,*args),
            "summary" : lambda *args: self.initTags( "", "", "summary", True,*args),
   
            "sup" : lambda *args: self.initTags( "", "", "sup", True,*args),
            "table" : lambda *args: self.initTags( "", "", "table", True,*args),
 
            "tbody" : lambda *args: self.initTags( "", "", "tbody", True,*args),
 
            "td" : lambda *args: self.initTags( "", "", "td", True,*args),
            "template" : lambda *args: self.initTags( "", "", "template", True,*args),
   
            "textarea" : lambda *args: self.initTags( "", "", "textarea", True,*args),
   
            "tfoot" : lambda *args: self.initTags( "", "", "tfoot", True,*args),
            "th" : lambda *args: self.initTags( "", "", "th", True,*args),
            "thead" : lambda *args: self.initTags( "", "", "thead", True,*args),
            "time" : lambda *args: self.initTags( "", "", "time", True,*args),
            "tr" : lambda *args: self.initTags( "", "", "tr", True,*args),
            "track" : lambda *args: self.initTags( "", "", "track", True,*args),
            "u" : lambda *args: self.initTags( "", "", "u", True,*args),
            "ul" : lambda *args: self.initTags( "", "", "ul", True,*args),
            "video" : lambda *args: self.initTags( "", "", "video", True,*args),
            "wbr" : lambda *args: self.initTags( "", "", "wbr", True,*args),
    "wrapper": lambda *args: "".join(map(str, args)),

"title": lambda *args: (
    (globals().__setitem__(self,'titlebool', True)) or
    self.initTags("", "", "title", True, *args, iterationSkipper())
)

            }


    def renderTemplate(self, path, resources={}):
        file_namespace = resources.copy()
        file_namespace.update(self.tags())
        file_namespace.update({
    "input": self.tags()["inp"]
})

        file_namespace.update({"useComponent":self.
        useComponent,"useLayout":self.useLayout})
        with open(os.path.join(self.FUBAM_TEMPLATES_DIR, f"{path}.pmx"), "r") as file:
            file_content = file.read()
            exec(file_content, file_namespace)
        return file_namespace.get("Export")
    def useComponent(self, path, resources={}):
        file_namespace = resources.copy()
        file_namespace.update(self.tags())
        file_namespace.update({
    "input": self.tags()["inp"]
})
        with open(f"{path}.pmx", 'r') as file:
            file_content = file.read()
            exec(file_content, file_namespace)
        return file_namespace.get("Export")
    
    def useLayout(self,file,code,resources={}):
        file_namespace = resources.copy()
        file_namespace.update(self.tags())
        file_namespace.update({"__extend__" : code})
        file_namespace.update({
    "input": self.tags()["inp"]
})

        with open(f"{file}.pmx", 'r') as f:
            file_content = f.read()
            exec(file_content, file_namespace)
        return file_namespace.get("Export")

    
    @staticmethod
    def compressJSFile(inputfile, outputfile=""):
        if not outputfile:
            g = inputfile.split(".")
            outputfile = ".".join(g[:-1]) + ".min.js" if g[-1].lower() == "js" else inputfile + ".min.js"
        with open(inputfile, "r") as infile, open(outputfile, "w") as outfile:
            outfile.write(jsmin(infile.read()))

    @staticmethod
    def compressCSSFile(inputfile, outputfile=""):
        if not outputfile:
            g = inputfile.split(".")
            outputfile = ".".join(g[:-1]) + ".min.css" if g[-1].lower() == "css" else inputfile + ".min.css"
        with open(inputfile, "r") as infile, open(outputfile, "w") as outfile:
            outfile.write(cssmin(infile.read()))
