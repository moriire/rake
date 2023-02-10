import requests
from bs4 import BeautifulSoup
import click
import os
import time
import PySimpleGUI as psg
from datetime import datetime
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


with open('./art.txt', 'r') as HELP:
        HELP = HELP.read()
HELP += f"""\nInformation Gathering Tool\nIbraheem Mobolaji Abdulsalam \xa9 {today.date().year}\n\n Usage:\n\t
            rake --url www.domain.tld --o raw|table\n\t
            rake --url www.domain.tld --o raw|table --save ./name.txt\n\n For more help options use --help or -h        
            """

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
@click.help_option("--help", "-h")
def cli():
    pass

   
@cli.command(name=" ")
def main():
    click.echo(HELP)

@cli.command()
@click.option('--url', "-u", multiple=True, required=True, help='The url of the domain. Alias -u')
@click.option('--save', "-s", multiple=True, help='Where to save the file. default is text file. Alias -s')
@click.option("--o", help="type of stout, options include raw, table. if not included, no stout for display")
def gather(url, o, save=None):
    """ This will start the program and gather all necessary infomation\n options:\n\t--show: 1. t - tabular display 2. s - Save to stdout """
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
 

if __name__=="__main__":
    
    cli()

