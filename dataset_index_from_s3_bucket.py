#!/usr/bin/env python3

# coding: utf-8

# Based on the ODC community script https://github.com/opendatacube/datacube-dataset-config/blob/master/scripts/index_from_s3_bucket.py

from pathlib import Path
import logging
import click
import boto3
from botocore import UNSIGNED
from botocore.config import Config
import datacube
from datacube.index.hl import Doc2Dataset
from datacube.utils import changes
from ruamel.yaml import YAML

from multiprocessing import Process, current_process, Queue, Manager, cpu_count
from queue import Empty

GUARDIAN = "GUARDIAN_QUEUE_EMPTY"

def get_s3_url(bucket_name, obj_key):
    return 's3://{bucket_name}/{obj_key}'.format(
        bucket_name=bucket_name, obj_key=obj_key)


def archive_document(doc, uri, index, sources_policy, require_lineage):
    def get_ids(dataset):
        ds = index.datasets.get(dataset.id, include_sources=True)
        for source in ds.sources.values():
            yield source.id
        yield dataset.id

    resolver = Doc2Dataset(index)
    dataset, err  = resolver(doc, uri)
    index.datasets.archive(get_ids(dataset))
    logging.info("Archiving %s and all sources of %s", dataset.id, dataset.id)


def add_dataset(doc, uri, index, sources_policy, require_lineage):
    logging.info("Indexing %s", uri)
    skip_lineage = not require_lineage
    resolver = Doc2Dataset(index, skip_lineage=skip_lineage)
    dataset, err  = resolver(doc, uri)
    if err is not None:
        logging.error("%s", err)
    else:
        try:
            # TODO: Sources policy to be checked in sentinel 2 dataset types
            index.datasets.add(dataset, sources_policy=sources_policy, with_lineage=require_lineage)
        except changes.DocumentMismatchError as e:
            index.datasets.update(dataset, {tuple(): changes.allow_any})
        except Exception as e:
            err = e
            logging.error("Unhandled exception %s", e)

    return dataset, err


def worker(bucket_name, config, start_date, end_date, func, unsafe, sources_policy, require_lineage, queue, profile_name, endpoint_url, unsigned_requests):
    dc=datacube.Datacube(config=config)
    index = dc.index

    if unsigned_requests:
        resource_config = Config(signature_version=UNSIGNED)
    else:
        resource_config = None

    session=boto3.session.Session(profile_name=profile_name)
    s3 = session.resource('s3', endpoint_url=endpoint_url, config=resource_config)

    safety = 'safe' if not unsafe else 'unsafe'

    while True:
        try:
            key = queue.get(timeout=60)
            if key == GUARDIAN:
                break
            logging.info("Processing %s %s", key, current_process())
            obj = s3.Object(bucket_name, key).get(ResponseCacheControl='no-cache')
            raw = obj['Body'].read()
            yaml = YAML(typ=safety, pure=False)
            yaml.default_flow_style = False
            data = yaml.load(raw)
            uri = get_s3_url(bucket_name, key)
            cdt = data.get('creation_dt', None)
            # Use the fact lexicographical ordering matches the chronological ordering
            if not cdt or cdt >= start_date and cdt < end_date:
                logging.info("calling %s", func)
                func(data, uri, index, sources_policy, require_lineage)
            queue.task_done()
        except Empty:
            break
        except EOFError:
            break


def iterate_datasets(bucket_name, config, prefix, start_date, end_date, func, unsafe, sources_policy, require_lineage, profile_name, endpoint_url, unsigned_requests):
    manager = Manager()
    queue = manager.Queue()

    if unsigned_requests:
        resource_config = Config(signature_version=UNSIGNED)
    else:
        resource_config = None

    session=boto3.session.Session(profile_name=profile_name)
    s3 = session.resource('s3', endpoint_url=endpoint_url, config=resource_config)

    bucket = s3.Bucket(bucket_name)
    logging.info("Bucket : %s prefix: %s ", bucket_name, str(prefix))
    worker_count = cpu_count() * 2

    processess = []
    for i in range(worker_count):
        proc = Process(target=worker, args=(bucket_name, config, start_date, end_date, func, unsafe, sources_policy, require_lineage, queue, profile_name, endpoint_url, unsigned_requests))
        processess.append(proc)
        proc.start()

    for obj in bucket.objects.filter(Prefix = str(prefix)):
        if (obj.key.endswith(".yaml")):
            queue.put(obj.key)

    # Insert as many sentinels as workers, so each of them will pick one and finish processing
    for i in range(worker_count):
        queue.put(GUARDIAN)

    for proc in processess:
        proc.join()


@click.command(help= "Enter Bucket name. Optional to enter configuration file to access a different database")
@click.argument('bucket_name')
@click.option('--config', '-c', help="Pass the configuration file to access the database",
        type=click.Path(exists=True))
@click.option('--prefix', '-p', help="Pass the prefix of the object to the bucket")
@click.option('--start_date', help="Pass the start acquisition date, in YYYY-MM-DD format")
@click.option('--end_date', help="Pass the end acquisition date, in YYYY-MM-DD format")
@click.option('--archive', is_flag=True, help="If true, datasets found in the specified bucket and prefix will be archived")
@click.option('--unsafe', is_flag=True, help="If true, YAML will be parsed unsafely; only use on trusted datasets!")
@click.option('--sources_policy', default="verify", help="verify, ensure, skip")
@click.option('--require_lineage', is_flag=True, default=False, help="Set to require that lineage is present")
@click.option('--profile_name', default=None, help="Pass the profile to use for the constructed S3 client")
@click.option('--endpoint_url', help="Pass the complete URL to use for the constructed S3 client")
@click.option('--unsigned_requests', is_flag=True, default=False, help="Set to not sign requests")
def main(bucket_name, config, prefix, start_date, end_date, archive, unsafe, sources_policy, require_lineage, profile_name, endpoint_url, unsigned_requests):
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)
    action = archive_document if archive else add_dataset
    iterate_datasets(bucket_name, config, prefix, start_date, end_date, action, unsafe, sources_policy, require_lineage, profile_name, endpoint_url, unsigned_requests)


if __name__ == "__main__":
    main()