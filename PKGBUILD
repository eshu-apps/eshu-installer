# Maintainer: Eshu Team <support@eshu-apps.com>
pkgname=eshu-installer
pkgver=0.4.0
pkgrel=1
pkgdesc="AI-Driven Universal Package Installer for Linux"
arch=('any')
url="https://eshu-apps.com"
license=('MIT')
depends=(
    'python>=3.9'
    'python-typer'
    'python-rich'
    'python-pydantic'
    'python-anthropic'
    'python-openai'
    'python-requests'
    'python-psutil'
    'python-yaml'
)
makedepends=('python-build' 'python-installer' 'python-wheel')
optdepends=(
    'ollama: For local AI support'
    'timeshift: For system snapshots'
    'snapper: For system snapshots (alternative)'
)
source=("$pkgname-$pkgver.tar.gz::https://github.com/eshu-apps/$pkgname/archive/v$pkgver.tar.gz")
sha256sums=('SKIP')  # Update with actual checksum when releasing

build() {
    cd "$pkgname-$pkgver"
    python -m build --wheel --no-isolation
}

package() {
    cd "$pkgname-$pkgver"
    python -m installer --destdir="$pkgdir" dist/*.whl

    # Install license
    install -Dm644 LICENSE "$pkgdir/usr/share/licenses/$pkgname/LICENSE"

    # Install documentation
    install -Dm644 README.md "$pkgdir/usr/share/doc/$pkgname/README.md"

    # Install shell script
    install -Dm755 install-eshu.sh "$pkgdir/usr/share/$pkgname/install-eshu.sh"
}

# vim:set ts=2 sw=2 et:
