"""Exercise variant packaging with a fake compiler; never compile firmware."""
from pathlib import Path
import tempfile
import subprocess
import shutil
import hashlib

project = Path(__file__).resolve().parents[1]
partition_scheme = "app13M_data7M_32MB"
expected_partition = f"PartitionScheme={partition_scheme}"

# Keep all user-facing and automated build entry points on one supported menu ID.
for relative in (
    "Compile-P4-Variants.ps1",
    "tools/build_p4.py",
    "README.md",
    "README.zh-CN.md",
):
    content = (project / relative).read_text(encoding="utf-8")
    assert expected_partition in content, f"{relative} is missing {expected_partition}"
    for stale in ("app3M_fat9M_16MB", "app3M_fat16M_16MB", "app5M_fat24M_32MB"):
        assert stale not in content, f"{relative} still contains stale partition ID {stale}"

with tempfile.TemporaryDirectory(prefix="p4-build-test-") as tmp:
    root = Path(tmp) / "P4-CAN-Universal-v9.99.0"
    root.mkdir()
    for name in (
        "Compile-P4-Variants.ps1",
        "tools/prepare_variant_build.py",
        "tools/build_dashboard.py",
    ):
        destination = root / name
        destination.parent.mkdir(exist_ok=True)
        shutil.copy(project / name, destination)

    (root / "P4-CAN-Universal-v9.99.0.ino").write_text("// mock", encoding="utf-8")
    (root / "dashboard_source.html").write_text("original dashboard", encoding="utf-8")
    (root / "index_html.h").write_text("original header", encoding="utf-8")
    (root / "zh-CN").mkdir()
    (root / "zh-CN/dashboard_source.zh-CN.html").write_bytes("<html>\\u4e2d\\u6587</html>".encode())
    before = {
        path.relative_to(root): hashlib.sha256(path.read_bytes()).digest()
        for path in root.rglob("*") if path.is_file()
    }

    (root / "fake.py").write_text(r'''import sys, gzip, re
from pathlib import Path
args = sys.argv
fqbn = args[args.index('--fqbn') + 1]
assert 'FlashSize=32M' in fqbn, fqbn
assert 'PartitionScheme=app13M_data7M_32MB' in fqbn, fqbn
with (Path(__file__).parent / 'fake-fqbns.txt').open('a', encoding='utf-8') as log:
    log.write(fqbn + '\\n')
p = Path(args[args.index('--output-dir') + 1])
p.mkdir(parents=True, exist_ok=True)
sketch = Path(args[-1])
name = next(sketch.glob('*.ino')).name
if '.zh-CN' in str(p):
    data = bytes(int(value, 16) for value in re.findall(r'0x([0-9A-Fa-f]{2})', (sketch / 'index_html.h').read_text()))
    assert gzip.decompress(data) == (sketch / 'zh-CN/dashboard_source.zh-CN.html').read_bytes()
    assert (sketch / 'dashboard_source.html').read_bytes() == gzip.decompress(data)
else:
    assert (sketch / 'index_html.h').read_text() == 'original header'
for suffix in ('bin', 'merged.bin', 'bootloader.bin', 'partitions.bin'):
    (p / (name + '.' + suffix)).write_bytes(b'test-firmware')
''', encoding="utf-8")

    cli = root / "fake-cli.cmd"
    cli.write_text('@echo off\npython "%~dp0fake.py" %*\nexit /b %errorlevel%\n', encoding="utf-8")
    result = subprocess.run(
        ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File",
         str(root / "Compile-P4-Variants.ps1"), "-ArduinoCli", str(cli)],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr

    fqbn_lines = (root / "fake-fqbns.txt").read_text(encoding="utf-8").splitlines()
    assert len(fqbn_lines) == 4, fqbn_lines
    assert sum("ChipVariant=postv3" in value for value in fqbn_lines) == 2, fqbn_lines
    assert sum("ChipVariant=prev3" in value for value in fqbn_lines) == 2, fqbn_lines
    assert all(expected_partition in value for value in fqbn_lines), fqbn_lines

    expected = {
        f"P4-CAN-Universal-v9.99.0{language}.{kind}.{revision}{suffix}"
        for language in ("", ".zh-CN")
        for kind, suffix in (("OTA", ".bin"), ("FULLFLASH", ".merged.bin"))
        for revision in ("REV1.X", "REV3.X")
    }
    assert {path.name for path in (root / "Final-Build").iterdir()} == expected
    assert not (root / "build_variants").exists(), "Successful builds must remove temporary build_variants"
    for name, digest in before.items():
        assert hashlib.sha256((root / name).read_bytes()).digest() == digest, name

print("PASS: shared 32 MB partition menu, four simulated builds, eight final binaries, Chinese gzip matches source, originals unchanged")
