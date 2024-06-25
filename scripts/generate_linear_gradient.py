import click
import cmasher as cmr

@click.command()
@click.option('--cmap', default='RdBu', help='Name of the colormap, use CamelCase, e.g., RdBu, Viridis, etc')
@click.option('--num', default=2, help='Number of stops for the gradient, e.g., 2, 3, 4, etc')
def generate_linear_gradient(cmap,num):
    colors = cmr.take_cmap_colors(cmap, num, return_fmt='hex')
    
    if num == 2:
        lin_colors = f'linear-gradient(0deg, {colors[0]}, {colors[1]})'
        click.echo(lin_colors)
    elif num == 3:
        lin_colors = f'linear-gradient(0deg, {colors[0]} 0%, {colors[1]} 50%, {colors[2]} 100%)'
        click.echo(lin_colors)
    else:
        click.echo(colors)

if __name__ == '__main__':
    generate_linear_gradient()