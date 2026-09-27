#!/usr/bin/env python3
"""
main.py — jpxtrading.id WebCloner
==================================
Clone the publicly visible appearance of a website into
a local static snapshot for educational purposes.
"""

import argparse
import os
import sys
import re
from urllib.parse import urlparse

from core.cloner import SiteCloner
from utils.logger import setup_logger

log = setup_logger("main")

# --------------------------------------------------
# Metadata
# --------------------------------------------------
APP_NAME = "jpxtrading.id WebCloner"
VERSION = "v1.0.0"
AUTHOR = "jpXCode"
GITHUB = "https://jpxcode.pages.dev"
TELEGRAM = "https://t.me/+QfMZP1CygAM3MDA1"

# --------------------------------------------------
# ANSI Colors
# --------------------------------------------------
RED = "\033[91m"
GRAY = "\033[90m"
RESET = "\033[0m"

# --------------------------------------------------
# Banner
# --------------------------------------------------
BANNER = r"""
▄▄▌ ▐ ▄▌▄▄▄ .▄▄▄▄·  ▄▄· ▄▄▌         ▐ ▄ ▄▄▄ .▄▄▄  
██· █▌▐█▀▄.▀·▐█ ▀█▪▐█ ▌▪██•  ▪     •█▌▐█▀▄.▀·▀▄ █·
██▪▐█▐▐▌▐▀▀▪▄▐█▀▀█▄██ ▄▄██▪   ▄█▀▄ ▐█▐▐▌▐▀▀▪▄▐▀▀▄ 
▐█▌██▐█▌▐█▄▄▌██▄▪▐█▐███▌▐█▌▐▌▐█▌.▐▌██▐█▌▐█▄▄▌▐█•█▌
 ▀▀▀▀ ▀▪ ▀▀▀ ·▀▀▀▀ ·▀▀▀ .▀▀▀  ▀█▄▀▪▀▀ █▪ ▀▀▀ .▀  ▀
                                                                                                                           
"""

# --------------------------------------------------
# Banner Printer
# --------------------------------------------------
def print_banner():
    print(RED + BANNER + RESET)

    print(GRAY + f" Tool    : {APP_NAME}" + RESET)
    print(GRAY + f" Version : {VERSION}" + RESET)
    print(GRAY + f" Author  : {AUTHOR}" + RESET)
    print(GRAY + f" Website : {GITHUB}" + RESET)
    print(GRAY + f" Telegram: {TELEGRAM}" + RESET)

    print(GRAY + """
 DISCLAIMER
 ----------
 This software is created strictly for educational purposes.
 Visual website replication is intended only for learning UI/UX concepts.

 Real cloning, scraping protected content, or unauthorized data extraction
 may be illegal. The author does not take responsibility for misuse.
""" + RESET)


# --------------------------------------------------
# Argument Parser
# --------------------------------------------------
def build_parser():
    parser = argparse.ArgumentParser(
        prog="webcloner",
        description="Clone the visual appearance of a website into a static bundle.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "url",
        nargs="?",
        help="Starting URL (must start with http:// or https://)"
    )

    parser.add_argument("--version", action="store_true",
                        help="Show program version")

    parser.add_argument("--about", action="store_true",
                        help="Show program information")

    parser.add_argument("--output", "-o",
                        default="./output",
                        metavar="DIR",
                        help="Root output directory")

    parser.add_argument("--max-pages", "-m",
                        type=int,
                        default=0,
                        metavar="N",
                        help="Max pages to crawl (0 = unlimited)")

    parser.add_argument("--delay",
                        type=float,
                        default=0.5,
                        metavar="SEC",
                        help="Delay between requests")

    parser.add_argument("--dynamic", "-d",
                        action="store_true",
                        help="Use Playwright for JS-rendered sites")

    parser.add_argument("--timeout", "-t",
                        type=int,
                        default=15,
                        metavar="SEC",
                        help="Request timeout")

    parser.add_argument("--inline",
                        action="store_true",
                        help="Inline CSS into HTML")

    return parser


# --------------------------------------------------
# Main Logic
# --------------------------------------------------
def main():
    parser = build_parser()
    args = parser.parse_args()

    # ---- Version flag ----
    if args.version:
        print(f"{APP_NAME} {VERSION}")
        sys.exit(0)

    # ---- About flag ----
    if args.about:
        print_banner()
        sys.exit(0)

    # ---- No arguments ----
    if not args.url:
        print_banner()
        parser.print_help()
        sys.exit(0)

    # ---- Validate URL ----
    if not args.url.startswith(("http://", "https://")):
        log.error("URL must start with http:// or https://")
        sys.exit(1)

    # ---- Startup banner ----
    print_banner()

    # ---- Configuration summary ----
    log.info(f"URL        : {args.url}")
    log.info(f"Output     : {os.path.abspath(args.output)}")
    log.info(f"Max pages  : {args.max_pages or 'unlimited'}")
    log.info(f"Delay      : {args.delay}s")
    log.info(f"Renderer   : {'Playwright (JS)' if args.dynamic else 'requests'}")
    log.info(f"CSS mode   : {'inline' if args.inline else 'styles.css'}")
    print()

    # ---- Run Cloner ----
    cloner = SiteCloner(
        url=args.url,
        output_root=args.output,
        max_pages=args.max_pages,
        delay=args.delay,
        use_playwright=args.dynamic,
        timeout=args.timeout,
        inline_css=args.inline,
    )

    ok = cloner.run()

    if ok:
        domain = re.sub(r"^www\.", "", urlparse(args.url).netloc)
        site_dir = os.path.join(os.path.abspath(args.output), domain)
        index_file = os.path.join(site_dir, "index.html")

        print()
        log.info("✅ Done!")
        log.info(f"📁 Site folder : {site_dir}")
        log.info(f"🌐 Open        : {index_file}")
        log.info(f"📄 Report      : {os.path.join(site_dir, '_cloner_report.txt')}")
    else:
        log.error("❌ Failed — see messages above.")
        sys.exit(1)


# --------------------------------------------------
# Entry Point
# --------------------------------------------------
if __name__ == "__main__":
    main()