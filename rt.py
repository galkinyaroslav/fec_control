# -*- coding: utf-8 -*-
#                           08 Dec 2022
vers = '08dec22;  26jul23, 28jul23'
#
import os,sys,re,telnetlib
import time
# ASCII=== AZaz~.===       space=20 ~=0x7E 0-9=0x30-0x39 dot=0x2E !=0x21 ?=0x3f  A=0x41, z=0x7A

host = "192.168.1.15";port = 30
host = "192.168.1.235";port = 30
#host = "192.168.1.37";port = 30
#host = "192.168.0.231";port = 30
#host = "192.168.0.195";port = 30

##host = "192.168.0.202";port = 30; # 20 Sept 2022

# host = "192.168.1.9";port = 30; # rcu-64 SV 19/09/2022

#host = "192.168.1.13";port = 30

def oscmd(cmd): pro = os.popen(cmd); ret=pro.read(); pro.close; return ret;

def op():
	global telnet
	telnet = telnetlib.Telnet(); telnet.open(host, port)
	out = telnet.read_until("return:", 105); print out;
	out = telnet.read_eager();out = telnet.read_eager();
	#
	ui();

def q(): telnet.write('!\r\n'); #def q(): telnet.write('q\r\n');

def pps(s='sss'):s='\033\[37;1;42m ' + s + '\033\[0m ';print s
def pp(str,f='w',b='d'):
    '''
    Печать символа или строки в цвете без перевода строки.
    Например: pp('111')               - белый на черном
              pp('111',f='y')         - желтый на черном
              pp('111',f='y',b='r')   - желтый на красном
    '''
    xfg={'d':'30','r':'31','g':'32','y':'33','b':'34','m':'35','c':'36','w':'37'}
    xbg={'d':'40','r':'41','g':'42','y':'43','b':'44','m':'45','c':'46','w':'47'}
    cstr="\033["+xfg[f]+';1;'+xbg[b]+'m'+str+"\033[0m"
    sys.stdout.write(cstr)

def h():
	help='''
К О М А Н Д Ы   UI   П И Т О Н А	
	In []:	op  - открыть соединение с китом ( при 1-м запуске скрипта ./ipc или после q )
	              и войти  в UI приложения
	        q   -   выйти из UI приложения и закрыть соединение с китом  ; x - выход из ui
	        
		Вспомогательные команды UI питона
		
		w 'command'  команда Ниосу выполнить команду 'command' ,   НАПРИМЕР  w 'rsa 7 1'
		ui и x -  вход и выход в/из UI приложени(е/я) для выполнения некоторых команд из UI питона
		          ( например, команды w  )
		clo - close connection         
		 
К О М А Н Д Ы    UI   П Р И Л О Ж Е Н И Я  RT.PY
_________________________________________________
    => <команда>
        rr                 - запуск rorun (  ReadOut на 999999 событий )	
	    trstat             - прочитать статус HSSI линка , ID карты и RCU - CID и RID
	    car?               - выбранная карта и её статус
	    car N              - выбрать карту N
	    scpll0 или scpll1  - получить скан по сдвигу фазы PLL ( напр. 0x001fc1fc или 0x003fd3f0 )
	    setpll sh0 sh1     - установить сдвиги фаз
	    getffw            - прием N тригеров с записью в файл	events.lst
	    tts n              - цикл n раз <cff,soft,rff>
	    tth n              - цикл n раз <cff,hard,rff>
	    rmsk         -  read  content of RCU Veto-for-Read register
		wmsk Data    -  write Data to RCU Veto-for-Read register
		rsa Reg      - read  Sampa register
		wsa Reg Data - write Sampa register
		pow Ncard    - power ON SAMPAs 
		ini Ncard    - initialize card Ncard 
		ini.<файл>   - инициализировать данными из файла  ini('ini.txt')
		ini.         - ini.txt по умолчанию
		adcs         - read 16 slow control values 
		adcd         - VAT мониторинг
		rff, cff, soft, scpll0, adj0   
	'''
	print help
def clo(): telnet.close();

