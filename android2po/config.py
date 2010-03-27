from os import path
import argparse


__all__ = ('Config',)


class Config(object):
    """Defines all the options supported by our configuration system.
    """
    OPTIONS = (
        {'name': 'android',
         'help': 'Android resource directory ($PROJECT/res by default)',
         'dest': 'resource_dir',
         'kwargs': {'metavar': 'DIR',}
         # No default, and will not actually be stored on the config object.
        },
        {'name': 'gettext',
         'help': 'directory containing the .po files ($PROJECT/locale by default)',
         'dest': 'gettext_dir',
         'kwargs': {'metavar': 'DIR',}
         # No default, and will not actually be stored on the config object.
        },
        {'name': 'no-template',
         'help': 'do not generate a .pot template file on export',
         'dest': 'no_template',
         'default': False,
         'kwargs': {'action': 'store_true',}
        },
        {'name': 'template',
         'help': 'filename to use for the .pot file(s); may contain %%s to be '+
                 'replaced with the xml kind',
         'dest': 'template_name',
         'default': 'template.pot',
         'kwargs': {'metavar': 'NAME',}
        },
    )

    def __init__(self):
        """Initialize all configuration values with a default.

        It is important that we do this here manually, rather than relying
        on the "default" mechanism of argparse, because we have multiple
        potential congiguration sources (command line, config file), and
        we don't want defaults to override actual values.

        The attributes we define here are also used to determine
        which command line options passed should be assigned to this
        object, and which should be exposed via a separate ``options``
        namespace.
        """
        for optdef in self.OPTIONS:
            if 'default' in optdef:
                setattr(self, optdef['dest'], optdef['default'])

    @classmethod
    def setup_arguments(cls, parser):
        """Setup our configuration values as arguments in the ``argparse``
        object in ``parser``.
        """
        for optdef in cls.OPTIONS:
            names = ('--%s' % optdef.get('name'),)
            kwargs = {
                'help': optdef.get('help', None),
                'dest': optdef.get('dest', None),
                # We handle defaults ourselves. This is actually important,
                # or defaults from one config source may override valid
                # values from another.
                'default': argparse.SUPPRESS,
            }
            kwargs.update(optdef.get('kwargs', {}))
            parser.add_argument(*names, **kwargs)

    @classmethod
    def rebase_paths(cls, config, base_path):
        """Make those config values that are paths relative to
        ``base_path``, because by default, paths are relative to
        the current working directory.
        """
        for name in ('gettext_dir', 'resource_dir'):
            value = getattr(config, name, None)
            if value is not None:
                setattr(config, name, path.normpath(path.join(base_path, value)))