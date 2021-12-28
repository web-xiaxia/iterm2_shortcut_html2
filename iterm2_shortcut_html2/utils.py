# -*- coding: utf-8 -*-
import iterm2
import json
import typing
from functools import wraps


def singleton(f):
    instance = {}

    @wraps(f)
    def get_instance(*args, **kwargs):
        if f not in instance:
            instance[f] = f(*args, **kwargs)
        return instance[f]

    return get_instance


async def alert(connection: iterm2.connection.Connection, title='', subtitle='', buttons=None) -> int:
    if not buttons:
        buttons = []
    buttons = json.dumps(buttons)

    return await iterm2.async_invoke_function(
        connection,
        (f'iterm2.alert(title: {title}, ' +
         f'subtitle: {subtitle}, ' +
         f'buttons: {buttons}, ' +
         f'window_id: {json.dumps(None)})'))


async def prompt(connection: iterm2.connection.Connection, title='', subtitle='', placeholder='',
                 default_value='') -> typing.Optional[str]:
    return await iterm2.async_invoke_function(
        connection,
        (f'iterm2.get_string(title: {title}, ' +
         f'subtitle: {subtitle}, ' +
         f'placeholder: {placeholder}, ' +
         f'defaultValue: {default_value}, ' +
         f'window_id: {json.dumps(None)})'))