def pow(k=2):
	powst = ttok('rxv 0x904 %d'%k).split()[1];time.sleep(0.5);
	if powst=='0x40000003':
		pp( '===> SAMPAS power status was = %s'%powst, b='b')
		#print 'SAMPAS power status was = %s'%powst;
		print '';
		return;
	if powst=='0x40000001' or powst=='0x40000002' : 
		ttok('wxv 0x904 0x3 %d'%k); time.sleep(0.5);
		pp('===> New SAMPAS power status = %s'%powst,b='y');
		return;
	ttok('wxv 0x904 0x1 %d'%k);  time.sleep(1.3); ttok('wxv 0x904 0x3 %d'%k); time.sleep(0.5);
	pp('===> New SAMPAS power status = %s'%powst,b='g');
	#print 'New SAMPAS power status = %s'%powst;
#	
def ini(k=1,fini=''):
	pow(k);
	if fini=='':
		ttok('wsa 13 30 %d'%k); time.sleep(0.3);  ttok('wsa 77 30 %d'%k); time.sleep(0.3);  # VACFG
		ttok('wsa 7 30 %d'%k);   time.sleep(0.3); ttok('wsa 8 0 %d'%k);  time.sleep(0.3);   # TWLen.0
		ttok('wsa 71 30 %d'%k); time.sleep(0.3);  ttok('wsa 72 0 %d'%k); time.sleep(0.3);   # TWLen.1
		ttok('wsa 9 0 %d'%k);   time.sleep(0.3);  ttok('wsa 10 0 %d'%k); time.sleep(0.3);
		ttok('wsa 73 0 %d'%k);  time.sleep(0.3);  ttok('wsa 74 0 %d'%k); time.sleep(0.3);   #AQStart
		ttok('wsa 11 30 %d'%k); time.sleep(0.3);  ttok('wsa 12 0 %d'%k); time.sleep(0.3);
		ttok('wsa 75 30 %d'%k); time.sleep(0.3);  time.sleep(0.3); ttok('wsa 76 0 %d'%k);  #AQStop
		time.sleep(0.3);
		#w('rsa 7');
		ttok('wxv 0x944 0x6600 %d'%k);   #        # wxv   0x944 0x6600 0;
		time.sleep(0.3);
		ttok('kmsffw 0x0 %d'%k);time.sleep(0.5); ttok('kmslkw 0xff %d'%k); # set k 0;kmsffw 0x0 $k; kmslkw 0x0 $k;
		time.sleep(0.5);
		ttok('getsetpll %d'%k );
		return
		#
	if fini=='ini.txt':
		print " Load from file ..."
		scri = oscmd("cat ini.txt");lscri=scri.splitlines();
		for l in lscri: # цикл по строкам скрипта
			if l[0]=='#':continue
			print l[0:len(l)-2]
			ttok(l);#w(';'+l+'\n');
			#print l 
		#print scri	
def ifcfg():
	rnam=['VAcfg', 'TWlen','TWlen2', 'AQStart','AQStart2', 'AQStop','AQStop2',]
	rlis=[  13 ,     7,8,             9,10,                 11,12 ]
	print '_______________________________________'
	for j in range( len(rlis) ):
		r=w('rsa %d'%rlis[j],0); time.sleep(0.3)
		print '%s %s (%d)'%(rnam[j],r[0:-2],rlis[j]) 
	print '_______________________________________'
	for j in range( len(rlis) ):
		r=w('rsa %d'%(rlis[j]+64),0); time.sleep(0.3)
		print '%s %s (%d)'%(rnam[j],r[0:-2],(rlis[j]+64)) 
	print '_______________________________________'			
#
def getcars():
	tab = oscmd("cat cars.tab"); ltab=tab.splitlines();
	print ltab
	for l in ltab: # цикл по строкам
		if l[0]=='#':continue
		num = l.split(','); print l,"\n",num,"\n\n"
		if len(num)<>4 :print "Error ! len=%d"%len(num);continue
		print 'Card %s  Link %s  PLLsh %s %s'%(num[0],num[1],num[2],num[3])
