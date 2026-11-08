#!/usr/bin/env python3
"""Print sheet names, header rows and a few sample rows of a workbook (for writing parsers)."""
import sys, openpyxl
for f in sys.argv[1:]:
    wb = openpyxl.load_workbook(f, read_only=True, data_only=True)
    print("FILE", f, wb.sheetnames)
    for sn in wb.sheetnames[:12]:
        ws = wb[sn]; rows = []
        for i, r in enumerate(ws.iter_rows(values_only=True)):
            rows.append(r)
            if i >= 6: break
        print("== SHEET", sn)
        for r in rows: print("   ", [x for x in r[:40]])
