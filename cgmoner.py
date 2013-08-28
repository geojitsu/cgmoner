#!/usr/bin/env python

from cgminerpc import CgminerClient
import smtplib
import socket

phoneList    = ['2025315762']#,'3042681600']
avalons      = [{"host":"alpha","ip":"10.38.95.50"},{"host":"beta","ip":"10.38.95.51"},{"host":"gamma","ip":"10.38.95.52"}]
criticalhash = 50000
    
def txtSend(siteID, phoner):
    server    = smtplib.SMTP( "smtp.gmail.com", 587 )
    server.starttls()
    #server.login( username, password )
    server.sendmail( 'AVALON TEST', phoner + '@txt.att.net', siteID )




for avalon in avalons:

    MHs = MHsAVG = temps =  elapsed = None
    HWErr = 0.0
    client = CgminerClient()

    try:
        json_data          = client.command(avalon['ip'], 4028, 'devs') 
        MHs, MHsAVG, temps = tuple([json_data["DEVS"][0]["MHS 5s"], json_data["DEVS"][0]["MHS av"],\
                             json_data["DEVS"][0]["Temperature"]])
        json_data          = client.command(avalon['ip'], 4028, 'summary')
        elapsed, HWErr     = tuple([json_data["SUMMARY"][0]["Elapsed"], json_data["SUMMARY"][0]['Hardware Errors']])
        json_data          = client.command(avalon['ip'], 4028, 'pools')
        diff1Shares        = json_data["POOLS"][0]["Diff1 Shares"]
        
        # Error rate calulation - 100 * HW / (diff1shares + HW)
        HWErr              = float((100 * HWErr))/float((diff1Shares + HWErr))
        
        #print "HW ERRROR " + str(HWErr)
        #print "Diff1Shares " + str(diff1Shares)
        #print "HW ERROR RATE %.3f" % (float((100 * HWErr))/float((diff1Shares + HWErr)))
    
        if elapsed > 3600:
            ehour = elapsed / 3600
            emins = ((elapsed % 3600) / 60)
        else:
            ehour = 0
            emins = elapsed / 60
            
        elapsed = str(ehour) + 'h ' + str(emins) + 'm'
    except Exception, e:
        print '[-] ER ROR: %s' % e

    for phone in phoneList:
        print('\tAvalon %s Statistics' % avalon['host'].upper())
        if MHs != None and MHs < criticalhash:
            #txtSend('AVALON MH/s: ' + MHs, phone)
            print('Health Critical!')
            print('Current Hash Rate - %s:\t%s\n' % (avalon['host'].upper(), MHs))
        else:
            print('Current Hash Rate:\t[[ %s ]]' % MHs)
            print('Current Mean Rate:\t[  %s  ]' % MHsAVG)
            print(unicode('Current Stats:\t\tT:%s C    E:%.2f%%') % (temps, HWErr))
            print('\t\t\tD:%s\n') % elapsed