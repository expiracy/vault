# JSON item report fixture

Task identifier: `count-json-items`. Standard-library task-tool fixture retained
from the original Vault integration pilot; it is not application code.

## Tools

| Detail | Contract |
| --- | --- |
| Source | [count_items.py](tools/count_items.py) |
| Inputs | [three items](inputs/items.json), a JSON array |
| Outputs | `outputs/count-report.json`, regenerated per invocation |
| Dependencies | Python 3.10 or later; standard library only |
| Effects | Reads its input and writes its requested output; no external state |

Working directory: this task directory.

```powershell
python tools/count_items.py --input inputs/items.json --output outputs/count-report.json
python tools/count_items.py --input inputs/items.json --output outputs/count-report.json --active-only
```

The reusable harness executes these arguments with its current Python interpreter.
Expected counts are three in default mode and two in active-only mode. It also
checks that invalid non-array input fails and does not replace an existing report.
