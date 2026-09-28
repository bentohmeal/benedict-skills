# Finds the files Benedict's rule says to use (see memory: cv-cover-letter-sources):
#   CV            = newest "Benedict_Toh Resume*" by date modified
#   CV layout     = newest "Benedict_Toh Resume*.docx" (used when the newest CV is a PDF)
#   Cover letter  = newest .docx in "Cover Letters 2027" (base template)
# Also reports whether experience-log.md was built from an older CV.
$ErrorActionPreference = 'Stop'
$apps = 'C:\Users\user\Documents\Google Drive\01. IB PE\Application Stuff (28 Aug 2026)\2026 Summer Applications'
$bank = 'C:\Users\user\Documents\Google Drive\Claude Things\Interview Prep\Master Bank'

$cvs = Get-ChildItem -LiteralPath "$apps\Resume" -File | Where-Object { $_.Name -like 'Benedict_Toh Resume*' } | Sort-Object LastWriteTime -Descending
$cv = $cvs | Select-Object -First 1
$cvDocx = $cvs | Where-Object { $_.Extension -eq '.docx' } | Select-Object -First 1
$cl = Get-ChildItem -LiteralPath "$apps\Cover Letters 2027" -File -Filter '*.docx' | Sort-Object LastWriteTime -Descending | Select-Object -First 1
$empty = Get-ChildItem -LiteralPath "$apps\Cover Letters 2027" -File | Where-Object { $_.Length -eq 0 }

"CV_LATEST=$($cv.FullName)"
"CV_LATEST_DATE=$($cv.LastWriteTime.ToString('yyyy-MM-dd'))"
"CV_LAYOUT_DOCX=$($cvDocx.FullName)"
"CV_LAYOUT_DATE=$($cvDocx.LastWriteTime.ToString('yyyy-MM-dd'))"
"COVER_LETTER_BASE=$($cl.FullName)"
"COVER_LETTER_BASE_DATE=$($cl.LastWriteTime.ToString('yyyy-MM-dd'))"
foreach ($e in $empty) { "WARN_EMPTY_FILE=$($e.FullName)" }

$log = Get-Content -LiteralPath "$bank\experience-log.md" -TotalCount 5 -Encoding UTF8 | Out-String
$m = [regex]::Match($log, 'Built from: `([^`]+)` \(modified (\d{4}-\d{2}-\d{2})\)')
if ($m.Success) {
  "EXPLOG_BUILT_FROM=$($m.Groups[1].Value) ($($m.Groups[2].Value))"
  if ($m.Groups[1].Value -ne $cv.Name -or $m.Groups[2].Value -ne $cv.LastWriteTime.ToString('yyyy-MM-dd')) { 'EXPLOG_STALE=yes' } else { 'EXPLOG_STALE=no' }
} else { 'EXPLOG_STALE=unknown' }
