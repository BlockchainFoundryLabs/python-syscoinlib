# Copyright (C) 2012-2016 The python-syscoinlib developers
#
# This file is part of python-syscoinlib.
#
# It is subject to the license terms in the LICENSE file found in the top-level
# directory of this distribution.
#
# No part of python-syscoinlib, including this file, may be copied, modified,
# propagated, or distributed except according to the terms contained in the
# LICENSE file.

from __future__ import absolute_import, division, print_function, unicode_literals

import syscoin.core

# Note that setup.py can break if __init__.py imports any external
# dependencies, as these might not be installed when setup.py runs. In this
# case __version__ could be moved to a separate version.py and imported here.
__version__ = '0.7.2'

class MainParams(syscoin.core.CoreMainParams):
    MESSAGE_START = b'\xf9\xbe\xb4\xd9'
    DEFAULT_PORT = 8369
    RPC_PORT = 8368
    DNS_SEEDS = ()
    BASE58_PREFIXES = {'PUBKEY_ADDR':63,
                       'SCRIPT_ADDR':5,
                       'SECRET_KEY' :128}

class TestNetParams(syscoin.core.CoreTestNetParams):
    MESSAGE_START = b'\xce\xe2\xca\xff'
    DEFAULT_PORT = 18369
    RPC_PORT = 18368
    DNS_SEEDS = ()
    BASE58_PREFIXES = {'PUBKEY_ADDR':65,
                       'SCRIPT_ADDR':196,
                       'SECRET_KEY' :239}

class RegTestParams(syscoin.core.CoreRegTestParams):
    MESSAGE_START = b'\xe2\xca\xff\xce'
    DEFAULT_PORT = 18369
    RPC_PORT = 18368
    DNS_SEEDS = ()
    BASE58_PREFIXES = {'PUBKEY_ADDR':65,
                       'SCRIPT_ADDR':196,
                       'SECRET_KEY' :239}

"""Master global setting for what chain params we're using.

However, don't set this directly, use SelectParams() instead so as to set the
syscoin.core.params correctly too.
"""
#params = syscoin.core.coreparams = MainParams()
params = MainParams()

def SelectParams(name):
    """Select the chain parameters to use

    name is one of 'mainnet', 'testnet', or 'regtest'

    Default chain is 'mainnet'
    """
    global params
    syscoin.core._SelectCoreParams(name)
    if name == 'mainnet':
        params = syscoin.core.coreparams = MainParams()
    elif name == 'testnet':
        params = syscoin.core.coreparams = TestNetParams()
    elif name == 'regtest':
        params = syscoin.core.coreparams = RegTestParams()
    else:
        raise ValueError('Unknown chain %r' % name)
