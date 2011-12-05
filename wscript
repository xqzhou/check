#! /usr/bin/env python
# encoding: utf-8
APPNAME = 'check'
VERSION = '0.9.8'

top = '.'
out = 'build'


def options(opt):
    opt.load('compiler_c')


def configure(conf):
    conf.load('compiler_c')
    
    for header in ['stddef.h', 'stdlib.h', 'string.h', 'memory.h', 'stdint.h', 
            'sys/time.h', 'unistd.h', 'fcntl.h', 'sys/types.h', 'sys/wait.h', 'sys/stat.h', 
            'dlfcn.h', 'inttypes.h', 'strings.h']:
        conf.check(header_name=header, mandatory=False)

    for pair in [('fileno', 'stdio.h'), ('localtime_r', 'time.h'), ('pipe', 'unistd.h'), 
            ('putenv', 'stdlib.h'), ('setenv', 'stdlib.h'), ('sleep', 'unistd.h'), ('strdup', 'string.h'), 
            ('strsignal', 'string.h'), ('unsetenv', 'stdlib.h')]:
        try:
            conf.check_cc(function_name=pair[0], header_name=pair[1], define_name=('HAVE_DECL_%s' % pair[0].upper()))
        except conf.errors.ConfigurationError:
            pass
        finally:
            conf.define('HAVE_%s' % pair[0].upper(), 1)

    conf.check_cc(function_name='malloc', header_name='stdlib.h', mandatory=False)
    conf.check_cc(function_name='realloc', header_name='stdlib.h', mandatory=False)

    conf.check(fragment='int main() { printf("%d", sizeof(int)); }\n', define_ret=True, quote=0,
            define_name='SIZEOF_INT', mandatory=True, execute=True, msg='Checking for size of int')
    conf.check(fragment='int main() { printf("%d", sizeof(long)); }\n', define_ret=True, quote=0,
            define_name='SIZEOF_LONG', mandatory=True, execute=True, msg='Checking for size of long')
    conf.check(fragment='int main() { printf("%d", sizeof(short)); }\n', define_ret=True, quote=0,
            define_name='SIZEOF_SHORT', mandatory=True, execute=True, msg='Checking for size of short')

    conf.write_config_header('config.h')


def build(bld):
    bld.recurse('src')