#		
def regs():w('regs');
##def ttok():w('ttok 1234;55');
# Запрос серверу обработать список выражений и вернуть результат
def ttok(s,pr=1):
	res=w('ttok '+s,pr);
	print '==> ttok %s done'%s
	return res

def ui():	
	s=''; coms=['rff','cff','soft','car?','car ','adj0','adj1','tts','hard','tth','cffa' ,'cffall' ,'rffa' ,'kmsff','kmslk','trstat' ];
	testcom = ['ffzz','ffdd','scpll0','rpllsh','wrpll','pllsh0','ffhidd','scpll1','shpll0','shpll1' ,'setpll','rddk','rddall','getdd' ,'getff'];
	testcom2 = ['carn','jtag0','jtag1','getffw ','getffw','trace1','trace0','ncar','vers','profirsa','xrsa','getpll','getsetpll','initk','wmma','rmma']
	coms = coms +testcom+testcom2;
	while s<>'q':
		s= raw_input('(v.%s) ==>'%vers);
		#print 'ok. got <%s>'%s[0:4]
		# Если первое слово - команда из 3х или 4х знаков, то будем разбирать выражение
		#
		if s[0:5]=='carn ':
			oscmd('echo '+'%d'%int(s[5:])+'>cardname.txt');
			cn=oscmd('cat cardname.txt');print "Current card n=%d"%int(cn);continue
		#
		if s[0:4]=='car ':
			ttok(';'+s+';') ; ttok(';'+'trstat'+';') ;continue
		if s[0:5]=='ncar ':
			ttok(';'+s+';') ; ttok(';'+'trstat'+';') ;continue
		if s=='car?':
			ttok(';'+s+';') ; ttok(';'+'trstat'+';') ;continue						
		#
		if s=='getdd':  ttok(';'+s+';'); getdd() ;continue
		if s=='getff':  ttok(';'+s+';'); getff() ;continue
		if s=='getffw': max=10; print "getffw start";    getffw(max);print "getffw done";continue;
		# GETFFW N
		if s[0:7]=="getffw ":print "getffw N started ...";com=s.split(' ');max=int(com[1]);  getffw(max);continue;		
		
		if s=='jtag0':  ttok(';'+s+';') ;continue 
		if s=='jtag1':  ttok(';'+s+';') ;continue
		if s=='trace0':  ttok(';'+s+';') ;continue 
		if s=='trace1':  ttok(';'+s+';') ;continue
		if s=='profirsa':  ttok(';'+s+';') ;continue
		if s[0:5]=='xrsa ':  ttok(';'+s+';') ;continue
		if s=='vers':  ttok(';'+s+';') ;continue
		if s=='op':     op() ;continue
		# Исполняются как выражения внесенные в список  coms команды
		#
		if s=='rr':rorun(99999999);continue
		if (len(s)==6)and(s[0:6] in coms)    :ttok(';'+s+';');continue
		if (len(s)==5)and(s[0:5] in coms)    :ttok(';'+s+';');continue
		if (len(s)==4)and(s[0:4] in coms)    :ttok(';'+s+';');continue
		if (len(s)==3)and(s[0:3] in coms)    :ttok(';'+s+';');continue
		#
		if (s[0:3] in coms )or( s[0:4] in coms)or( s[0:6] in coms)or( s[0:5] in coms)  :  ttok(';'+s+';');continue
		if (s[0:3] in coms )or( s[0:4] in coms)or( s[0:6] in coms)or( s[0:5] in coms)  :  ttok(';'+s+';');continue		
		#
		if s[0:2]=="w.": w(s[2:]+'.');continue
		#
		#if s[0:4]=="rxv ": w(s+'.'); continue
		if s[0:4]=="rxv ": ttok(s+'.'); continue
		if s[0:4]=="wxv ": ttok(s+'.'); continue
		#
		# ? if s[0:4]=="wxv ": w(s+'.'); continue
		if s[0:4]=="rsa ": w('ttok '+s+'.'); continue
		# ? if s[0:4]=="wsa ": w(s);     continue
		if s[0:4]=="wsa ": w('ttok '+s+'.');     continue
		
		
		#
		if s[0:4]=="ini ": Ncar=int(s[4:]); ini( int(s[4:])); continue
		if s[0:5]=="ifcfg": ifcfg();     continue
		#
		if s[0:5]=="rmma ": w(s+'.'); continue
		if s[0:5]=="wmma ": w(s);     continue
		#
		if s[0:4]=="rmsk": w(s);     continue
		if s[0:5]=="test ": w(s);     continue
		if s[0:7]=="wmsk 0x": w(s);  continue
		if s=="regs":regs();continue
		if s=="adcs":adcs();continue;
		if s[0:5]=="adcd ":com=s.split(' ');max=int(com[1]);  adcd(max);continue;	
		if s=="adcd":adcd(3);continue;
		if s=="adc":adc();continue

				
		#
		if s[0:4]=="pow ":pow(int(s[4:])); continue
		if s=="ini": ini(); continue
		if s=="ini.":ini('ini.txt');continue
		#
		if s[0:4]=="soft":ttok("wsa 14 1 0");ttok("wsa 78 1 0");   continue
		#
		if s[0:4]=="ttok":ttok(s[4:]);continue
		# разбор выражения , если в начале <;>
		if s[0:1]==";":ttok(s[1:]);continue
		if s=="h" or s=='??' or s=='': h() ;continue
		if s=='?' : print ' %s %s'%(coms,testcom);continue
		if s=="q": q();clo();break;
		if s=="e": q();break;
		if s=="x": break;
		if s=="re": re();continue
		#if s=="rff" or s=="cff" or s=="soft" or s=="car?" or len(s)==s.split(';')[0]       :ttok(';'+s+';');continue
		#
		print '  Got <%s>. Bad.  Good commands : '%s; h()
		print ' %s %s'%(coms,testcom)

