Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# ---------------------------------------------------------------------------
#  Paths
# ---------------------------------------------------------------------------
$ScriptDir   = Split-Path -Parent $MyInvocation.MyCommand.Definition
$ExePath     = Join-Path $ScriptDir "win32\GDS3D.exe"
$RecentFile  = Join-Path $ScriptDir ".launcher_recent"   # persists recent GDS picks
$MaxRecent   = 6

# ---------------------------------------------------------------------------
#  Persist recent files
# ---------------------------------------------------------------------------
function Load-Recent {
    if (Test-Path $RecentFile) {
        return @(Get-Content $RecentFile | Where-Object { $_ -and (Test-Path $_) } | Select-Object -First $MaxRecent)
    }
    return @()
}

function Save-Recent($path) {
    $existing = Load-Recent | Where-Object { $_ -ne $path }
    @($path) + $existing | Select-Object -First $MaxRecent | Set-Content $RecentFile
}

# ---------------------------------------------------------------------------
#  Built-in tech files
# ---------------------------------------------------------------------------
$BuiltinTech = [ordered]@{
    "SkyWater SKY130  (130nm CMOS)"              = "techfiles\sky130.txt"
    "SkyWater SKY130  (S10 variant)"             = "techfiles\sky130_s10.txt"
    "IHP SG13G2  (130nm SiGe BiCMOS)"           = "techfiles\sg13g2.txt"
    "Generic / Example  (mock 8-metal process)"  = "techfiles\example.txt"
    "Browse for custom tech file..."             = "__BROWSE__"
}

# ---------------------------------------------------------------------------
#  Colours
# ---------------------------------------------------------------------------
$BG      = [System.Drawing.Color]::FromArgb(15,  15,  25)
$CARD    = [System.Drawing.Color]::FromArgb(26,  26,  42)
$CARD2   = [System.Drawing.Color]::FromArgb(32,  32,  52)
$ACCENT  = [System.Drawing.Color]::FromArgb(99, 102, 241)
$ACCENT2 = [System.Drawing.Color]::FromArgb(139, 92, 246)
$SUCCESS = [System.Drawing.Color]::FromArgb(34, 197, 94)
$TEXT    = [System.Drawing.Color]::FromArgb(235, 235, 255)
$MUTED   = [System.Drawing.Color]::FromArgb(130, 140, 165)
$WARN    = [System.Drawing.Color]::FromArgb(251, 191,  36)
$ERR     = [System.Drawing.Color]::FromArgb(239,  68,  68)
$WHITE   = [System.Drawing.Color]::White

# ---------------------------------------------------------------------------
#  Helpers
# ---------------------------------------------------------------------------
function Make-Label($txt, $x, $y, $w, $h, $sz=9, $bold=$false, $col=$null) {
    $l           = New-Object System.Windows.Forms.Label
    $l.Text      = $txt
    $l.Location  = New-Object System.Drawing.Point($x, $y)
    $l.Size      = New-Object System.Drawing.Size($w, $h)
    $l.ForeColor = if ($col) { $col } else { $TEXT }
    $style       = if ($bold) { [System.Drawing.FontStyle]::Bold } else { [System.Drawing.FontStyle]::Regular }
    $l.Font      = New-Object System.Drawing.Font("Segoe UI", $sz, $style)
    $l.BackColor = [System.Drawing.Color]::Transparent
    return $l
}

function Make-Card($x, $y, $w, $h, $col=$null) {
    $p           = New-Object System.Windows.Forms.Panel
    $p.Location  = New-Object System.Drawing.Point($x, $y)
    $p.Size      = New-Object System.Drawing.Size($w, $h)
    $p.BackColor = if ($col) { $col } else { $CARD }
    return $p
}

