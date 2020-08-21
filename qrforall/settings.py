from split_settings.tools import optional, include

include(
    'setting/base.py',
    optional('setting/development.py')
)
