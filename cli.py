import click

from text_generator.generate import generate_sequence
from text_generator.graph import graph_from_iterable
from text_generator.io import dump_graph, load_graph
from text_generator.tokenize import tokenize_text


@click.group()
def cli():
    """
    This project provides a CLi and a Python package for generating unnatural language.
    It uses Markov chains to make directed graph of words and then generates sentences.
    Each edge contains `count` of how many times two nodes it connects were found in
    text. During text generation `count` is used to randomly choose next word.
    """
    pass


@cli.command()
@click.option(
    "-in",
    "--input",
    "file_inputs",
    required=True,
    multiple=True,
    type=click.Path(exists=True, dir_okay=False),
    help="text files to parse (can be repeated)",
)
@click.option(
    "-out",
    "--output",
    "graph_output",
    required=True,
    type=click.Path(dir_okay=False),
    help="path to file to export graph into",
)
@click.option(
    "-g",
    "--graph",
    "graph_path",
    type=click.Path(exists=True, dir_okay=False),
    help="path to an exsiting graph file",
)
@click.option(
    "-o",
    "--order",
    "order",
    default=1,
    type=int,
    show_default=True,
    help="order of graph (read README to know more)",
)
def parse(graph_path, file_inputs, graph_output, order):
    """generate a graph from text files"""

    tokens = []

    with click.progressbar(file_inputs, label="processing files...") as bar:
        for file_input in bar:
            with open(file_input, "r") as f:
                text = " ".join(
                    [line.strip() for line in f.readlines() if line.strip()]
                )
                tokens.extend(tokenize_text(text))

    graph = None
    if graph_path:
        click.echo("loading pre-existing graph...")
        graph = load_graph(graph_path)

    click.echo("generating graph...")
    graph = graph_from_iterable(tokens, order, graph)

    click.echo("saving graph...")
    dump_graph(graph, graph_output)

    click.secho("done!", fg="green")


@cli.command()
@click.option(
    "-g",
    "--graph",
    "graph_path",
    required=True,
    type=click.Path(exists=True, dir_okay=False),
    help="path to the graph file",
)
@click.option(
    "-w",
    "--words",
    "words",
    default=255,
    type=int,
    show_default=True,
    help="number of words to generate",
)
@click.option(
    "-o",
    "--order",
    "order",
    default=1,
    type=int,
    show_default=True,
    help="order of graph (read README to know more)",
)
def generate(graph_path, words, order):
    """generate text from a graph"""

    click.echo("loading graph...")
    graph = load_graph(graph_path)
    click.echo("graph loaded")

    click.echo("generating text...")
    sequence = generate_sequence(graph, words, order)

    text = " ".join(sequence)
    click.echo(text)

    if len(sequence) == words:
        color = "green"

    color = "green" if len(sequence) == words else "yellow"
    click.secho(f"{len(sequence)} words generated", fg=color)


if __name__ == "__main__":
    cli()