def w(dd='2',pr=1):
	if pr==1:print '===> <%s>'%dd
	telnet.write('%s\r\n'%dd); oscmd('sleep 0.3'); #oscmd('sleep 1');
	res = ''; oo=telnet.read_eager();
	if len(oo)>0:
		res = oo
		if pr==1: print oo,   #if len(oo)>0:print len(oo),"<",oo,">",
	oo=telnet.read_eager(); 
	if len(oo)>0:
		res = res + oo
		if pr==1: print oo,  #if len(oo)>0:print len(oo),"<",oo,">",
	oo=telnet.read_eager();
	if len(oo)>0:
		res = res + oo
		if pr==1: print oo,
	return res	
#
def wr(k=0):telnet.write('ttok ;getdd %d;\r\n'%k);
## ok def ru(to=105):out = telnet.read_until("\03", to); return out; # print out;
#
# wr();oo=ru(5);o=oo.split(',');print len(o),' ',o[0],' ... ',o[399]
def ru(to=105):out = telnet.read_until("5555aaaa", to); return out; # print out;
	#if re()<>0 :re();
	#out = telnet.read_until("\n", 105); print out;
	#out = telnet.read_until("\03", 105); print out;

def getdd():
	s='';
	for j in range(100):
		oo=telnet.read_eager();
		if len(oo)>0:s=s+oo; print len(oo),"<",oo,">",;
		if len(oo)==0:break;
	print "\n\n";print s;	
	return
def getff():
	wr(0);oo=ru(5);o1=oo.split(','); wr(1);oo=ru(5);o2=oo.split(',');
	print o1;print o2;
	'''
	oo=telnet.read_until('\03');print oo;return
	s='';
	for j in range(100):
		oo=telnet.read_eager();
		if len(oo)>0:s=s+oo; print len(oo),"<",oo,">",;
		if len(oo)==0:break;
	print "\n\n";print s;'''	
	return
def wrEvent(s='123'):
	fo=open('event.txt','w');fo.write(s);fo.close();
def wrList(l=[]):
	s='';
	for j in xrange(len(l)):
		s = s + ' 0x%s'%l[j]
	fo=open('event.lst','w');fo.write(s);fo.close();	
