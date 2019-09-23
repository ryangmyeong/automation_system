import os
import time
import sys
#import adb
sys.path.append('./lib')
sys.path.append('lib')
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'lib'))
import adb
import xml.sax
# for debug, comment it
from atf import *

CUR_DIR = os.path.abspath(__file__).strip(os.path.abspath(__file__).split('/')[-1])
testTimes = 1
timeWaitStep = 2
timeWaitActivity = 10
timeWaitTest = 300
result = []
result_str = ''
out_dir=time.strftime('%Y%m%d_%H%M%S')
tr = TestResult(__file__)
apk_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'src', 'RL_Benchmark.apk')
#apk_path = './src/RL_Benchmark.apk'


class Rlbench(xml.sax.ContentHandler):
    def __init__(self):
        self.current = None
        self.name = None
        self.score = None

    def startElement(self, tag, attr):
        self.current = tag
        if tag == 'long':
			tr.sub_score(attr['name'], attr['value'])



def waitDisplay(waittime):
	for i in range(100):
		time.sleep(waittime/100.0)
		sys.stdout.write("\r	testing %d%% done" % (i+1))
		sys.stdout.flush()

def get_result():
	print os.path.join(CUR_DIR,out_dir, 'rlbenchmark.txt')

	alltext = 'adb shell cat /data/data/com.redlicense.benchmark.sqlite/shared_prefs/rlbenchmark.xml >'+os.path.join(CUR_DIR,out_dir, 'rlbenchmark.txt')
	os.popen(alltext)
	#print alltext
	parser = xml.sax.make_parser()
	Handler = Rlbench()
	parser.setContentHandler(Handler)
	
	parser.parse(os.path.join(CUR_DIR,out_dir, 'rlbenchmark.txt'))
	
	text = os.popen("adb shell cat /data/data/com.redlicense.benchmark.sqlite/shared_prefs/rlbenchmark.xml | grep overall | grep -o -e '[0-9]\+'").readlines()
	if len(text) > 0 :
		#print text[0]
		result = int(text[0])/1000.0
		result = str(result)
		return result
	else:
		print 'Error, no result find'
		return 'Error, no result find'



def click_test():
	adb.dpad_up()
	adb.dpad_up()
	adb.dpad_up()
	adb.dpad_center()

	#adb.dpad_center()
	#adb.dpad_center()
	
	#os.system('adb shell input keyevent KEYCODE_DPAD_RIGHT')
	#adb.dpad_center()


def startRLBench():
	os.system('adb logcat -c')
	clear_data_rlbench()
	os.system('adb shell am start -n com.redlicense.benchmark.sqlite/.Main')
	time.sleep(timeWaitActivity)

def clear_data_rlbench():
	os.system('adb shell pm clear com.redlicense.benchmark.sqlite')

def installApk():
	os.system('adb install '+apk_path)
	time.sleep(5)
	adbPressHome()

def adbPressHome():
	os.system('adb shell input keyevent 3')
	os.system('adb shell input keyevent 4')
	time.sleep(timeWaitStep)

def adbUnlockScreen():
	os.system('adb shell input keyevent 82')
	adbPressHome()


def check_device():
	text = os.popen('adb devices').readlines()
	if len(text) != 3 :
		return False
	else:
		return True

def dotest():

	for i in range(4):
		startRLBench()
		click_test()
		waitDisplay(30)
		result = get_result()
		print '\nRLBenchMark Result : '+result  #add by liangyuxiang20170330
		adb.killapp()
		if result == 'Error, no result find':
			continue
		else:
			break
	return result

def main():
	
	print CUR_DIR
	if not os.path.exists(os.path.join(CUR_DIR,'./'+out_dir+'/')):
		os.mkdir(os.path.join(CUR_DIR,'./'+out_dir+'/'))
	if not check_device():
		print 'Error no device'
		print 'Quit'
		return

	os.system('adb root')
	adbUnlockScreen()

	# comment for debug
	# adb.system_setup(tog_bt=True,tog_wifi=True,tog_gps=True,)
	os.system('adb shell input keyevent KEYCODE_DPAD_UP')
	time.sleep(2)
	os.system('adb shell input keyevent KEYCODE_DPAD_CENTER')
	time.sleep(2)
	adb.turn_airplane('1')
	adb.turn_bluetooth('0')
	adb.turn_wifi('0')
	adb.turn_gps('0')
	adb.set_display_time()

	installApk()
	#dotest()
	result = dotest()

	print "Result is {overall}".format(overall= result)
	adbPressHome()
	# comment for debug
	tr.result(result)
	tr.add_attachment(os.path.join(CUR_DIR,out_dir, 'rlbenchmark.txt'),'rlbenchmark.txt')
	tr.save()


if __name__ == "__main__":
	main()