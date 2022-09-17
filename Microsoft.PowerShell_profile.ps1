Import-Module PSReadline
Set-PSReadlineOption -EditMode Emacs
# See more about Predictive IntelliSense: https://devblogs.microsoft.com/powershell/announcing-psreadline-2-1-with-predictive-intellisense/
Set-PSReadLineOption -PredictionSource History

# See all keybindings: Get-PSReadLineKeyHandler -Bound -Unbound
Set-PSReadlineKeyHandler -Key Tab -Function MenuComplete
Set-PSReadlineKeyHandler -Chord "Ctrl+/" -Function Undo
Set-PSReadLineKeyHandler -Chord 'F2' -Function SwitchPredictionView

# #region start emacs daemon
# Start-Job -ScriptBlock {emacs --daemon}
# #endregion

# #region alias configuration
<# - Alias for Emacs Client #>
# Function EMC([string]$File) { emacsclient -c "$File" }
# Set-Alias -Name ec -Value EMC

# Function EMT([string]$File) { emacsclient -t "$File"}
# Set-Alias -Name en -Value EMT

<# - Alias for Vim #>
Set-Alias -Name vi -Value vim

<# - Alias for LSD #>
Function LLIT([string]$Folder) { lsd -l "$Folder" }
Function LALIT([string]$Folder) { lsd -al "$Folder" }

Set-Alias -Option AllScope -Name ls -Value lsd
Set-Alias -Name ll -Value LLIT
Set-Alias -Name lal -Value LALIT
# #endregion

#region theme configuration
# - Starship
# Invoke-Expression (&starship init powershell)

# - Dracula
# Invoke-Expression -Command $PSScriptRoot\dracula-prompt-configuration.ps1

# - Paradox
# Import-Module posh-git
# Import-Module oh-my-posh
# Set-Theme Operator

Set-PSReadLineOption -Colors @{
  # Terms
  "Default"   = [ConsoleColor]::White
  "Parameter" = [ConsoleColor]::DarkCyan
  "Type"      = [ConsoleColor]::DarkBlue
  "Number"    = [ConsoleColor]::Magenta
  "String"    = [ConsoleColor]::Magenta
  "Comment"   = [ConsoleColor]::Yellow
  "Variable"  = [ConsoleColor]::Green
  "Keyword"   = [ConsoleColor]::Blue
  "Operator"  = [ConsoleColor]::Blue
  "Command"   = [ConsoleColor]::Blue
  "Member"    = [ConsoleColor]::Blue
  "Error"     = [ConsoleColor]::Red
  # Predictive IntelliSense
  "InlinePrediction" = [ConsoleColor]::DarkGray
}
#endregion

#region conda initialize
# !! Contents within this block are managed by 'conda init' !!
# (& "D:\Devs\Anaconda3\Scripts\conda.exe" "shell.powershell" "hook") | Out-String | Invoke-Expression
#endregion

#region Chocolatey initialize
$ChocolateyProfile = "$env:ChocolateyInstall\helpers\chocolateyProfile.psm1"
if (Test-Path($ChocolateyProfile)) {
  Import-Module "$ChocolateyProfile"
}
#endregion

function proxy_on() {
  $Env:all_proxy = "http://127.0.0.1:7890"
  $Env:http_proxy = "http://127.0.0.1:7890"
  $Env:https_proxy = "http://127.0.0.1:7890"
  Write-Output "Proxy is turned on $Env:all_proxy"
}

function proxy_off() {
  $Env:all_proxy = ""
  $Env:http_proxy = ""
  $Env:https_proxy = ""
  Write-Output "Proxy is turned off"
}

function prompt {
  $namePrefix = $(if ($HOST.Name -eq 'ServerRemoteHost')
    { $env:USERNAME + '@' + $env:COMPUTERNAME + ' '} else { '' })

  $currentDir = (Convert-Path .)
  if ($currentDir.Contains($HOME)) {
      $currentDir = $currentDir.Replace($HOME, "~")
  }

  $(if (Test-Path variable:/PSDebugContext) { ' [DBG]: ' }
    else { ' ' }) + $currentDir + ' ' +
      $(if ($NestedPromptLevel -ge 1) { '>>' }) + '% '

  Write-Host "$namePrefix" -BackgroundColor Cyan -ForegroundColor Black -NoNewline
}

Import-Module ZLocation
