import os
import re
import time
import sys

def read_process(cmd, args=''):
    fullcmd = '%s %s' % (cmd, args)
    pipeout = os.popen(cmd)
    try:
        firstline = pipeout.readline()
        cmd_not_found = re.search(
            b'(not recognized|No such file|not found)',
            firstline,
            re.IGNORECASE
        )
        if cmd_not_found:
            raise IOError('%s must be on your system path.' % cmd)
        output = firstline + pipeout.read()
        # pb_flush(task)
    finally:
        pipeout.close()
    return output

def bashsh(**args):
    sh_args = args['cmd']
    for arg in args['args']:
        sh_args += ' ' + arg
    if args['append']:
        sh_args += " >> {}/{}.txt".format(args['output_path'],args['task_name'])
    else:
        sh_args += " > {}/{}.txt".format(args['output_path'],args['task_name'])
    pb_flush(args['task_name'])
    read_process(sh_args)

def mongosh(**args):
    sh_args = "mongo \
        --quiet \
        --port {} \
        -u {} \
        -p {} \
        --authenticationDatabase=admin".format(args['port'],args['username'],args['password'])
    if args['isTls']:
        sh_args += " --tls \
            --tlsCertificateKeyFile {} \
            --tlsCAFile {} \
            --tlsCertificateKeyFilePassword {}".format(args['tlsCertificateKeyFile'],args['tlsCAFile'],args['tlsCertificateKeyFilePassword'])
    sh_args += " ./vars.js ./{}".format(args['js'])
    read_process(sh_args)