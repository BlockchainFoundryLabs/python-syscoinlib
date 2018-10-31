# Copyright (C) 2013-2015 The python-syscoinlib developers
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

from syscoin.core.key import CPubKey
from syscoin.core.serialize import ImmutableSerializable
from syscoin.wallet import P2PKHSyscoinAddress
import syscoin
import base64
import sys

_bchr = chr
_bord = ord
if sys.version > '3':
    long = int
    _bchr = lambda x: bytes([x])
    _bord = lambda x: x


def VerifyMessage(address, message, sig):
    sig = base64.b64decode(sig)
    hash = message.GetHash()

    pubkey = CPubKey.recover_compact(hash, sig)

    return str(P2PKHSyscoinAddress.from_pubkey(pubkey)) == str(address)


def SignMessage(key, message):
    sig, i = key.sign_compact(message.GetHash())

    meta = 27 + i
    if key.is_compressed:
        meta += 4

    return base64.b64encode(_bchr(meta) + sig)


class SyscoinMessage(ImmutableSerializable):
    __slots__ = ['magic', 'message']

    def __init__(self, message="", magic="Syscoin Signed Message:\n"):
        object.__setattr__(self, 'message', message.encode("utf-8"))
        object.__setattr__(self, 'magic', magic.encode("utf-8"))

    @classmethod
    def stream_deserialize(cls, f):
        magic = syscoin.core.serialize.BytesSerializer.stream_deserialize(f)
        message = syscoin.core.serialize.BytesSerializer.stream_deserialize(f)
        return cls(message, magic)

    def stream_serialize(self, f):
        syscoin.core.serialize.BytesSerializer.stream_serialize(self.magic, f)
        syscoin.core.serialize.BytesSerializer.stream_serialize(self.message, f)

    def __str__(self):
        return self.message.decode('ascii')

    def __repr__(self):
        return 'SyscoinMessage(%s, %s)' % (self.magic, self.message)