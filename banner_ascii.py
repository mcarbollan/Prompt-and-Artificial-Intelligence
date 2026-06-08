"""Gerador de banner ASCII para o projeto Mission Control AI."""

import argparse

import pyfiglet
from rich.align import Align
from rich.console import Console
from rich.text import Text

console = Console()


def mostrar_banner(font="ansi_shadow", text="Mission Control AI"):
    """Mostra o banner principal."""
    linha1 = pyfiglet.figlet_format("Global Solution", font=font)
    linha2 = pyfiglet.figlet_format(text, font=font)

    console.print(Align.center(Text(linha1, style="bold #A855F7")))
    console.print(Align.center(Text(linha2, style="bold #06B6D4")))
    console.print(
        Align.center(
            Text("-- 2026.1 · Prompt Engineering and AI · FIAP --", style="italic #8484A0")
        )
    )


def listar_fontes():
    """Lista fontes disponíveis no PyFiglet."""
    for fonte in pyfiglet.FigletFont.getFonts():
        print(fonte)


def demonstrar_fontes(text="Mission Control AI"):
    """Mostra algumas fontes úteis."""
    fontes = ["ansi_shadow", "slant", "big", "standard", "digital", "doom", "isometric1", "small"]

    for fonte in fontes:
        console.print(f"\nFonte: {fonte}", style="bold yellow")
        console.print(pyfiglet.figlet_format(text, font=fonte))


def main():
    parser = argparse.ArgumentParser(description="Gerador de banner ASCII.")
    parser.add_argument("-fonts", action="store_true", help="Lista todas as fontes disponíveis")
    parser.add_argument("-demo", action="store_true", help="Demonstra algumas fontes")
    parser.add_argument("-font", default="ansi_shadow", help="Fonte do banner")
    parser.add_argument("-text", default="Mission Control AI", help="Texto do banner")
    args = parser.parse_args()

    if args.fonts:
        listar_fontes()
    elif args.demo:
        demonstrar_fontes(args.text)
    else:
        mostrar_banner(args.font, args.text)


if __name__ == "__main__":
    main()