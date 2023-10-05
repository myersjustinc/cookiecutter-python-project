from argparse import ArgumentParser
import json
import os
from pathlib import Path
from shlex import quote as sh_quote
from shutil import copytree, which
import subprocess
from textwrap import dedent


# SET `${WORKON_HOME}` --------------------------------------------------------


project_root = Path(__file__).parent.resolve()
project_slug = '{{cookiecutter.project_slug}}'

venv_dir = project_root / '.virtualenv'
venv_dir.mkdir(parents=False, exist_ok=True)

pipenv_interpreter = Path(which('pipenv')).resolve().parent / 'python3'
project_env_path = project_root / '.env'

env_json = json.dumps({
    'project_env_path': str(project_env_path),
    'venv_dir': str(venv_dir),
    'project_slug': project_slug,
})

workon_script = dedent(f'''
    import json
    import os.path
    from pipenv.vendor.dotenv import set_key

    args = json.loads({repr(env_json)})  # FIXME: eval

    set_key(
        args['project_env_path'],
        'WORKON_HOME',
        args['venv_dir'])
    set_key(
        args['project_env_path'],
        'PIPENV_CUSTOM_VENV_NAME',
        args['project_slug'])
    set_key(
        args["project_env_path"],
        'JUPYTER_DATA_DIR',
        os.path.join(
            args['venv_dir'], args['project_slug'], 'share', 'jupyter'))
    ''')
subprocess.run(
    [str(pipenv_interpreter),],
    check=True, input=workon_script, cwd=project_root,
    capture_output=True, encoding='utf-8')


# PREPARE PROJECT'S VIRTUAL ENVIRONMENT ---------------------------------------


install_args = {
    'categories': [],
    'dev': True,
}

parser = ArgumentParser()
parser.add_argument(
    '--python', help='Python version to use with the project')
args = parser.parse_args()
if args.python:
    install_args['python'] = args.python

pipfile_path = project_root / 'Pipfile'
if not pipfile_path.is_file():
    del install_args['dev']
    install_args['packages'] = [
        'altair',
        'import_ipynb',
        'itables',
        'jupyterlab',
        'jupyterlab-quarto',
        'jupyterlab_templates',
        'jupytext',
        'matplotlib',
        'pandas',
        'quarto',
    ]

install_json = json.dumps(install_args)
install_script = dedent(f'''
    import json
    from pipenv.utils.environment import load_dot_env
    from pipenv.project import Project
    from pipenv.routines.install import do_install
    args = json.loads({repr(install_json)})  # FIXME: eval
    project = Project()
    load_dot_env(project)
    do_install(project, **args)
    ''')
subprocess.run(
    [str(pipenv_interpreter),],
    check=True, input=install_script, cwd=project_root, encoding='utf-8')


# INSTALL JUPYTER NOTEBOOK TEMPLATES ------------------------------------------


notebook_templates_dir = project_root / 'analysis' / 'notebook_templates'
jupyter_templates_dir = (
    venv_dir / project_slug / 'share' / 'jupyter' / 'notebook_templates')
jupyter_templates_dir.parent.mkdir(parents=True, exist_ok=True)
jupyter_templates_dir.symlink_to(
    notebook_templates_dir, target_is_directory=True)


# PAIR EXISTING NOTEBOOKS -----------------------------------------------------


project_interpreter = venv_dir / project_slug / 'bin' / 'python3'

notebook_source_paths = []
for subdir_name in ('analysis', 'etl',):
    for notebook_type in ('qmd', 'ipynb',):
        notebook_source_paths.extend(
            (project_root / subdir_name).glob(f'**/*.{notebook_type}'))
jupytext_args = ['--set-formats', 'qmd,ipynb']
jupytext_args.extend(map(str, notebook_source_paths))

jupytext_json = json.dumps(jupytext_args)
pairing_script = dedent(f'''
    import json
    from jupytext.cli import jupytext
    args = json.loads({repr(jupytext_json)})  # FIXME: eval
    jupytext(args)
    ''')
subprocess.run(
    [str(project_interpreter),],
    check=True, input=pairing_script, cwd=project_root, encoding='utf-8')


# FINISH PATHING CONFIGURATION ------------------------------------------------


jupyter_data_dir = venv_dir / project_slug / 'share' / 'jupyter'
kernel_dir = jupyter_data_dir / 'kernels' / 'python3'
kernel_config = {
    'argv': [
        str(kernel_dir / 'kernel.sh'),
        '{connection_file}'],
    'display_name': project_slug,
    'language': 'python',
    'metadata': {
        'debugger': True,
    },
}
with (kernel_dir / 'kernel.json').open('w') as output_file:
    json.dump(kernel_config, output_file, indent=2)

kernel_script_path = kernel_dir / 'kernel.sh'
with kernel_script_path.open('w') as output_file:
    output_file.write(
        '#!/bin/bash\n')
    output_file.write(
        f'cd {sh_quote(str(project_root))}\n')
    output_file.write(
        f'exec {sh_quote(str(project_interpreter))} '
        '-m ipykernel_launcher -f "$1"\n')

kernel_script_path.chmod(0o777)
