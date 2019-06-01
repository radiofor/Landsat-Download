# -*- coding: utf-8 -*-
import click
from Landsat import update_metadata


@click.command()
def submit():
    update_metadata.update_list()


if __name__ == '__main__':
    submit()