function Make-Button($txt, $x, $y, $w, $h, $bg=$ACCENT, $sz=9) {
    $b            = New-Object System.Windows.Forms.Button
    $b.Text       = $txt
    $b.Location   = New-Object System.Drawing.Point($x, $y)
    $b.Size       = New-Object System.Drawing.Size($w, $h)
    $b.BackColor  = $bg
    $b.ForeColor  = $WHITE
    $b.FlatStyle  = "Flat"
    $b.FlatAppearance.BorderSize = 0
    $b.Font       = New-Object System.Drawing.Font("Segoe UI", $sz, [System.Drawing.FontStyle]::Bold)
    $b.Cursor     = [System.Windows.Forms.Cursors]::Hand
    return $b
}

# ---------------------------------------------------------------------------
#  FORM
# ---------------------------------------------------------------------------
$Form                 = New-Object System.Windows.Forms.Form
$Form.Text            = "GDS3D Launcher  v1.9"
$Form.Size            = New-Object System.Drawing.Size(660, 640)
$Form.StartPosition   = "CenterScreen"
$Form.BackColor       = $BG
$Form.ForeColor       = $TEXT
$Form.FormBorderStyle = "FixedSingle"
$Form.MaximizeBox     = $false
$Form.Font            = New-Object System.Drawing.Font("Segoe UI", 9)

# ── Header ─────────────────────────────────────────────────────────────────
$Header          = Make-Card 0 0 660 78 $CARD
$Form.Controls.Add($Header)

$Header.Controls.Add((Make-Label "GDS3D Launcher" 16 7 400 40 18 $true $ACCENT))
$Header.Controls.Add((Make-Label "Render any GDSII chip layout in 3D  |  SkyWater, IHP and more" 18 50 560 20 9 $false $MUTED))

$AccentBar          = Make-Card 0 78 660 3 $ACCENT
$Form.Controls.Add($AccentBar)

# ── Section 1: GDS file ───────────────────────────────────────────────────
$Form.Controls.Add((Make-Label "1.  GDS File" 22 96 200 22 10 $true $ACCENT))
$Form.Controls.Add((Make-Label "Choose any .gds file from your computer" 22 118 400 18 8.5 $false $MUTED))

$GdsCard = Make-Card 18 140 618 68
$Form.Controls.Add($GdsCard)

$GdsPathBox           = New-Object System.Windows.Forms.TextBox
$GdsPathBox.Location  = New-Object System.Drawing.Point(12, 20)
$GdsPathBox.Size      = New-Object System.Drawing.Size(466, 26)
$GdsPathBox.BackColor = [System.Drawing.Color]::FromArgb(36, 36, 56)
$GdsPathBox.ForeColor = $MUTED
$GdsPathBox.BorderStyle = "FixedSingle"
$GdsPathBox.Font      = New-Object System.Drawing.Font("Consolas", 8.5)
$GdsPathBox.Text      = "No file selected..."
$GdsPathBox.ReadOnly  = $true
$GdsCard.Controls.Add($GdsPathBox)

$BrowseBtn = Make-Button "Browse..." 486 17 120 32
$GdsCard.Controls.Add($BrowseBtn)

# ── Section 2: Recent files ───────────────────────────────────────────────
$RecentList = Load-Recent
$RecentCard = $null
$RecentLabel = $null

