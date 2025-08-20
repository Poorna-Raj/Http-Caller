import requests
import typer
import json
from rich.console import Console
from rich.syntax import Syntax

app = typer.Typer()
console = Console()

@app.command()
def request(
    method:str,
    url:str,
    data:str = typer.Option(None,"--data","-d",help="JSON Body"),
    header:str = typer.Option(None,"--header","-H",help="Key:Value headers"),):

    headers = {}
    if header:
        try:
            key,value = header.split(":")
            headers[key.strip()] = value.strip()
        except ValueError:
            console.print("[red]Invalid Headers! Use key:value format.[/red]")
            raise typer.Exit()
        
    try:
        response = requests.request(method=method.upper(),url=url,headers=headers,data=data)
        console.print(f"[bold green]{response.status_code}[/bold green]")

        try:
            json_obj = response.json()
            json_text = json.dumps(json_obj, indent=2)
            syntax = Syntax(json_text,"json",theme="monokai",line_numbers=True)
            console.print(syntax)
        except Exception:
            console.print(response.text)
    except Exception as e:
        console.print(f"[red]Request failed due to: {e}[/red]")

if __name__ == "__main__":
    app()
