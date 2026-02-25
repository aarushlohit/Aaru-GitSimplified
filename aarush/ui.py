from rich import print

def success(msg: str) -> None:
    print(f"[green]✔ {msg}[/green]")
def error(msg: str) -> None:
    print(f"[red]✖ {msg}[/red]")
def info(msg: str) -> None:
    print(f"[cyan]ℹ {msg}[/cyan]")
    