from urllib import request
from bs4 import BeautifulSoup
import click
import os
import time
from PySimpleGUI import (Button, Text, Radio, Input, Submit, FolderBrowse, Window)
from datetime import datetime
import random
import json

today =datetime.today()

class Rake(BeautifulSoup):
    def __init__(self, domain):
        self.url = f"https://www.whois.com/whois/{domain}"
        self.req = request.urlopen(self.url)
        """
        with open(domain, "r") as req:
            self.req = req.read()
        """
        super(Rake, self).__init__(self.req.text, "html.parser")
        #super(Rake, self).__init__(self.req, "html.parser")

    def raw_data(self):
        return self.find("pre", attrs={"class": "df-raw", "id" :"registrarData"})

    def find_data(self, ele):
        return self.find_all(ele, attrs={})

    def content(self):
        return self.raw_data().contents[0].split("\n")

    def info(self):
        table = {}
        for i in self.content():
            data = i.split(":")
            table[data[0]] = data[1].strip()
        return table

    def json(self, fp):
        return json.dump(self.info, fp)

    def txt(self, fp):
        with open(fp, "a") as out:
            for (k, v) in self.info().items():
                out.write(f"{k}: {v}\n")
            return True 

    def csv(self, fp):
        with open(loc, "a") as out:
            out.write("Data, Detail")
            for (k, v) in self.info().items():
                out.write(f"{k}, {v}\n")
            return True

    def pages(self):
        pages = []
        for page in self.find_data("a"):
            p = page.attrs.get("href")
            if p != "#":
                pages.append(page.getText())
        return pages
                
    def media(self):
        pages = []
        all_media = self.find_data("img")+self.find_data("audio")+self.find_data("video")
        for page in all_media:
            p = page.attrs.get("src")
            if p != "#" or p!="":
                pages.append(page.getText())
        return pages

    def count(self, ele):
        return len(self.find_data(ele))#.contents[0].split("\n")

    def clone(self, fp="./index.html"):
        with open(fp, "w") as cl:
            return cl.write(self.req)

    def assets(self):
        (css, js) = {}, {}
        all_media = self.find_data("img")+self.find_data("script")+self.find_data("style")
        for n, page in enumerate(all_media):
            (jv, st) = page.attrs.get("src"), page.attrs.get("href")
            match (jv, st):
                case (True, None):
                    js[f"js_{n}"] = st
                case (None, True):                        
                    css[f"css_{n}"] = jv
        return (css, js)
    
    def clone_with_assets(self, fp="./index.html"):
        with open(fp, "w") as cl:
            return cl.write(self.req)

"""
if __name__ == "__main__":
    r = Rake("../buy_me_a_coffee/Desktop/acsolot/buy_me_a_coffee/templates/homepage.html")
    print(r.assets())
"""
COLORS = (
        'blue',
        'green',
        'yellow',
    )
fg = None
with open('./art.txt', 'r') as HELP:
        HELP = HELP.read()
        fg = random.choice(COLORS)
HELP += f"""\nInformation Gathering Tool\nIbraheem Mobolaji Abdulsalam \xa9 {today.date().year}\n\n Usage:\n\t
            rake start --url www.domain.tld --o raw|table\n\t
            rake start --url www.domain.tld --o raw|table --save ./name.txt\n\n For more help options use --help or -h        
            """

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass

@cli.command()
def index():
    click.secho(HELP, fg=fg)

@cli.command()
@click.option('--url', "-u", required=True, help='The url of the domain. Alias -u')
@click.argument("fpath", required=False)
def clone(url, fpath=None):
    """
    For cloning web page.
    Usage:
        rake clone --url www.domain.tld
        rake clone -u www.domain.tld
    """
    try:
        r = Rake(domain = url)
    except Exception:
        return click.echo("Internet Error")
    else:
        return r.clone(fpath)

@cli.command()
def gui():
    """
    GUI mode for all operations. The output can also be exported into various file formats.
    Usage:
        rake gui - Wait for a gui window to popup
    """
    layout = [
        [Text("Enter URL:")],
        [Input(key="url", focus=True, tooltip="Enter URL")],
        [FolderBrowse(key="folder"), Text("No directory selected", key="folder_out")],
        [Text("Operations:")],
        [
         Radio("Information", group_id="out", key="info"),
         Radio("Clone", group_id="out", key="clone"),
         Radio("Stats", group_id="out", key="stats"),
         Radio("None", default=True, group_id="out", key="non")
        ],
        [Text("Output:")],
        [
         Radio("Text", group_id="out", key="txt"),
         Radio("CSV", group_id="out", key="csv"),
         Radio("JSON", group_id="out", key="json"),
         Radio("None", default=True, group_id="out", key="non")
        ],
        [Text("Filename:")],
        [Input("", key="fp", enable_events=True)],
        [Text("Idle", key="progress")],
        [Submit("Start", key="start")]

    ]
    win = Window("Rake-Information gathering tool", layout)
    while True:
        evt, vals = win.Read(0)
        dr = ""
        filename =  ""
        print(evt, vals)
        if vals["json"]:
            filename = f"{path}.json"
        if vals['csv']:
            filename = f"{path}.csv"
        if vals['txt']:
            filename = f"{path}.txt"
        path = os.path.join(dr, filename)
        vals["fp"] = path

        if vals["folder"] != "":
            dr = vals["folder"]
            vals["folder_out"] = dr
            path = os.path.join(dr, filename)
            vals["fp"] = path
        if evt == "start":
            try:
                r = Rake(domain = vals['url'])
            except Exception:
                return click.secho("Internet Error", fg="red")
            else:
                if vals["json"]:
                    r.json(path)
                if vals['csv']:
                    r.csv(path)
                if vals['txt']:
                    r.txt(path)
                if vals['non']:
                    return r.info()

@cli.command(name = "start")
@click.option('--url', "-u", required=True, help='The url of the domain. Alias -u')
@click.option("--o", help="type of stout, options include raw, table. if not included, no stout for display")
@click.argument("fpath", required=False)
def gather(url, o, fpath=None):
    r"""
    This is another whois on command line.\nEvery information regarding a domain will be retrieved and can also be exported
    """
    try:
        r = Rake(domain = url)
    except Exception:
        return click.echo("Internet Error")
    match o:
        case None:
            click.echo("processed with no output")
        case "raw":
            click.echo(r.info())
        case "table":
            for (i, j) in r.info().items():
                time.sleep(1)
                click.echo(f"\t{i}: {j}")
        case "csv":
            if fpath is None:
                click.secho("You need to set file path.\ntry:\nrake start --url domain.tld --o csv path/filename.txt", fg="red")
            else:
                r.csv(fpath)
        case "json":
            if fpath is None:
                click.secho("You need to set file path.\ntry:\nrake start --url domain.tld --o json path/filename.json", fg="red")
            else:
                r.json(fpath)
                click.echo()
        case "txt":
            if fpath is None:
                click.secho("You need to set file path.\ntry:\nrake start --url domain.tld --o txt path/filename.txt", fg="red")
            else:
                r.txt(fpath)



    