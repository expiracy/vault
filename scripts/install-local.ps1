[CmdletBinding()]
param(
    [string]$DocsRoot = (Split-Path -Parent $PSScriptRoot),
    [string]$UserDirectory = [Environment]::GetFolderPath('UserProfile'),
    [string]$PreviousDocsRoot
)

$ErrorActionPreference = 'Stop'
function Normalize-DocsPath([string]$pathValue) {
    $fullPath = [IO.Path]::GetFullPath($pathValue)
    if ($fullPath.Length -gt [IO.Path]::GetPathRoot($fullPath).Length) {
        $fullPath = $fullPath.TrimEnd([IO.Path]::DirectorySeparatorChar, [IO.Path]::AltDirectorySeparatorChar)
    }
    return $fullPath
}

function Assert-ConfigurationDepth([object]$configurationValue, [int]$depth = 0) {
    if ($depth -gt 100) {
        throw 'Configuration nesting exceeds the safely supported JSON depth. No installation changes were made.'
    }
    if ($configurationValue -is [Collections.IDictionary]) {
        foreach ($childValue in $configurationValue.Values) {
            Assert-ConfigurationDepth $childValue ($depth + 1)
        }
    } elseif ($configurationValue -is [pscustomobject]) {
        foreach ($property in $configurationValue.PSObject.Properties) {
            Assert-ConfigurationDepth $property.Value ($depth + 1)
        }
    } elseif ($configurationValue -is [Collections.IEnumerable] -and $configurationValue -isnot [string]) {
        foreach ($childValue in $configurationValue) {
            Assert-ConfigurationDepth $childValue ($depth + 1)
        }
    }
}

