import requests
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
        self.req = requests.get(self.url)
        super(Rake, self).__init__(self.req.text, "html.parser")

    def raw_data(self):
        return self.find("pre", attrs={"class": "df-raw", "id" :"registrarData"})

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
                
    def gui(self):
        return "no gui yet"

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
    return click.secho(HELP, fg=fg)

@cli.command()
def gui():
    layout = [
        [Text("Enter URL:")],
        [Input(key="url", focus=True, tooltip="Enter URL")],
        [FolderBrowse(key="folder"), Text("No directory selected", key="folder_out")],
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
    try:
        r = Rake(domain = url)
    except Exception:
        click.echo("Internet Error")
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