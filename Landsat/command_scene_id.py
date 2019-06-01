# -*- coding: utf-8 -*-
import click
from Landsat.google_task import GoogleTask


@click.command()
@click.option('--scene_ids_file', type=str, prompt=True)
@click.option('--out_path', type=str, prompt=True)
def submit(scene_ids_file, out_path):
    task = GoogleTask(scene_ids_file=scene_ids_file, out_path=out_path)
    task.start()


if __name__ == '__main__':
    submit()
