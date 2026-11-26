import json
import os

with open('dashboard_data.json', 'r', encoding='utf-8') as f:
    data_json = f.read()

data_dict = json.loads(data_json)
tot_ass = data_dict['assurance']['total']
tot_psb = data_dict['psb']['total']
tot_samp = tot_ass['sampling'] + tot_psb['sampling']
tot_done = tot_ass['done'] + tot_psb['done']
tot_saldo = tot_ass['saldo'] + tot_psb['saldo']
tot_ach = round(tot_done / tot_samp * 100, 2) if tot_samp > 0 else 0
saldo_pct = round(tot_saldo / tot_samp * 100, 2) if tot_samp > 0 else 0
refreshed_at = data_dict.get('meta', {}).get('refreshed_at', '26 Nov 2026')
gauge_offset = round(502.65 - (502.65 * tot_ach) / 100, 2)

html_content = f'''<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Dashboard Monitoring Uji Petik - District Bogor & Sukabumi</title>
  <link rel="icon" type="image/x-icon" href="favicon.ico">
  <link rel="icon" type="image/png" sizes="32x32" href="favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="64x64" href="favicon.png">
  <link rel="apple-touch-icon" href="favicon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <script src="html2canvas.min.js"></script>
  <style>
    :root {{
      --bg: #070a12;
      --bg-subtle: #0d121f;
      --card-bg: rgba(17, 24, 39, 0.75);
      --card-solid: #111827;
      --card-border: rgba(255, 255, 255, 0.08);
      --card-hover: rgba(30, 41, 59, 0.85);
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
      --primary: #3b82f6;
      --primary-hover: #2563eb;
      --primary-gradient: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
      --primary-glow: rgba(59, 130, 246, 0.25);
      --success: #10b981;
      --success-gradient: linear-gradient(135deg, #10b981 0%, #059669 100%);
      --success-glow: rgba(16, 185, 129, 0.25);
      --warning: #f59e0b;
      --warning-gradient: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
      --warning-glow: rgba(245, 158, 11, 0.25);
      --danger: #ef4444;
      --danger-gradient: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
      --danger-glow: rgba(239, 68, 68, 0.25);
      --accent: #8b5cf6;
      --accent-gradient: linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%);
      --telkom-red: #f43f5e;
      --header-bg: linear-gradient(135deg, rgba(15, 23, 42, 0.85) 0%, rgba(13, 18, 31, 0.95) 100%);
      --chart-track: rgba(255, 255, 255, 0.06);
      --input-bg: rgba(15, 23, 42, 0.8);
      --input-border: rgba(255, 255, 255, 0.12);
      --table-head: rgba(15, 23, 42, 0.9);
      --table-head-border: rgba(255, 255, 255, 0.08);
      --table-row-border: rgba(255, 255, 255, 0.05);
      --table-row-hover: rgba(59, 130, 246, 0.06);
      --stat-box-bg: rgba(15, 23, 42, 0.6);
      --glass-shadow: 0 16px 36px -10px rgba(0, 0, 0, 0.6);
    }}

    body.light-theme {{
      --bg: #f8fafc;
      --bg-subtle: #f1f5f9;
      --card-bg: rgba(255, 255, 255, 0.85);
      --card-solid: #ffffff;
      --card-border: rgba(0, 0, 0, 0.07);
      --card-hover: #ffffff;
      --text-main: #0f172a;
      --text-muted: #475569;
      --text-dim: #94a3b8;
      --primary: #2563eb;
      --primary-hover: #1d4ed8;
      --primary-gradient: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
      --primary-glow: rgba(37, 99, 235, 0.16);
      --success: #059669;
      --success-gradient: linear-gradient(135deg, #10b981 0%, #059669 100%);
      --success-glow: rgba(5, 150, 105, 0.16);
      --warning: #d97706;
      --warning-gradient: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
      --warning-glow: rgba(217, 119, 6, 0.16);
      --danger: #dc2626;
      --danger-gradient: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
      --danger-glow: rgba(220, 38, 38, 0.16);
      --accent: #7c3aed;
      --accent-gradient: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
      --header-bg: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
      --chart-track: #e2e8f0;
      --input-bg: #ffffff;
      --input-border: #cbd5e1;
      --table-head: #f1f5f9;
      --table-head-border: #e2e8f0;
      --table-row-border: #f1f5f9;
      --table-row-hover: #f1f5f9;
      --stat-box-bg: #f8fafc;
      --glass-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.06);
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background-color: var(--bg);
      color: var(--text-main);
      min-height: 100vh;
      line-height: 1.5;
      padding-bottom: 80px;
      transition: background-color 0.3s cubic-bezier(0.4, 0, 0.2, 1), color 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      background-image: 
        radial-gradient(at 0% 0%, rgba(59, 130, 246, 0.08) 0px, transparent 50%),
        radial-gradient(at 100% 0%, rgba(244, 63, 94, 0.06) 0px, transparent 50%),
        radial-gradient(at 50% 100%, rgba(139, 92, 246, 0.06) 0px, transparent 50%);
      background-attachment: fixed;
    }}

    .container {{
      max-width: 1440px;
      margin: 0 auto;
      padding: 24px 20px;
    }}

    /* HEADER */
    .header {{
      background: var(--header-bg);
      border: 1px solid var(--card-border);
      border-radius: 20px;
      padding: 18px 26px;
      margin-bottom: 24px;
      display: flex;
      flex-wrap: nowrap;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      box-shadow: var(--glass-shadow);
      backdrop-filter: blur(16px);
      position: relative;
      overflow: hidden;
    }}

    .header::before {{
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 3px;
      background: linear-gradient(90deg, #f43f5e 0%, #3b82f6 50%, #10b981 100%);
    }}

    .header-branding {{
      display: flex;
      align-items: center;
      gap: 16px;
    }}

    .header-logo-chip {{
      width: 48px;
      height: 48px;
      border-radius: 14px;
      background: linear-gradient(135deg, #f43f5e 0%, #e11d48 100%);
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      font-weight: 900;
      font-size: 20px;
      box-shadow: 0 8px 18px rgba(244, 63, 94, 0.35);
      flex-shrink: 0;
    }}

    .header-logo-img {{
      width: 60px;
      height: 60px;
      object-fit: contain;
      filter: drop-shadow(0 6px 14px rgba(0, 0, 0, 0.45));
      flex-shrink: 0;
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }}

    .header-logo-img:hover {{
      transform: scale(1.08);
      filter: drop-shadow(0 8px 18px rgba(244, 63, 94, 0.4));
    }}

    .header-badge {{
      background: linear-gradient(135deg, rgba(244, 63, 94, 0.15), rgba(225, 29, 72, 0.08));
      border: 1px solid rgba(244, 63, 94, 0.3);
      color: #fb7185;
      font-size: 11px;
      font-weight: 800;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      padding: 4px 10px;
      border-radius: 999px;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }}

    body.light-theme .header-badge {{
      background: #ffe4e6;
      color: #e11d48;
      border-color: #fecdd3;
    }}

    .header-badge::before {{
      content: '';
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background-color: currentColor;
      animation: pulse 1.8s infinite;
    }}

    @keyframes pulse {{
      0%, 100% {{ opacity: 1; transform: scale(1); }}
      50% {{ opacity: 0.4; transform: scale(0.85); }}
    }}

    h1 {{
      font-size: 25px;
      font-weight: 800;
      letter-spacing: -0.03em;
      color: var(--text-main);
      margin-top: 4px;
    }}

    .header-subtitle {{
      font-size: 13px;
      color: var(--text-muted);
      margin-top: 3px;
      display: flex;
      gap: 12px;
      align-items: center;
      flex-wrap: wrap;
    }}

    .header-subtitle strong {{
      color: var(--text-main);
    }}

    .header-actions {{
      display: flex;
      align-items: center;
      gap: 8px;
      flex-shrink: 0;
    }}

    .btn {{
      padding: 9px 15px;
      border-radius: 12px;
      font-size: 12.5px;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
      text-decoration: none;
      border: 1px solid transparent;
      user-select: none;
      box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
      white-space: nowrap;
    }}

    .btn:active {{
      transform: scale(0.97);
    }}

    .btn-primary {{
      background: var(--primary-gradient);
      color: white;
      box-shadow: 0 4px 14px var(--primary-glow);
    }}

    .btn-primary:hover {{
      transform: translateY(-2px);
      box-shadow: 0 6px 20px var(--primary-glow);
    }}

    .btn-success {{
      background: var(--success-gradient);
      color: white;
      box-shadow: 0 4px 14px var(--success-glow);
    }}

    .btn-success:hover {{
      transform: translateY(-2px);
      box-shadow: 0 6px 20px var(--success-glow);
    }}

    .btn-outline {{
      background: var(--card-bg);
      border-color: var(--card-border);
      color: var(--text-main);
      backdrop-filter: blur(8px);
    }}

    .btn-outline:hover {{
      background: var(--card-hover);
      border-color: var(--primary);
      transform: translateY(-2px);
    }}

    .btn-theme {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      color: var(--text-main);
      border-radius: 12px;
      padding: 10px 14px;
      cursor: pointer;
      font-weight: 700;
      font-size: 13px;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.25s ease;
    }}

    .btn-theme:hover {{
      background: var(--card-hover);
      transform: translateY(-1px);
    }}

    /* NAVIGATION TABS */
    .nav-tabs {{
      display: flex;
      gap: 8px;
      margin-bottom: 24px;
      overflow-x: auto;
      padding: 4px;
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 16px;
      backdrop-filter: blur(12px);
    }}

    .nav-tab {{
      padding: 11px 20px;
      border-radius: 12px;
      background: transparent;
      border: none;
      color: var(--text-muted);
      font-size: 13px;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 8px;
      transition: all 0.25s ease;
      white-space: nowrap;
    }}

    .nav-tab:hover {{
      color: var(--text-main);
      background: rgba(255, 255, 255, 0.04);
    }}

    body.light-theme .nav-tab:hover {{
      background: rgba(0, 0, 0, 0.04);
    }}

    .nav-tab.active {{
      background: var(--primary-gradient);
      color: white;
      box-shadow: 0 4px 16px var(--primary-glow);
    }}

    .nav-tab .badge {{
      background: rgba(255, 255, 255, 0.18);
      color: currentColor;
      padding: 2px 7px;
      border-radius: 999px;
      font-size: 11px;
      font-family: 'JetBrains Mono', monospace;
      font-weight: 700;
    }}

    /* HERO GAUGE SECTION */
    .hero-kpi-grid {{
      display: grid;
      grid-template-columns: 340px 1fr;
      gap: 18px;
      margin-bottom: 24px;
    }}

    @media (max-width: 1024px) {{
      .hero-kpi-grid {{
        grid-template-columns: 1fr;
      }}
    }}

    .gauge-card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 20px;
      padding: 26px;
      box-shadow: var(--glass-shadow);
      backdrop-filter: blur(14px);
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
      position: relative;
      overflow: hidden;
    }}

    .radial-chart-wrapper {{
      position: relative;
      width: 190px;
      height: 190px;
      margin: 10px 0;
    }}

    .radial-chart-wrapper svg {{
      transform: rotate(-90deg);
      width: 100%;
      height: 100%;
    }}

    .radial-track {{
      fill: none;
      stroke: var(--chart-track);
      stroke-width: 14;
    }}

    .radial-fill {{
      fill: none;
      stroke: url(#gauge-gradient);
      stroke-width: 14;
      stroke-linecap: round;
      stroke-dasharray: 502;
      stroke-dashoffset: 56.6;
      transition: stroke-dashoffset 1.5s cubic-bezier(0.4, 0, 0.2, 1);
    }}

    .gauge-center-text {{
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      text-align: center;
    }}

    .gauge-percentage {{
      font-size: 38px;
      font-weight: 900;
      font-family: 'JetBrains Mono', monospace;
      letter-spacing: -0.04em;
      color: var(--text-main);
      line-height: 1;
    }}

    .gauge-label {{
      font-size: 11px;
      font-weight: 700;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.08em;
      margin-top: 4px;
    }}

    .stat-cards-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
      gap: 16px;
    }}

    .stat-card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 18px;
      padding: 20px 22px;
      box-shadow: var(--glass-shadow);
      backdrop-filter: blur(14px);
      position: relative;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: transform 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    }}

    .stat-card:hover {{
      transform: translateY(-3px);
      border-color: rgba(59, 130, 246, 0.3);
    }}

    .stat-card-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
    }}

    .stat-card-title {{
      font-size: 11px;
      font-weight: 800;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.07em;
    }}

    .stat-card-icon {{
      width: 36px;
      height: 36px;
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 17px;
    }}

    .stat-val {{
      font-size: 32px;
      font-weight: 900;
      font-family: 'JetBrains Mono', monospace;
      letter-spacing: -0.03em;
      color: var(--text-main);
      line-height: 1.1;
    }}

    .stat-subtext {{
      font-size: 12px;
      color: var(--text-muted);
      margin-top: 8px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    .stat-progress-bar {{
      height: 6px;
      background: var(--chart-track);
      border-radius: 999px;
      overflow: hidden;
      margin-top: 10px;
    }}

    .stat-progress-fill {{
      height: 100%;
      border-radius: 999px;
      transition: width 1s ease;
    }}

    /* ALERT BANNER */
    .alert-banner {{
      background: linear-gradient(135deg, rgba(239, 68, 68, 0.12) 0%, rgba(185, 28, 28, 0.05) 100%);
      border: 1px solid rgba(239, 68, 68, 0.3);
      border-radius: 16px;
      padding: 18px 22px;
      margin-bottom: 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      backdrop-filter: blur(12px);
    }}

    body.light-theme .alert-banner {{
      background: #fef2f2;
      border-color: #fecaca;
    }}

    .alert-left {{
      display: flex;
      align-items: center;
      gap: 14px;
    }}

    .alert-icon-box {{
      width: 40px;
      height: 40px;
      border-radius: 12px;
      background: rgba(239, 68, 68, 0.2);
      color: #ef4444;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 20px;
      flex-shrink: 0;
    }}

    .alert-text h4 {{
      font-size: 14px;
      font-weight: 800;
      color: #ef4444;
      margin-bottom: 2px;
    }}

    .alert-text p {{
      font-size: 13px;
      color: var(--text-muted);
    }}

    /* PANELS */
    .panel {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 20px;
      padding: 24px 28px;
      margin-bottom: 24px;
      box-shadow: var(--glass-shadow);
      backdrop-filter: blur(14px);
    }}

    .panel-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
      flex-wrap: wrap;
      gap: 14px;
    }}

    .panel-title {{
      font-size: 16px;
      font-weight: 800;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .panel-subtitle {{
      font-size: 12px;
      color: var(--text-muted);
      margin-top: 2px;
    }}

    /* AREA SCORECARDS */
    .area-scorecards-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 16px;
      margin-bottom: 24px;
    }}

    .area-scorecard {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 18px;
      padding: 20px;
      box-shadow: var(--glass-shadow);
      transition: transform 0.2s;
    }}

    .area-scorecard:hover {{
      transform: translateY(-2px);
    }}

    .area-card-top {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
    }}

    .area-name {{
      font-size: 14px;
      font-weight: 800;
      color: var(--text-main);
    }}

    .area-pct {{
      font-size: 20px;
      font-weight: 900;
      font-family: 'JetBrains Mono', monospace;
    }}

    /* SA MATRIX */
    .sa-matrix-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
      gap: 12px;
    }}

    .sa-tile {{
      background: var(--stat-box-bg);
      border: 1px solid var(--card-border);
      border-radius: 14px;
      padding: 14px 16px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 8px;
      transition: all 0.2s ease;
    }}

    .sa-tile:hover {{
      transform: translateY(-2px);
      border-color: var(--primary);
    }}

    .sa-tile.done {{
      border-left: 4px solid var(--success);
    }}

    .sa-tile.pending {{
      border-left: 4px solid var(--danger);
    }}

    .sa-tile-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    .sa-title {{
      font-size: 12px;
      font-weight: 800;
      color: var(--text-main);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}

    /* FILTERS */
    .filter-bar {{
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      align-items: center;
    }}

    .search-input {{
      background: var(--input-bg);
      border: 1px solid var(--input-border);
      border-radius: 12px;
      padding: 10px 16px;
      color: var(--text-main);
      font-size: 13px;
      font-weight: 500;
      outline: none;
      min-width: 240px;
    }}

    .search-input:focus {{
      border-color: var(--primary);
      box-shadow: 0 0 0 3px var(--primary-glow);
    }}

    .select-input {{
      background: var(--input-bg);
      border: 1px solid var(--input-border);
      border-radius: 12px;
      padding: 10px 16px;
      color: var(--text-main);
      font-size: 13px;
      font-weight: 600;
      outline: none;
      cursor: pointer;
    }}

    /* TABLES */
    .table-container {{
      overflow-x: auto;
      border-radius: 16px;
      border: 1px solid var(--card-border);
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
      text-align: left;
    }}

    thead th {{
      background: var(--table-head);
      color: var(--text-muted);
      font-weight: 700;
      padding: 14px 16px;
      white-space: nowrap;
      border-bottom: 1px solid var(--table-head-border);
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.06em;
    }}

    tbody td {{
      padding: 14px 16px;
      border-bottom: 1px solid var(--table-row-border);
      color: var(--text-main);
    }}

    tbody tr:last-child td {{
      border-bottom: none;
    }}

    tbody tr:hover td {{
      background-color: var(--table-row-hover);
    }}

    .num-col {{
      text-align: right;
      font-family: 'JetBrains Mono', monospace;
      font-weight: 700;
    }}

    /* BADGES */
    .badge {{
      display: inline-flex;
      align-items: center;
      gap: 5px;
      padding: 5px 12px;
      border-radius: 999px;
      font-size: 11px;
      font-weight: 800;
      white-space: nowrap;
    }}

    .badge-success {{
      background: rgba(16, 185, 129, 0.15);
      color: #10b981;
      border: 1px solid rgba(16, 185, 129, 0.3);
    }}

    body.light-theme .badge-success {{
      background: #ecfdf5;
      color: #059669;
      border-color: #a7f3d0;
    }}

    .badge-danger {{
      background: rgba(239, 68, 68, 0.15);
      color: #ef4444;
      border: 1px solid rgba(239, 68, 68, 0.3);
    }}

    body.light-theme .badge-danger {{
      background: #fef2f2;
      color: #dc2626;
      border-color: #fecaca;
    }}

    .badge-warning {{
      background: rgba(245, 158, 11, 0.15);
      color: #f59e0b;
      border: 1px solid rgba(245, 158, 11, 0.3);
    }}

    body.light-theme .badge-warning {{
      background: #fffbeb;
      color: #d97706;
      border-color: #fde68a;
    }}

    /* MINI PROGRESS BARS */
    .table-progress {{
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .table-progress-bar {{
      flex: 1;
      height: 6px;
      background: var(--chart-track);
      border-radius: 999px;
      overflow: hidden;
      min-width: 50px;
    }}

    .table-progress-fill {{
      height: 100%;
      border-radius: 999px;
    }}

    /* BOTTLENECK */
    .bottleneck-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 16px;
      margin-bottom: 24px;
    }}

    .bottleneck-card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 18px;
      padding: 22px;
      position: relative;
      overflow: hidden;
      box-shadow: var(--glass-shadow);
      transition: transform 0.2s;
    }}

    .bottleneck-card:hover {{
      transform: translateY(-2px);
    }}

    .bottleneck-card.critical {{
      border-left: 5px solid var(--danger);
    }}

    .bottleneck-card.warning {{
      border-left: 5px solid var(--warning);
    }}

    .bottleneck-title {{
      font-size: 15px;
      font-weight: 800;
      color: var(--text-main);
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 6px;
    }}

    .bottleneck-info {{
      font-size: 12px;
      color: var(--text-muted);
      margin-bottom: 12px;
    }}

    .bottleneck-stat {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 10px 14px;
      background: var(--stat-box-bg);
      border-radius: 10px;
      font-size: 12px;
      margin-top: 10px;
      border: 1px solid var(--card-border);
    }}

    /* CHARTS */
    .chart-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(420px, 1fr));
      gap: 20px;
      margin-bottom: 24px;
    }}

    .chart-box {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 20px;
      padding: 24px;
      box-shadow: var(--glass-shadow);
    }}

    .chart-title {{
      font-size: 14px;
      font-weight: 800;
      color: var(--text-main);
      margin-bottom: 18px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    .bar-row {{
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 14px;
      font-size: 12px;
    }}

    .bar-label {{
      width: 140px;
      color: var(--text-muted);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      font-weight: 600;
    }}

    .bar-track {{
      flex: 1;
      height: 24px;
      background: var(--chart-track);
      border-radius: 8px;
      overflow: hidden;
      position: relative;
      display: flex;
    }}

    .bar-fill {{
      height: 100%;
      display: flex;
      align-items: center;
      justify-content: flex-end;
      padding-right: 8px;
      font-size: 11px;
      font-weight: 800;
      color: white;
      transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
    }}

    .bar-value {{
      width: 65px;
      text-align: right;
      font-family: 'JetBrains Mono', monospace;
      font-weight: 800;
      color: var(--text-main);
    }}

    /* TABS */
    .tab-content {{
      display: none;
    }}

    .tab-content.active {{
      display: block;
      animation: fadeIn 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }}

    @keyframes fadeIn {{
      from {{ opacity: 0; transform: translateY(6px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}

    /* ========================================= */
    /* PORTRAIT MODAL & CONTAINER                */
    /* ========================================= */
    .modal-overlay {{
      display: none;
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(0, 0, 0, 0.85);
      z-index: 9999;
      justify-content: center;
      align-items: center;
      padding: 16px;
      backdrop-filter: blur(14px);
    }}

    .modal-overlay.active {{
      display: flex;
    }}

    .modal-box {{
      background: var(--bg);
      border: 1px solid var(--card-border);
      border-radius: 24px;
      max-width: 1260px;
      width: 96%;
      max-height: 96vh;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      box-shadow: 0 30px 60px -15px rgba(0, 0, 0, 0.7);
    }}

    .modal-header {{
      padding: 18px 26px;
      background: var(--card-bg);
      border-bottom: 1px solid var(--card-border);
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 14px;
    }}

    .portrait-view-selector {{
      display: flex;
      gap: 6px;
      background: var(--stat-box-bg);
      padding: 4px;
      border-radius: 12px;
      border: 1px solid var(--card-border);
    }}

    .portrait-view-btn {{
      padding: 7px 14px;
      border-radius: 9px;
      border: none;
      background: transparent;
      color: var(--text-muted);
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.2s ease;
    }}

    .portrait-view-btn.active {{
      background: var(--primary-gradient);
      color: white;
      box-shadow: 0 2px 8px var(--primary-glow);
    }}

    .modal-body {{
      padding: 26px;
      overflow-y: auto;
      display: flex;
      justify-content: center;
      background: var(--bg-subtle);
    }}

    /* CAPTURE TARGET CONTAINER */
    #portrait-canvas-target {{
      width: 1180px;
      background: var(--card-solid);
      border: 1px solid var(--card-border);
      border-radius: 20px;
      padding: 28px 24px;
      color: var(--text-main);
      box-shadow: 0 16px 40px rgba(0, 0, 0, 0.35);
      position: relative;
    }}

    .portrait-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
      padding-bottom: 16px;
      border-bottom: 2px solid var(--card-border);
    }}

    .portrait-stat-grid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 12px;
      margin-bottom: 16px;
    }}

    .portrait-stat-item {{
      background: var(--stat-box-bg);
      border: 1px solid var(--card-border);
      border-radius: 14px;
      padding: 16px 14px;
      text-align: center;
    }}

    .portrait-section {{
      background: var(--stat-box-bg);
      border: 1px solid var(--card-border);
      border-radius: 14px;
      padding: 16px 18px;
    }}

    .portrait-grid-2col {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 14px;
      margin-bottom: 14px;
    }}

    .portrait-table-box {{
      border: 1px solid var(--card-border);
      border-radius: 14px;
      overflow: hidden;
      margin-bottom: 14px;
      background: var(--card-solid);
    }}

    .portrait-table-box table {{
      width: 100%;
      border-collapse: collapse;
      table-layout: fixed;
    }}

    .portrait-table-box table thead th {{
      background: var(--stat-box-bg);
      padding: 8px 6px;
      font-size: 11px;
      font-weight: 800;
      letter-spacing: 0.02em;
      border-bottom: 1px solid var(--card-border);
      white-space: nowrap;
    }}

    .portrait-table-box table tbody td {{
      padding: 5px 6px;
      font-size: 11px;
      border-bottom: 1px solid var(--table-row-border);
      vertical-align: middle;
    }}

    .portrait-summary-bar {{
      background: var(--stat-box-bg);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 12px 18px;
      margin-bottom: 16px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 12px;
    }}

    footer {{
      text-align: center;
      font-size: 12px;
      color: var(--text-dim);
      margin-top: 48px;
      padding-top: 20px;
      border-top: 1px solid var(--card-border);
    }}

    footer a {{
      color: var(--primary);
      text-decoration: none;
      font-weight: 600;
    }}

    @media (max-width: 900px) {{
      .header {{
        flex-direction: column;
        align-items: flex-start;
      }}
      .header-actions {{
        width: 100%;
        justify-content: flex-start;
        flex-wrap: wrap;
      }}
      .chart-grid {{
        grid-template-columns: 1fr;
      }}
      #portrait-canvas-target {{
        width: 100%;
        padding: 20px 14px;
      }}
    }}
  </style>
</head>
<body>

<svg style="position: absolute; width: 0; height: 0;" aria-hidden="true">
  <defs>
    <linearGradient id="gauge-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#3b82f6" />
      <stop offset="50%" stop-color="#8b5cf6" />
      <stop offset="100%" stop-color="#10b981" />
    </linearGradient>
  </defs>
</svg>

<div class="container">
  <!-- HEADER -->
  <header class="header">
    <div class="header-branding">
      <img src="logo_transparan.png" alt="Monitoring Uji Petik Logo" class="header-logo-img" />
      <div>
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 4px;">
          <span class="header-badge">LIVE MONITORING</span>
          <span style="font-size: 12px; color: var(--telkom-red); font-weight: 800; letter-spacing: 0.04em;">TELKOM DISTRICT BOGOR DAN SUKABUMI</span>
        </div>
        <h1>Dashboard Monitoring Uji Petik</h1>
        <div class="header-subtitle">
          <span>📍 District: <strong>BOGOR DAN SUKABUMI</strong></span>
          <span>•</span>
          <span id="data-cutoff-label">📅 Data Cut-off: <strong id="cutoff-date-val">{refreshed_at}</strong></span>
          <span>•</span>
          <span id="sync-status-badge" style="display: inline-flex; align-items: center; gap: 4px; font-size: 11px; color: var(--success); background: rgba(16, 185, 129, 0.12); padding: 2px 8px; border-radius: 20px; font-weight: 700;">🟢 Live Google Sheet</span>
        </div>
      </div>
    </div>
    <div class="header-actions">
      <button onclick="syncGoogleSheetsData()" id="btn-sync-sheet" class="btn btn-outline" style="border-color: rgba(59, 130, 246, 0.4); display: inline-flex; align-items: center; gap: 6px;" title="Tarik dan sinkronkan data terbaru langsung dari Google Sheet">
        <span id="sync-icon">🔄</span> <span id="sync-text">Sinkron Sheet</span>
      </button>

      <button onclick="toggleTheme()" id="btn-theme" class="btn btn-theme" title="Ganti Mode Terang / Gelap">
        ☀️ Mode Terang
      </button>

      <button onclick="openPortraitModal()" class="btn btn-success" title="Mode Potret Infografis Lengkap untuk WhatsApp / Simpan JPG">
        📱 Mode Potret (JPG)
      </button>

      <a href="https://docs.google.com/spreadsheets/d/1iCLX_scRmLAMwKrjOS2FkasGwB2q8NOtfzjxxYol8Ow/edit" target="_blank" class="btn btn-outline">
        📊 Spreadsheet
      </a>
      <button onclick="exportTableCSV()" class="btn btn-outline">
        📥 CSV
      </button>
      <button onclick="window.print()" class="btn btn-primary">
        🖨️ Cetak
      </button>
    </div>
  </header>

  <!-- NAVIGATION TABS -->
  <nav class="nav-tabs">
    <button class="nav-tab active" onclick="switchTab('overview')">
      <span>🌟 Ringkasan Eksekutif</span>
    </button>
    <button class="nav-tab" onclick="switchTab('assurance')">
      <span>🛠️ Uji Petik Assurance</span>
      <span class="badge" id="nav-badge-ass">{tot_ass['ach']}%</span>
    </button>
    <button class="nav-tab" onclick="switchTab('psb')">
      <span>📡 Uji Petik PSB</span>
      <span class="badge" id="nav-badge-psb">{tot_psb['ach']}%</span>
    </button>
    <button class="nav-tab" onclick="switchTab('bottleneck')">
      <span>⚠️ Analisis Saldo & Bottleneck</span>
      <span class="badge" id="nav-badge-saldo" style="background: rgba(239,68,68,0.25); color: #f87171;">{tot_saldo} Saldo</span>
    </button>
    <button class="nav-tab" onclick="switchTab('pic')">
      <span>👤 Leaderboard PIC Area</span>
    </button>
  </nav>

  <!-- TAB 1: EXECUTIVE OVERVIEW -->
  <div id="tab-overview" class="tab-content active">
    <div class="hero-kpi-grid">
      <div class="gauge-card">
        <div style="font-size: 12px; font-weight: 800; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.08em;">
          TOTAL CAPAIAN DISTRICT BOGOR
        </div>
        <div class="radial-chart-wrapper">
          <svg viewBox="0 0 190 190">
            <circle class="radial-track" cx="95" cy="95" r="80"></circle>
            <circle class="radial-fill" id="gauge-circle" cx="95" cy="95" r="80" style="stroke-dasharray: 502.65; stroke-dashoffset: {gauge_offset};"></circle>
          </svg>
          <div class="gauge-center-text">
            <div class="gauge-percentage" id="kpi-gauge-pct">{tot_ach}%</div>
            <div class="gauge-label">TARGET 100%</div>
          </div>
        </div>
        <div style="font-size: 13px; color: var(--text-muted); margin-top: 4px;" id="kpi-realisasi-sub">
          Realisasi: <strong style="color: var(--success);">{tot_done}</strong> dari <strong>{tot_samp}</strong> Sampling
        </div>
      </div>

      <div class="stat-cards-grid">
        <div class="stat-card">
          <div class="stat-card-header">
            <span class="stat-card-title">Target Sampling</span>
            <div class="stat-card-icon" style="background: var(--primary-glow); color: var(--primary);">🎯</div>
          </div>
          <div>
            <div class="stat-val" id="kpi-total-target">{tot_samp}</div>
            <div class="stat-subtext" id="kpi-target-subtext">
              <span>Assurance: <strong>{tot_ass['sampling']}</strong></span>
              <span>PSB: <strong>{tot_psb['sampling']}</strong></span>
            </div>
            <div class="stat-progress-bar">
              <div class="stat-progress-fill" style="width: 100%; background: var(--primary);"></div>
            </div>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-card-header">
            <span class="stat-card-title">Realisasi Selesai</span>
            <div class="stat-card-icon" style="background: var(--success-glow); color: var(--success);">✅</div>
          </div>
          <div>
            <div class="stat-val" id="kpi-total-done" style="color: var(--success);">{tot_done}</div>
            <div class="stat-subtext" id="kpi-done-subtext">
              <span>Assurance: <strong>{tot_ass['done']}</strong></span>
              <span>PSB: <strong>{tot_psb['done']}</strong></span>
            </div>
            <div class="stat-progress-bar">
              <div class="stat-progress-fill" id="kpi-done-bar" style="width: {tot_ach}%; background: var(--success);"></div>
            </div>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-card-header">
            <span class="stat-card-title">Sisa Saldo Belum</span>
            <div class="stat-card-icon" style="background: var(--danger-glow); color: var(--danger);">⏳</div>
          </div>
          <div>
            <div class="stat-val" id="kpi-total-saldo" style="color: var(--danger);">{tot_saldo}</div>
            <div class="stat-subtext" id="kpi-saldo-subtext">
              <span>Assurance: <strong>{tot_ass['saldo']}</strong></span>
              <span>PSB: <strong>{tot_psb['saldo']}</strong></span>
            </div>
            <div class="stat-progress-bar">
              <div class="stat-progress-fill" id="kpi-saldo-bar" style="width: {saldo_pct}%; background: var(--danger);"></div>
            </div>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-card-header">
            <span class="stat-card-title">Kualitas Uji (OK)</span>
            <div class="stat-card-icon" style="background: rgba(139,92,246,0.15); color: var(--accent);">⭐</div>
          </div>
          <div>
            <div class="stat-val" style="color: var(--accent);">100%</div>
            <div class="stat-subtext">
              <span>0 Temuan NOK</span>
              <span style="color: var(--success); font-weight: 700;">Standard Sesuai</span>
            </div>
            <div class="stat-progress-bar">
              <div class="stat-progress-fill" style="width: 100%; background: var(--accent);"></div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ALERT BANNER -->
    <div class="alert-banner">
      <div class="alert-left">
        <div class="alert-icon-box">🚨</div>
        <div class="alert-text">
          <h4>Fokus Intervensi Saldo Tertinggal</h4>
          <p>Dari total <strong id="alert-total-saldo">{tot_saldo} saldo</strong> tersisa di District Bogor & Sukabumi, segera selesaikan sebelum cut-off operasional.</p>
        </div>
      </div>
      <button onclick="switchTab('bottleneck')" class="btn btn-outline" style="flex-shrink: 0;">
        Lihat Rincian PIC →
      </button>
    </div>

    <!-- COMPARISON CHARTS -->
    <div class="chart-grid">
      <div class="chart-box">
        <div class="chart-title">
          <span>📊 Perbandingan Pencapaian Stream</span>
          <span style="font-size: 11px; color: var(--text-muted); font-weight: 600;">Target : 100%</span>
        </div>
        <div id="chart-stream-bars"></div>
      </div>

      <div class="chart-box">
        <div class="chart-title">
          <span>🏛️ Rekap Uji Petik Assurance per Area</span>
          <span style="font-size: 11px; color: var(--text-muted); font-weight: 600;">4 Area Regional</span>
        </div>
        <div id="chart-area-bars"></div>
      </div>
    </div>

    <!-- PSB SA MATRIX -->
    <div class="panel">
      <div class="panel-header">
        <div>
          <div class="panel-title">📡 Matriks Kinerja 12 Service Area (SA) — Uji Petik PSB</div>
          <div class="panel-subtitle">Status penyelesaian sampling pasang sambungan baru per wilayah service area</div>
        </div>
        <div style="display: flex; gap: 8px;">
          <span class="badge badge-success">8 SA Selesai (100%)</span>
          <span class="badge badge-danger">4 SA Tertinggal</span>
        </div>
      </div>
      <div class="sa-matrix-grid" id="sa-matrix-container"></div>
    </div>
  </div>

  <!-- TAB 2: UJI PETIK ASSURANCE -->
  <div id="tab-assurance" class="tab-content">
    <div class="area-scorecards-grid" id="assurance-area-cards"></div>

    <div class="panel">
      <div class="panel-header">
        <div>
          <div class="panel-title">📋 Data Rekap Uji Petik Assurance per Sektor</div>
          <div class="panel-subtitle">23 Sektor di District Bogor dengan rincian PIC dan status eviden</div>
        </div>
        <div class="filter-bar">
          <input type="text" id="search-ass" placeholder="🔍 Cari Sektor atau PIC..." class="search-input" oninput="renderAssuranceTable()">
          <select id="filter-ass-status" class="select-input" onchange="renderAssuranceTable()">
            <option value="ALL">Semua Status</option>
            <option value="SALDO">Memiliki Sisa Saldo</option>
            <option value="DONE">Selesai 100%</option>
          </select>
        </div>
      </div>

      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>No</th>
              <th>Sektor</th>
              <th>PIC Area</th>
              <th class="num-col">Sampling</th>
              <th class="num-col">Done</th>
              <th class="num-col">Saldo</th>
              <th>Progress Ach</th>
              <th class="num-col">% Ach</th>
              <th>Status Uji</th>
            </tr>
          </thead>
          <tbody id="tbody-assurance"></tbody>
          <tfoot id="tfoot-assurance"></tfoot>
        </table>
      </div>
    </div>
  </div>

  <!-- TAB 3: UJI PETIK PSB -->
  <div id="tab-psb" class="tab-content">
    <div class="stat-cards-grid" style="margin-bottom: 24px;">
      <div class="stat-card">
        <div class="stat-card-header"><span class="stat-card-title">Target PSB</span><span>📡</span></div>
        <div class="stat-val" id="psb-card-target">{tot_psb['sampling']}</div>
        <div class="stat-subtext" id="psb-card-subtarget">Total {len(data_dict['psb']['sto_list'])} STO di District Bogor</div>
      </div>
      <div class="stat-card">
        <div class="stat-card-header"><span class="stat-card-title">Done PSB</span><span>✅</span></div>
        <div class="stat-val" id="psb-card-done" style="color: var(--success);">{tot_psb['done']}</div>
        <div class="stat-subtext" id="psb-card-ach">Capaian: {tot_psb['ach']}%</div>
      </div>
      <div class="stat-card">
        <div class="stat-card-header"><span class="stat-card-title">Saldo PSB</span><span>⏳</span></div>
        <div class="stat-val" id="psb-card-saldo" style="color: var(--danger);">{tot_psb['saldo']}</div>
        <div class="stat-subtext" id="psb-card-subsaldo">Sisa order belum uji</div>
      </div>
      <div class="stat-card">
        <div class="stat-card-header"><span class="stat-card-title">Kualitas QC</span><span>⭐</span></div>
        <div class="stat-val" style="color: var(--accent);">100%</div>
        <div class="stat-subtext">0 NOK dilaporkan</div>
      </div>
    </div>

    <div class="panel">
      <div class="panel-header">
        <div>
          <div class="panel-title">📋 Data Monitoring Uji Petik PSB per STO</div>
          <div class="panel-subtitle">Rincian 34 STO beserta Service Area (SA) dan PIC</div>
        </div>
        <div class="filter-bar">
          <input type="text" id="search-psb" placeholder="🔍 Cari STO, SA, atau PIC..." class="search-input" oninput="renderPSBTable()">
          <select id="filter-psb-sa" class="select-input" onchange="renderPSBTable()">
            <option value="ALL">Semua Service Area (SA)</option>
          </select>
          <select id="filter-psb-status" class="select-input" onchange="renderPSBTable()">
            <option value="ALL">Semua Status</option>
            <option value="SALDO">Memiliki Sisa Saldo</option>
            <option value="DONE">Selesai 100%</option>
          </select>
        </div>
      </div>

      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>No</th>
              <th>STO</th>
              <th>Service Area (SA)</th>
              <th>PIC Area</th>
              <th class="num-col">Sampling</th>
              <th class="num-col">Done</th>
              <th class="num-col">Saldo</th>
              <th>Progress QC</th>
              <th class="num-col">% QC</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody id="tbody-psb"></tbody>
          <tfoot id="tfoot-psb"></tfoot>
        </table>
      </div>
    </div>
  </div>

  <!-- TAB 4: BOTTLENECK -->
  <div id="tab-bottleneck" class="tab-content">
    <div class="alert-banner">
      <div class="alert-left">
        <div class="alert-icon-box">🚨</div>
        <div class="alert-text">
          <h4>Rangkuman Bottleneck & Rekomendasi Tindak Lanjut Cepat</h4>
          <p>Terdapat 7 PIC yang memiliki sisa saldo pekerjaan. Prioritas utama ada pada 3 PIC dengan saldo terbesar (32 dari 40 saldo total). Lakukan koordinasi lapangan segera.</p>
        </div>
      </div>
    </div>

    <div class="bottleneck-grid" id="bottleneck-cards-container"></div>

    <div class="panel">
      <div class="panel-header">
        <div class="panel-title">🎯 Matriks Rekomendasi Tindakan Lapangan</div>
      </div>
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>Prioritas</th>
              <th>Wilayah / Sektor</th>
              <th>Stream</th>
              <th>PIC Area</th>
              <th>Sisa Saldo</th>
              <th>Kendala Terindikasi</th>
              <th>Tindakan Rekomendasi</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><span class="badge badge-danger">P1 - CRITICAL</span></td>
              <td><strong>SEKTOR CIBADAK</strong></td>
              <td>Assurance</td>
              <td>ERWIN PERMANA (885959)</td>
              <td class="num-col"><strong style="color:var(--danger);">12</strong></td>
              <td>Eviden tertahan proses / sampling lapangan lambat</td>
              <td>Supervisi langsung Team Leader; dispatch teknisi pendamping sampling hari ini.</td>
            </tr>
            <tr>
              <td><span class="badge badge-danger">P1 - CRITICAL</span></td>
              <td><strong>SA SUKABUMI (STO SKB)</strong></td>
              <td>PSB</td>
              <td>FAUZAN ADZIMA (16860876)</td>
              <td class="num-col"><strong style="color:var(--danger);">7</strong></td>
              <td>Volume PSB tinggi (299 PS) namun sampling baru 3 dari 10</td>
              <td>Jadwalkan uji petik PSB maraton untuk 7 order sisa sebelum cut-off.</td>
            </tr>
            <tr>
              <td><span class="badge badge-danger">P1 - CRITICAL</span></td>
              <td><strong>SA CIBADAK (CBD & CCR)</strong></td>
              <td>PSB</td>
              <td>JANUAR FADLILLAH (16911813)</td>
              <td class="num-col"><strong style="color:var(--danger);">8</strong></td>
              <td>STO CBD saldo 5, CCR saldo 2, KLU saldo 1</td>
              <td>Bagi penugasan sampling STO Cibadak & Cicurug ke teknisi quality control terdekat.</td>
            </tr>
            <tr>
              <td><span class="badge badge-warning">P2 - MEDIUM</span></td>
              <td><strong>SUKABUMI 2</strong></td>
              <td>Assurance</td>
              <td>RIZKI NOVIANDY FAJAR</td>
              <td class="num-col"><strong style="color:var(--warning);">2</strong></td>
              <td>Upload eviden proses approval</td>
              <td>Approval eviden segera di sistem oleh TL / Manager.</td>
            </tr>
            <tr>
              <td><span class="badge badge-warning">P2 - MEDIUM</span></td>
              <td><strong>DRAMAGA & SENTUL</strong></td>
              <td>Assurance & PSB</td>
              <td>RIFQI AL AMIN, DENI LESMANA, DEDENG W.</td>
              <td class="num-col"><strong style="color:var(--warning);">6</strong></td>
              <td>Masing-masing saldo 1-2 sampling</td>
              <td>Closing 100% dalam 1x24 jam untuk mencapai target zero defect.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- TAB 5: PIC LEADERBOARD -->
  <div id="tab-pic" class="tab-content">
    <div class="panel">
      <div class="panel-header">
        <div>
          <div class="panel-title">🏆 Performa & Beban Kerja PIC Area</div>
          <div class="panel-subtitle">Rekap gabungan penugasan Assurance dan PSB per PIC Area</div>
        </div>
        <div class="filter-bar">
          <input type="text" id="search-pic" placeholder="🔍 Cari nama PIC..." class="search-input" oninput="renderPICTable()">
        </div>
      </div>

      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>Rank</th>
              <th>Nama PIC Area</th>
              <th class="num-col">Total Target</th>
              <th class="num-col">Total Selesai</th>
              <th class="num-col">Sisa Saldo</th>
              <th>Tingkat Penyelesaian</th>
              <th class="num-col">% Ach Gabungan</th>
              <th>Status Performa</th>
            </tr>
          </thead>
          <tbody id="tbody-pic"></tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- FOOTER -->
  <footer>
    <p>Dashboard Monitoring Uji Petik Assurance & PSB • TELKOM DISTRICT BOGOR DAN SUKABUMI</p>
    <p style="margin-top: 4px;">Data terintegrasi otomatis dari <a href="https://docs.google.com/spreadsheets/d/1iCLX_scRmLAMwKrjOS2FkasGwB2q8NOtfzjxxYol8Ow/edit" target="_blank">Google Spreadsheet</a></p>
  </footer>
</div>

<!-- ==================================================== -->
<!-- PORTRAIT PREVIEW & EXPORT MODAL                     -->
<!-- ==================================================== -->
<div id="portrait-modal" class="modal-overlay">
  <div class="modal-box">
    <div class="modal-header">
      <div style="display: flex; align-items: center; gap: 12px;">
        <span style="font-size: 24px;">📱</span>
        <div>
          <h3 style="font-size: 16px; font-weight: 800; color: var(--text-main);">Mode Potret Infografis (Siap Simpan JPG)</h3>
          <div style="font-size: 12px; color: var(--text-muted);">Pilih data yang ingin diekspor ke gambar vertikal resolusi tinggi:</div>
        </div>
      </div>
      
      <!-- VIEW SELECTOR BUTTONS -->
      <div class="portrait-view-selector">
        <button id="pview-psb" onclick="selectPortraitView('psb')" class="portrait-view-btn">
          📡 Uji Petik PSB (34 STO)
        </button>
        <button id="pview-assurance" onclick="selectPortraitView('assurance')" class="portrait-view-btn">
          🛠️ Assurance (23 Sektor)
        </button>
        <button id="pview-overview" onclick="selectPortraitView('overview')" class="portrait-view-btn">
          🌟 Ringkasan Eksekutif
        </button>
      </div>

      <div style="display: flex; gap: 8px;">
        <button onclick="downloadPortraitJPG()" id="btn-save-jpg" class="btn btn-success">
          💾 Download JPG Sekarang
        </button>
        <button onclick="closePortraitModal()" class="btn btn-outline">
          ✕ Tutup
        </button>
      </div>
    </div>

    <div class="modal-body">
      <!-- THE CAPTURE TARGET -->
      <div id="portrait-canvas-target">
        <!-- DYNAMICALLY INJECTED VIA JS: PSB, ASSURANCE, OR OVERVIEW -->
      </div>
    </div>
  </div>
</div>

<script>
const DATA = {data_json};
let currentTab = 'overview';
let activePortraitView = 'overview';

// THEME MANAGEMENT (DARK / LIGHT)
function initTheme() {{
  const savedTheme = localStorage.getItem('uji_petik_theme') || 'dark';
  if (savedTheme === 'light') {{
    document.body.classList.add('light-theme');
    updateThemeButton(true);
  }} else {{
    document.body.classList.remove('light-theme');
    updateThemeButton(false);
  }}
}}

function toggleTheme() {{
  const isLight = document.body.classList.toggle('light-theme');
  localStorage.setItem('uji_petik_theme', isLight ? 'light' : 'dark');
  updateThemeButton(isLight);
}}

function updateThemeButton(isLight) {{
  const btn = document.getElementById('btn-theme');
  if (isLight) {{
    btn.innerHTML = '🌙 Mode Gelap';
    btn.title = 'Beralih ke tampilan gelap';
  }} else {{
    btn.innerHTML = '☀️ Mode Terang';
    btn.title = 'Beralih ke tampilan terang';
  }}
}}

// TAB SWITCHING
function switchTab(tabId) {{
  currentTab = tabId;
  document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.nav-tab').forEach(el => el.classList.remove('active'));
  
  const target = document.getElementById('tab-' + tabId);
  if (target) target.classList.add('active');
  
  const tabs = document.querySelectorAll('.nav-tab');
  const indexMap = {{'overview': 0, 'assurance': 1, 'psb': 2, 'bottleneck': 3, 'pic': 4}};
  if (tabs[indexMap[tabId]]) {{
    tabs[indexMap[tabId]].classList.add('active');
  }}
}}

// PORTRAIT MODAL & JPG CAPTURE
function openPortraitModal() {{
  if (currentTab === 'psb') {{
    selectPortraitView('psb');
  }} else if (currentTab === 'assurance') {{
    selectPortraitView('assurance');
  }} else {{
    selectPortraitView('overview');
  }}
  document.getElementById('portrait-modal').classList.add('active');
}}

function closePortraitModal() {{
  document.getElementById('portrait-modal').classList.remove('active');
}}

function selectPortraitView(viewType) {{
  activePortraitView = viewType;
  document.querySelectorAll('.portrait-view-btn').forEach(btn => btn.classList.remove('active'));
  const btn = document.getElementById('pview-' + viewType);
  if (btn) btn.classList.add('active');

  const container = document.getElementById('portrait-canvas-target');

  if (viewType === 'psb') {{
    renderPSBPortrait(container);
  }} else if (viewType === 'assurance') {{
    renderAssurancePortrait(container);
  }} else {{
    renderOverviewPortrait(container);
  }}
}}

// COMMON EXECUTIVE SUMMARY BANNER (FOTO KE-2: 4 KPI TILES + PROGRESS CAPAIAN PER STREAM DYNAMIC)
function getExecutiveBannerHtml(viewType = 'overview') {{
  const ass = DATA.assurance.total;
  const psb = DATA.psb.total;
  const totSamp = ass.sampling + psb.sampling;
  const totDone = ass.done + psb.done;
  const totSaldo = ass.saldo + psb.saldo;
  const totAch = totSamp > 0 ? (Math.round((totDone / totSamp) * 10000) / 100) : 0;

  let targetVal, targetSub;
  let doneVal, doneSub;
  let saldoVal, saldoSub;
  let achVal, achSub, achLabel;
  let progressBarHtml = '';

  if (viewType === 'assurance') {{
    targetVal = ass.sampling;
    targetSub = `${{DATA.assurance.sektors.length}} Sektor Assurance`;
    doneVal = ass.done;
    doneSub = `Tercapai ${{ass.ach}}%`;
    saldoVal = ass.saldo;
    saldoSub = `Sisa Belum Uji`;
    achLabel = '% ACH';
    achVal = `${{ass.ach}}%`;
    achSub = `Kualitas OK: 100%`;

    progressBarHtml = `
      <div class="portrait-section" style="margin-top: 14px; margin-bottom: 20px;">
        <div style="font-size: 13px; font-weight: 800; color: var(--text-main); margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center;">
          <span>📊 Capaian Uji Petik Assurance (${{DATA.assurance.sektors.length}} Sektor)</span>
          <span style="font-size: 11px; color: var(--text-muted); font-weight: 700;">Target: 100%</span>
        </div>
        <div class="bar-row" style="margin-bottom: 2px;">
          <div class="bar-label" style="width: 170px;"><strong>Assurance (${{DATA.assurance.sektors.length}} Sektor)</strong></div>
          <div class="bar-track">
            <div class="bar-fill" style="width: ${{ass.ach}}%; background: linear-gradient(90deg, #3b82f6, #60a5fa);">${{ass.ach}}%</div>
          </div>
          <div class="bar-value">${{ass.done}}/${{ass.sampling}} (${{ass.saldo}} Saldo Tersisa)</div>
        </div>
      </div>
    `;
  }} else if (viewType === 'psb') {{
    targetVal = psb.sampling;
    targetSub = `${{DATA.psb.sto_list.length}} STO Pasang Baru`;
    doneVal = psb.done;
    doneSub = `Tercapai ${{psb.ach}}%`;
    saldoVal = psb.saldo;
    saldoSub = `Sisa Belum Uji`;
    achLabel = '% QC';
    achVal = `${{psb.ach}}%`;
    achSub = `Kualitas OK: 100%`;

    progressBarHtml = `
      <div class="portrait-section" style="margin-top: 14px; margin-bottom: 20px;">
        <div style="font-size: 13px; font-weight: 800; color: var(--text-main); margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center;">
          <span>📊 Capaian Uji Petik Pasang Baru (${{DATA.psb.sto_list.length}} STO)</span>
          <span style="font-size: 11px; color: var(--text-muted); font-weight: 700;">Target: 100%</span>
        </div>
        <div class="bar-row" style="margin-bottom: 2px;">
          <div class="bar-label" style="width: 170px;"><strong>PSB (${{DATA.psb.sto_list.length}} STO)</strong></div>
          <div class="bar-track">
            <div class="bar-fill" style="width: ${{psb.ach}}%; background: linear-gradient(90deg, #10b981, #34d399);">${{psb.ach}}%</div>
          </div>
          <div class="bar-value">${{psb.done}}/${{psb.sampling}} (${{psb.saldo}} Saldo Tersisa)</div>
        </div>
      </div>
    `;
  }} else {{
    targetVal = totSamp;
    targetSub = `Ass ${{ass.sampling}} • PSB ${{psb.sampling}}`;
    doneVal = totDone;
    doneSub = `Tercapai ${{totAch}}%`;
    saldoVal = totSaldo;
    saldoSub = `Ass ${{ass.saldo}} • PSB ${{psb.saldo}}`;
    achLabel = '% ACH';
    achVal = `${{totAch}}%`;
    achSub = `QC OK: 100%`;

    progressBarHtml = `
      <div class="portrait-section" style="margin-top: 14px; margin-bottom: 20px;">
        <div style="font-size: 13px; font-weight: 800; color: var(--text-main); margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center;">
          <span>📊 Progress Capaian per Stream Layanan</span>
          <span style="font-size: 11px; color: var(--text-muted); font-weight: 700;">Target: 100%</span>
        </div>
        <div class="bar-row" style="margin-bottom: 10px;">
          <div class="bar-label" style="width: 170px;"><strong>Assurance (${{DATA.assurance.sektors.length}} Sektor)</strong></div>
          <div class="bar-track">
            <div class="bar-fill" style="width: ${{ass.ach}}%; background: linear-gradient(90deg, #3b82f6, #60a5fa);">${{ass.ach}}%</div>
          </div>
          <div class="bar-value">${{ass.done}}/${{ass.sampling}} (${{ass.saldo}} Saldo)</div>
        </div>
        <div class="bar-row" style="margin-bottom: 2px;">
          <div class="bar-label" style="width: 170px;"><strong>PSB (${{DATA.psb.sto_list.length}} STO)</strong></div>
          <div class="bar-track">
            <div class="bar-fill" style="width: ${{psb.ach}}%; background: linear-gradient(90deg, #10b981, #34d399);">${{psb.ach}}%</div>
          </div>
          <div class="bar-value">${{psb.done}}/${{psb.sampling}} (${{psb.saldo}} Saldo)</div>
        </div>
      </div>
    `;
  }}

  return `
    <!-- 4 KPI TILES -->
    <div class="portrait-stat-grid">
      <div class="portrait-stat-item">
        <div style="font-size: 11px; color: var(--text-muted); font-weight: 800; letter-spacing: 0.05em;">TARGET</div>
        <div style="font-size: 26px; font-weight: 900; font-family: 'JetBrains Mono', monospace; color: var(--primary); margin-top: 3px;">${{targetVal}}</div>
        <div style="font-size: 10px; color: var(--text-dim); margin-top: 3px;">${{targetSub}}</div>
      </div>
      <div class="portrait-stat-item">
        <div style="font-size: 11px; color: var(--text-muted); font-weight: 800; letter-spacing: 0.05em;">DONE</div>
        <div style="font-size: 26px; font-weight: 900; font-family: 'JetBrains Mono', monospace; color: var(--success); margin-top: 3px;">${{doneVal}}</div>
        <div style="font-size: 10px; color: var(--text-dim); margin-top: 3px;">${{doneSub}}</div>
      </div>
      <div class="portrait-stat-item">
        <div style="font-size: 11px; color: var(--text-muted); font-weight: 800; letter-spacing: 0.05em;">SALDO</div>
        <div style="font-size: 26px; font-weight: 900; font-family: 'JetBrains Mono', monospace; color: var(--danger); margin-top: 3px;">${{saldoVal}}</div>
        <div style="font-size: 10px; color: var(--text-dim); margin-top: 3px;">${{saldoSub}}</div>
      </div>
      <div class="portrait-stat-item">
        <div style="font-size: 11px; color: var(--text-muted); font-weight: 800; letter-spacing: 0.05em;">${{achLabel}}</div>
        <div style="font-size: 26px; font-weight: 900; font-family: 'JetBrains Mono', monospace; color: var(--accent); margin-top: 3px;">${{achVal}}</div>
        <div style="font-size: 10px; color: var(--text-dim); margin-top: 3px;">${{achSub}}</div>
      </div>
    </div>

    ${{progressBarHtml}}
  `;
}}

// HELPER: GENERATE PSB SUB-TABLE FOR 2-COLUMN BALANCED LAYOUT
function generatePSBTableHtml(items, startIdx) {{
  let rows = '';
  items.forEach((item, i) => {{
    const idx = startIdx + i;
    const isDone = item.saldo === 0;
    const badgeText = isDone ? 'SUDAH' : 'BELUM (' + item.saldo + ')';
    const badgeClass = isDone ? 'badge-success' : 'badge-danger';
    const numColor = item.saldo > 0 ? 'var(--danger)' : 'var(--text-muted)';
    const pctColor = isDone ? 'var(--success)' : (item.qc >= 50 ? 'var(--warning)' : 'var(--danger)');

    rows += `
      <tr>
        <td class="num-col" style="color: var(--text-dim); width: 24px; text-align: center; padding: 6px 2px;">${{idx + 1}}</td>
        <td style="width: 40px; text-align: center; padding: 6px 2px;"><strong style="color: var(--primary); font-size: 12px;">${{item.sto}}</strong></td>
        <td style="width: 135px; padding: 6px 4px; vertical-align: middle;">
          <div style="font-size: 10.5px; font-weight: 700; color: var(--text-main); line-height: 1.25; word-break: break-word;">${{item.sa}}</div>
        </td>
        <td style="width: 105px; padding: 6px 4px; vertical-align: middle;">
          <div style="font-size: 9.5px; color: var(--text-muted); line-height: 1.2; word-break: break-word;">${{item.pic}}</div>
        </td>
        <td class="num-col" style="width: 30px; text-align: center; padding: 6px 2px;">${{item.sampling}}</td>
        <td class="num-col" style="width: 30px; text-align: center; color: var(--success); font-weight: 700; padding: 6px 2px;">${{item.done}}</td>
        <td class="num-col" style="width: 30px; text-align: center; color: ${{numColor}}; font-weight: 800; padding: 6px 2px;">${{item.saldo}}</td>
        <td class="num-col" style="width: 42px; text-align: center; color: ${{pctColor}}; font-weight: 800; padding: 6px 2px;">${{item.qc}}%</td>
        <td style="width: 68px; text-align: center; padding: 6px 2px;"><span class="badge ${{badgeClass}}" style="font-size: 9px; padding: 2px 5px;">${{badgeText}}</span></td>
      </tr>
    `;
  }});

  return `
    <div class="portrait-table-box" style="margin-bottom: 0;">
      <table>
        <thead>
          <tr>
            <th style="width: 24px; text-align: center; padding: 8px 2px;">NO</th>
            <th style="width: 40px; text-align: center; padding: 8px 2px;">STO</th>
            <th style="width: 135px; text-align: left; padding: 8px 4px;">SA</th>
            <th style="width: 105px; text-align: left; padding: 8px 4px;">PIC AREA</th>
            <th class="num-col" style="width: 30px; text-align: center; padding: 8px 2px;">SMP</th>
            <th class="num-col" style="width: 30px; text-align: center; padding: 8px 2px;">DONE</th>
            <th class="num-col" style="width: 30px; text-align: center; padding: 8px 2px;">SLD</th>
            <th class="num-col" style="width: 42px; text-align: center; padding: 8px 2px;">% QC</th>
            <th style="width: 68px; text-align: center; padding: 8px 2px;">STATUS</th>
          </tr>
        </thead>
        <tbody>
          ${{rows}}
        </tbody>
      </table>
    </div>
  `;
}}

// RENDER FULL PSB PORTRAIT (34 STO SPLIT INTO 2 BALANCED COLUMNS)
function renderPSBPortrait(container) {{
  const half = Math.ceil(DATA.psb.sto_list.length / 2);
  const leftItems = DATA.psb.sto_list.slice(0, half);
  const rightItems = DATA.psb.sto_list.slice(half);

  const leftTable = generatePSBTableHtml(leftItems, 0);
  const rightTable = generatePSBTableHtml(rightItems, half);

  container.innerHTML = `
    <!-- HEADER -->
    <div class="portrait-header">
      <div style="display: flex; align-items: center; gap: 14px;">
        <img src="logo_transparan.png" style="width: 74px; height: 74px; object-fit: contain; filter: drop-shadow(0 4px 12px rgba(0,0,0,0.4)); flex-shrink: 0;" alt="Monitoring Uji Petik Logo" />
        <div>
          <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
            <span class="header-badge" style="font-size: 10px; padding: 4px 8px;">LAPORAN OPERASIONAL</span>
            <span style="font-size: 11px; font-weight: 800; color: var(--telkom-red);">TELKOM DISTRICT BOGOR DAN SUKABUMI</span>
          </div>
          <h2 style="font-size: 20px; font-weight: 900; color: var(--text-main); letter-spacing: -0.02em;">
            MONITORING UJI PETIK PSB (${{DATA.psb.sto_list.length}} STO)
          </h2>
          <div style="font-size: 12px; color: var(--text-muted); margin-top: 2px;">
            Distrik: <strong>BOGOR DAN SUKABUMI</strong> • ${{DATA.psb.sto_list.length}} STO (${{leftItems.length}} Kolom Kiri + ${{rightItems.length}} Kolom Kanan)
          </div>
        </div>
      </div>
      <div style="text-align: right;">
        <div style="font-size: 12px; font-weight: 800; color: var(--primary);">Cut-off: ${{DATA.meta.refreshed_at || '26 Nov 2026'}}</div>
        <div style="font-size: 11px; color: var(--text-dim); margin-top: 2px;">Kualitas Uji (OK): 100%</div>
      </div>
    </div>

    <!-- FOTO KE-2 (EXECUTIVE KPI & CAPAIAN PER STREAM BANNER) -->
    ${{getExecutiveBannerHtml('psb')}}

    <!-- 2-COLUMN BALANCED TABLES (17 STO LEFT & 17 STO RIGHT) -->
    <div class="portrait-grid-2col">
      ${{leftTable}}
      ${{rightTable}}
    </div>

    <!-- SUMMARY TOTAL DISTRICT BAR -->
    <div class="portrait-summary-bar">
      <div>
        <span style="font-weight: 800; color: var(--text-main); font-size: 13px;">TOTAL DISTRICT BOGOR & SUKABUMI (PSB ${{DATA.psb.sto_list.length}} STO)</span>
      </div>
      <div style="display: flex; gap: 20px; align-items: center; font-family: 'JetBrains Mono', monospace; font-size: 13px;">
        <span>Target: <strong style="color: var(--primary);">${{DATA.psb.total.sampling}}</strong></span>
        <span>Done: <strong style="color: var(--success);">${{DATA.psb.total.done}}</strong></span>
        <span>Saldo: <strong style="color: var(--danger); font-size: 14px;">${{DATA.psb.total.saldo}}</strong></span>
        <span>% QC: <strong style="color: var(--warning); font-size: 14px;">${{DATA.psb.total.ach}}%</strong></span>
        <span class="badge badge-warning" style="font-size: 11px; padding: 4px 10px;">${{DATA.psb.total.saldo}} SALDO</span>
      </div>
    </div>

    <!-- FOOTER SIGNATURE -->
    <div style="display: flex; justify-content: space-between; align-items: center; font-size: 11px; color: var(--text-dim); padding-top: 10px; border-top: 1px solid var(--card-border);">
      <span>TELKOM DISTRICT BOGOR DAN SUKABUMI</span>
      <span>Halaman Laporan Lengkap Uji Petik PSB (Layout Proporsional 2 Kolom)</span>
    </div>
  `;
}}

// HELPER: GENERATE ASSURANCE SUB-TABLE FOR 2-COLUMN BALANCED LAYOUT
function generateAssuranceTableHtml(items, startIdx) {{
  let rows = '';
  items.forEach((item, i) => {{
    const idx = startIdx + i;
    const isDone = item.saldo === 0;
    const badgeText = isDone ? 'SUDAH' : 'BELUM (' + item.saldo + ')';
    const badgeClass = isDone ? 'badge-success' : 'badge-danger';
    const numColor = item.saldo > 0 ? 'var(--danger)' : 'var(--text-muted)';
    const pctColor = isDone ? 'var(--success)' : (item.ach >= 80 ? 'var(--warning)' : 'var(--danger)');

    rows += `
      <tr>
        <td class="num-col" style="color: var(--text-dim); width: 24px; text-align: center; padding: 6px 2px;">${{idx + 1}}</td>
        <td style="width: 215px; padding: 6px 6px; vertical-align: middle;">
          <div style="font-weight: 800; font-size: 10.5px; color: var(--text-main); line-height: 1.25; word-break: break-word;">${{item.sektor}}</div>
        </td>
        <td style="width: 95px; padding: 6px 4px; vertical-align: middle;">
          <div style="font-size: 9.5px; color: var(--text-muted); line-height: 1.2; word-break: break-word;">${{item.pic || '-'}}</div>
        </td>
        <td class="num-col" style="width: 30px; text-align: center; padding: 6px 2px;">${{item.sampling}}</td>
        <td class="num-col" style="width: 30px; text-align: center; color: var(--success); font-weight: 700; padding: 6px 2px;">${{item.done}}</td>
        <td class="num-col" style="width: 30px; text-align: center; color: ${{numColor}}; font-weight: 800; padding: 6px 2px;">${{item.saldo}}</td>
        <td class="num-col" style="width: 42px; text-align: center; color: ${{pctColor}}; font-weight: 800; padding: 6px 2px;">${{item.ach}}%</td>
        <td style="width: 68px; text-align: center; padding: 6px 2px;"><span class="badge ${{badgeClass}}" style="font-size: 9px; padding: 2px 5px;">${{badgeText}}</span></td>
      </tr>
    `;
  }});

  return `
    <div class="portrait-table-box" style="margin-bottom: 0;">
      <table>
        <thead>
          <tr>
            <th style="width: 24px; text-align: center; padding: 8px 2px;">NO</th>
            <th style="width: 215px; text-align: left; padding: 8px 6px;">SEKTOR ASSURANCE</th>
            <th style="width: 95px; text-align: left; padding: 8px 4px;">PIC AREA</th>
            <th class="num-col" style="width: 30px; text-align: center; padding: 8px 2px;">SMP</th>
            <th class="num-col" style="width: 30px; text-align: center; padding: 8px 2px;">DONE</th>
            <th class="num-col" style="width: 30px; text-align: center; padding: 8px 2px;">SLD</th>
            <th class="num-col" style="width: 42px; text-align: center; padding: 8px 2px;">% ACH</th>
            <th style="width: 68px; text-align: center; padding: 8px 2px;">STATUS</th>
          </tr>
        </thead>
        <tbody>
          ${{rows}}
        </tbody>
      </table>
    </div>
  `;
}}

// RENDER FULL ASSURANCE PORTRAIT (23 SEKTOR SPLIT INTO 2 BALANCED COLUMNS)
function renderAssurancePortrait(container) {{
  const half = Math.ceil(DATA.assurance.sektors.length / 2);
  const leftItems = DATA.assurance.sektors.slice(0, half);
  const rightItems = DATA.assurance.sektors.slice(half);

  const leftTable = generateAssuranceTableHtml(leftItems, 0);
  const rightTable = generateAssuranceTableHtml(rightItems, half);

  container.innerHTML = `
    <!-- HEADER -->
    <div class="portrait-header">
      <div style="display: flex; align-items: center; gap: 14px;">
        <img src="logo_transparan.png" style="width: 74px; height: 74px; object-fit: contain; filter: drop-shadow(0 4px 12px rgba(0,0,0,0.4)); flex-shrink: 0;" alt="Monitoring Uji Petik Logo" />
        <div>
          <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
            <span class="header-badge" style="font-size: 10px; padding: 4px 8px;">LAPORAN OPERASIONAL</span>
            <span style="font-size: 11px; font-weight: 800; color: var(--telkom-red);">TELKOM DISTRICT BOGOR DAN SUKABUMI</span>
          </div>
          <h2 style="font-size: 20px; font-weight: 900; color: var(--text-main); letter-spacing: -0.02em;">
            MONITORING UJI PETIK ASSURANCE (${{DATA.assurance.sektors.length}} SEKTOR)
          </h2>
          <div style="font-size: 12px; color: var(--text-muted); margin-top: 2px;">
            Distrik: <strong>BOGOR DAN SUKABUMI</strong> • ${{DATA.assurance.sektors.length}} Sektor (${{leftItems.length}} Kolom Kiri + ${{rightItems.length}} Kolom Kanan)
          </div>
        </div>
      </div>
      <div style="text-align: right;">
        <div style="font-size: 12px; font-weight: 800; color: var(--primary);">Cut-off: ${{DATA.meta.refreshed_at || '26 Nov 2026'}}</div>
        <div style="font-size: 11px; color: var(--text-dim); margin-top: 2px;">Capaian Total: ${{DATA.assurance.total.ach}}%</div>
      </div>
    </div>

    <!-- FOTO KE-2 (EXECUTIVE KPI & CAPAIAN PER STREAM BANNER) -->
    ${{getExecutiveBannerHtml('assurance')}}

    <!-- 2-COLUMN BALANCED TABLES (12 SEKTOR LEFT & 11 SEKTOR RIGHT) -->
    <div class="portrait-grid-2col">
      ${{leftTable}}
      ${{rightTable}}
    </div>

    <!-- SUMMARY TOTAL DISTRICT BAR -->
    <div class="portrait-summary-bar">
      <div>
        <span style="font-weight: 800; color: var(--text-main); font-size: 13px;">TOTAL DISTRICT BOGOR & SUKABUMI (ASSURANCE ${{DATA.assurance.sektors.length}} SEKTOR)</span>
      </div>
      <div style="display: flex; gap: 20px; align-items: center; font-family: 'JetBrains Mono', monospace; font-size: 13px;">
        <span>Target: <strong style="color: var(--primary);">${{DATA.assurance.total.sampling}}</strong></span>
        <span>Done: <strong style="color: var(--success);">${{DATA.assurance.total.done}}</strong></span>
        <span>Saldo: <strong style="color: var(--danger); font-size: 14px;">${{DATA.assurance.total.saldo}}</strong></span>
        <span>% Ach: <strong style="color: var(--success); font-size: 14px;">${{DATA.assurance.total.ach}}%</strong></span>
        <span class="badge badge-warning" style="font-size: 11px; padding: 4px 10px;">${{DATA.assurance.total.saldo}} SALDO</span>
      </div>
    </div>

    <!-- FOOTER SIGNATURE -->
    <div style="display: flex; justify-content: space-between; align-items: center; font-size: 11px; color: var(--text-dim); padding-top: 10px; border-top: 1px solid var(--card-border);">
      <span>TELKOM DISTRICT BOGOR DAN SUKABUMI</span>
      <span>Halaman Laporan Lengkap Uji Petik Assurance (Layout Proporsional 2 Kolom)</span>
    </div>
  `;
}}

// RENDER OVERVIEW PORTRAIT (EXECUTIVE POSTER)
function renderOverviewPortrait(container) {{
  const ass = DATA.assurance.total;
  const psb = DATA.psb.total;
  const totSaldo = ass.saldo + psb.saldo;

  // Dynamically extract top bottleneck PICs
  const bMap = {{}};
  DATA.assurance.sektors.forEach(s => {{
    if (s.saldo > 0) {{
      const rawPic = s.pic || 'Unknown';
      const name = rawPic.split('|')[0].trim();
      if (!bMap[name]) bMap[name] = {{ name: name, role: s.sektor + ' - Assurance', saldo: 0 }};
      bMap[name].saldo += s.saldo;
    }}
  }});
  DATA.psb.sto_list.forEach(s => {{
    if (s.saldo > 0) {{
      const rawPic = s.pic || 'Unknown';
      const name = rawPic.split('-')[0].trim();
      if (!bMap[name]) bMap[name] = {{ name: name, role: 'SA ' + s.sa + ' STO ' + s.sto + ' - PSB', saldo: 0 }};
      bMap[name].saldo += s.saldo;
    }}
  }});

  const bList = Object.values(bMap).sort((a, b) => b.saldo - a.saldo);
  const top3 = bList.slice(0, 3);
  const top3Sum = top3.reduce((acc, curr) => acc + curr.saldo, 0);
  const top3Pct = totSaldo > 0 ? Math.round((top3Sum / totSaldo) * 1000) / 10 : 0;

  const top3Html = top3.map(item => `
    <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 12px; background: var(--card-solid); border-radius: 8px; border: 1px solid var(--card-border);">
      <span><strong>${{item.name}}</strong><br><small style="color: var(--text-muted);">${{item.role}}</small></span>
      <strong style="color: var(--danger); font-size: 14px;">${{item.saldo}} Saldo</strong>
    </div>
  `).join('');

  container.innerHTML = `
    <div class="portrait-header">
      <div style="display: flex; align-items: center; gap: 14px;">
        <img src="logo_transparan.png" style="width: 74px; height: 74px; object-fit: contain; filter: drop-shadow(0 4px 12px rgba(0,0,0,0.4)); flex-shrink: 0;" alt="Monitoring Uji Petik Logo" />
        <div>
          <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
            <span class="header-badge" style="font-size: 10px; padding: 4px 8px;">RINGKASAN EKSEKUTIF</span>
            <span style="font-size: 11px; font-weight: 800; color: var(--telkom-red);">TELKOM DISTRICT BOGOR DAN SUKABUMI</span>
          </div>
          <h2 style="font-size: 22px; font-weight: 900; color: var(--text-main); letter-spacing: -0.02em;">
            MONITORING UJI PETIK (ASSURANCE & PSB)
          </h2>
          <div style="font-size: 12px; color: var(--text-muted); margin-top: 2px;">
            Distrik: <strong>BOGOR DAN SUKABUMI</strong> • Executive Summary
          </div>
        </div>
      </div>
      <div style="text-align: right;">
        <div style="font-size: 12px; font-weight: 800; color: var(--primary);">Cut-off: ${{DATA.meta.refreshed_at || '26 Nov 2026'}}</div>
        <div style="font-size: 11px; color: var(--text-dim); margin-top: 2px;">Kualitas Uji (OK): 100%</div>
      </div>
    </div>

    <!-- FOTO KE-2 (EXECUTIVE KPI & CAPAIAN PER STREAM BANNER) -->
    ${{getExecutiveBannerHtml('overview')}}

    <!-- 2-COLUMN OVERVIEW DETAILS -->
    <div class="portrait-grid-2col">
      <!-- TOP BOTTLENECK IN PORTRAIT -->
      <div class="portrait-section" style="border-left: 5px solid var(--danger); margin-bottom: 0;">
        <div style="font-size: 13px; font-weight: 800; color: var(--danger); margin-bottom: 12px; display: flex; justify-content: space-between;">
          <span>🚨 Fokus Intervensi PIC & Saldo Tertinggal</span>
          <span>${{top3Sum}}/${{totSaldo}} Saldo (${{top3Pct}}%)</span>
        </div>
        <div style="font-size: 12px; display: flex; flex-direction: column; gap: 8px;">
          ${{top3Html || '<div style="color:var(--success); padding:8px;">Semua order telah selesai (0 saldo)!</div>'}}
        </div>
      </div>

      <!-- STREAM COMPARISON TILE -->
      <div class="portrait-section" style="border-left: 5px solid var(--primary); margin-bottom: 0;">
        <div style="font-size: 13px; font-weight: 800; color: var(--primary); margin-bottom: 12px; display: flex; justify-content: space-between;">
          <span>📋 Rekapitulasi per Stream Layanan</span>
          <span>District Bogor-Sukabumi</span>
        </div>
        <div style="font-size: 12px; display: flex; flex-direction: column; gap: 8px;">
          <div style="padding: 10px 12px; background: var(--card-solid); border-radius: 8px; border: 1px solid var(--card-border);">
            <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
              <strong>Assurance (${{DATA.assurance.sektors.length}} Sektor)</strong>
              <span class="badge badge-success" style="font-size: 10px;">${{ass.ach}}% ACH</span>
            </div>
            <div style="font-size: 11px; color: var(--text-muted);">Target: ${{ass.sampling}} | Selesai: ${{ass.done}} | Sisa: <strong style="color: var(--danger);">${{ass.saldo}} Saldo</strong></div>
          </div>
          <div style="padding: 10px 12px; background: var(--card-solid); border-radius: 8px; border: 1px solid var(--card-border);">
            <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
              <strong>PSB Pasang Baru (${{DATA.psb.sto_list.length}} STO)</strong>
              <span class="badge ${{psb.ach >= 80 ? 'badge-success' : 'badge-warning'}}" style="font-size: 10px;">${{psb.ach}}% ACH</span>
            </div>
            <div style="font-size: 11px; color: var(--text-muted);">Target: ${{psb.sampling}} | Selesai: ${{psb.done}} | Sisa: <strong style="color: var(--danger);">${{psb.saldo}} Saldo</strong></div>
          </div>
          <div style="padding: 8px 12px; background: var(--card-solid); border-radius: 8px; border: 1px solid var(--card-border); font-size: 11px; color: var(--text-dim); display: flex; justify-content: space-between;">
            <span>Standar Kualitas Uji (QC):</span>
            <strong style="color: var(--success);">100% OK Sesuai SOP</strong>
          </div>
        </div>
      </div>
    </div>

    <!-- FOOTER SIGNATURE -->
    <div style="padding-top: 14px; margin-top: 16px; border-top: 1px solid var(--card-border); display: flex; justify-content: space-between; align-items: center; font-size: 11px; color: var(--text-dim);">
      <span>TELKOM DISTRICT BOGOR DAN SUKABUMI</span>
      <span>Status Kualitas Uji: <strong>100% OK</strong></span>
    </div>
  `;
}}

// DOWNLOAD PORTRAIT AS JPG (FULL HEIGHT WITHOUT ANY TRUNCATION, PROPORTIONAL 1180PX WIDTH)
async function downloadPortraitJPG() {{
  const target = document.getElementById('portrait-canvas-target');
  const btn = document.getElementById('btn-save-jpg');
  const originalText = btn.innerHTML;
  
  btn.innerHTML = '⏳ Menyiapkan Seluruh Data...';
  btn.disabled = true;

  const modalBox = document.querySelector('.modal-box');
  const modalBody = document.querySelector('.modal-body');

  // Save current scroll & styles so we can restore them seamlessly
  const savedScrollTop = modalBody ? modalBody.scrollTop : 0;
  const prevBoxMaxH = modalBox ? modalBox.style.maxHeight : '';
  const prevBoxOverflow = modalBox ? modalBox.style.overflow : '';
  const prevBodyOverflow = modalBody ? modalBody.style.overflow : '';
  const prevBodyHeight = modalBody ? modalBody.style.height : '';
  const prevBodyMaxH = modalBody ? modalBody.style.maxHeight : '';

  try {{
    // 1. Reset scroll to top
    if (modalBody) modalBody.scrollTop = 0;

    // 2. Temporarily unconstrain height & overflow so browser expands to 100% of data
    if (modalBox) {{
      modalBox.style.maxHeight = 'none';
      modalBox.style.overflow = 'visible';
    }}
    if (modalBody) {{
      modalBody.style.overflow = 'visible';
      modalBody.style.height = 'auto';
      modalBody.style.maxHeight = 'none';
    }}

    // Allow browser DOM reflow
    await new Promise(resolve => setTimeout(resolve, 80));

    // 3. Accurately calculate full dimensions (width 1180px for balanced aspect ratio)
    const fullHeight = Math.max(target.scrollHeight, target.offsetHeight, 600);
    const fullWidth = 1180;

    const isLight = document.body.classList.contains('light-theme');
    const bgColor = isLight ? '#ffffff' : '#111827';

    // 4. Run html2canvas with full dimensions and unconstrained clone
    const canvas = await html2canvas(target, {{
      scale: 2,
      useCORS: true,
      backgroundColor: bgColor,
      logging: false,
      width: fullWidth,
      height: fullHeight,
      windowWidth: Math.max(document.documentElement.clientWidth, 1260),
      windowHeight: fullHeight + 300,
      scrollY: 0,
      scrollX: 0,
      x: 0,
      y: 0,
      onclone: (clonedDoc) => {{
        clonedDoc.body.style.minWidth = '1220px';
        const cOverlay = clonedDoc.getElementById('portrait-modal');
        const cBox = clonedDoc.querySelector('.modal-box');
        const cBody = clonedDoc.querySelector('.modal-body');
        const cTarget = clonedDoc.getElementById('portrait-canvas-target');

        if (cOverlay) {{
          cOverlay.style.position = 'static';
          cOverlay.style.display = 'block';
          cOverlay.style.height = 'auto';
          cOverlay.style.maxHeight = 'none';
          cOverlay.style.overflow = 'visible';
          cOverlay.style.padding = '0';
        }}
        if (cBox) {{
          cBox.style.position = 'static';
          cBox.style.display = 'block';
          cBox.style.height = 'auto';
          cBox.style.maxHeight = 'none';
          cBox.style.maxWidth = 'none';
          cBox.style.width = '100%';
          cBox.style.overflow = 'visible';
          cBox.style.boxShadow = 'none';
          cBox.style.border = 'none';
        }}
        if (cBody) {{
          cBody.style.position = 'static';
          cBody.style.display = 'block';
          cBody.style.height = 'auto';
          cBody.style.maxHeight = 'none';
          cBody.style.overflow = 'visible';
          cBody.style.padding = '0';
        }}
        if (cTarget) {{
          cTarget.style.position = 'static';
          cTarget.style.height = 'auto';
          cTarget.style.maxHeight = 'none';
          cTarget.style.overflow = 'visible';
          cTarget.style.boxShadow = 'none';
          cTarget.style.margin = '0 auto';
          cTarget.style.width = '1180px';
          cTarget.style.maxWidth = '1180px';
          cTarget.style.minWidth = '1180px';
        }}
      }}
    }});

    const imgData = canvas.toDataURL('image/jpeg', 0.95);
    const link = document.createElement('a');
    link.href = imgData;
    const viewName = activePortraitView.toUpperCase();
    link.download = 'Uji_Petik_District_Bogor_' + viewName + '_' + new Date().toISOString().slice(0, 10) + '.jpg';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    btn.innerHTML = '✅ Berhasil Disimpan!';
    setTimeout(() => {{
      btn.innerHTML = originalText;
      btn.disabled = false;
    }}, 2000);
  }} catch (err) {{
    console.error('Gagal mengekspor JPG:', err);
    alert('Terjadi kesalahan saat memproses gambar JPG. Silakan coba lagi.');
    btn.innerHTML = originalText;
    btn.disabled = false;
  }} finally {{
    // 5. Always restore original modal styles and scroll position
    if (modalBox) {{
      modalBox.style.maxHeight = prevBoxMaxH;
      modalBox.style.overflow = prevBoxOverflow;
    }}
    if (modalBody) {{
      modalBody.style.overflow = prevBodyOverflow;
      modalBody.style.height = prevBodyHeight;
      modalBody.style.maxHeight = prevBodyMaxH;
      modalBody.scrollTop = savedScrollTop;
    }}
  }}
}}

// DYNAMIC OVERVIEW CHARTS & MATRICES
function renderOverviewCharts() {{
  const streamBox = document.getElementById('chart-stream-bars');
  const assAch = DATA.assurance.total.ach;
  const psbAch = DATA.psb.total.ach;
  const totSamp = DATA.assurance.total.sampling + DATA.psb.total.sampling;
  const totDone = DATA.assurance.total.done + DATA.psb.total.done;
  const totAch = totSamp > 0 ? (Math.round((totDone / totSamp) * 10000) / 100) : 0;
  
  if (streamBox) {{
    streamBox.innerHTML = `
      <div class="bar-row">
        <div class="bar-label"><strong>Assurance</strong></div>
        <div class="bar-track">
          <div class="bar-fill" style="width: ${{assAch}}%; background: linear-gradient(90deg, #3b82f6, #60a5fa);">${{assAch}}%</div>
        </div>
        <div class="bar-value">${{DATA.assurance.total.done}}/${{DATA.assurance.total.sampling}}</div>
      </div>
      <div class="bar-row">
        <div class="bar-label"><strong>PSB</strong></div>
        <div class="bar-track">
          <div class="bar-fill" style="width: ${{psbAch}}%; background: linear-gradient(90deg, #10b981, #34d399);">${{psbAch}}%</div>
        </div>
        <div class="bar-value">${{DATA.psb.total.done}}/${{DATA.psb.total.sampling}}</div>
      </div>
      <div class="bar-row">
        <div class="bar-label" style="color: var(--accent);"><strong>District Bogor</strong></div>
        <div class="bar-track">
          <div class="bar-fill" style="width: ${{totAch}}%; background: linear-gradient(90deg, #8b5cf6, #c084fc);">${{totAch}}%</div>
        </div>
        <div class="bar-value">${{totDone}}/${{totSamp}}</div>
      </div>
    `;
  }}

  const areaBox = document.getElementById('chart-area-bars');
  if (areaBox) {{
    let areaHtml = '';
    DATA.assurance.groups.forEach(g => {{
      let color = g.ach >= 95 ? 'var(--success-gradient)' : (g.ach >= 80 ? 'var(--warning-gradient)' : 'var(--danger-gradient)');
      areaHtml += `
        <div class="bar-row">
          <div class="bar-label"><strong>${{g.name}}</strong></div>
          <div class="bar-track">
            <div class="bar-fill" style="width: ${{g.ach}}%; background: ${{color}};">${{g.ach}}%</div>
          </div>
          <div class="bar-value">${{g.done}}/${{g.sampling}}</div>
        </div>
      `;
    }});
    areaBox.innerHTML = areaHtml;
  }}

  const saContainer = document.getElementById('sa-matrix-container');
  if (saContainer && DATA.psb.sa_summary) {{
    let saHtml = '';
    DATA.psb.sa_summary.forEach(sa => {{
      const isDone = sa.saldo === 0;
      const tileClass = isDone ? 'done' : 'pending';
      const statusText = isDone ? '100% TUNTAS' : sa.saldo + ' Saldo';
      const badgeClass = isDone ? 'badge-success' : 'badge-danger';
      
      saHtml += `
        <div class="sa-tile ${{tileClass}}">
          <div class="sa-tile-header">
            <span class="sa-title" title="${{sa.sa}}">${{sa.sa}}</span>
            <span class="badge ${{badgeClass}}">${{statusText}}</span>
          </div>
          <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-top: 4px;">
            <div style="font-size: 11px; color: var(--text-muted);">
              Done: <strong style="color: var(--text-main);">${{sa.done}}</strong>/${{sa.sampling}}
            </div>
            <div style="font-size: 14px; font-weight: 800; font-family: 'JetBrains Mono', monospace; color: ${{isDone ? 'var(--success)' : 'var(--danger)'}};">
              ${{sa.ach}}%
            </div>
          </div>
        </div>
      `;
    }});
    saContainer.innerHTML = saHtml;
  }}
}}

// ASSURANCE TABLE
function renderAssuranceTable() {{
  const tbody = document.getElementById('tbody-assurance');
  if (!tbody) return;
  const search = document.getElementById('search-ass').value.toLowerCase();
  const statusFilter = document.getElementById('filter-ass-status').value;

  let filtered = DATA.assurance.sektors.filter(item => {{
    const matchSearch = item.sektor.toLowerCase().includes(search) || item.pic.toLowerCase().includes(search);
    if (!matchSearch) return false;
    if (statusFilter === 'SALDO') return item.saldo > 0;
    if (statusFilter === 'DONE') return item.saldo === 0;
    return true;
  }});

  tbody.innerHTML = filtered.map((item, idx) => {{
    const isDone = item.saldo === 0;
    const progressColor = isDone ? 'var(--success)' : (item.ach >= 80 ? 'var(--warning)' : 'var(--danger)');
    const badgeClass = isDone ? 'badge-success' : 'badge-danger';
    const badgeText = isDone ? 'SUDAH' : 'BELUM (' + item.saldo + ' Saldo)';

    return `
      <tr>
        <td class="num-col" style="color: var(--text-muted);">${{idx + 1}}</td>
        <td><strong>${{item.sektor}}</strong></td>
        <td><span style="font-size:12px; color: var(--text-muted);">${{item.pic || '-'}}</span></td>
        <td class="num-col">${{item.sampling}}</td>
        <td class="num-col" style="color: var(--success); font-weight: 800;">${{item.done}}</td>
        <td class="num-col" style="color: ${{item.saldo > 0 ? 'var(--danger)' : 'var(--text-muted)'}}; font-weight: 800;">${{item.saldo}}</td>
        <td>
          <div class="table-progress">
            <div class="table-progress-bar">
              <div class="table-progress-fill" style="width: ${{item.ach}}%; background: ${{progressColor}};"></div>
            </div>
          </div>
        </td>
        <td class="num-col" style="font-weight: 800; color: ${{progressColor}};">${{item.ach}}%</td>
        <td><span class="badge ${{badgeClass}}">${{badgeText}}</span></td>
      </tr>
    `;
  }}).join('');

  const tfoot = document.getElementById('tfoot-assurance');
  if (tfoot) {{
    const tot = DATA.assurance.total;
    tfoot.innerHTML = `
      <tr style="background: var(--card-solid); font-weight: 800; border-top: 2px solid var(--card-border);">
        <td colspan="3" style="text-align: right; font-size: 12px;">TOTAL ASSURANCE (${{DATA.assurance.sektors.length}} SEKTOR):</td>
        <td class="num-col" style="color: var(--primary); font-size: 13px;">${{tot.sampling}}</td>
        <td class="num-col" style="color: var(--success); font-size: 13px;">${{tot.done}}</td>
        <td class="num-col" style="color: var(--danger); font-size: 14px;">${{tot.saldo}}</td>
        <td colspan="2" class="num-col" style="color: var(--success); font-size: 13px;">${{tot.ach}}%</td>
        <td><span class="badge ${{tot.saldo === 0 ? 'badge-success' : 'badge-warning'}}">${{tot.saldo}} SALDO</span></td>
      </tr>
    `;
  }}
}}

// AREA SCORECARDS (ASSURANCE)
function renderAssuranceAreaCards() {{
  const container = document.getElementById('assurance-area-cards');
  if (!container || !DATA.assurance.groups) return;
  container.innerHTML = DATA.assurance.groups.map(g => {{
    const isCritical = g.saldo >= 5;
    const borderStyle = isCritical ? 'border-left: 4px solid var(--danger);' : '';
    const pctColor = g.ach >= 90 ? 'var(--success)' : (g.ach >= 75 ? 'var(--warning)' : 'var(--danger)');
    const saldoColor = g.saldo > 0 ? 'var(--danger)' : 'var(--success)';
    return `
      <div class="area-scorecard" style="${{borderStyle}}">
        <div class="area-card-top">
          <span class="area-name" style="${{isCritical ? 'color: var(--danger);' : ''}}">Area ${{g.name}}</span>
          <span class="area-pct" style="color: ${{pctColor}};">${{g.ach}}%</span>
        </div>
        <div style="font-size: 12px; color: var(--text-muted);">Sampling: <strong>${{g.sampling}}</strong> • Done: <strong>${{g.done}}</strong></div>
        <div style="margin-top: 6px; font-size: 12px; color: ${{saldoColor}}; font-weight: ${{isCritical ? '800' : '700'}};">Sisa Saldo: ${{g.saldo}} Order${{isCritical ? ' (Kritis)' : ''}}</div>
      </div>
    `;
  }}).join('');
}}

// PSB TABLE
function renderPSBTable() {{
  const tbody = document.getElementById('tbody-psb');
  if (!tbody) return;
  const search = document.getElementById('search-psb').value.toLowerCase();
  const saFilter = document.getElementById('filter-psb-sa').value;
  const statusFilter = document.getElementById('filter-psb-status').value;

  let filtered = DATA.psb.sto_list.filter(item => {{
    const matchSearch = item.sto.toLowerCase().includes(search) || item.sa.toLowerCase().includes(search) || item.pic.toLowerCase().includes(search);
    if (!matchSearch) return false;
    if (saFilter !== 'ALL' && item.sa !== saFilter) return false;
    if (statusFilter === 'SALDO') return item.saldo > 0;
    if (statusFilter === 'DONE') return item.saldo === 0;
    return true;
  }});

  tbody.innerHTML = filtered.map((item, idx) => {{
    const isDone = item.saldo === 0;
    const progressColor = isDone ? 'var(--success)' : (item.qc >= 50 ? 'var(--warning)' : 'var(--danger)');
    const badgeClass = isDone ? 'badge-success' : 'badge-danger';
    const badgeText = isDone ? 'SUDAH' : 'BELUM (' + item.saldo + ' Saldo)';

    return `
      <tr>
        <td class="num-col" style="color: var(--text-muted);">${{idx + 1}}</td>
        <td><strong style="color: var(--primary); font-size: 14px;">${{item.sto}}</strong></td>
        <td><span style="font-weight: 600;">${{item.sa}}</span></td>
        <td><span style="font-size:12px; color: var(--text-muted);">${{item.pic}}</span></td>
        <td class="num-col">${{item.sampling}}</td>
        <td class="num-col" style="color: var(--success); font-weight: 800;">${{item.done}}</td>
        <td class="num-col" style="color: ${{item.saldo > 0 ? 'var(--danger)' : 'var(--text-muted)'}}; font-weight: 800;">${{item.saldo}}</td>
        <td>
          <div class="table-progress">
            <div class="table-progress-bar">
              <div class="table-progress-fill" style="width: ${{item.qc}}%; background: ${{progressColor}};"></div>
            </div>
          </div>
        </td>
        <td class="num-col" style="font-weight: 800; color: ${{progressColor}};">${{item.qc}}%</td>
        <td><span class="badge ${{badgeClass}}">${{badgeText}}</span></td>
      </tr>
    `;
  }}).join('');

  const tfoot = document.getElementById('tfoot-psb');
  if (tfoot) {{
    const tot = DATA.psb.total;
    tfoot.innerHTML = `
      <tr style="background: var(--card-solid); font-weight: 800; border-top: 2px solid var(--card-border);">
        <td colspan="4" style="text-align: right; font-size: 12px;">TOTAL PSB (${{DATA.psb.sto_list.length}} STO):</td>
        <td class="num-col" style="color: var(--primary); font-size: 13px;">${{tot.sampling}}</td>
        <td class="num-col" style="color: var(--success); font-size: 13px;">${{tot.done}}</td>
        <td class="num-col" style="color: var(--danger); font-size: 14px;">${{tot.saldo}}</td>
        <td colspan="2" class="num-col" style="color: var(--warning); font-size: 13px;">${{tot.ach}}%</td>
        <td><span class="badge ${{tot.saldo === 0 ? 'badge-success' : 'badge-warning'}}">${{tot.saldo}} SALDO</span></td>
      </tr>
    `;
  }}
}}

// DYNAMIC BOTTLENECK CARDS (AUTOMATICALLY EXTRACTED FROM LIVE DATA)
function renderBottlenecks() {{
  const container = document.getElementById('bottleneck-cards-container');
  if (!container) return;

  const items = [];

  DATA.assurance.sektors.forEach(s => {{
    if (s.saldo > 0) {{
      items.push({{
        title: s.sektor + ' (Assurance)',
        pic: s.pic || '-',
        saldo: s.saldo,
        target: s.sampling,
        done: s.done,
        ach: s.ach,
        severity: s.saldo >= 5 ? 'critical' : 'warning',
        note: `Penyumbang ${{s.saldo}} saldo pada Assurance. Capaian saat ini ${{s.ach}}%.`
      }});
    }}
  }});

  DATA.psb.sto_list.forEach(s => {{
    if (s.saldo > 0) {{
      items.push({{
        title: `SA ${{s.sa}} - STO ${{s.sto}} (PSB)`,
        pic: s.pic || '-',
        saldo: s.saldo,
        target: s.sampling,
        done: s.done,
        ach: s.qc,
        severity: s.saldo >= 3 ? 'critical' : 'warning',
        note: `Penyumbang ${{s.saldo}} saldo pada PSB. Capaian saat ini ${{s.qc}}%.`
      }});
    }}
  }});

  items.sort((a, b) => b.saldo - a.saldo || a.ach - b.ach);
  const topBottlenecks = items.slice(0, 6);

  if (topBottlenecks.length === 0) {{
    container.innerHTML = `
      <div style="grid-column: 1 / -1; text-align: center; padding: 40px; background: var(--card-solid); border-radius: 16px; border: 1px solid var(--card-border);">
        <div style="font-size: 40px; margin-bottom: 10px;">🎉</div>
        <h3 style="color: var(--success); font-size: 20px; font-weight: 800;">SELURUH ORDER SUDAH TUNTAS (0 SALDO)!</h3>
        <p style="color: var(--text-muted); font-size: 13px; margin-top: 6px;">Luar biasa! Tidak ada kendala bottleneck tersisa di District Bogor & Sukabumi.</p>
      </div>
    `;
    return;
  }}

  container.innerHTML = topBottlenecks.map(b => `
    <div class="bottleneck-card ${{b.severity}}">
      <div class="bottleneck-title">
        <span>${{b.title}}</span>
        <span class="badge ${{b.severity === 'critical' ? 'badge-danger' : 'badge-warning'}}">${{b.saldo}} SALDO</span>
      </div>
      <div class="bottleneck-info">👤 PIC: <strong>${{b.pic}}</strong></div>
      <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 10px;">${{b.note}}</p>
      <div class="bottleneck-stat">
        <span>Target: <strong>${{b.target}}</strong></span>
        <span>Done: <strong style="color:var(--success);">${{b.done}}</strong></span>
        <span>Ach: <strong style="color:${{b.ach < 50 ? 'var(--danger)' : 'var(--warning)'}};">${{b.ach}}%</strong></span>
      </div>
    </div>
  `).join('');
}}

// PIC LEADERBOARD
function renderPICTable() {{
  const tbody = document.getElementById('tbody-pic');
  if (!tbody) return;
  const search = document.getElementById('search-pic').value.toLowerCase();

  const picMap = {{}};
  DATA.assurance.sektors.forEach(s => {{
    const rawPic = s.pic || 'Unknown';
    const name = rawPic.split('|')[0].trim();
    if (!picMap[name]) picMap[name] = {{ name: name, sampling: 0, done: 0, saldo: 0 }};
    picMap[name].sampling += s.sampling;
    picMap[name].done += s.done;
    picMap[name].saldo += s.saldo;
  }});

  DATA.psb.sto_list.forEach(s => {{
    const rawPic = s.pic || 'Unknown';
    const name = rawPic.split('-')[0].trim();
    if (!picMap[name]) picMap[name] = {{ name: name, sampling: 0, done: 0, saldo: 0 }};
    picMap[name].sampling += s.sampling;
    picMap[name].done += s.done;
    picMap[name].saldo += s.saldo;
  }});

  let picList = Object.values(picMap).map(p => {{
    p.ach = p.sampling > 0 ? Math.round((p.done / p.sampling) * 10000) / 100 : 0;
    return p;
  }});

  picList.sort((a, b) => b.saldo - a.saldo || a.ach - b.ach);

  let filtered = picList.filter(p => p.name.toLowerCase().includes(search));

  tbody.innerHTML = filtered.map((p, idx) => {{
    const isDone = p.saldo === 0;
    const progressColor = isDone ? 'var(--success)' : (p.ach >= 80 ? 'var(--warning)' : 'var(--danger)');
    const badge = isDone ? '<span class="badge badge-success">⭐ 100% COMPLETE</span>' : (p.saldo >= 5 ? '<span class="badge badge-danger">⚠️ CRITICAL FOLLOW-UP</span>' : '<span class="badge badge-warning">⏳ SISA ' + p.saldo + ' SALDO</span>');
    const medal = idx === 0 ? '🥇' : (idx === 1 ? '🥈' : (idx === 2 ? '🥉' : '#' + (idx + 1)));

    return `
      <tr>
        <td class="num-col" style="color: var(--text-muted); font-weight: 800;">${{medal}}</td>
        <td><strong style="font-size: 14px;">${{p.name}}</strong></td>
        <td class="num-col">${{p.sampling}}</td>
        <td class="num-col" style="color: var(--success); font-weight: 800;">${{p.done}}</td>
        <td class="num-col" style="color: ${{p.saldo > 0 ? 'var(--danger)' : 'var(--text-muted)'}}; font-weight: 800;">${{p.saldo}}</td>
        <td>
          <div class="table-progress">
            <div class="table-progress-bar">
              <div class="table-progress-fill" style="width: ${{p.ach}}%; background: ${{progressColor}};"></div>
            </div>
          </div>
        </td>
        <td class="num-col" style="font-weight: 800; color: ${{progressColor}};">${{p.ach}}%</td>
        <td>${{badge}}</td>
      </tr>
    `;
  }}).join('');
}}

// CSV EXPORT
function exportTableCSV() {{
  let csv = 'Stream,Sektor_STO,Area_SA,PIC,Sampling,Done,Saldo,Ach_Pct,Status\\n';
  DATA.assurance.sektors.forEach(s => {{
    csv += `Assurance,"${{s.sektor}}","District Bogor","${{s.pic}}",${{s.sampling}},${{s.done}},${{s.saldo}},${{s.ach}}%,${{s.saldo === 0 ? 'SUDAH' : 'BELUM'}}\\n`;
  }});
  DATA.psb.sto_list.forEach(s => {{
    csv += `PSB,"${{s.sto}}","${{s.sa}}","${{s.pic}}",${{s.sampling}},${{s.done}},${{s.saldo}},${{s.qc}}%,${{s.saldo === 0 ? 'SUDAH' : 'BELUM'}}\\n`;
  }});

  const blob = new Blob([csv], {{ type: 'text/csv;charset=utf-8;' }});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'rekap_uji_petik_district_bogor.csv';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
}}

function populateSAFilter() {{
  const select = document.getElementById('filter-psb-sa');
  if (!select) return;
  const currentVal = select.value;
  select.innerHTML = '<option value="ALL">Semua Service Area (SA)</option>';
  const sas = Array.from(new Set(DATA.psb.sto_list.map(s => s.sa))).sort();
  sas.forEach(sa => {{
    const opt = document.createElement('option');
    opt.value = sa;
    opt.textContent = sa;
    select.appendChild(opt);
  }});
  select.value = currentVal || 'ALL';
}}

// DYNAMIC TOP KPI STATS
function renderExecutiveStats() {{
  const ass = DATA.assurance.total;
  const psb = DATA.psb.total;
  const totSamp = ass.sampling + psb.sampling;
  const totDone = ass.done + psb.done;
  const totSaldo = ass.saldo + psb.saldo;
  const totAch = totSamp > 0 ? (Math.round((totDone / totSamp) * 10000) / 100) : 0;
  const saldoPct = totSamp > 0 ? (Math.round((totSaldo / totSamp) * 10000) / 100) : 0;

  const gaugeCircle = document.getElementById('gauge-circle');
  const gaugePct = document.getElementById('kpi-gauge-pct');
  const realisasiSub = document.getElementById('kpi-realisasi-sub');
  if (gaugePct) gaugePct.textContent = totAch + '%';
  if (realisasiSub) realisasiSub.innerHTML = `Realisasi: <strong style="color: var(--success);">${{totDone}}</strong> dari <strong>${{totSamp}}</strong> Sampling`;
  if (gaugeCircle) {{
    const radius = 80;
    const circ = 2 * Math.PI * radius; // 502.65
    const offset = circ - (circ * totAch) / 100;
    gaugeCircle.style.strokeDasharray = `${{circ}}`;
    gaugeCircle.style.strokeDashoffset = `${{offset}}`;
  }}

  const elTarget = document.getElementById('kpi-total-target');
  const elTargetSub = document.getElementById('kpi-target-subtext');
  if (elTarget) elTarget.textContent = totSamp;
  if (elTargetSub) elTargetSub.innerHTML = `<span>Assurance: <strong>${{ass.sampling}}</strong></span><span>PSB: <strong>${{psb.sampling}}</strong></span>`;

  const elDone = document.getElementById('kpi-total-done');
  const elDoneSub = document.getElementById('kpi-done-subtext');
  const elDoneBar = document.getElementById('kpi-done-bar');
  if (elDone) elDone.textContent = totDone;
  if (elDoneSub) elDoneSub.innerHTML = `<span>Assurance: <strong>${{ass.done}}</strong></span><span>PSB: <strong>${{psb.done}}</strong></span>`;
  if (elDoneBar) elDoneBar.style.width = totAch + '%';

  const elSaldo = document.getElementById('kpi-total-saldo');
  const elSaldoSub = document.getElementById('kpi-saldo-subtext');
  const elSaldoBar = document.getElementById('kpi-saldo-bar');
  if (elSaldo) elSaldo.textContent = totSaldo;
  if (elSaldoSub) elSaldoSub.innerHTML = `<span>Assurance: <strong>${{ass.saldo}}</strong></span><span>PSB: <strong>${{psb.saldo}}</strong></span>`;
  if (elSaldoBar) elSaldoBar.style.width = saldoPct + '%';

  const elAlertSaldo = document.getElementById('alert-total-saldo');
  if (elAlertSaldo) elAlertSaldo.textContent = totSaldo + ' saldo';

  const cardTarget = document.getElementById('psb-card-target');
  const cardDone = document.getElementById('psb-card-done');
  const cardAch = document.getElementById('psb-card-ach');
  const cardSaldo = document.getElementById('psb-card-saldo');
  if (cardTarget) cardTarget.textContent = psb.sampling;
  if (cardDone) cardDone.textContent = psb.done;
  if (cardAch) cardAch.textContent = `Capaian: ${{psb.ach}}%`;
  if (cardSaldo) cardSaldo.textContent = psb.saldo;
}}

// DYNAMIC NAVIGATION BADGES
function renderNavigationBadges() {{
  const ass = DATA.assurance.total;
  const psb = DATA.psb.total;
  const totSaldo = ass.saldo + psb.saldo;

  const bAss = document.getElementById('nav-badge-ass');
  const bPsb = document.getElementById('nav-badge-psb');
  const bSaldo = document.getElementById('nav-badge-saldo');

  if (bAss) bAss.textContent = ass.ach + '%';
  if (bPsb) bPsb.textContent = psb.ach + '%';
  if (bSaldo) {{
    bSaldo.textContent = totSaldo + ' Saldo';
    if (totSaldo === 0) {{
      bSaldo.style.background = 'rgba(16,185,129,0.25)';
      bSaldo.style.color = '#34d399';
    }} else {{
      bSaldo.style.background = 'rgba(239,68,68,0.25)';
      bSaldo.style.color = '#f87171';
    }}
  }}
}}

// LIVE SINKRONISASI REALTIME DARI GOOGLE SHEETS
const GOOGLE_SHEET_ID = "1iCLX_scRmLAMwKrjOS2FkasGwB2q8NOtfzjxxYol8Ow";

async function fetchGoogleSheetGviz(sheetName) {{
  const url = `https://docs.google.com/spreadsheets/d/${{GOOGLE_SHEET_ID}}/gviz/tq?tqx=out:json&sheet=${{encodeURIComponent(sheetName)}}&t=${{Date.now()}}`;
  const res = await fetch(url);
  if (!res.ok) throw new Error(`HTTP ${{res.status}}`);
  const text = await res.text();
  const match = text.match(/google\.visualization\.Query\.setResponse\(([\s\S]*)\);/);
  if (!match) throw new Error("Format respon Google Sheets tidak sesuai");
  return JSON.parse(match[1]);
}}

async function syncGoogleSheetsData(silent = false) {{
  const btn = document.getElementById('btn-sync-sheet');
  const icon = document.getElementById('sync-icon');
  const text = document.getElementById('sync-text');
  const statusBadge = document.getElementById('sync-status-badge');
  const cutoffLabel = document.getElementById('cutoff-date-val');

  if (!silent && btn) {{
    btn.disabled = true;
    if (icon) icon.textContent = '⏳';
    if (text) text.textContent = 'Menyinkronkan...';
  }}

  try {{
    const [assGviz, psbGviz] = await Promise.all([
      fetchGoogleSheetGviz('UJI PETIK ASSURANCE'),
      fetchGoogleSheetGviz('UJI PETIK PSB')
    ]);

    // Parse ASSURANCE rows
    const assRows = assGviz.table.rows;
    const newAssSektors = [];
    const newGroups = [];

    for (let r = 3; r < Math.min(assRows.length, 33); r++) {{
      const row = assRows[r];
      if (!row || !row.c) continue;
      const c = row.c.map(cell => cell && cell.v !== undefined ? cell.v : null);
      const no = c[0];
      const sektor = c[1];
      const pic = c[2];
      const samp = Number(c[3]) || 0;
      const saldo = Number(c[4]) || 0;
      const done = Number(c[5]) || 0;
      const ach = Number(c[6]) || 0;

      if (sektor && pic) {{
        newAssSektors.push({{
          no: typeof no === 'number' ? no : newAssSektors.length + 1,
          sektor: String(sektor).trim(),
          pic: String(pic).trim(),
          sampling: samp,
          saldo: saldo,
          done: done,
          ach: Math.round(ach * 10000) / 100
        }});
      }} else if (!pic && c[0] && String(c[0]).trim() !== 'WITEL BOGOR') {{
        newGroups.push({{
          name: String(c[0]).trim(),
          sampling: samp,
          saldo: saldo,
          done: done,
          ach: Math.round(ach * 10000) / 100
        }});
      }}
    }}

    // Parse PSB rows
    const psbRows = psbGviz.table.rows;
    const newPsbSto = [];
    for (let r = 4; r < Math.min(psbRows.length, 45); r++) {{
      const row = psbRows[r];
      if (!row || !row.c) continue;
      const c = row.c.map(cell => cell && cell.v !== undefined ? cell.v : null);
      const no = c[1];
      const sa = c[2];
      const pic = c[4];
      const sto = c[5];
      const samp = Number(c[6]) || 0;
      const done = Number(c[7]) || 0;
      const saldo = Number(c[8]) || 0;
      const qc = Number(c[9]) || 0;
      const ach = Number(c[10]) || 0;

      if (sto) {{
        newPsbSto.push({{
          no: typeof no === 'number' ? no : newPsbSto.length + 1,
          sa: String(sa || '').trim(),
          pic: String(pic || '').trim(),
          sto: String(sto).trim(),
          sampling: samp,
          done: done,
          saldo: saldo,
          qc: Math.round(qc * 10000) / 100,
          ach: Math.round(ach * 10000) / 100
        }});
      }}
    }}

    // Update DATA state
    if (newAssSektors.length > 0) {{
      DATA.assurance.sektors = newAssSektors;
      const totSamp = newAssSektors.reduce((a, b) => a + b.sampling, 0);
      const totDone = newAssSektors.reduce((a, b) => a + b.done, 0);
      const totSaldo = newAssSektors.reduce((a, b) => a + b.saldo, 0);
      DATA.assurance.total = {{
        sampling: totSamp,
        done: totDone,
        saldo: totSaldo,
        ach: totSamp > 0 ? Math.round((totDone / totSamp) * 10000) / 100 : 0
      }};
      if (newGroups.length > 0) DATA.assurance.groups = newGroups;
    }}

    if (newPsbSto.length > 0) {{
      DATA.psb.sto_list = newPsbSto;
      
      // Deteksi baris TOTAL resmi di Google Sheet (baris 38/39)
      let officialTotal = null;
      for (let r = psbRows.length - 1; r >= 30; r--) {{
        const row = psbRows[r];
        if (!row || !row.c) continue;
        const samp = Number(row.c[6] && row.c[6].v);
        const done = Number(row.c[7] && row.c[7].v);
        const saldo = Number(row.c[8] && row.c[8].v);
        if (samp > 50 && done > 0) {{
          const qc = Number(row.c[9] && row.c[9].v) || (done / samp);
          officialTotal = {{
            sampling: samp,
            done: done,
            saldo: saldo,
            ach: Math.round(qc * 10000) / 100
          }};
          break;
        }}
      }}

      if (officialTotal) {{
        DATA.psb.total = officialTotal;
      }} else {{
        const totSamp = newPsbSto.reduce((a, b) => a + b.sampling, 0);
        const totDone = newPsbSto.reduce((a, b) => a + b.done, 0);
        const totSaldo = newPsbSto.reduce((a, b) => a + b.saldo, 0);
        DATA.psb.total = {{
          sampling: totSamp,
          done: totDone,
          saldo: totSaldo,
          ach: totSamp > 0 ? Math.round((totDone / totSamp) * 10000) / 100 : 0
        }};
      }}
    }}

    const now = new Date();
    const timeStr = now.toLocaleDateString('id-ID', {{ day: '2-digit', month: 'short', year: 'numeric' }}) + ', ' + now.toLocaleTimeString('id-ID', {{ hour: '2-digit', minute: '2-digit', second: '2-digit' }});
    DATA.meta.refreshed_at = timeStr;

    // Cache to localStorage
    try {{
      localStorage.setItem('uji_petik_live_cache_v3', JSON.stringify({{ data: DATA, timestamp: Date.now() }}));
    }} catch(e) {{}}

    // Update UI elements
    if (cutoffLabel) cutoffLabel.textContent = timeStr;
    if (statusBadge) {{
      statusBadge.style.display = 'inline-flex';
      statusBadge.innerHTML = '🟢 Terhubung Google Sheet: ' + now.toLocaleTimeString('id-ID', {{ hour: '2-digit', minute: '2-digit' }});
    }}

    renderAll();

    if (!silent) {{
      alert(`✅ Berhasil Sinkronisasi Langsung dari Google Sheet!\\n\\n` +
            `• Assurance: ${{DATA.assurance.total.done}}/${{DATA.assurance.total.sampling}} (${{DATA.assurance.total.ach}}%) • Saldo: ${{DATA.assurance.total.saldo}}\\n` +
            `• PSB: ${{DATA.psb.total.done}}/${{DATA.psb.total.sampling}} (${{DATA.psb.total.ach}}%) • Saldo: ${{DATA.psb.total.saldo}}\\n` +
            `• Total Saldo Distrik: ${{DATA.assurance.total.saldo + DATA.psb.total.saldo}} Saldo`);
    }}
  }} catch (err) {{
    console.warn("Live sync Google Sheet error:", err);
    if (statusBadge) {{
      statusBadge.innerHTML = '🟡 Mode Offline / Data Tersimpan';
    }}
    if (!silent) {{
      alert("⚠️ Gagal sinkronisasi langsung dari Google Sheet (mungkin kendala jaringan). Menggunakan data tersimpan terakhir.");
    }}
  }} finally {{
    if (btn) {{
      btn.disabled = false;
      if (icon) icon.textContent = '🔄';
      if (text) text.textContent = 'Sinkron Sheet';
    }}
  }}
}}

// MASTER RENDER ALL
function renderAll() {{
  renderExecutiveStats();
  renderNavigationBadges();
  renderOverviewCharts();
  renderAssuranceAreaCards();
  renderAssuranceTable();
  populateSAFilter();
  renderPSBTable();
  renderBottlenecks();
  renderPICTable();
  if (document.getElementById('portrait-modal').classList.contains('active')) {{
    selectPortraitView(activePortraitView);
  }}
}}

window.addEventListener('DOMContentLoaded', () => {{
  initTheme();

  // 1. Restore from localStorage cache if available
  try {{
    const cached = localStorage.getItem('uji_petik_live_cache_v3');
    if (cached) {{
      const parsed = JSON.parse(cached);
      if (parsed && parsed.data) {{
        DATA.assurance = parsed.data.assurance;
        DATA.psb = parsed.data.psb;
        if (parsed.data.meta) DATA.meta = parsed.data.meta;
        const cutoffLabel = document.getElementById('cutoff-date-val');
        if (cutoffLabel && DATA.meta.refreshed_at) cutoffLabel.textContent = DATA.meta.refreshed_at;
      }}
    }}
  }} catch(e) {{}}

  // 2. Render all components immediately
  renderAll();

  // 3. Automatically trigger silent live sync from Google Sheet in background
  syncGoogleSheetsData(true);

  // 4. Auto-sync every 3 minutes while dashboard is kept open
  setInterval(() => {{
    syncGoogleSheetsData(true);
  }}, 180000);
}});
</script>

</body>
</html>'''

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print('Successfully built dashboard with Google Sheet Live Sync!')
