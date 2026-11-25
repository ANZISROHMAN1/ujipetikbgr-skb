#!/usr/bin/env python3
"""
Script to refresh data from Google Spreadsheet:
URL: https://docs.google.com/spreadsheets/d/1iCLX_scRmLAMwKrjOS2FkasGwB2q8NOtfzjxxYol8Ow/edit
Outputs: data.xlsx, dashboard_data.json
"""
import urllib.request
import openpyxl
import json
import os
import sys
from datetime import datetime

SPREADSHEET_ID = "1iCLX_scRmLAMwKrjOS2FkasGwB2q8NOtfzjxxYol8Ow"
EXPORT_URL = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/export?format=xlsx"

def download_data():
    print(f"[*] Downloading latest spreadsheet from Google Sheets...")
    req = urllib.request.Request(
        EXPORT_URL,
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    )
    try:
        with urllib.request.urlopen(req) as resp, open("data.xlsx", "wb") as f:
            f.write(resp.read())
        print("[+] Downloaded data.xlsx successfully.")
    except Exception as e:
        print(f"[!] Warning: Could not download directly ({e}). Using existing data.xlsx if present.")
        if not os.path.exists("data.xlsx"):
            print("[-] Error: data.xlsx not found.")
            sys.exit(1)

def parse_and_export():
    print("[*] Parsing data.xlsx...")
    wb = openpyxl.load_workbook("data.xlsx", data_only=True)
    
    # 1. ASSURANCE
    ws_ass = wb['UJI PETIK ASSURANCE']
    ass_sektors = []
    for r in range(5, 33):
        c1 = ws_ass.cell(r, 1).value
        c2 = ws_ass.cell(r, 2).value
        c3 = ws_ass.cell(r, 3).value
        c4 = ws_ass.cell(r, 4).value or 0
        c5 = ws_ass.cell(r, 5).value or 0
        c6 = ws_ass.cell(r, 6).value or 0
        c7 = ws_ass.cell(r, 7).value or 0
        is_subtotal = (c2 is None and c3 is None)
        ass_sektors.append({
            'row': r,
            'label': str(c1) if c1 is not None else '',
            'sektor': str(c2) if c2 else str(c1).strip(),
            'pic': str(c3).strip() if c3 else '',
            'sampling': int(c4) if isinstance(c4, (int, float)) else 0,
            'saldo': int(c5) if isinstance(c5, (int, float)) else 0,
            'done': int(c6) if isinstance(c6, (int, float)) else 0,
            'ach': round(float(c7) * 100, 2) if isinstance(c7, (int, float)) else 0,
            'is_subtotal': is_subtotal
        })

    ass_details = []
    for r in range(7, 32):
        no = ws_ass.cell(r, 9).value
        sektor = ws_ass.cell(r, 14).value
        if sektor:
            ass_details.append({
                'no': int(no) if isinstance(no, (int, float)) else len(ass_details) + 1,
                'sektor': str(sektor).strip(),
                'data_juli': int(ws_ass.cell(r, 15).value or 0),
                'jml_gaul': int(ws_ass.cell(r, 16).value or 0),
                'jml_hvc': int(ws_ass.cell(r, 17).value or 0),
                'sampling': int(ws_ass.cell(r, 18).value or 0),
                'sudah': int(ws_ass.cell(r, 19).value or 0),
                'belum': int(ws_ass.cell(r, 20).value or 0),
                'ok': int(ws_ass.cell(r, 21).value or 0),
                'nok': int(ws_ass.cell(r, 22).value or 0),
                'dispatch_sudah': int(ws_ass.cell(r, 23).value or 0),
                'dispatch_belum': int(ws_ass.cell(r, 24).value or 0),
                'eviden_proses': int(ws_ass.cell(r, 25).value or 0),
                'eviden_belum_appr': int(ws_ass.cell(r, 26).value or 0),
                'eviden_return': int(ws_ass.cell(r, 27).value or 0),
                'status': str(ws_ass.cell(r, 28).value or '').strip()
            })

    # 2. PSB
    ws_psb = wb['UJI PETIK PSB']
    psb_sto = []
    for r in range(7, 41):
        no = ws_psb.cell(r, 2).value
        sa = ws_psb.cell(r, 3).value
        pic = ws_psb.cell(r, 5).value
        sto = ws_psb.cell(r, 6).value
        samp = ws_psb.cell(r, 7).value or 0
        done = ws_psb.cell(r, 8).value or 0
        saldo = ws_psb.cell(r, 9).value or 0
        qc = ws_psb.cell(r, 10).value or 0
        ach = ws_psb.cell(r, 11).value or 0
        if sto:
            psb_sto.append({
                'no': int(no) if isinstance(no, (int, float)) else len(psb_sto) + 1,
                'sa': str(sa).strip(),
                'pic': str(pic).strip(),
                'sto': str(sto).strip(),
                'sampling': int(samp),
                'done': int(done),
                'saldo': int(saldo),
                'qc': round(float(qc) * 100, 2),
                'ach': round(float(ach) * 100, 2)
            })

    psb_sa = []
    for r in range(7, 19):
        sa_name = ws_psb.cell(r, 13).value
        samp = ws_psb.cell(r, 14).value or 0
        done = ws_psb.cell(r, 15).value or 0
        saldo = ws_psb.cell(r, 16).value or 0
        qc = ws_psb.cell(r, 17).value or 0
        ach = ws_psb.cell(r, 18).value or 0
        if sa_name:
            psb_sa.append({
                'sa': str(sa_name).strip(),
                'sampling': int(samp),
                'done': int(done),
                'saldo': int(saldo),
                'qc': round(float(qc) * 100, 2),
                'ach': round(float(ach) * 100, 2)
            })

    psb_details = []
    for r in range(7, 41):
        no = ws_psb.cell(r, 28).value
        sto = ws_psb.cell(r, 33).value
        if sto:
            psb_details.append({
                'no': int(no) if isinstance(no, (int, float)) else len(psb_details) + 1,
                'sto': str(sto).strip(),
                'populasi_sept': int(ws_psb.cell(r, 34).value or 0),
                'undspec': int(ws_psb.cell(r, 35).value or 0),
                'ffg': int(ws_psb.cell(r, 36).value or 0),
                'hvc': int(ws_psb.cell(r, 37).value or 0),
                'sampling': int(ws_psb.cell(r, 38).value or 0),
                'sudah': int(ws_psb.cell(r, 39).value or 0),
                'belum': int(ws_psb.cell(r, 40).value or 0),
                'ok': int(ws_psb.cell(r, 41).value or 0),
                'nok_hvc': int(ws_psb.cell(r, 42).value or 0),
                'nok_total': int(ws_psb.cell(r, 43).value or 0),
                'nok_history': int(ws_psb.cell(r, 44).value or 0),
                'dispatch_sudah': int(ws_psb.cell(r, 45).value or 0),
                'dispatch_belum': int(ws_psb.cell(r, 46).value or 0),
                'eviden_proses': int(ws_psb.cell(r, 47).value or 0),
                'eviden_belum_appr': int(ws_psb.cell(r, 48).value or 0),
                'eviden_return': int(ws_psb.cell(r, 49).value or 0),
                'pct_ujipetik': round(float(ws_psb.cell(r, 50).value or 0) * 100, 2),
                'pct_ok': round(float(ws_psb.cell(r, 51).value or 0) * 100, 2),
                'status': str(ws_psb.cell(r, 53).value or '').strip()
            })

    clean_ass_sektors = [s for s in ass_sektors if not s['is_subtotal']]
    ass_groups = []
    for s in ass_sektors:
        lbl = s['label'].strip()
        if s['is_subtotal'] and lbl and lbl != 'WITEL BOGOR':
            ass_groups.append({
                'name': lbl,
                'sampling': s['sampling'],
                'saldo': s['saldo'],
                'done': s['done'],
                'ach': s['ach']
            })

    tot_ass_samp = sum(s['sampling'] for s in clean_ass_sektors)
    tot_ass_done = sum(s['done'] for s in clean_ass_sektors)
    tot_ass_saldo = sum(s['saldo'] for s in clean_ass_sektors)
    tot_ass_ach = round((tot_ass_done / tot_ass_samp) * 100, 2) if tot_ass_samp > 0 else 0

    tot_psb_samp = sum(s['sampling'] for s in psb_sto)
    tot_psb_done = sum(s['done'] for s in psb_sto)
    tot_psb_saldo = sum(s['saldo'] for s in psb_sto)
    tot_psb_ach = round((tot_psb_done / tot_psb_samp) * 100, 2) if tot_psb_samp > 0 else 0

    output_data = {
        'meta': {
            'title': 'DASHBOARD MONITORING UJI PETIK DISTRICT BOGOR',
            'district': 'BOGOR',
            'regional': 'EASTERN JABOTABEK',
            'refreshed_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'source_spreadsheet': 'https://docs.google.com/spreadsheets/d/' + SPREADSHEET_ID + '/edit'
        },
        'assurance': {
            'total': {'sampling': tot_ass_samp, 'saldo': tot_ass_saldo, 'done': tot_ass_done, 'ach': tot_ass_ach},
            'groups': ass_groups if ass_groups else [
                {'name': 'CIBINONG', 'sampling': 67, 'saldo': 1, 'done': 66, 'ach': 98.51},
                {'name': 'KUJANG', 'sampling': 104, 'saldo': 3, 'done': 101, 'ach': 97.12},
                {'name': 'SENTUL', 'sampling': 50, 'saldo': 0, 'done': 50, 'ach': 100.00},
                {'name': 'SUKABUMI', 'sampling': 40, 'saldo': 12, 'done': 28, 'ach': 70.00}
            ],
            'sektors': clean_ass_sektors,
            'details': ass_details
        },
        'psb': {
            'total': {'sampling': tot_psb_samp, 'saldo': tot_psb_saldo, 'done': tot_psb_done, 'ach': tot_psb_ach},
            'sa_summary': psb_sa,
            'sto_list': psb_sto,
            'details': psb_details
        }
    }

    with open("dashboard_data.json", "w") as f:
        json.dump(output_data, f, indent=2)

    print("[+] dashboard_data.json updated successfully!")

if __name__ == "__main__":
    if "--no-download" not in sys.argv:
        download_data()
    parse_and_export()
