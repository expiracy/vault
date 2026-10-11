[CmdletBinding()]
param(
    [string]$DocsRoot = (Split-Path -Parent $PSScriptRoot),
    [string]$UserDirectory = [Environment]::GetFolderPath('UserProfile')
)

$ErrorActionPreference = 'Stop'
$docsPath = (Resolve-Path -LiteralPath $DocsRoot).Path
$userPath = [IO.Path]::GetFullPath($UserDirectory)
$agentPath = Join-Path $userPath '.agents'
$codexPath = Join-Path $userPath '.codex'
$skillPath = Join-Path $agentPath 'skills'
$configPath = Join-Path $agentPath 'agent-docs.json'
$instructionsPath = Join-Path $codexPath 'AGENTS.md'
$beginMarker = '<!-- agent-docs:begin -->'
$endMarker = '<!-- agent-docs:end -->'
$skillNames = @('docs-context', 'write-project-doc')

foreach ($requiredPath in @('AGENTS.md', 'CATALOG.md', '.agents/skills/docs-context/SKILL.md', '.agents/skills/write-project-doc/SKILL.md')) {
    if (-not (Test-Path -LiteralPath (Join-Path $docsPath $requiredPath) -PathType Leaf)) {
        throw "Missing required docs file: $requiredPath"
    }
}

# Preflight all destinations before making changes. Never replace unrelated skills.
$configuration = @{}
if (Test-Path -LiteralPath $configPath) {
    $existingConfiguration = Get-Content -LiteralPath $configPath -Raw | ConvertFrom-Json
    foreach ($property in $existingConfiguration.PSObject.Properties) {
        $configuration[$property.Name] = $property.Value
    }
    if ($configuration.ContainsKey('docs_root') -and
        [IO.Path]::GetFullPath([string]$configuration['docs_root']) -ne $docsPath) {
        throw 'A different central docs root is already configured. Review that configuration before relocating it.'
    }
}
$existingInstructions = ''
if (Test-Path -LiteralPath $instructionsPath) {
    $existingInstructions = [IO.File]::ReadAllText($instructionsPath)
}
$beginCount = [regex]::Matches($existingInstructions, [regex]::Escape($beginMarker)).Count
$endCount = [regex]::Matches($existingInstructions, [regex]::Escape($endMarker)).Count
if ($beginCount -gt 1 -or $endCount -gt 1 -or $beginCount -ne $endCount -or
    ($beginCount -eq 1 -and $existingInstructions.IndexOf($endMarker) -lt $existingInstructions.IndexOf($beginMarker))) {
    throw 'Malformed or repeated agent-docs block in global AGENTS.md. Review it before installation.'
}
foreach ($skillName in $skillNames) {
    $destination = Join-Path $skillPath $skillName
    $source = Join-Path $docsPath ".agents/skills/$skillName"
    if (Test-Path -LiteralPath $destination) {
        $entry = Get-Item -LiteralPath $destination -Force
        if ($entry.LinkType -notin @('Junction', 'SymbolicLink') -or
            [IO.Path]::GetFullPath([string](@($entry.Target)[0])) -ne [IO.Path]::GetFullPath($source)) {
            throw "Existing skill destination belongs to something else: $destination"
        }
    }
}

foreach ($directory in @($agentPath, $codexPath, $skillPath)) {
    New-Item -ItemType Directory -Path $directory -Force | Out-Null
}
foreach ($skillName in $skillNames) {
    $destination = Join-Path $skillPath $skillName
    if (-not (Test-Path -LiteralPath $destination)) {
        New-Item -ItemType Junction -Path $destination -Target (Join-Path $docsPath ".agents/skills/$skillName") | Out-Null
    }
}
$configuration['docs_root'] = $docsPath.Replace('\', '/')
$encoding = [Text.UTF8Encoding]::new($false)
[IO.File]::WriteAllText($configPath, (($configuration | ConvertTo-Json -Depth 10) + "`n"), $encoding)

$block = @'
<!-- agent-docs:begin -->
## Shared project documentation

For project design, documentation, feature changes, or resuming project work, consult the central documentation repository. Find its root in `~/.agents/agent-docs.json` (`docs_root`), then read `CATALOG.md` and the relevant `PROJECT.md` before choosing existing feature and task documents. Read the central repo's `AGENTS.md` before editing its files.

The user skills `docs-context` and `write-project-doc` provide context and Markdown writing guidance. Update appropriate existing documents by default; keep current facts separate from proposals and preserve task history. If no project matches, do not invent a match or create unrelated records.

These instructions do not grant filesystem access. Use the session's existing permissions and request a narrowly scoped grant only if an actual required operation is blocked.
<!-- agent-docs:end -->
'@
if ($beginCount -eq 1) {
    $pattern = '(?s)' + [regex]::Escape($beginMarker) + '.*?' + [regex]::Escape($endMarker)
    $updatedInstructions = [regex]::Replace($existingInstructions, $pattern, [Text.RegularExpressions.MatchEvaluator]{ param($match) $block })
} else {
    $separator = if ([string]::IsNullOrWhiteSpace($existingInstructions)) { '' } else { "`n`n" }
    $updatedInstructions = $existingInstructions + $separator + $block + "`n"
}
[IO.File]::WriteAllText($instructionsPath, $updatedInstructions, $encoding)
Write-Output "Configured central docs: $docsPath"
Write-Output "Linked skills: $($skillNames -join ', ')"
Write-Output "Startup instructions: $instructionsPath"
