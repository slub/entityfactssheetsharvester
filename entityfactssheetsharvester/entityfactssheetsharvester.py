#!/usr/bin/python3
# -*- coding: utf-8 -*-
import argparse
import json
import os
import sys

import requests

from threading import current_thread
from rx import create, of
from rx import operators as op
from rx.scheduler import ThreadPoolScheduler

ENTITYFACTS_BASE_URI = "http://hub.culturegraph.org/entityfacts/"
UTF8_CHARSET_ID = 'utf-8'
LINEBREAK = "\n"

THREAD_POOL_SCHEDULER = ThreadPoolScheduler(10)


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def get_gnd_identifier(line):
    gnd_identifier = line
    # remove line break
    lastchar = line[-1]
    oslinebreak = os.linesep
    if lastchar == oslinebreak:
        gnd_identifier = line[0:-1]
    eprint("GND identifier '{0}' (thread = '{1}')".format(gnd_identifier, current_thread().name))
    return gnd_identifier


def entityfacts_request(request_uri, gnd_identifier):
    eprint("try to retrieve EntityFacts sheet for GND identifier '{0}' (thread = '{1}')".format(gnd_identifier,
                                                                                                current_thread().name))
    response = requests.get(request_uri, timeout=60)
    if response.status_code != 200:
        eprint("couldn't fetch EntityFacts sheet for GND identifier '{0}' (thread = '{1}')".format(gnd_identifier,
                                                                                                   current_thread().name))
        return None

    response_body = response.content.decode(UTF8_CHARSET_ID)
    eprint("retrieved EntityFacts sheet for GND identifier '{0}' (thread = '{1}')".format(gnd_identifier,
                                                                                          current_thread().name))
    return response_body


def retrieve_entityfacts_sheet_obs(gnd_identifier):
    return of(gnd_identifier).pipe(op.map(lambda gndid: retrieve_entityfacts_sheet(gnd_identifier)),
                                   op.filter(lambda value: value is not None))


def retrieve_entityfacts_sheet(gnd_identifier):
    entityfacts_sheets_uri = ENTITYFACTS_BASE_URI + gnd_identifier
    response_tuple = entityfacts_request(entityfacts_sheets_uri, gnd_identifier)
    if response_tuple is None:
        return None

    entityfacts_sheet_tuple = (response_tuple, gnd_identifier)

    return entityfacts_sheet_tuple


def format_entityfacts_sheet_obs(entityfacts_sheet_tuple_obs):
    return entityfacts_sheet_tuple_obs.pipe(op.map(lambda ef_sheet_tuple: format_entityfacts_sheet(ef_sheet_tuple)))


def format_entityfacts_sheet(entityfacts_sheet_tuple):
    gnd_identifier = entityfacts_sheet_tuple[1]
    eprint("format EntityFacts sheet for GND identifier '{0}' (thread = '{1}')".format(gnd_identifier,
                                                                                       current_thread().name))
    entityfacts_sheet_json = json.loads(entityfacts_sheet_tuple[0])
    flat_entityfacts_sheet_json = json.dumps(entityfacts_sheet_json, indent=None)
    return flat_entityfacts_sheet_json, gnd_identifier


def write_entityfacts_sheet_obs(flat_entityfacts_sheet_json_tuple_obs):
    return flat_entityfacts_sheet_json_tuple_obs.pipe(op.map(lambda flat_ef_sheet_json_tuple: write_entityfacts_sheet(
        flat_ef_sheet_json_tuple)))


def write_entityfacts_sheet(flat_entityfacts_sheet_json_tuple):
    gnd_identifier = flat_entityfacts_sheet_json_tuple[1]
    eprint("write EntityFacts sheet for GND identifier '{0}' (thread = '{1}')".format(gnd_identifier,
                                                                                      current_thread().name))
    sys.stdout.write(flat_entityfacts_sheet_json_tuple[0] + LINEBREAK)

    return gnd_identifier


def push_input(observer, scheduler):
    for line in sys.stdin:
        observer.on_next(line)
    return observer.on_completed()


def run():
    parser = argparse.ArgumentParser(prog='entityfactssheetsharvester',
                                     description='Retrieves EntityFacts sheets from a given CSV with GND identifiers and returns them as line-delimited JSON records.',
                                     epilog='example: entityfactssheetsharvester < [INPUT CSV FILE WITH GND IDENTIFIERS] > [PATH TO THE OUTPUT LINE-DELIMITED JSON RECORDS FILE]',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    args = parser.parse_args()

    if hasattr(args, 'help') and args.help:
        parser.print_usage(sys.stderr)
        exit(-1)

    source = create(push_input)

    all_in_one = source.pipe(op.map(lambda line: get_gnd_identifier(line)),
                             op.map(lambda gnd_identifier: retrieve_entityfacts_sheet_obs(gnd_identifier)),
                             op.map(lambda ef_sheet_tuple_obs: format_entityfacts_sheet_obs(ef_sheet_tuple_obs)),
                             op.map(lambda flat_ef_sheet_json_tuple_obs: write_entityfacts_sheet_obs(
                                 flat_ef_sheet_json_tuple_obs)),
                             op.flat_map(lambda x: x))

    all_in_one.subscribe(
        on_next=lambda gnd_identifier: eprint(
            "PROCESSED GND identifier '{0}': {1}".format(gnd_identifier, current_thread().name)),
        on_error=lambda e: eprint(e),
        on_completed=lambda: eprint("PROCESS done!"),
        scheduler=THREAD_POOL_SCHEDULER)


if __name__ == "__main__":
    run()