$docsPath = Normalize-DocsPath (Resolve-Path -LiteralPath $DocsRoot).Path
$previousPath = $null
if ($PSBoundParameters.ContainsKey('PreviousDocsRoot')) {
    if ([string]::IsNullOrWhiteSpace($PreviousDocsRoot)) {
        throw 'PreviousDocsRoot must identify the previous central docs root.'
    }
    # The old checkout may already have moved, so do not require it to exist.
    $previousPath = Normalize-DocsPath $PreviousDocsRoot
}
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
foreach ($filePath in @($configPath, $instructionsPath)) {
    if (Test-Path -LiteralPath $filePath) {
        if (-not (Test-Path -LiteralPath $filePath -PathType Leaf)) {
            throw "Installation file belongs to a directory: $filePath"
        }
        $attributes = [IO.File]::GetAttributes($filePath)
        if ($attributes -band [IO.FileAttributes]::ReadOnly) {
            throw "Installation file is read-only. No installation changes were made: $filePath"
        }
        if ($attributes -band [IO.FileAttributes]::ReparsePoint) {
            throw "Installation file is a link. Review it before installation: $filePath"
        }
    }
}
$relocating = $false
$configuration = @{}
if (Test-Path -LiteralPath $configPath) {
    $existingConfiguration = Get-Content -LiteralPath $configPath -Raw -Encoding UTF8 | ConvertFrom-Json
    foreach ($property in $existingConfiguration.PSObject.Properties) {
        $configuration[$property.Name] = $property.Value
    }
    if ($configuration.ContainsKey('docs_root')) {
        $configuredPath = Normalize-DocsPath ([string]$configuration['docs_root'])
        if ($configuredPath -ne $docsPath) {
            if ($null -eq $previousPath -or $configuredPath -ne $previousPath) {
                throw 'A different central docs root is already configured. Supply its exact path with PreviousDocsRoot to relocate it.'
            }
            $relocating = $true
        }
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
foreach ($directory in @($agentPath, $codexPath, $skillPath)) {
    if ((Test-Path -LiteralPath $directory) -and -not (Test-Path -LiteralPath $directory -PathType Container)) {
        throw "Installation directory belongs to a file: $directory"
    }
}
$existingSkills = @{}
if (Test-Path -LiteralPath $skillPath -PathType Container) {
    # Enumerate the parent so dangling links left by a physical move are visible.
    foreach ($entry in Get-ChildItem -LiteralPath $skillPath -Force) {
        if ($entry.Name -in $skillNames) {
            $existingSkills[$entry.Name] = $entry
        }
    }
}
$skillPlans = foreach ($skillName in $skillNames) {
    $destination = Join-Path $skillPath $skillName
    $source = Normalize-DocsPath (Join-Path $docsPath ".agents/skills/$skillName")
    $action = 'create'
    if ($existingSkills.ContainsKey($skillName)) {
        $entry = $existingSkills[$skillName]
        if (-not $entry.PSIsContainer -or $entry.LinkType -notin @('Junction', 'SymbolicLink') -or
            @($entry.Target).Count -ne 1 -or [string]::IsNullOrWhiteSpace([string](@($entry.Target)[0]))) {
            throw "Existing skill destination belongs to something else: $destination"
        }
        $targetPath = [string](@($entry.Target)[0])
        if (-not [IO.Path]::IsPathRooted($targetPath)) {
            $targetPath = Join-Path $skillPath $targetPath
        }
        $targetPath = Normalize-DocsPath $targetPath
        if ($targetPath -eq $source) {
            $action = 'keep'
        } elseif ($relocating -and
            $targetPath -eq (Normalize-DocsPath (Join-Path $previousPath ".agents/skills/$skillName"))) {
            $action = 'retarget'
        } else {
            throw "Existing skill destination belongs to something else: $destination"
        }
    }
    [pscustomobject]@{ Destination = $destination; Source = $source; Action = $action }
}

# Prepare JSON before changing any link, so unrelated settings cannot be truncated.
$configuration['docs_root'] = $docsPath.Replace('\', '/')
Assert-ConfigurationDepth $configuration
$configurationJson = ($configuration | ConvertTo-Json -Depth 100 -WarningAction Stop) + "`n"

$block = @'
<!-- agent-docs:begin -->
## Shared Vault documentation and tools

For project design, documentation, feature changes, or resuming project work, consult the central documentation vault. Find its root in `~/.agents/agent-docs.json` (`docs_root`), then read `CATALOG.md` and the relevant `PROJECT.md` before choosing existing feature and task documents. Follow the existing task context to task-owned tools and instructions. Read the central repo's `AGENTS.md` before editing its files.

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

# Keep originals until every destination has been published. Renaming a junction
# preserves the link itself, including a dangling link after a physical move.
$transactionId = [Guid]::NewGuid().ToString('N')
$transactionPath = Join-Path $agentPath ".agent-docs-install-$transactionId"
$createdDirectories = [Collections.Generic.List[string]]::new()
$filePlans = @(
    [pscustomobject]@{ Destination = $configPath; Content = $configurationJson },
    [pscustomobject]@{ Destination = $instructionsPath; Content = $updatedInstructions }
)
foreach ($plan in $filePlans) {
    $plan | Add-Member -NotePropertyName Stage -NotePropertyValue ($plan.Destination + ".agent-docs-$transactionId.new")
    $plan | Add-Member -NotePropertyName Backup -NotePropertyValue ($plan.Destination + ".agent-docs-$transactionId.backup")
    $plan | Add-Member -NotePropertyName Existed -NotePropertyValue (Test-Path -LiteralPath $plan.Destination -PathType Leaf)
    $plan | Add-Member -NotePropertyName Published -NotePropertyValue $false
}
foreach ($plan in $skillPlans) {
    $name = Split-Path -Leaf $plan.Destination
    $plan | Add-Member -NotePropertyName Stage -NotePropertyValue (Join-Path $transactionPath "$name.new")
    $plan | Add-Member -NotePropertyName Backup -NotePropertyValue (Join-Path $transactionPath "$name.backup")
    $plan | Add-Member -NotePropertyName BackedUp -NotePropertyValue $false
    $plan | Add-Member -NotePropertyName Published -NotePropertyValue $false
}
$encoding = [Text.UTF8Encoding]::new($false)
$committed = $false
$rollbackErrors = [Collections.Generic.List[string]]::new()
try {
    foreach ($directory in @($userPath, $agentPath, $codexPath, $skillPath, $transactionPath)) {
        if (-not (Test-Path -LiteralPath $directory -PathType Container)) {
            [IO.Directory]::CreateDirectory($directory) | Out-Null
            $createdDirectories.Add($directory)
        }
    }
    foreach ($plan in $filePlans) {
        [IO.File]::WriteAllText($plan.Stage, $plan.Content, $encoding)
    }
    foreach ($plan in $skillPlans) {
        if ($plan.Action -ne 'keep') {
            New-Item -ItemType Junction -Path $plan.Stage -Target $plan.Source | Out-Null
        }
    }
    foreach ($plan in $skillPlans) {
        if ($plan.Action -eq 'retarget') {
            [IO.Directory]::Move($plan.Destination, $plan.Backup)
            $plan.BackedUp = $true
        }
        if ($plan.Action -ne 'keep') {
            [IO.Directory]::Move($plan.Stage, $plan.Destination)
            $plan.Published = $true
        }
    }
    foreach ($plan in $filePlans) {
        if ($plan.Existed) {
            [IO.File]::Replace($plan.Stage, $plan.Destination, $plan.Backup)
        } else {
            [IO.File]::Move($plan.Stage, $plan.Destination)
        }
        $plan.Published = $true
    }
    $committed = $true
} catch {
    $installationError = $_
    for ($index = $filePlans.Count - 1; $index -ge 0; $index--) {
        $plan = $filePlans[$index]
        if ($plan.Published) {
            try {
                if ($plan.Existed) {
                    # Use the consumed stage path for the discarded new version;
                    # PowerShell coerces a null string argument to an empty path.
                    [IO.File]::Replace($plan.Backup, $plan.Destination, $plan.Stage)
                } else {
                    [IO.File]::Delete($plan.Destination)
                }
                $plan.Published = $false
            } catch {
                $rollbackErrors.Add("$($plan.Destination): $($_.Exception.Message)")
            }
        }
    }
    for ($index = $skillPlans.Count - 1; $index -ge 0; $index--) {
        $plan = $skillPlans[$index]
        try {
            if ($plan.Published) {
                # Remove only our new junction entry, never its target contents.
                [IO.Directory]::Delete($plan.Destination, $false)
                $plan.Published = $false
            }
            if ($plan.BackedUp) {
                [IO.Directory]::Move($plan.Backup, $plan.Destination)
                $plan.BackedUp = $false
            }
        } catch {
            $rollbackErrors.Add("$($plan.Destination): $($_.Exception.Message)")
        }
    }
    if ($rollbackErrors.Count -gt 0) {
        throw "Installation failed: $($installationError.Exception.Message). Rollback also failed: $($rollbackErrors -join '; '). Retained backups use transaction $transactionId."
    }
    throw "Installation failed; destination files and skill links were restored: $($installationError.Exception.Message)"
} finally {
    foreach ($plan in $filePlans) {
        foreach ($temporaryFile in @($plan.Stage, $plan.Backup)) {
            # Preserve a backup if restoring this destination failed.
            if ($temporaryFile -eq $plan.Backup -and -not $committed -and $plan.Published) { continue }
            try {
                [IO.File]::Delete($temporaryFile)
            } catch {
                Write-Warning "Could not remove installer temporary file $temporaryFile : $($_.Exception.Message)"
            }
        }
    }
    foreach ($plan in $skillPlans) {
        foreach ($temporaryLink in @($plan.Stage, $plan.Backup)) {
            if ($temporaryLink -eq $plan.Backup -and -not $committed -and $plan.BackedUp) { continue }
            if (Get-Item -LiteralPath $temporaryLink -Force -ErrorAction SilentlyContinue) {
                try {
                    [IO.Directory]::Delete($temporaryLink, $false)
                } catch {
                    Write-Warning "Could not remove installer temporary link $temporaryLink : $($_.Exception.Message)"
                }
            }
        }
    }
    for ($index = $createdDirectories.Count - 1; $index -ge 0; $index--) {
        $directory = $createdDirectories[$index]
        if ($directory -eq $transactionPath -or -not $committed) {
            try {
                [IO.Directory]::Delete($directory, $false)
            } catch {
                # A populated directory can contain restored files or retained
                # recovery backups. Do not recurse or remove unrelated contents.
                if ($directory -eq $transactionPath) {
                    Write-Warning "Installer recovery directory retained: $directory"
                }
            }
        }
    }
}
Write-Output "Configured central docs: $docsPath"
Write-Output "Linked skills: $($skillNames -join ', ')"
Write-Output "Startup instructions: $instructionsPath"
