import subprocess


def test_main():
    assert (
        subprocess.check_output(["import-siruta-csv"], text=True)
        == """Reading PosixPath('data/siruta-judete.csv') with fields: ['JUD', 'DENJ', 'FSJ', 'MNEMONIC', 'ZONA']
Reading PosixPath('data/siruta_an_2024.csv') with fields: ['SIRUTA', 'DENLOC', 'CODP', 'JUD', 'SIRSUP', 'TIP', 'NIV', 'MED', 'REGIUNE', 'FSJ', 'FSL', 'NUTS']
"""
    )
