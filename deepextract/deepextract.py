# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import Any, Generator, List
from collections import deque

__all__ = [
    'deep_extract',
    'deep_extract_items',
    'deep_extract_trace',
]


@dataclass
class DeepExtractItem:
    key: str
    value: Any


def deep_extract_key(data, key):
    try:
        for k, v in data.items():
            if k == key:
                yield DeepExtractItem(k, v)
            for result in deep_extract_key(v, key):
                yield result
    except AttributeError:
        if isinstance(data, list):
            for item in data:
                for result in deep_extract_key(item, key):
                    yield result


def deep_extract_match(data, match):
    try:
        for k, v in data.items():
            if match(k):
                yield DeepExtractItem(k, v)
            for result in deep_extract_match(v, match):
                yield result
    except AttributeError:
        if isinstance(data, list):
            for item in data:
                for result in deep_extract_match(item, match):
                    yield result


def deep_extract(data, key_match) -> Generator:
    """
        Given a nested dictionary 'data'
        Walk dictionaries/lists looking for keys that match 'key_match'
    """
    if hasattr(key_match, '__call__'):
        return deep_extract_match(data, key_match)
    else:
        return deep_extract_key(data, key_match)


def deep_extract_items(data, key_match) -> List[DeepExtractItem]:
    """
        Convenience wrapper
        Gives a list from the generator returned from deep_extract
    """
    return list(deep_extract(data, key_match))


def deep_extract_trace(data, key) -> (List[DeepExtractItem], List[Any]):
    """
        Given a nested dictionary 'data'
        Walk dictionaries/lists looking for keys that match 'key'
        Give a list of items recovered and the path taken to retrieve them
    """
    trace = list()
    work = deque()
    items = list(_deep_extract_trace(data, key, trace, work))
    return items, trace


def _deep_extract_trace(data, key, trace, work):
    # uses trace and work to give paths in a less surprising order
    # top to bottom
    try:
        for k, v in data.items():
            if k == key:
                work.appendleft(k)
                yield DeepExtractItem(k, v)
            for result in _deep_extract_trace(v, key, trace, work):
                work.appendleft(k)
                yield result
    except AttributeError:
        if isinstance(data, list):
            for ndx, item in enumerate(data):
                for result in _deep_extract_trace(item, key, trace, work):
                    work.appendleft(ndx)
                    yield result
    if work:
        trace.append(list(work))
        work.clear()