if ($RecentList.Count -gt 0) {
    $Form.Controls.Add((Make-Label "Recent Files" 22 218 200 20 9 $true $MUTED))
    $RecentCard = Make-Card 18 238 618 ($RecentList.Count * 26 + 10) $CARD2
    $Form.Controls.Add($RecentCard)

    $ry = 5
    foreach ($rf in $RecentList) {
        $fname   = [System.IO.Path]::GetFileName($rf)
        $fdir    = [System.IO.Path]::GetDirectoryName($rf)
        $shortdir= if ($fdir.Length -gt 45) { "..." + $fdir.Substring($fdir.Length - 45) } else { $fdir }

        $lnk           = New-Object System.Windows.Forms.LinkLabel
        $lnk.Text      = "$fname   ($shortdir)"
        $lnk.Tag       = $rf
        $lnk.Location  = New-Object System.Drawing.Point(12, $ry)
        $lnk.Size      = New-Object System.Drawing.Size(594, 20)
        $lnk.Font      = New-Object System.Drawing.Font("Consolas", 8.5)
        $lnk.LinkColor = $ACCENT
        $lnk.ActiveLinkColor = $ACCENT2
        $lnk.BackColor = [System.Drawing.Color]::Transparent
        $lnk.Add_LinkClicked({
            param($s, $e)
            $p = $s.Tag
            if (Test-Path $p) {
                $GdsPathBox.Text      = $p
                $GdsPathBox.ForeColor = $TEXT
                $fname2               = [System.IO.Path]::GetFileName($p)
                Set-Status "Selected: $fname2" $SUCCESS
            } else {
                Set-Status "File no longer found: $p" $ERR
            }
        })
        $RecentCard.Controls.Add($lnk)
        $ry += 26
    }
    $recentBottom = 238 + $RecentCard.Height + 8
} else {
    $recentBottom = 218
}

# ── Section 3: Tech file ──────────────────────────────────────────────────
$techY = $recentBottom
$Form.Controls.Add((Make-Label "2.  Technology / Process File" 22 $techY 400 22 10 $true $ACCENT))
$Form.Controls.Add((Make-Label "Match the process used to design your GDS" 22 ($techY+22) 400 18 8.5 $false $MUTED))

$TechCard = Make-Card 18 ($techY+44) 618 68
$Form.Controls.Add($TechCard)

$TechDrop                = New-Object System.Windows.Forms.ComboBox
$TechDrop.Location       = New-Object System.Drawing.Point(12, 18)
$TechDrop.Size           = New-Object System.Drawing.Size(594, 30)
$TechDrop.BackColor      = [System.Drawing.Color]::FromArgb(36, 36, 56)
$TechDrop.ForeColor      = $TEXT
$TechDrop.DropDownStyle  = "DropDownList"
$TechDrop.Font           = New-Object System.Drawing.Font("Segoe UI", 9)
$TechDrop.FlatStyle      = "Flat"
foreach ($k in $BuiltinTech.Keys) { [void]$TechDrop.Items.Add($k) }
$TechDrop.SelectedIndex  = 0
$TechCard.Controls.Add($TechDrop)

# storage for custom tech path
$CustomTechPath = ""

# ── Section 4: Options ────────────────────────────────────────────────────
$optY = $techY + 44 + 68 + 12
$Form.Controls.Add((Make-Label "3.  Options" 22 $optY 300 22 10 $true $ACCENT))

$OptCard = Make-Card 18 ($optY+24) 618 36
$Form.Controls.Add($OptCard)

$ChkVerbose           = New-Object System.Windows.Forms.CheckBox
$ChkVerbose.Text      = "Verbose output  (show layer info in console)"
$ChkVerbose.Location  = New-Object System.Drawing.Point(12, 8)
$ChkVerbose.Size      = New-Object System.Drawing.Size(400, 22)
$ChkVerbose.ForeColor = $TEXT
$ChkVerbose.BackColor = [System.Drawing.Color]::Transparent
$ChkVerbose.Checked   = $true
$OptCard.Controls.Add($ChkVerbose)

# ── Status bar + Launch button (anchored to bottom) ───────────────────────
$statusY = $Form.ClientSize.Height - 96
$StatusCard = Make-Card 18 $statusY 618 36 $CARD2
$Form.Controls.Add($StatusCard)

$StatusLabel          = Make-Label "  Ready  --  select a GDS file then click Launch" 0 8 610 22 8.5 $false $MUTED
$StatusCard.Controls.Add($StatusLabel)

$LaunchBtn = Make-Button "Launch GDS3D  >>>" 18 ($statusY+44) 618 42 $ACCENT2 12
$Form.Controls.Add($LaunchBtn)

