import sys
import logging
import jinja2.filters

from ..kore import KoreCli, KoreKreator,  AppDef
from ..kore._korecli import argument as argument
from ..kore._appdef import b64encode
from . import _krypt

logger = logging.getLogger(__name__)
class KryptKreator(KoreKreator):
    def kreate_cli(self):
        return KryptCli(self)

    def tune_appdef(self, appdef: AppDef):
        appdef.values["dekrypt"] = _krypt.dekrypt_str
        _krypt._krypt_key = b64encode(
            appdef.yaml.get(
                "krypt_key",
                "no-krypt-key-defined"))

class KryptCli(KoreCli):
    def __init__(self, kreator):
        jinja2.filters.FILTERS["dekrypt"] = _krypt.dekrypt_str
        super().__init__(kreator)
        self.add_subcommand(dekyaml, [argument(
            "-f", "--file", help="yaml file to enkrypt")],
            aliases=["dy"])
        self.add_subcommand(dekstr, [argument(
            "-s", "--str", help="string value to dekrypt")],
            aliases=["ds"])
        self.add_subcommand(dekfile, [argument(
            "file", help=" filename to dekrypt")],
            aliases=["df"])
        self.add_subcommand(enkyaml, [argument(
            "-f", "--file", help="yaml filename to enkrypt")],
            aliases=["ey"])
        self.add_subcommand(enkfile, [argument(
            "file", help=" filename to enkrypt")],
            aliases=["ef"])
        self.add_subcommand(enkstr, [argument(
            "-s", "--str", help="string value to enkrypt")],
            aliases=["es"])


def dekyaml(cli):
    """dekrypt values in a yaml file"""
    appdef: AppDef = cli.kreator.kreate_appdef(cli.args.appdef)

    filename = (cli.args.file or
                f"{appdef.dir}/secrets-{appdef.name}-{appdef.env}.yaml")
    _krypt.dekrypt_yaml(filename, ".")


def dekstr(cli):
    """dekrypt string value"""
    cli.kreator.kreate_appdef(cli.args.appdef)
    value = cli.args.str
    if not value:
        if not cli.args.quiet:
            print("Enter string to dekrypt")
        value = sys.stdin.readline().strip()
    print(_krypt.dekrypt_str(value))


def dekfile(cli):
    "dekrypt an entire file"
    cli.kreator.kreate_appdef(cli.args.appdef)
    filename = cli.args.file
    _krypt.dekrypt_file(filename)


def enkyaml(cli):
    "enkrypt values in a yaml file"
    appdef: AppDef = cli.kreator.kreate_appdef(cli.args.appdef)
    filename = (cli.args.file
                or f"{appdef.dir}/secrets-{appdef.name}-{appdef.env}.yaml")
    _krypt.enkrypt_yaml(filename, ".")


def enkfile(cli):
    "enkrypt an entire file"
    cli.kreator.kreate_appdef(cli.args.appdef)
    filename = cli.args.file
    _krypt.enkrypt_file(filename)


def enkstr(cli):
    """enkrypt string value"""
    cli.kreator.kreate_appdef(cli.args.appdef)
    value = cli.args.str
    if not value:
        if not cli.args.quiet:
            print("Enter string to enkrypt")
        value = sys.stdin.readline().strip()
    print(_krypt.enkrypt_str(value))
