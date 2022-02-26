from cx_Freeze import *

setup(
    name = 'Generate-pass',
    version = '2',
    description = 'Programme qui genère des mot de passe et qui le change automatiquement dans l\'interface routeur',
    executables = [Executable('main.py')]
)
