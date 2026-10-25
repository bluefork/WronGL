#!/bin/bash
set -e

# Define variables
APP_NAME="wrongl"
VERSION="1.0"
ARCH="amd64"
DEB_DIR="build_deb/${APP_NAME}_${VERSION}_${ARCH}"

echo "Building .deb package for WronGL..."

# Create directory structure
mkdir -p "${DEB_DIR}/DEBIAN"
mkdir -p "${DEB_DIR}/usr/bin"
mkdir -p "${DEB_DIR}/usr/share/applications"
mkdir -p "${DEB_DIR}/usr/share/icons/hicolor/256x256/apps"

# Copy binary (Assume PyInstaller output is in dist/WronGL)
cp dist/WronGL "${DEB_DIR}/usr/bin/wrongl"
chmod +x "${DEB_DIR}/usr/bin/wrongl"

# Copy icon
cp wrongl/resources/icon.png "${DEB_DIR}/usr/share/icons/hicolor/256x256/apps/wrongl.png"

# Create .desktop file
cat <<EOF > "${DEB_DIR}/usr/share/applications/wrongl.desktop"
[Desktop Entry]
Name=WronGL
Comment=Smart Layout Converter
Exec=/usr/bin/wrongl
Icon=wrongl
Terminal=false
Type=Application
Categories=Utility;TextTools;
EOF

# Create DEBIAN/control file
cat <<EOF > "${DEB_DIR}/DEBIAN/control"
Package: ${APP_NAME}
Version: ${VERSION}
Section: utils
Priority: optional
Architecture: ${ARCH}
Depends: python3-tk, xclip, libayatana-appindicator3-1 | libappindicator3-1
Maintainer: WronGL Contributors
Description: Smart bidirectional keyboard layout converter for Persian and English.
EOF

# Build the .deb
dpkg-deb --build --root-owner-group "${DEB_DIR}"
mv "${DEB_DIR}.deb" "dist/WronGL_v${VERSION}_${ARCH}.deb"
echo "Successfully built dist/WronGL_v${VERSION}_${ARCH}.deb"