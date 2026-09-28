# QA for a tailored cover letter or CV (.docx or .txt/.md).
# Flags: (1) any firm name other than the target, (2) present-tense verbs about finished internships,
#        (3) leftover {Firm}/{Role}/[placeholder] tokens, (4) deal figures that don't match the Master Bank.
# Usage: powershell -File qa-letter.ps1 -Path "C:\...\Benedict_Toh (BlackRock).docx" -Firm "BlackRock"
# Exit code 0 = clean, 1 = issues found.
param(
  [Parameter(Mandatory = $true)][string]$Path,
  [Parameter(Mandatory = $true)][string]$Firm,
  [string[]]$Aliases = @()
)
$ErrorActionPreference = 'Stop'
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = 'C:\Users\user\Documents\Google Drive'
$apps = "$root\01. IB PE\Application Stuff (28 Aug 2026)\2026 Summer Applications"

if ($Path -like '*.docx') { $text = & "$here\docx-text.ps1" -Path $Path | Out-String }
else { $text = Get-Content -LiteralPath $Path -Raw -Encoding UTF8 }

# --- firm names to watch for: recruiting tracker + cover-letter filenames + common banks/funds ---
$names = New-Object System.Collections.Generic.HashSet[string]
$tracker = "$root\Claude Things\Weekly Tracker\Recruiting\recruiting-tracker.md"
if (Test-Path -LiteralPath $tracker) {
  foreach ($l in Get-Content -LiteralPath $tracker -Encoding UTF8) {
    if ($l -match '^\|\s*([^|]+?)\s*\|' -and $l -notmatch '^\|\s*(Firm|-+)\s*\|') { [void]$names.Add($Matches[1]) }
  }
}
foreach ($d in "$apps\Cover Letters 2027", "$apps\Cover Letters") {
  if (Test-Path -LiteralPath $d) {
    Get-ChildItem -LiteralPath $d -File | ForEach-Object { if ($_.BaseName -match '\(([^)]+)\)') { [void]$names.Add($Matches[1]) } }
  }
}
'Barclays','Goldman Sachs','J.P. Morgan','JPMorgan','Morgan Stanley','Citi','Citigroup','Bank of America','BofA','UBS',
'Deutsche Bank','HSBC','Jefferies','Lazard','Macquarie','Nomura','Mizuho','SMBC','MUFG','BNP Paribas','Standard Chartered',
'Blackstone','KKR','Carlyle','EQT','CVC','TPG','Bain Capital','Warburg Pincus','Apollo','Ares','Brookfield','Temasek','GIC',
'Pantheon','Partners Group','BlackRock','Hamilton Lane','Ardian','Coller','HarbourVest','Pentagreen','Keppel','PwC','EY' |
  ForEach-Object { [void]$names.Add($_) }

# Firms legitimately named in Benedict's own experience or deals — never flagged.
$ownHistory = 'Partners Group','Pantheon','Pantheon Ventures','PwC','PricewaterhouseCoopers','CAP 1','CAP 1 Financial Group','EQT',
  'Shikoku','Archipelago Capital Partners','SMU'
$target = @($Firm) + $Aliases

$issues = @()
foreach ($n in $names) {
  if ($n -eq '—' -or $n.Length -lt 2) { continue }
  if ($target | Where-Object { $_ -ieq $n -or $n -like "*$_*" -or $_ -like "*$n*" }) { continue }
  if ($ownHistory | Where-Object { $_ -ieq $n }) { continue }
  $rx = '(?<![A-Za-z])' + [regex]::Escape($n) + '(?![A-Za-z])'
  foreach ($m in [regex]::Matches($text, $rx)) {
    $s = [Math]::Max(0, $m.Index - 50); $len = [Math]::Min(110, $text.Length - $s)
    $issues += "WRONG FIRM '$n': ..." + ($text.Substring($s, $len) -replace '\s+', ' ') + '...'
  }
}
if ($text -notmatch [regex]::Escape($Firm)) { $issues += "TARGET MISSING: '$Firm' does not appear anywhere" }

# --- present tense for finished internships (all of Benedict's internships have ended) ---
foreach ($v in 'I support','I execute','I conduct','I analyse','I analyze','I build','I work on','I am interning','I currently') {
  if ($text -match ([regex]::Escape($v) + '(?![A-Za-z])')) { $issues += "TENSE: '$v' - internship is finished, use past tense" }
}
# --- unfilled placeholders ---
foreach ($m in [regex]::Matches($text, '\{Firm\}|\{Role\}|\[(?:PLACEHOLDER|placeholder|to fill|confirm)[^\]]*\]')) { $issues += "PLACEHOLDER: $($m.Value)" }
# --- figures known to conflict with the Master Bank (PG dossier wins) ---
if ($text -match '3\.7\s?bn|3\.7 billion') { $issues += 'FIGURE: Kafka EV should be ~USD 3.6bn (Master Bank)' }
if ($text -match '5\.25x|6\.0x total') { $issues += 'FIGURE: Mosaic leverage should be ~5.3x (Master Bank)' }

if ($issues.Count) { 'ISSUES FOUND:'; $issues | Sort-Object -Unique | ForEach-Object { " - $_" }; exit 1 }
'CLEAN: no wrong firm names, tense problems, placeholders or conflicting figures found.'
exit 0
