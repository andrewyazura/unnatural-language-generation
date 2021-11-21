import click
from text_generator.generator import Generator


@click.group()
def cli():
    pass


@click.command()
@click.option(
    "--json", "json_path", type=click.Path(exists=True, file_okay=True, dir_okay=False)
)
@click.option("-n", "--words", "words", default=5, type=int, show_default=True)
@click.option("-o", "--order", "order", default=1, type=int, show_default=True)
def generate(json_path, words, order):
    """Generate random sequence from graph"""
    if json_path:
        click.echo(f"Loading generator from '{json_path}'...")
        generator = Generator.load_from_json(json_path, order=order)
    else:
        generator = Generator(order)

    click.echo(f"Generating text...")
    click.echo(generator.generate(words))


@click.command()
@click.option(
    "--json", "json_path", type=click.Path(exists=True, file_okay=True, dir_okay=False)
)
@click.option(
    "--input",
    "input_path",
    required=True,
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
)
@click.option(
    "--output", "output_path", type=click.Path(file_okay=True, dir_okay=False)
)
@click.option("-o", "--order", "order", default=1, type=int, show_default=True)
def process(json_path, input_path, output_path, order):
    """Generate random sequence from graph"""
    if json_path:
        click.echo(f"Loading generator from '{json_path}'...")
        generator = Generator.load_from_json(json_path, order=order)
    else:
        generator = Generator(order)

    click.echo("Processing text...")
    with open(input_path, "r") as f:
        generator.process_text(f.read())

    if output_path:
        generator.dump_to_json(output_path)

    click.echo("Done")


@click.command()
@click.option(
    "--json",
    "json_path",
    required=True,
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
)
@click.option("-o", "--order", "order", default=1, type=int, show_default=True)
def info(json_path, order):
    """Generate random sequence from graph"""
    click.echo(f"Loading generator from '{json_path}'...")
    generator = Generator.load_from_json(json_path, order=order)
    click.echo(generator.graph_info())


cli.add_command(generate)
cli.add_command(process)
cli.add_command(info)
