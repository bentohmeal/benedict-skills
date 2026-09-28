# Prints the plain text of a .docx (one paragraph per line; headings prefixed with [StyleName]).
# Usage: powershell -File docx-text.ps1 -Path "C:\...\file.docx"
# Uses regex, not [xml], because some of Benedict's docs contain malformed XML.
param([Parameter(Mandatory = $true)][string]$Path)
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.IO.Compression.FileSystem
$z = [IO.Compression.ZipFile]::OpenRead($Path)
try {
  $r = New-Object IO.StreamReader($z.GetEntry('word/document.xml').Open())
  $x = $r.ReadToEnd(); $r.Close()
} finally { $z.Dispose() }
$out = foreach ($m in [regex]::Matches($x, '<w:p[ >].*?</w:p>', 'Singleline')) {
  $t = ([regex]::Matches($m.Value, '<w:t(?: [^>]*)?>([^<]*)</w:t>') | ForEach-Object { $_.Groups[1].Value }) -join ''
  $t = [Net.WebUtility]::HtmlDecode($t)
  if ($t.Trim()) {
    $style = [regex]::Match($m.Value, '<w:pStyle w:val="(Heading[^"]*|Title)"').Groups[1].Value
    if ($style) { "[$style] $t" } else { $t }
  }
}
[Console]::OutputEncoding = [Text.Encoding]::UTF8
$out -join "`n"
