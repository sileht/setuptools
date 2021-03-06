import re

from paver.easy import task, path as Path
import pip


def remove_all(paths):
    for path in paths:
        path.rmtree() if path.isdir() else path.remove()


@task
def update_vendored():
    vendor = Path('pkg_resources/_vendor')
    remove_all(vendor.glob('packaging*'))
    remove_all(vendor.glob('six*'))
    remove_all(vendor.glob('pyparsing*'))
    install_args = [
        'install',
        '-r', str(vendor / 'vendored.txt'),
        '-t', str(vendor),
    ]
    pip.main(install_args)
    packaging = vendor / 'packaging'
    for file in packaging.glob('*.py'):
        text = file.text()
        text = re.sub(r' (pyparsing|six)', r' pkg_resources.extern.\1', text)
        file.write_text(text)
    remove_all(vendor.glob('*.dist-info'))
    remove_all(vendor.glob('*.egg-info'))
