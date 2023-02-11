import requests
from bs4 import BeautifulSoup
import click
import os
import time
import PySimpleGUI as psg
from datetime import datetime
import random
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

    def save(self, loc="./output.txt"):
        with open(loc, "a") as out:
            for (k, v) in self.info().items():
                out.write(f"{k}: {v}\n")
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
            rake --url www.domain.tld --o raw|table\n\t
            rake --url www.domain.tld --o raw|table --save ./name.txt\n\n For more help options use --help or -h        
            """

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
@click.help_option("--help", "-h", help=click.secho(HELP, fg=fg))
def cli():
    pass

#@cli.command(name=None)
@click.option('--url', "-u", required=True, help='The url of the domain. Alias -u')
@click.option('--save', "-s", help='Where to save the file. default is text file. Alias -s')
@click.option("--o", help="type of stout, options include raw, table. if not included, no stout for display")
def gather(url, o, save=None):
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

    if save:
        dr = os.path.isfile(save)
        match dr:
            case True:
                click.echo(r.save(loc=save))
            case False:
                click.echo("Invalid file path")
 