#                  				
def getffn(n=1):
	for j in range(n):
		ttok(";tth 1;");
		wr(0);oo1=ru(5);o1=oo1.split(','); wr(1);oo2=ru(5);o2=oo2.split(',');
		if j==j:
			#print o1;print o2; # wrEvent(oo1+oo2);
			#oo12 =oo1[1:400]+oo2[1:400]; wrEvent(oo12); print oo12;	
			o12 =o1[1:401]+o2[1:(768-400+1)];
			wrList(o12);   # wrEvent(o12);
			print o12;
			print ' len = ',len(o12)	
	return
#
def carfil(cn='',fn=0):
	global carN; global filN;
	if cn=='' and fn==0:
		carN='286';oscmd('echo '+carN+'>cardname.txt');
		fn=1;oscmd('echo '+'\"'+"%d"%fn+'\"'  + '>filenum.txt');
	return (carN,filN)
def filn():
	return oscmd('cat filenum.txt')
def carn(): return oscmd('cat cardname.txt');		
#                GETFFW N  - прием N тригеров с записью в файл	events.lst
#                            теперь и копия в /tmp/event.txt
global ddmon; ddmon  = '/home/serg/pyt/tmp';
def wfmon(ss,ff):
	global ddmon; fo=open('%s/%s'%(ddmon,ff),'w');fo.write(ss);fo.close();
	#print '<wfmon %s %s> done'%(ss[0:50],ff)
	
def rfmon(ff):global ddmon; fi=open('%s/%s'%(ddmon,ff),'r');s=fi.readline();return s;
def rereq():s=rfmon('evereq.txt');return s;
def werdy(dd):wfmon(dd,'everdy.txt');

def nostop():oscmd('echo ".">toConsole.txt');return
def ifstop():
	 if oscmd('cat toConsole.txt')=='stop\n':return 1;
	 return 0;

def rr(n=1):rorun(n);
def rorun(n=2):
	nostop();
	for j in xrange(1,n):
		ttok(";tth 1;");
		wr(0);oo1=ru(5);o1=oo1.split(','); wr(1);oo2=ru(5);o2=oo2.split(',');
		o12 =o1[1:401]+o2[1:(768-400+1)]; s='';
		for jj in xrange(12*16*4):s = s + ' 0x%s'%o12[jj]
		s=s+'\n';
		if rereq()=='yes':
			wfmon(s,'event.txt');
			wfmon('%d'%j,'everdy.txt'); print 'Event %d written for mon'%j
			wfmon('no','evereq.txt')
		oscmd('sleep 2');
		if ifstop()==1:print 'Stop detected';  break
	#	
	print '<rorun> done.'	
	#return s[0:100]
	
def getffw(n=1):
	global carN; global filN; filN=int(filn())+1;
	ddmon = 'home/serg/pyt/tmp' 
	print '\nRun file %d'%filN;
	#oscmd('echo 00 >/home/serg/pyt/tmp/everdy.txt'); x = oscmd('cat /home/serg/pyt/tmp/everdy.txt');
	#print ' See /home/serg/tmp/everdy.txt :<%s> '%x;
	fo=open('events.lst','w'); oscmd('echo ".">toConsole.txt');
	for j in xrange(1,n+1):
		#oscmd('echo 00 >/home/serg/pyt/tmp/everdy.txt');
		ttok(";tth 1;");
		wr(0);oo1=ru(5);o1=oo1.split(','); wr(1);oo2=ru(5);o2=oo2.split(',');
		# WRITE DATA TO FILE
		if j==j:	
			o12 =o1[1:401]+o2[1:(768-400+1)];
			s='';
			for jj in xrange(12*16*4):s = s + ' 0x%s'%o12[jj]
			s=s+'\n';   fo.write(s);
			# data for monitoring
			fe=open('/tmp/event.txt','w');fe.write(s);fe.close();
			#wfmon(s,'event.txt');
			#oscmd('echo 0%d>/home/serg/pyt/tmp/everdy.txt'%j); 
			#
		ifstop = oscmd('cat toConsole.txt'); 
		if ifstop=='stop\n':print "stop detected";break
		oscmd('sleep 1');	
	fo.close()
	fn = '%d-%d.txt'%(int(carn()),filN)
	oscmd('cp events.lst ./runs/%s'%fn);
	#x = oscmd('cat /home/serg/pyt/tmp/everdy.txt');
	#print ' See /home/serg/tmp/everdy.txt :<%s> '%x;
	#oscmd('cp events.lst /tmp/event.txt');
	#oscmd('echo 0%d>/tmp/everdy.txt'%n);			
	return
	
