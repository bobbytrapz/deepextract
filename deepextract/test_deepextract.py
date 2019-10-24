import unittest
from .deepextract import (
    deep_extract_items, deep_extract_trace, DeepExtractItem)


class TestDeepExtract(unittest.TestCase):
    def test_simple(self):
        data = simple_data
        items = deep_extract_items(data, "cat")
        self.assertEqual(items, [DeepExtractItem("cat", True)])

    def test_depth(self):
        data = less_simple_data
        items = deep_extract_items(data, "pet")
        self.assertEqual(items, [
            DeepExtractItem("pet", "cat"),
            DeepExtractItem("pet", "dog"),
        ])

    def test_deeper(self):
        data = even_less_simple_data
        items = deep_extract_items(data, "id")
        self.assertEqual(items, [
            DeepExtractItem("id", 1000),
            DeepExtractItem("id", 2000),
            DeepExtractItem("id", 3000),
            DeepExtractItem("id", 4000),
            DeepExtractItem("id", 5000),
            DeepExtractItem("id", 6000),
            DeepExtractItem("id", 7000),
        ])

    def test_trace_steps(self):
        data = even_less_simple_data
        _, trace = deep_extract_trace(data, "task")
        self.assertEqual(trace[0], [0, "activity", "day", 0, "task"])
        data = trace_steps(data, trace[0][:-1])
        self.assertEqual(data["task"], "run")

    def test_trace_logical_order(self):
        data = even_less_simple_data
        items, trace = deep_extract_trace(data, "task")
        self.assertEqual([item.value for item in items],
                         [trace_steps(data, t) for t in trace])


def trace_steps(data, trace):
    for step in trace:
        data = data[step]
    return data


simple_data = {
    "cat": True,
    "dog": False,
}

less_simple_data = [
    {
        "pet": "cat",
        "hungry": True,
    },
    {
        "pet": "dog",
        "hungry": True,
    }
]

even_less_simple_data = [
    {
        "id": 1000,
        "pet": "cat",
        "activity": {
            "day": [
                {
                    "id": 2000,
                    "task": "run",
                }
            ],
            "night": [
                {
                    "id": 3000,
                    "task": "sleep",
                }
            ]
        }
    },
    {
        "id": 4000,
        "pet": "dog",
        "activities": {
            "day": [
                {
                    "id": 5000,
                    "task": "bark",
                },
                {
                    "id": 6000,
                    "task": "run",
                },
            ],
            "night": [
                {
                    "id": 7000,
                    "task": "sleep",
                }
            ]
        }
    },
]
