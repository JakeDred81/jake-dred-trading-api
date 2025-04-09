# scanner_output_parser.py

def format_scan_result(scan):
    try:
        indicators = scan.get("indicators", {})
        breakdown = scan.get("breakdown", {})
        playbook = scan.get("playbook", {})

        parts = [
            f"📊 {scan['ticker'].upper()}",
            f"Score: {scan['score']}",
            f"Recommendation: {scan['recommendation']}",
            f"Pattern: {scan.get('pattern', 'None')}",
            f"Catalyst: {scan.get('catalyst', 'None')}",
            f"Candle Pattern: {scan.get('candle_pattern', 'None')}",
            f"Indicators:" if indicators else ""
        ]

        for key, val in indicators.items():
            parts.append(f"  - {key}: {val}")

        parts.append("Breakdown:")
        for key, val in breakdown.items():
            parts.append(f"  - {key}: {val}")

        parts.append("Playbook:")
        parts.append(f"  - Entry: {playbook.get('entry', 'N/A')}")
        parts.append(f"  - Stop: {playbook.get('stop', 'N/A')}")
        parts.append(f"  - Target: {playbook.get('target', 'N/A')}")

        options = playbook.get("options", {})
        if options:
            parts.append("  - Options:")
            parts.append(f"     • Conservative: {options.get('conservative', 'N/A')}")
            parts.append(f"     • Aggressive: {options.get('aggressive', 'N/A')}")

        return "\n".join(parts)

    except Exception as e:
        return f"⚠️ Error formatting scan result: {str(e)}"
