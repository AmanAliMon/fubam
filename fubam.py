from fubam_c.tags import *


_a = None
_abbr = None
_address = None
_area = None
_article = None
_aside = None
_audio = None
_b = None
_base = None
_bdi = None
_bdo = None
_blockquote = None
_body = None
_br = None
_button = None
_canvas = None
_caption = None
_cite = None
_code = None
_col = None
_colgroup = None
_data = None
_datalist = None
_dd = None
_details = None
_dfn = None
_dialog = None
_div = None
_dl = None
_dt = None
_em = None
_embed = None
_fieldset = None
_figcaption = None
_figure = None
_footer = None
_form = None
_h1 = None
_h2 = None
_h3 = None
_h4 = None
_h5 = None
_h6 = None
_head = None
_header = None
_hgroup = None
_hr = None
_html = None
_i = None
_iframe = None
_img = None
_inp = None
_ins = None
_kbd = None
_keygen = None
_label = None
_legend = None
_li = None
_link = None
_main = None
__map = None
_mark = None
_menu = None
_menuitem = None
_meta = None
_meter = None
_nav = None
_noscript = None
_obj = None
_ol = None
_optgroup = None
_option = None
_output = None
_p = None
_param = None
_picture = None
_pre = None
_progress = None
_q = None
_rb = None
_rp = None
_rt = None
_rtc = None
_ruby = None
_s = None
_samp = None
_script = None
_section = None
_select = None
_small = None
_source = None
_span = None
_strong = None
_style = None
_sub = None
_summary = None
_sup = None
_table = None
_tbody = None
_td = None
_template = None
_textarea = None
_tfoot = None
_th = None
_thead = None
_time = None
_title = None
_tr = None
_track = None
_u = None
_ul = None
_video = None
_wbr = None
_wrapper = None

FUBAM_TEMPLATES_DIR = "templates"
def render_pythonMarkup(path,resources={}):
    file_namespace = resources
    print(file_namespace)
    with open(f"./{FUBAM_TEMPLATES_DIR}/{path}.pmx", 'r') as file:
        file_content = file.read()
        exec(file_content, file_namespace)

    result = file_namespace.get('HTML')
    return result

def render_component(path,resources={}):
    file_namespace = resources
    with open(f"./{path}.pmx", 'r') as file:
        file_content = file.read()
        exec(file_content, file_namespace)

    result = file_namespace.get('HTML')
    return result


def compressJSFile(inputfile,outputfile=""):
    o = outputfile
    if outputfile == "":
        g = inputfile.split(".")
        if g[-1] in ["js","JS"]:
            o += (".").join([g[h] for h in range(len(g) -1)])
            o += ".min.js"
        else:
            o = inputfile + ".min.js"
    open(o,"w").write(jsmin(open(inputfile,"r").read()))

def compressCSSFile(inputfile,outputfile=""):
    o = outputfile
    if outputfile == "":
        g = inputfile.split(".")
        if g[-1] in ["CSS","css"]:
            o += (".").join([g[h] for h in range(len(g) -1)])
            o += ".min.css"
        else:
            o = inputfile + ".min.css"
    open(o,"w").write(cssmin(open(inputfile,"r").read()))
