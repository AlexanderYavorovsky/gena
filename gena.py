import subprocess
import os
import argparse
import random

csmith_src = 'https://github.com/csmith-project/csmith.git'
csmith_dir = 'csmith'
gen_dir = 'generated'
gen_filename = 'my1.c'
out_filename = 'my1.out'

# TODO: more options
template_config = {
    '--seed': range(1, 100),
    '--max-funcs': range(1, 20),
    '--max-expr-complexity': range(2, 30)
}

config = dict()

# TODO: make more clearly
parser = argparse.ArgumentParser(description='Generate random .out file')
parser.add_argument('-s', '--source', help='name of the generated .c file')
parser.add_argument('-o', '--out', help='name of the generated .out file')
parser.add_argument('-d', '--outdir', help='''related path to the directory
                    where generated files will be stored''')

args = parser.parse_args()

if args.source:
    gen_filename = args.source
if args.out:
    out_filename = args.out
if args.outdir:
    gen_dir = args.outdir


def install_csmith():
    # clone repo
    if not os.path.isdir(csmith_dir):
        subprocess.run(['git', 'clone', csmith_src])

    os.chdir(csmith_dir)

    # install requirements
    subprocess.run(['sudo', 'apt', 'install', 'g++', 'cmake', 'm4'])

    # TODO: cmake install prefix?
    # TODO: get rid of install, use package;
    #       do not forget to fix all paths to csmith and its .h
    subprocess.run(['cmake', '.'])
    subprocess.run(['make'])
    subprocess.run(['sudo', 'make', 'install'], capture_output=True)


def install_tools():
    # TODO: use unknown elf
    # subprocess.run(['sudo', 'apt', 'install', 'gcc-riscv64-unknown-elf'])
    subprocess.run(['sudo', 'apt', 'install', 'gcc-riscv64-linux-gnu'])


def generate_config(config):
    for flag in template_config.keys():
        if random.randint(0, 2):
            config[flag] = str(random.choice(template_config[flag]))
            print(flag)
            print(config[flag])


def generate(dest_name):
    os.chdir('..')
    if not os.path.isdir(gen_dir):
        os.mkdir(gen_dir)
    os.chdir(gen_dir)

    generate_config(config)

    # TODO: arguments from mutation
    run_process = ['/usr/local/bin/csmith']
    for flag in config.keys():
        run_process.append(flag)
        run_process.append(config[flag])
    gen_proc = subprocess.run(run_process, capture_output=True, text=True)

    with open(dest_name, 'w') as f:
        f.write(gen_proc.stdout)


def build(src_name, dest_name):
    # TODO: use unknown elf instead
    subprocess.run(
        ['riscv64-linux-gnu-gcc', '--static', '-O0',
         '-I/usr/local/include', src_name, '-o', dest_name],
        capture_output=True)


print('Gena is waking up!')

install_csmith()
install_tools()
generate(gen_filename)
build(gen_filename, out_filename)

# TODO: send to gem5, receive config from mutator, run again

print(f'Generated file {os.path.join(gen_dir, gen_filename)}'
      f' and built it into {os.path.join(gen_dir, out_filename)}')
print('Gena is going to sleep...')