# ---------------------------------------------------------------------------
#  Status helper
# ---------------------------------------------------------------------------
function Set-Status($msg, $col) {
    $StatusLabel.Text      = "  $msg"
    $StatusLabel.ForeColor = $col
}

# ---------------------------------------------------------------------------
#  EVENTS
# ---------------------------------------------------------------------------

# Browse GDS
$BrowseBtn.Add_Click({
    $dlg                  = New-Object System.Windows.Forms.OpenFileDialog
    $dlg.Title            = "Select a GDSII file"
    $dlg.Filter           = "GDSII Files (*.gds;*.gds2)|*.gds;*.gds2|All Files (*.*)|*.*"
    $dlg.InitialDirectory = [System.Environment]::GetFolderPath("MyDocuments")
    if ($dlg.ShowDialog() -eq "OK") {
        $GdsPathBox.Text      = $dlg.FileName
        $GdsPathBox.ForeColor = $TEXT
        $fn = [System.IO.Path]::GetFileName($dlg.FileName)
        Set-Status "Selected: $fn" $SUCCESS
    }
})

# Custom tech browse when "Browse for custom..." selected
$TechDrop.Add_SelectedIndexChanged({
    if ($BuiltinTech[$TechDrop.SelectedItem] -eq "__BROWSE__") {
        $dlg        = New-Object System.Windows.Forms.OpenFileDialog
        $dlg.Title  = "Select a GDS3D process/tech file"
        $dlg.Filter = "Text Files (*.txt)|*.txt|All Files (*.*)|*.*"
        $dlg.InitialDirectory = Join-Path $ScriptDir "techfiles"
        if ($dlg.ShowDialog() -eq "OK") {
            $script:CustomTechPath = $dlg.FileName
            $fn = [System.IO.Path]::GetFileName($dlg.FileName)
            Set-Status "Custom tech file: $fn" $SUCCESS
        } else {
            $TechDrop.SelectedIndex = 0
        }
    } else {
        $script:CustomTechPath = ""
    }
})

# Hover effects
$LaunchBtn.Add_MouseEnter({ $LaunchBtn.BackColor = $ACCENT })
$LaunchBtn.Add_MouseLeave({ $LaunchBtn.BackColor = $ACCENT2 })
$BrowseBtn.Add_MouseEnter({ $BrowseBtn.BackColor = [System.Drawing.Color]::FromArgb(79, 82, 221) })
$BrowseBtn.Add_MouseLeave({ $BrowseBtn.BackColor = $ACCENT })

# Launch
$LaunchBtn.Add_Click({
    $GdsFile = $GdsPathBox.Text.Trim()

    if ([string]::IsNullOrEmpty($GdsFile) -or $GdsFile -eq "No file selected...") {
        Set-Status "Please select a GDS file first!" $WARN ; return
    }
    if (-not (Test-Path $GdsFile)) {
        Set-Status "GDS file not found: $GdsFile" $ERR ; return
    }
    if (-not (Test-Path $ExePath)) {
        Set-Status "GDS3D.exe not found at: $ExePath" $ERR ; return
    }

    # Resolve tech file
    if ($script:CustomTechPath) {
        $TechFile = $script:CustomTechPath
    } else {
        $relTech  = $BuiltinTech[$TechDrop.SelectedItem]
        $TechFile = Join-Path $ScriptDir $relTech
    }

    if (-not (Test-Path $TechFile)) {
        Set-Status "Tech file not found: $TechFile" $ERR ; return
    }

    # Build args as an array
    $ArgArray = @("-p", $TechFile, "-i", $GdsFile)
    if ($ChkVerbose.Checked) { $ArgArray += "-v" }

    # Save to recent
    Save-Recent $GdsFile

    $fn = [System.IO.Path]::GetFileName($GdsFile)
    Set-Status "Launching: $fn" $SUCCESS

    Start-Process -FilePath $ExePath -ArgumentList $ArgArray -WorkingDirectory $ScriptDir
})

[void]$Form.ShowDialog()
