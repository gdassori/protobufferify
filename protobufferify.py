from decimal import Decimal
from google.protobuf.internal.containers import BaseContainer
from google.protobuf.message import Message
from google.protobuf.reflection import GeneratedProtocolMessageType


def is_protobuf(data) -> bool:
    return isinstance(data, Message)


def unprotobufferify(protobuf_obj) -> dict:
    if isinstance(protobuf_obj, Message):
        ed = {}
        fields = protobuf_obj.ListFields()
        for field in fields:
            ed[field[0].name] = unprotobufferify(field[1])
        return ed
    elif isinstance(protobuf_obj, BaseContainer):
        data = []
        for element in protobuf_obj:
            ed = unprotobufferify(element)
            data.append(ed)
        return data
    else:
        return protobuf_obj


def protobufferify(data: dict, protobuf_obj: Message):
    o = protobuf_obj() if isinstance(protobuf_obj, GeneratedProtocolMessageType) \
        else protobuf_obj
    for field in data:
        if isinstance(data[field], list):
            for i in data[field]:
                try:
                    getattr(o, field).add()
                    protobufferify(i, getattr(o, field)[-1])
                except AttributeError:
                    getattr(o, field).append(i)
        elif isinstance(data[field], dict):
            protobufferify(data[field], getattr(o, field))
        elif isinstance(data[field], Decimal):
            setattr(o, field, float(data[field]))
        else:
            setattr(o, field, data[field])
    o.SerializeToString()
    return o
