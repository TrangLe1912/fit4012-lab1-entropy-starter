from pathlib import Path
import subprocess
import sys
import re

root = Path('.')
errors = []
warnings = []

required_files = [
    'README.md',
    'report-page.md',
    'src/entropy_redundancy.cpp',
    'src/mod_inverse.cpp',
    'tests/test_cases.md',
    'logs/run_log.md',
]

for rel in required_files:
    if not (root / rel).exists():
        errors.append(f'Thieu file bat buoc: {rel}')

if errors:
    for e in errors:
        print(f'::error::{e}')
    sys.exit(1)

entropy_code = (root / 'src/entropy_redundancy.cpp').read_text(encoding='utf-8')
modinv_code = (root / 'src/mod_inverse.cpp').read_text(encoding='utf-8')
report = (root / 'report-page.md').read_text(encoding='utf-8')
tests = (root / 'tests/test_cases.md').read_text(encoding='utf-8')
log = (root / 'logs/run_log.md').read_text(encoding='utf-8')
readme = (root / 'README.md').read_text(encoding='utf-8')

if 'TODO(student)' in entropy_code:
    errors.append('src/entropy_redundancy.cpp van con TODO(student).')
if 'TODO(student)' in modinv_code:
    errors.append('src/mod_inverse.cpp van con TODO(student).')

if 'return -1.0;' in entropy_code:
    errors.append('calculate_redundancy() chua duoc hoan thien.')
if re.search(r'int\s+mod_inverse\s*\([^)]*\)\s*\{[^}]*return\s+-1\s*;', modinv_code, flags=re.DOTALL):
    errors.append('mod_inverse() chua duoc hoan thien.')

checked_tests = len(re.findall(r'^-\s*\[[xX]\]', tests, flags=re.MULTILINE))
if checked_tests < 5:
    errors.append('tests/test_cases.md can tick it nhat 5 test cases.')

checked_logs = len(re.findall(r'^-\s*\[[xX]\]', log, flags=re.MULTILINE))
if checked_logs < 5:
    errors.append('logs/run_log.md can danh dau it nhat 5 muc da chay.')

if 'Điều em học được từ bài lab' in log and 'Viết 3-5 dòng ngắn gọn ở đây.' in log:
    warnings.append('Nen thay placeholder trong phan tong ket cua run log.')

for keyword in ['entropy', 'redundancy', 'modulo', 'GitHub']:
    if keyword.lower() not in readme.lower():
        warnings.append(f'README nen co noi dung lien quan den: {keyword}')

if '| aaaa |  |  |  |' in report:
    warnings.append('report-1page.md van chua dien bang ket qua entropy/redundancy.')

compile_targets = [
    ('src/entropy_redundancy.cpp', 'entropy_app'),
    ('src/mod_inverse.cpp', 'modinv_app'),
]

for source, out in compile_targets:
    try:
        subprocess.run(
            ['g++', '-std=c++17', '-O2', '-Wall', '-Wextra', '-pedantic', source, '-o', out],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        errors.append(f'Khong bien dich duoc {source}: {exc.stderr.strip()}')

try:
    commit_count = int(subprocess.check_output(['git', 'rev-list', '--count', 'HEAD'], text=True).strip())
    if commit_count < 3:
        warnings.append('Repo nen co it nhat 3 commits tong cong.')
except Exception as exc:
    warnings.append(f'Khong doc duoc lich su git: {exc}')

for w in warnings:
    print(f'::warning::{w}')

if errors:
    for e in errors:
        print(f'::error::{e}')
    sys.exit(1)

print('::notice::FIT4012 Buổi 2 auto check passed.')
