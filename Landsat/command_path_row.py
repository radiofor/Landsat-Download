# -*- coding: utf-8 -*-
import click
from Landsat.google_task import GoogleTask


@click.command()
@click.option('--spacecraft_id', type=click.Choice(['1', '2', '3', '4', '5', '7', '8']), prompt=True)
@click.option('--sensing_time', type=str, prompt=True, nargs=2)
@click.option('--wrs_paths', type=int, prompt=True, nargs=2)
@click.option('--wrs_rows', type=int, prompt=True, nargs=2)
@click.option('--cloud_cover', type=float, prompt=True)
@click.option('--out_path', type=str, prompt=True)
def submit(spacecraft_id, sensing_time, wrs_paths, wrs_rows, cloud_cover, out_path):
    task = GoogleTask(spacecraft_id=spacecraft_id, sensing_time=sensing_time, wrs_paths=wrs_paths, wrs_rows=wrs_rows,
                      cloud_cover=cloud_cover, out_path=out_path)
    task.start()


if __name__ == '__main__':
    submit()
