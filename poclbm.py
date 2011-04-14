#!/usr/bin/python

import pyopencl as cl
from time import sleep
from BitcoinMiner import *
from optparse import OptionParser

parser = OptionParser(version=USER_AGENT)
parser.add_option('--user',           dest='user',     default='bitcoin',   help='user name')
parser.add_option('--pass',           dest='password', default='password',  help='password')
parser.add_option('--host',           dest='host',     default='127.0.0.1', help='RPC host (without \'http://\')')
parser.add_option('--port',           dest='port',     default='8332',      help='RPC port', type='int')
parser.add_option('-r', '--rate',     dest='rate',     default=1,           help='hash rate display interval in seconds, default=1', type='float')
parser.add_option('-f', '--fps_fast', dest='fps_fast', default=10,          help='primary framerate, default=10, decrease for more hashing performance', type='int')
parser.add_option('-s', '--fps_slow', dest='fps_slow', default=100,         help='secondary framerate, default=100, increase for less desktop lag', type='int')
parser.add_option('-d', '--device',   dest='device',   default=-1,          help='use device by id, by default asks for device', type='int')
parser.add_option('-a', '--askrate',  dest='askrate',  default=5,           help='how many seconds between getwork requests, default 5, max 10', type='int')
parser.add_option('-w', '--worksize', dest='worksize', default=-1,          help='work group size, default is maximum returned by opencl', type='int')
parser.add_option('-v', '--vectors',  dest='vectors',  action='store_true', help='use vectors')
parser.add_option('--verbose',        dest='verbose',  action='store_true', help='verbose output, suitable for redirection to log file')
parser.add_option('--platform',       dest='platform', default=-1,          help='use platform by id', type='int')
(options, args) = parser.parse_args()

if not -1 < options.port < 0xFFFF:
	print 'invalid port'
	sys.exit()

platforms = cl.get_platforms()

if options.platform >= len(platforms) or (options.platform == -1 and len(platforms) > 1):
	print 'Wrong platform or more than one OpenCL platforms found, use --platform to select one of the following\n'
	for i in xrange(len(platforms)):
		print '[%d]\t%s' % (i, platforms[i].name)
	sys.exit()

if options.platform == -1:
	options.platform = 0

devices = platforms[options.platform].get_devices()
if (options.device == -1 or options.device >= len(devices)):
	print 'No device specified or device not found, use -d to specify one of the following\n'
	for i in xrange(len(devices)):
		print '[%d]\t%s' % (i, devices[i].name)
	sys.exit()

miner = None
try:
	miner = BitcoinMiner(devices[options.device],
		options.host,
		options.user,
		options.password,
		options.port,
		options.rate,
		options.askrate,
		options.worksize,
		options.vectors,
		options.verbose)
	miner.fps_slow = options.fps_slow
	miner.fps_fast = options.fps_fast
	miner.swapFrame()
	miner.mine()
except KeyboardInterrupt:
	print '\b\b  \nStopping...'
finally:
	if miner: miner.exit()
sleep(1.1)
