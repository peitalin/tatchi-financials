from __future__ import annotations

import argparse
from typing import Callable
from typing import Optional
from typing import Sequence

from pipeline import generate_wallet_financial_bundle_main
from pipeline import plot_wallet_financial_projections_main
from pipeline import wallet_financial_revenues_main

CommandFn = Callable[[Optional[Sequence[str]]], int]


COMMANDS: dict[str, CommandFn] = {
    "bundle": generate_wallet_financial_bundle_main,
    "revenues": wallet_financial_revenues_main,
    "plot": plot_wallet_financial_projections_main,
}


def _parse_args(argv: Sequence[str] | None = None) -> tuple[str, list[str]]:
    parser = argparse.ArgumentParser(
        description="Entrypoint for wallet financial workbook generation and chart rendering."
    )
    parser.add_argument(
        "command",
        choices=tuple(COMMANDS.keys()),
        help="Subcommand to run: bundle | revenues | plot",
    )
    args, passthrough = parser.parse_known_args(argv)
    return args.command, passthrough


def main(argv: Sequence[str] | None = None) -> int:
    command, passthrough = _parse_args(argv)
    return int(COMMANDS[command](passthrough))


if __name__ == "__main__":
    raise SystemExit(main())
