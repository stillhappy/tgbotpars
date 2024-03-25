def process_strings(strings):
    result = []
    prev_values = None

    for s in strings:
        values, timestamp = s.split('|')
        val1, val2 = map(float, values.split())

        if prev_values is None:
            prev_values = [val1, val2]
            result.append(f"{val1:.3f}⚪ {val2:.3f}⚪|{timestamp[5:-3]}")
        else:
            val1_symbol = "🟢" if val1 > prev_values[0] else "🔴" if val1 < prev_values[0] else "⚪"
            val2_symbol = "🟢" if val2 > prev_values[1] else "🔴" if val2 < prev_values[1] else "⚪"
            result.append(f"{val1:.3f}{val1_symbol} {val2:.3f}{val2_symbol}|{timestamp[5:-3]}")
            prev_values = [val1, val2]

    return "\n".join(result)
