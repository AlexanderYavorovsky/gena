import subprocess
import os

csmith_src = 'https://github.com/csmith-project/csmith.git'
csmith_dir = 'csmith'
gen_dir = 'generated'
gen_filename = 'my1.c'
out_filename = 'my1.out'

# TODO: use argv

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
    # TODO: install riscv64-linux-gnu-gcc
    pass


def generate(dest_name):
    os.chdir('..')
    if not os.path.isdir(gen_dir):
        os.mkdir(gen_dir)
    os.chdir(gen_dir)

    # TODO: arguments from mutation
    gen_proc = subprocess.run(
        ['/usr/local/bin/csmith'],
        capture_output=True, text=True)

    with open(dest_name, 'w') as f:
        f.write(gen_proc.stdout)


def build(src_name, dest_name):
    # TODO: use riscv instead
    subprocess.run(
        ['gcc', '--static', '-O0',
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
