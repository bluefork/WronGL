"""Command Line Interface for WronGL."""
from __future__ import annotations

import argparse
import sys
from wrongl.core.converter import Converter
from wrongl.core.detector import detect, should_auto_convert

def main() -> int:
    parser = argparse.ArgumentParser(description="WronGL — Smart layout converter CLI")
    parser.add_argument("text", nargs="?", help="Text to convert. If omitted, reads from stdin.")
    parser.add_argument("-d", "--direction", choices=["en2fa", "fa2en", "auto"], default="auto")
    parser.add_argument("-n", "--digits", action="store_true", help="Convert digits")
    
    args = parser.parse_args()
    
    text = args.text
    if not text:
        if not sys.stdin.isatty():
            text = sys.stdin.read().strip()
        else:
            parser.print_help()
            return 1
            
    if not text:
        return 0

    direction = args.direction
    if direction == "auto":
        r = detect(text)
        if not should_auto_convert(r):
            print(f"Warning: Low confidence ({r.confidence:.2f}). Assuming {r.direction}.", file=sys.stderr)
        direction = r.direction

    conv = Converter(convert_digits=args.digits, normalize_arabic=True)
    result = conv.en_to_fa(text) if direction == "en2fa" else conv.fa_to_en(text)
    
    print(result)
    return 0

if __name__ == "__main__":
    sys.exit(main())