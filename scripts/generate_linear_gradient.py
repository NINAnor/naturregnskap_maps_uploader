import click
import cmasher as cmr


@click.command(
    help="Generate the css string for gradients based on a colormap name",
)
@click.option(
    "--cmap",
    default="RdBu",
    help="Name of the colormap, use CamelCase, e.g., RdBu, Viridis, etc",
)
@click.option(
    "--num",
    default=2,
    help="Number of stops for the gradient, e.g., 2, 3, 4, etc",
    type=int,
)
def generate_linear_gradient(cmap: str, num: int) -> None:
    colors = ",".join(cmr.take_cmap_colors(cmap, num, return_fmt="hex"))
    click.echo(f"linear-gradient(0deg, {colors})")


if __name__ == "__main__":
    generate_linear_gradient()