def adc(pr=1):res=ttok('adc;',pr); return res;
def adcs(n=10,pr=0):
	for j in range(n):
		res=adc(pr); print 's: ',res[0:len(res)-2];
		oscmd('sleep 0.1');
		
#                       ADCD  - VAT мониторинг
global T,v1	;	 	 
def adcd(n=10,pr=0):
	oscmd('echo ".">toConsole.txt');
	#       0       1     2       3      4      5      6      7      8     9      10     11     12     13     14     15
	#    |......|......|......|......|......|......|......|......|......|......|......|......|......|......|......|......|......|
	hd = "\n    |  T    1.7Vi  1.1Vc5 1.25Vd mA2 S0 mA1 S0 1.1Vr  1.25Va mA0 S0  Tsam  1.25Va mA3 S1 1.1Vr  mA4 S1 mA5 S1 1.25Va \n"
	global T,Ts;
	oscmd("echo "+ '\"' + "%s"%hd[8:] + '\"' + ">VAT.txt");
	for j in range(n):
		if j/20*20==j:
			ifstop = oscmd('cat toConsole.txt'); 
			if ifstop=='stop\n':print "stop detected";break
			#car=ttok('car?;',0);lcar=car.split(' '); print lcar[0]+lcar[1],;
			pp(hd); #print hd
		res=adc(pr); ar=res.split(',');
		if len(ar)<16:print "Wrong length %d"%len(ar);break 
		if 0==0:
			r = 0.61*int(ar[0],16);  a= -1.064200E-09; b= -5.759725E-06; c= -1.789883E-01; d= 2.048570E+02; #set v int*0.61; 
			rs= 0.61*int(ar[9],16);
			T = a*r**3+b*r**2+c*r+d; sT="%2.1f"%T;  Ts = a*rs**3+b*rs**2+c*rs+d; sTs="%2.1f"%Ts;  
			v1=0.61*int(ar[1],16);  sv1="%2.1f"%v1;
			vn=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15];svn=vn;
			for k in [1,2,3,4,5,6,7,8,10,11,12,13,14,15]:
				vn[k]=0.61*int(ar[k],16);
				svn[k]="%2.1f"%vn[k];
			#            0    1  2  3   4  5  6  7  8    9
			print '      %s  %s %s %s  %s  %s %s %s  %s  %s  %s %s  %s %s  %s  %s '%\
			(sT,svn[1],svn[2],svn[3],svn[4],svn[5],svn[6],svn[7],svn[8],sTs,svn[10],svn[11],svn[12],svn[13],svn[14],svn[15] );
			sout = '      %s  %s %s %s  %s  %s %s %s  %s  %s  %s %s  %s %s  %s  %s '%\
			(sT,svn[1],svn[2],svn[3],svn[4],svn[5],svn[6],svn[7],svn[8],sTs,svn[10],svn[11],svn[12],svn[13],svn[14],svn[15] );
			oscmd("echo " + '\"%s\"'%sout + ">>VAT.txt");	
		#print 's: ',res[0:len(res)-2];
		#
		oscmd('sleep 0.1');
		 
def r(ret="\n"):
	out = telnet.read_until("%s"%ret, 105); print out;
	#out = telnet.read_until("%s"%ret, 105); print out;

def re():
	oo=telnet.read_eager();
	if len(oo)>0: print len(oo),"<",oo,">",; 
	return len(oo);

def qq(): telnet.write('quit\r\n');

carN = 286; filN = 0;
h();
pwd=oscmd('pwd'); welcomtx = "Start rt.py from "+pwd+'(vers %s)'%vers;#print "Start rt.py from "+pwd+'(vers %s)'%vers;
pp(welcomtx,f='g',b='d')
#ui();

'''

'''

