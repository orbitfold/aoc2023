import click

@click.command()
@click.option('-i', '--input', help='Input file')
def calibration(input_file):
    pass

if __name__ == '__main__':
    calibration()
