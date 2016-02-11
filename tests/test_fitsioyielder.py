#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_fitsioyielder
----------------------------------

Tests for `fitsioyielder` module.
"""

import pytest
import fitsio
import numpy as np
from fitsioyielder import fitsioyielder

@pytest.fixture(scope='session')
def filename():
    return 'test.fits'

@pytest.fixture(scope='session')
def data():
    return np.random.randint(0, 10, size=(100, 100))


@pytest.fixture
def hduname():
    return 'flux'


@pytest.yield_fixture
def hdulist(filename, tmpdir, data, hduname):
    fname = str(tmpdir.join(filename))
    with fitsio.FITS(fname, 'rw', clobber=True) as outfile:
        outfile.write(data, extname=hduname)
        yield outfile

@pytest.fixture
def chunker(hdulist, hduname):
    hdu = hdulist[hduname]
    return fitsioyielder.ChunkedAdapter(hdu)


def test_chunk_size(chunker):
    next_chunk = next(chunker(chunksize=10))
    assert next_chunk.shape[0] == 10



'''
Expected API

with fitsio.FITS(filename) as infile:
    hdu = infile['flux']
    chunker = fitsioyielder.ChunkedAdapter(hdu)
    for chunk in chunker(chunksize=10): # or chunker(memory_limit=2048)
        # do something with chunk
'''