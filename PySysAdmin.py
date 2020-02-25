#!/usr/bin/python3.6

import schedule
import time
import psutil
import smtplib
import sys
import os
import subprocess
from datetime import date

#-------------------- bytes 2 human def --------------------------------
def bytes2human(n):
    # http://code.activestate.com/recipes/578019
    # >>> bytes2human(10000)
    # '9.8K'
    # >>> bytes2human(100001221)
    # '95.4M'
    symbols = (' kb', ' mb', ' gb', ' tb', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n
#-----------------------------------------------------------------------
#==========================================================================
def SendEmail(zvTo,zvBody):
	# Write email
	TO = zvTo
	FROM = "system@hostname"

	BODY = zvBody

	server = smtplib.SMTP('emailrelay.server.com')
	server.sendmail(FROM, [TO], BODY)
	server.quit()
#====================================================================================================

#================================= os info =============================
def SysAdm():
	#--------------- Disk -------------------------
	zvDf = 'Root ( / ):\n' + "total: "+bytes2human(psutil.disk_usage('/').total) + ", used: "+bytes2human(psutil.disk_usage('/').used) + ", free: "+bytes2human(psutil.disk_usage('/').free) + ", percent: "+str(psutil.disk_usage('/').percent) + "%\n\n"

	zvDf = zvDf + 'HC ( /mnt/iscsi/HCPROD ):\n' + "total: "+bytes2human(psutil.disk_usage('/mnt/iscsi/HCPROD').total) + ", used: "+bytes2human(psutil.disk_usage('/mnt/iscsi/HCPROD').used) + ", free: "+bytes2human(psutil.disk_usage('/mnt/iscsi/HCPROD').free) + ", percent: "+str(psutil.disk_usage('/mnt/iscsi/HCPROD').percent) + "%\n\n"

	zvDf = zvDf + 'RM ( /mnt/iscsi/RMPROD ):\n' + "total: "+bytes2human(psutil.disk_usage('/mnt/iscsi/RMPROD').total) + ", used: "+bytes2human(psutil.disk_usage('/mnt/iscsi/RMPROD').used) + ", free: "+bytes2human(psutil.disk_usage('/mnt/iscsi/RMPROD').free) + ", percent: "+str(psutil.disk_usage('/mnt/iscsi/RMPROD').percent) + "%\n\n"

	zvDf = zvDf + 'cache ( /mnt/iscsi/INTERSYSTEM ):\n' + "total: "+bytes2human(psutil.disk_usage('/mnt/iscsi/INTERSYSTEM').total) + ", used: "+bytes2human(psutil.disk_usage('/mnt/iscsi/INTERSYSTEM').used) + ", free: "+bytes2human(psutil.disk_usage('/mnt/iscsi/INTERSYSTEM').free) + ", percent: "+str(psutil.disk_usage('/mnt/iscsi/INTERSYSTEM').percent) + "%\n\n"

	zvDf = zvDf + 'cache_temp ( /mnt/iscsi/CACHETEMP ):\n' + "total: "+bytes2human(psutil.disk_usage('/mnt/iscsi/CACHETEMP').total) + ", used: "+bytes2human(psutil.disk_usage('/mnt/iscsi/CACHETEMP').used) + ", free: "+bytes2human(psutil.disk_usage('/mnt/iscsi/CACHETEMP').free) + ", percent: "+str(psutil.disk_usage('/mnt/iscsi/CACHETEMP').percent) + "%\n\n"

	zvDf = zvDf + 'journals ( /mnt/iscsi/JOURNALS ):\n' + "total: "+bytes2human(psutil.disk_usage('/mnt/iscsi/JOURNALS').total) + ", used: "+bytes2human(psutil.disk_usage('/mnt/iscsi/JOURNALS').used) + ", free: "+bytes2human(psutil.disk_usage('/mnt/iscsi/JOURNALS').free) + ", percent: "+str(psutil.disk_usage('/mnt/iscsi/JOURNALS').percent) + "%\n\n"

	zvDf = zvDf + 'wij ( /mnt/iscsi/WIJ ):\n' + "total: "+bytes2human(psutil.disk_usage('/mnt/iscsi/WIJ').total) + ", used: "+bytes2human(psutil.disk_usage('/mnt/iscsi/WIJ').used) + ", free: "+bytes2human(psutil.disk_usage('/mnt/iscsi/WIJ').free) + ", percent: "+str(psutil.disk_usage('/mnt/iscsi/WIJ').percent) + "%"
	#----------------------------------------------

	#----------------- CPU ------------------------
	zvCpuUsgL = psutil.cpu_percent(interval=1, percpu=True)
	zvCpuUsg = ''
	zvCpuCnt = 1
	for i in zvCpuUsgL:
		if zvCpuCnt % 5 == 0:
			zvCpuUsg = zvCpuUsg + 'Cpu' + str(zvCpuCnt) + ' = ' + str(i) + '%\n'
			zvCpuCnt = zvCpuCnt + 1
		else:
			zvCpuUsg = zvCpuUsg + 'Cpu' + str(zvCpuCnt) + ' = ' + str(i) + '% ,'
			zvCpuCnt = zvCpuCnt + 1
	#----------------------------------------------

	#---------------- load avg ---------------------
	zvLodAvg = psutil.getloadavg()
	zvLodAvg = str(zvLodAvg)

	zvLodAvg1 = zvLodAvg.split("(")[1]
	zvLodAvg1 = zvLodAvg1.split(",")[0]

	zvLodAvg5 = zvLodAvg.split(", ")[1]
	zvLodAvg5 = zvLodAvg5.split(",")[0]

	zvLodAvg15 = zvLodAvg.split(", ")[2]
	zvLodAvg15 = zvLodAvg15.split(")")[0]

	zvLodAvg = """
	Load Avg:
	last 1  min = """ + zvLodAvg1 + """
	last 5  min = """ + zvLodAvg5 + """
	last 15 min = """ + zvLodAvg15 + ""
	#-----------------------------------------------

	#--------------- memory ------------------------
	zvMem = psutil.virtual_memory()

	zvMemTmp = ""
	zvMemTmp = zvMemTmp + "Total = " + bytes2human(zvMem.total) + "\n"
	zvMemTmp = zvMemTmp + "Available = " + bytes2human(zvMem.available) + "\n"
	zvMemTmp = zvMemTmp + "Percent = " + bytes2human(zvMem.percent) + "\n"
	zvMemTmp = zvMemTmp + "Used = " + bytes2human(zvMem.used) + "\n"
	zvMemTmp = zvMemTmp + "Free = " + bytes2human(zvMem.free) + "\n"
	zvMemTmp = zvMemTmp + "Active = " + bytes2human(zvMem.active) + "\n"
	zvMemTmp = zvMemTmp + "Inactive = " + bytes2human(zvMem.inactive) + "\n"
	zvMemTmp = zvMemTmp + "Buffers = " + bytes2human(zvMem.buffers) + "\n"
	zvMemTmp = zvMemTmp + "Cached = " + bytes2human(zvMem.cached) + "\n"
	zvMemTmp = zvMemTmp + "Shared = " + bytes2human(zvMem.shared) + "\n"
	zvMemTmp = zvMemTmp + "Slab = " + bytes2human(zvMem.slab) + "\n"

	zvMem = zvMemTmp
	#-----------------------------------------------

	#---------------- network -----------------------
	zvNet = psutil.net_if_stats()
	zvNet = str(zvNet)
	zvNet = zvNet.split("{")[1]
	zvNet = zvNet.split("}")[0]

	zvNet1 = zvNet.split(r"'eth1':")[0]
	zvNet2 = r"'eth1':" + zvNet.split(r"'eth1':")[1]

	zvNet = zvNet1 + "\n" + zvNet2
	#------------------------------------------------

	#==========================================================================

	#======== cache check ========================================
	subprocess.check_call(["/root/PySysAdmin/PyShell/PyShell.sh"])

	# HC
	with open('/root/PySysAdmin/temp/TmpCmdHc.txt', 'r') as file:
		zvTxt = file.read()
		zvTxt = str(zvTxt)
		zvTxt = zvTxt.split('Blk')[1]
		zvTxt = zvTxt.split('%SYS>')[0]
		zvTxt = "HC:" + "\n" + zvTxt
	#--------------------------------------------------------------------

	# Rm
	with open('/root/PySysAdmin/temp/TmpCmdRm.txt', 'r') as file:
		zvRmTxt = file.read()
		zvRmTxt = str(zvRmTxt)
		zvRmTxt = zvRmTxt.split('Blk')[1]
		zvRmTxt = zvRmTxt.split('%SYS>')[0]
		zvRmTxt = "RM:" + "\n" + zvRmTxt

	#List
	with open('/root/PySysAdmin/temp/TmpCacheLst.txt', 'r') as file:
		zvLstTxt = file.read()
	#--------------------------------------------------------------------

	#------ Error Logs ---------------------------
	zvErr = ""
	with open('/root/PySysAdmin/temp/TmpCmd.txt', 'r') as file:
		zvErr = file.read()
	#------------------------------------------------

	zvReport = """\
	Subject: ArtivaProd System Check

	   ----==={ OS }===----


	""" 'Disk:' + "\n\n" + zvDf + "\n" + zvLodAvg + "\n\n" + 'CPU Use:\n' + zvCpuUsg + "\n\n" + "Memory:" + "\n" + zvMem + "\n" + "Network:" + "\n" + zvNet +"""
	_________________________________________________________
	_________________________________________________________

	   ----==={ Cache }===----


	""" + str(zvTxt) + "\n" + str(zvRmTxt) + """
	_________________________________________________________
	_________________________________________________________

	ERRORS:

	""" + zvErr

	zvEmailList = ['name@email.com']

	for x in zvEmailList:
		SendEmail(x,zvReport)
#======================================================================
#====================================================================================================


# mon
schedule.every().monday.at("07:30").do(SysAdm)
schedule.every().monday.at("11:30").do(SysAdm)
schedule.every().monday.at("16:30").do(SysAdm)

# tue
schedule.every().tuesday.at("07:30").do(SysAdm)
schedule.every().tuesday.at("11:30").do(SysAdm)
schedule.every().tuesday.at("16:30").do(SysAdm)

# wed
schedule.every().wednesday.at("07:30").do(SysAdm)
schedule.every().wednesday.at("11:30").do(SysAdm)
schedule.every().wednesday.at("16:30").do(SysAdm)

# thu
schedule.every().thursday.at("07:30").do(SysAdm)
schedule.every().thursday.at("11:30").do(SysAdm)
schedule.every().thursday.at("16:30").do(SysAdm)

# fri
schedule.every().friday.at("07:30").do(SysAdm)
schedule.every().friday.at("11:30").do(SysAdm)
schedule.every().friday.at("16:30").do(SysAdm)

#-------------------------------------------------------------

while True:
    schedule.run_pending()
    time.sleep(1)
