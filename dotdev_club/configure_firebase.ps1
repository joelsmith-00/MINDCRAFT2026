# Firebase Configuration Script for DOTDEV Club App
# This script helps automate the Firebase setup process

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Firebase Configuration Helper" -ForegroundColor Cyan
Write-Host "  DOTDEV Club App" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Function to check if a file exists
function Test-FileExists {
    param([string]$Path)
    return Test-Path -Path $Path
}

# Function to create directory if it doesn't exist
function Ensure-Directory {
    param([string]$Path)
    if (-not (Test-Path -Path $Path)) {
        New-Item -ItemType Directory -Path $Path -Force | Out-Null
        Write-Host "✓ Created directory: $Path" -ForegroundColor Green
    }
}

# Check if we're in the right directory
if (-not (Test-FileExists "pubspec.yaml")) {
    Write-Host "❌ Error: pubspec.yaml not found!" -ForegroundColor Red
    Write-Host "Please run this script from the dotdev_club project root directory." -ForegroundColor Yellow
    exit 1
}

Write-Host "✓ Found Flutter project" -ForegroundColor Green
Write-Host ""

# Step 1: Check for google-services.json
Write-Host "[Step 1/5] Checking for google-services.json..." -ForegroundColor Yellow
$googleServicesPath = "android\app\google-services.json"

if (Test-FileExists $googleServicesPath) {
    Write-Host "✓ google-services.json found!" -ForegroundColor Green
} else {
    Write-Host "❌ google-services.json NOT found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please download google-services.json from Firebase Console and place it at:" -ForegroundColor Yellow
    Write-Host "  $googleServicesPath" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Instructions:" -ForegroundColor Yellow
    Write-Host "1. Go to Firebase Console > Project Settings" -ForegroundColor White
    Write-Host "2. Scroll to 'Your apps' section" -ForegroundColor White
    Write-Host "3. Click on your Android app" -ForegroundColor White
    Write-Host "4. Download google-services.json" -ForegroundColor White
    Write-Host "5. Place it in: android\app\" -ForegroundColor White
    Write-Host ""
    
    $continue = Read-Host "Do you want to continue anyway? (y/n)"
    if ($continue -ne "y") {
        exit 1
    }
}
Write-Host ""

# Step 2: Check Android build.gradle configuration
Write-Host "[Step 2/5] Checking Android configuration..." -ForegroundColor Yellow
$buildGradlePath = "android\build.gradle"

if (Test-FileExists $buildGradlePath) {
    $buildGradleContent = Get-Content $buildGradlePath -Raw
    
    if ($buildGradleContent -match "com.google.gms:google-services") {
        Write-Host "✓ Google Services plugin found in build.gradle" -ForegroundColor Green
    } else {
        Write-Host "⚠ Google Services plugin NOT found in build.gradle" -ForegroundColor Yellow
        Write-Host "  You may need to add it manually." -ForegroundColor Yellow
    }
} else {
    Write-Host "⚠ android\build.gradle not found" -ForegroundColor Yellow
}
Write-Host ""

# Step 3: Check app-level build.gradle
Write-Host "[Step 3/5] Checking app-level build.gradle..." -ForegroundColor Yellow
$appBuildGradlePath = "android\app\build.gradle"

if (Test-FileExists $appBuildGradlePath) {
    $appBuildGradleContent = Get-Content $appBuildGradlePath -Raw
    
    if ($appBuildGradleContent -match "com.google.gms.google-services") {
        Write-Host "✓ Google Services plugin applied in app/build.gradle" -ForegroundColor Green
    } else {
        Write-Host "⚠ Google Services plugin NOT applied in app/build.gradle" -ForegroundColor Yellow
        Write-Host "  You may need to add it manually." -ForegroundColor Yellow
    }
} else {
    Write-Host "⚠ android\app\build.gradle not found" -ForegroundColor Yellow
}
Write-Host ""

# Step 4: Collect Firebase configuration
Write-Host "[Step 4/5] Firebase Configuration Setup" -ForegroundColor Yellow
Write-Host ""
Write-Host "Please enter your Firebase configuration values." -ForegroundColor Cyan
Write-Host "You can find these in Firebase Console > Project Settings > Your apps" -ForegroundColor Cyan
Write-Host ""

$apiKey = Read-Host "Enter API Key (starts with AIzaSy...)"
$appId = Read-Host "Enter App ID (format: 1:123456789:android:...)"
$senderId = Read-Host "Enter Messaging Sender ID (numbers only)"
$projectId = Read-Host "Enter Project ID (default: dotdev-club)" 
if ([string]::IsNullOrWhiteSpace($projectId)) {
    $projectId = "dotdev-club"
}
$storageBucket = Read-Host "Enter Storage Bucket (default: dotdev-club.appspot.com)"
if ([string]::IsNullOrWhiteSpace($storageBucket)) {
    $storageBucket = "dotdev-club.appspot.com"
}

Write-Host ""
Write-Host "Configuration Summary:" -ForegroundColor Cyan
Write-Host "  API Key: $apiKey" -ForegroundColor White
Write-Host "  App ID: $appId" -ForegroundColor White
Write-Host "  Sender ID: $senderId" -ForegroundColor White
Write-Host "  Project ID: $projectId" -ForegroundColor White
Write-Host "  Storage Bucket: $storageBucket" -ForegroundColor White
Write-Host ""

$confirm = Read-Host "Is this correct? (y/n)"
if ($confirm -ne "y") {
    Write-Host "Configuration cancelled." -ForegroundColor Yellow
    exit 0
}

# Step 5: Generate configuration code
Write-Host ""
Write-Host "[Step 5/5] Generating configuration code..." -ForegroundColor Yellow

$configCode = @"
await Firebase.initializeApp(
  options: const FirebaseOptions(
    apiKey: '$apiKey',
    appId: '$appId',
    messagingSenderId: '$senderId',
    projectId: '$projectId',
    storageBucket: '$storageBucket',
  ),
);
"@

# Save to a file
$outputFile = "firebase_config_output.txt"
$configCode | Out-File -FilePath $outputFile -Encoding UTF8

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Configuration Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "✓ Configuration code saved to: $outputFile" -ForegroundColor Green
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "1. Open lib\main.dart" -ForegroundColor White
Write-Host "2. Find the Firebase.initializeApp() section" -ForegroundColor White
Write-Host "3. Replace it with the code from $outputFile" -ForegroundColor White
Write-Host "4. Run: flutter pub get" -ForegroundColor White
Write-Host "5. Run: flutter run" -ForegroundColor White
Write-Host ""
Write-Host "Configuration code:" -ForegroundColor Cyan
Write-Host "-----------------------------------" -ForegroundColor Gray
Write-Host $configCode -ForegroundColor Yellow
Write-Host "-----------------------------------" -ForegroundColor Gray
Write-Host ""

# Open the output file
Write-Host "Opening configuration file..." -ForegroundColor Cyan
Start-Process notepad.exe -ArgumentList $outputFile

Write-Host ""
Write-Host "🎉 Setup helper complete! Good luck with your DOTDEV Club app!" -ForegroundColor Green
Write-Host ""
