Helps extract keys from deeply nested objects. I wrote for dealing with complicated json data.

License is CC0

## install

Just save [deepextract](/deepextract/deepextract.py?raw=true) to where you need it.

## api

```
>>> from deepextract import *
>>> data = {
  "path": "/root",
  "images": [
    {
      "path": "/images/001.png",
      "animal": "cat",
    },
    {
      "path": "/images/002.png",
      "animal": "dog",
    }
  ]
}

# deep_extract_items
>>> deep_extract_items(data, "path")
[DeepExtractItem(key='path', value='/root'),
 DeepExtractItem(key='path', value='/images/001.png'),
 DeepExtractItem(key='path', value='/images/002.png')]

# deep_extract_items
>>> deep_extract_items(data, lambda k: len(k) > 4)
[DeepExtractItem(key='images', value=[{'path': '/images/001.png', 'animal': 'cat'}, {'path': '/images/002.png', 'animal': 'dog'}]),
 DeepExtractItem(key='animal', value='cat'),
 DeepExtractItem(key='animal', value='dog')]

# deep_extract_trace
>>> items, trace = deep_extract_trace(data, "animal")
>>> items
[DeepExtractItem(key='animal', value='cat'),
 DeepExtractItem(key='animal', value='dog')]
>>> trace
[['images', 0, 'animal'], ['images', 1, 'animal']]

# deep_extract
>>> [item.value for item in deep_extract(data, "path")]
['/root', '/images/001.png', '/images/002.png']
```
