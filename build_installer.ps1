# Sinhala TTS Installer Builder - PowerShell Version
# This script works better with virtual environments

Write-Host ""
Write-Host "=========================================" -ForegroundColor Green
Write-Host "  Sinhala TTS - Complete Installer Build" -ForegroundColor Green  
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""

# Function to check if command exists
function Test-Command($cmdname) {
    return [bool](Get-Command -Name $cmdname -ErrorAction SilentlyContinue)
}

# Step 1: Check required files
Write-Host "[1/7] Checking required files..." -ForegroundColor Yellow

$requiredFiles = @(
    "enhanced_sinhala_tts.py",
    "sinhala_text_to_phoneme.py",
    "phonemes",
    "sinhala_tts.spec"
)

foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "✓ $file found" -ForegroundColor Green
    } else {
        Write-Host "❌ $file not found!" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

# Step 2: Check Python environment
Write-Host ""
Write-Host "[2/7] Checking Python environment..." -ForegroundColor Yellow

if (Test-Command python) {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "❌ Python not found!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Step 3: Install PyInstaller
Write-Host ""
Write-Host "[3/7] Installing PyInstaller..." -ForegroundColor Yellow

$installResult = python -m pip install pyinstaller --upgrade --quiet 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ PyInstaller installed successfully" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to install PyInstaller!" -ForegroundColor Red
    Write-Host "Error output: $installResult" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Step 4: Clean previous builds
Write-Host ""
Write-Host "[4/7] Cleaning previous builds..." -ForegroundColor Yellow

$dirsToClean = @("dist", "build", "installer_output")
foreach ($dir in $dirsToClean) {
    if (Test-Path $dir) {
        Remove-Item $dir -Recurse -Force
        Write-Host "✓ Cleaned $dir directory" -ForegroundColor Green
    }
}

New-Item -ItemType Directory -Path "installer_output" -Force | Out-Null

# Step 5: Build executable
Write-Host ""
Write-Host "[5/7] Building executable..." -ForegroundColor Yellow
Write-Host "This may take several minutes..." -ForegroundColor Cyan

$buildResult = python -m PyInstaller sinhala_tts.spec --noconfirm 2>&1
if ($LASTEXITCODE -eq 0 -and (Test-Path "dist\SinhalaTTS.exe")) {
    Write-Host "✓ Executable built successfully!" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to build executable!" -ForegroundColor Red
    Write-Host "Build output: $buildResult" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Step 6: Prepare installer files
Write-Host ""
Write-Host "[6/7] Preparing installer files..." -ForegroundColor Yellow

# Copy phonemes if not already included
if (-not (Test-Path "dist\phonemes")) {
    Copy-Item "phonemes" "dist\phonemes" -Recurse -Force
    Write-Host "✓ Copied phoneme files" -ForegroundColor Green
}

# Copy documentation
if (Test-Path "README.md") { Copy-Item "README.md" "dist\" -Force }
if (Test-Path "LICENSE.txt") { Copy-Item "LICENSE.txt" "dist\" -Force }

Write-Host "✓ All files prepared for installer" -ForegroundColor Green

# Step 7: Create installer with Inno Setup
Write-Host ""
Write-Host "[7/7] Creating Windows installer..." -ForegroundColor Yellow

# Find Inno Setup
$innoSetupPaths = @(
    "C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
    "C:\Program Files\Inno Setup 6\ISCC.exe",
    "C:\Program Files (x86)\Inno Setup 5\ISCC.exe",
    "C:\Program Files\Inno Setup 5\ISCC.exe"
)

$innoSetup = $null
foreach ($path in $innoSetupPaths) {
    if (Test-Path $path) {
        $innoSetup = $path
        break
    }
}

if (-not $innoSetup) {
    Write-Host ""
    Write-Host "⚠️  WARNING: Inno Setup not found!" -ForegroundColor Yellow
    Write-Host "Please install Inno Setup from: https://jrsoftware.org/isdl.php" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "After installing Inno Setup, you can create the installer manually by:" -ForegroundColor Cyan
    Write-Host "1. Opening installer.iss in Inno Setup" -ForegroundColor Cyan
    Write-Host "2. Clicking Build -> Compile" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Your executable is ready at: dist\SinhalaTTS.exe" -ForegroundColor Green
    Write-Host ""
    Write-Host "===========================================" -ForegroundColor Yellow
    Write-Host "        EXECUTABLE BUILD COMPLETED!" -ForegroundColor Yellow
    Write-Host "===========================================" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 0
}

# Create the installer
Write-Host "Using Inno Setup: $innoSetup" -ForegroundColor Cyan
$innoResult = & $innoSetup "installer.iss" 2>&1

if ($LASTEXITCODE -eq 0 -and (Test-Path "installer_output\SinhalaTTS_Setup_v1.0.exe")) {
    Write-Host "✓ Installer created successfully!" -ForegroundColor Green
    
    # Success message
    Write-Host ""
    Write-Host "===========================================" -ForegroundColor Green
    Write-Host "          BUILD COMPLETED SUCCESSFULLY!" -ForegroundColor Green
    Write-Host "===========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Your installer is ready:" -ForegroundColor Cyan
    Write-Host "  Location: installer_output\SinhalaTTS_Setup_v1.0.exe" -ForegroundColor White
    
    $installerSize = (Get-Item "installer_output\SinhalaTTS_Setup_v1.0.exe").Length
    Write-Host "  Size: $([math]::Round($installerSize / 1MB, 2)) MB" -ForegroundColor White
    
    Write-Host ""
    Write-Host "The installer includes:" -ForegroundColor Cyan
    Write-Host "  ✓ SinhalaTTS.exe (main application)" -ForegroundColor Green
    Write-Host "  ✓ All required dependencies" -ForegroundColor Green
    Write-Host "  ✓ Phoneme audio files" -ForegroundColor Green
    Write-Host "  ✓ Documentation files" -ForegroundColor Green
    Write-Host "  ✓ Uninstaller" -ForegroundColor Green
    Write-Host ""
    Write-Host "You can now distribute this installer to others!" -ForegroundColor Yellow
} else {
    Write-Host "❌ Failed to create installer!" -ForegroundColor Red
    Write-Host "Inno Setup output: $innoResult" -ForegroundColor Red
}

Write-Host ""
Read-Host "Press Enter to exit" 