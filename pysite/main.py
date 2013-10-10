from django.db import models
from django.http import HttpResponse  
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect 
from django.core.urlresolvers import reverse 
from django.conf import settings

from forms import FormSensor
from forms import FormTarget
from forms import FormBackground
from forms import MessageForm
from forms import MessageForm2
from forms import FormWavelength_chosen
from forms import FormWavelength_to_choose
from forms import FormScene
from forms import FormCustomize
from forms import FormBKG_chosen
from forms import FormBKG_tochoose
from forms import FormRadianceChoice
from forms import FormSNRChoice
from forms import FormFinalSubmition
from forms import FormBkgName

from ctypes import *
import Image
import struct
import string
import matplotlib.pyplot as plt1
import matplotlib.pyplot as plt2
import matplotlib.pyplot as plt3
import math
import os
import re
import random

                
def startpage(request):
    if request.method == 'POST': # click submit on page startpage
        form = MessageForm2(request.POST) 
        if form.is_valid(): 
            pfiles = form.cleaned_data['pfile_selection'] 
#            f = open("C:\Django\pysite\pfilename.txt", "w")
#            f.write(pfiles)
#            f.close()            
            if pfiles != 'Customized.fcm': # if select predefined page
#############
#############parse corresponding fcm, read corresponding sensor WV file
############
#                data = open('C:/FASSP_EMMETT/v2.4/pfiles/'+pfiles).read()
#                open('C:/FASSP_EMMETT/v2.4/pfiles/customized.fcm', 'wb').write(data)
#                Sensorchosen = findsensorname('customized.fcm','C:/FASSP_EMMETT/v2.4/pfiles/')
                
############ write wavelength file
#                parsesensor(Sensorchosen,'C:/FASSP_EMMETT/v2.4/sens/')
                
#                parseFCM_genPrefill('customized.fcm','C:/FASSP_EMMETT/v2.4/pfiles/') 
                #os.system("C:/Django/pysite/pre.exe")
#                dict = parseFCM_genPrefill('customized.fcm','C:/FASSP_EMMETT/v2.4/pfiles/')
                dict = parseFCM_genPrefill(pfiles,'C:/FASSP_EMMETT/v2.4/pfiles/')                
                
                form = MessageForm()
###############read corresponding WV file, according to sensor name
                formtochoose = FormWavelength_to_choose(SensorName = dict['Sensor Name'])
                formchosen = FormWavelength_chosen()
               
                formtarget = FormTarget(
                TargetName = dict['Target Name'],
                TargetScale = dict['Target Scale'],
                TargetPercentage = dict['Target Percentage'],
                BkgName = dict['Bkg Name'])
                
                formscene = FormScene(
                AtmosphericHaze = dict['Atmospheric Haze'],
                GroundAltitude = dict['Ground Altitude'],
                SolarAngle = dict['Solar Angle'],
                AtmosphericModel = dict['Atmospheric Model'],
                CloudIndex = dict['Cloud Index'],
                MeteorologicalRange = dict['Meteorological Range'])
           
                formsensor = FormSensor(        
                SensorName = dict['Sensor Name'],
                NoiseFactor = dict['Noise Factor'],
                GainFactor = dict['Gain Factor'],
                RltvCalibrationError = dict['Rltv Calibration Error'],
                IntegrationTime = dict['Integration Time'],
                SensorAltitude = dict['Sensor Altitude'])
         
                formbackground = FormBackground(
                BkgName = dict['Bkg Name'],
                BkgName2 = dict['Bkg Name'],
                BkgScale = dict['Bkg Scale'],
                BkgPercentage = dict['Bkg Percentage'])
               
                
#                data = open('C:/FASSP_EMMETT/v2.4/pfiles/'+pfiles).read()
#                f = open('C:/FASSP_EMMETT/v2.4/pfiles/customized.fcm', 'wb')
 #               f.write(data) 
 #               f.close()
            
                return render_to_response('paraselection.html',
                {'form': form,'formtochoose': formtochoose,'formchosen': formchosen,'FormTarget': formtarget
                          ,'FormScene': formscene,'FormBackground': formbackground,'FormSensor': formsensor})
            else: # if select customized page
                return render_to_response('customize.html',
                {'FormCustomize': FormCustomize, 'FormBKG_chosen': FormBKG_chosen,'FormBKG_tochoose': FormBKG_tochoose})
 #           {'form': form})                    
 #raise Exception(formto\choose)                          
    else: 
        form = MessageForm2()

    return render_to_response('startpage.html',{'form': form})
    
    
def customize(request):
#    raise Exception(request)   
    if request.method == 'POST':  # click submit on customize page
        formcustomize = FormCustomize(request.POST) 
        if formcustomize.is_valid(): 
            BKGchosen  = formcustomize.cleaned_data['hiddentxt']
            BKGcount = BKGchosen.count(',')
            BKGchosen = BKGchosen[:-1]
            BKGperc = '100,' + (BKGcount-1) * '0,'
            BKGperc = BKGperc[:-1]
            Sensorchosen = formcustomize.cleaned_data['sensor_selection']
            Targetchosen = formcustomize.cleaned_data['target_selection']
            
            #write customized.fcm from template.fcm using data
#            data = open('C:/FASSP_EMMETT/v2.4/pfiles/template.fcm').read()
#            data = re.sub('backnamehere',BKGchosen, data) 
#            data = re.sub('sensornamehere',Sensorchosen, data) 
#            data = re.sub('targetnamehere',Targetchosen, data) 
#            data = re.sub('backperchere',BKGperc, data) 
#            data = re.sub('backnumhere',str(BKGcount), data)         
#            open('C:/FASSP_EMMETT/v2.4/pfiles/customized.fcm', 'wb').write(data)
#raise Exception(BKGperc)         
#############read corresponding wavelength.txt according to sensor name
#            parsesensor(Sensorchosen,'C:/FASSP_EMMETT/v2.4/sens/')
            
            dict = parseFCM_genPrefill('customized.fcm','C:/FASSP_EMMETT/v2.4/pfiles/') 
            dict['Target Name'] = Targetchosen
            dict['Sensor Name'] = Sensorchosen
            dict['Bkg Name'] = BKGchosen
            dict['Bkg Percentage'] = BKGperc
#            os.system("C:/Django/pysite/pre.exe") 
#            raise Exception(BKGchosen)               
            
            form = MessageForm()
#############read corresponding wavelength.txt according to sensor name
            formtochoose = FormWavelength_to_choose(SensorName = dict['Sensor Name'])
            formchosen = FormWavelength_chosen()
            
            formtarget = FormTarget(
            TargetName = dict['Target Name'],
            TargetScale = dict['Target Scale'],
            TargetPercentage = dict['Target Percentage'],
            BkgName = dict['Bkg Name'])
            
            formscene = FormScene(
            AtmosphericHaze = dict['Atmospheric Haze'],
            GroundAltitude = dict['Ground Altitude'],
            SolarAngle = dict['Solar Angle'],
            AtmosphericModel = dict['Atmospheric Model'],
            CloudIndex = dict['Cloud Index'],
            MeteorologicalRange = dict['Meteorological Range'])
       
            formsensor = FormSensor(        
            SensorName = dict['Sensor Name'],
            NoiseFactor = dict['Noise Factor'],
            GainFactor = dict['Gain Factor'],
            RltvCalibrationError = dict['Rltv Calibration Error'],
            IntegrationTime = dict['Integration Time'],
            SensorAltitude = dict['Sensor Altitude'])
     
            formbackground = FormBackground(
            BkgName = dict['Bkg Name'],
            BkgScale = dict['Bkg Scale'],
            BkgPercentage = dict['Bkg Percentage'])
            

#            raise Exception(Sensorchosen) 
            return render_to_response('paraselection.html',
            {'form': form,'formtochoose': formtochoose,'formchosen': formchosen,'FormTarget': formtarget
                      ,'FormScene': formscene,'FormBackground': formbackground,'FormSensor': formsensor})               
 #raise Exception(formtochoose)                          
    else:
        return render_to_response('jump.html')    
    
    
def paraselection(request):

    if request.method == 'POST': # click submit on page paraseletion:
#        raise Exception(request.POST)
        form = MessageForm(request.POST) # this form is to store the chosen wavelength, and sessionID
        formfinal = FormFinalSubmition(request.POST)     
        
        # if (form.is_valid() and formscene.is_valid() and formsensor.is_valid() 
        # and formtarget.is_valid() and formbackground.is_valid()) :
        if(form.is_valid()):
            #since I don't know how to pass a multi choice form's all options(the form wavelength chosen)
            #so I just use a hidden txt block to transfer them.
            hiddentxt  = form.cleaned_data['hiddentxt']
#            raise Exception(hiddentxt)                
            #store all chosen wavelength
            f = open("C:/Django/pysite/wchosen.txt", "w")
            for x in range(0,len(hiddentxt)):
                f.write("%s" % (hiddentxt[x]))
            f.close()

            Atmospheric_haze = request.POST['Atmospheric_haze']
            Solangle = request.POST['Solangle'] 
            Atmospheric_model = request.POST['Atmospheric_model']
            CloadIndex = request.POST['icld']
            Ground_altitude = request.POST['Ground_altitude']
            Meteorological_Range = request.POST['Mrange']
            
            Noisefac = request.POST['Noisefac'] 
            Gainfac = request.POST['Gainfac'] 
            Relcal = request.POST['Relcal'] 
            Platalt = request.POST['Platalt'] 
            Tint = request.POST['Tint'] 
            
            Targscale = request.POST['Targscale'] 
            Targperc = request.POST['Targperc'] 
            Targinback = request.POST['Targinback']
            Targinback = str(int(Targinback)+1)
            TargName = request.POST['Targname']
       
            Bkgscale = request.POST['Bkgscale'] 
            Backperc = request.POST['Backperc'] 
            Bkgname = request.POST['Bkgname2'] 
            
            while not Backperc[-1].isdigit():
                Backperc = Backperc[:-1]
#            raise Exception(Backperc)             
 #############################random number 
            session_key = str(random.random())[2:]
            request.session['session_key'] = session_key
            path = 'C:/Django/pysite/media/'+session_key+'/'
            if os.path.exists(path)==False:
                os.mkdir(path);  
                
            #modify custimized fcm file
            FCMdata = open('C:/FASSP_EMMETT/v2.4/pfiles/customized.fcm').read()
            
            FCMdata = modifyCustomFCM('ihaze', str(Atmospheric_haze), FCMdata)
            FCMdata = modifyCustomFCM('solangle', str(Solangle), FCMdata)
            FCMdata = modifyCustomFCM('gndalt', str(Ground_altitude), FCMdata) 
            FCMdata = modifyCustomFCM('model', str(Atmospheric_model), FCMdata) 
            FCMdata = modifyCustomFCM('icld', str(CloadIndex), FCMdata)  
            FCMdata = modifyCustomFCM('metrange', str(Meteorological_Range), FCMdata)              
            
            FCMdata = modifyCustomFCM('noisefac', str(Noisefac), FCMdata)
            FCMdata = modifyCustomFCM('gainfac', str(Gainfac), FCMdata)
            FCMdata = modifyCustomFCM('relcal', str(Relcal), FCMdata)        
            FCMdata = modifyCustomFCM('platalt', str(Platalt), FCMdata)
            FCMdata = modifyCustomFCM('tint', str(Tint), FCMdata)
            
            FCMdata = modifyCustomFCM('targscale', str(Targscale), FCMdata)            
            FCMdata = modifyCustomFCM('targperc', str(Targperc), FCMdata)
            FCMdata = modifyCustomFCM('targinback', str(Targinback), FCMdata)
            
            FCMdata = modifyCustomFCM('backscale', str(Bkgscale), FCMdata)
            FCMdata = modifyCustomFCM('backname', str(Bkgname), FCMdata)
            FCMdata = modifyCustomFCM('backperc', Backperc, FCMdata,1)
##########writing chosen wvlg to FCM file            
            FCMdata = modifyCustomFCM('wavelengthchosen', str(hiddentxt), FCMdata)
            open('C:/FASSP_EMMETT/v2.4/pfiles/customized.fcm', 'wb').write(FCMdata)
            

          
            
############################################################################################################
            feedback = os.system("C:/Django/pysite/working.exe")
            #give fcm file to queue, then check sessionid folder. if while here, then user quits what will happen?
############################################################################################################   
#            feedback =0;   
            if feedback == -1:
                return render_to_response('errorpage.html')           
            

            Wlnumbers = readfile('wavelength')
            wchosenlength = len(Wlnumbers)
            #read txt file generated by working.exe
            Ltnumbers = readfile('LBT')
            SNRn = readfile('SNR')
            ROC = readfile('ROC')

            showback = len(Ltnumbers)/wchosenlength-1


                
            TgtName = []
            TgtName.append(str(TargName))
            
            LTdisplay = Ltnumbers[(showback*wchosenlength):(showback*wchosenlength+wchosenlength)]    
            plt1.plot(Wlnumbers,LTdisplay)
            plt1.xlim([400, 2500]) 
            plt1.title('Scene Mean Spectral Radiance')
            plt1.legend(TgtName,prop={'size':8})
            plt1.xlabel('Wavelength(microns)')
            plt1.ylabel('Spectral Radiance(mW/cm^2-sr-um)')
            plt1.savefig("C:/Django/pysite/media/"+session_key+"/rad.png",dpi=100)
            plt1.clf()
#            im = Image.open("C:/Django/pysite/media/rad.png")
#            out = im.resize((800,600))
#            out.save('C:/Django/pysite/media/rad.png')
            

            SNRdisplay = SNRn[showback*wchosenlength:(showback*wchosenlength+wchosenlength)]
            plt2.plot(Wlnumbers,SNRdisplay)
            plt2.xlim([400, 2500]) 
            plt2.ylim([0, 110]) 
            plt2.title('Sensor Signal-to-Noise Ratio')
            plt2.legend(TgtName,prop={'size':8})
            plt2.xlabel('Wavelength(microns)')
            plt2.ylabel('Signal-to-Noise Ratio')
            plt2.savefig("C:/Django/pysite/media/"+session_key+"/snr.png",dpi=100)
            plt2.clf()
#            im = Image.open("C:/Django/pysite/media/snr.png")
#            out = im.resize((800,600))
 #           out.save('C:/Django/pysite/media/snr.png')

            Pdmin = ROC[0:7]
            Pfa = ROC[7:14]
            
            plt3.semilogx(Pfa,Pdmin)            
            plt3.plot(Pfa,Pdmin,"b")
            plt3.axis([1e-6, 1, 0, 1])
            plt3.title('ROC Curve')
            plt3.xlabel('Probability of False Alarm')
            plt3.ylabel('Probability of Detection')
            plt3.savefig("C:/Django/pysite/media/"+session_key+"/roc.png",dpi=100)
            plt3.clf()            
#            im = Image.open("C:/Django/pysite/media/output3.png")
            
            dataL = open('C:/Django/pysite/LBT.txt').readlines()
            dataSNR = open('C:/Django/pysite/SNR.txt').readlines()
            dataROC = open('C:/Django/pysite/ROC.txt').readlines()
            
            DataTitleL = [];
            DataTitleSNR = [];
            
            datasize = len(dataL);
            for x in range(0,datasize/wchosenlength-2):
                DataTitleL.append('L of Background ' + str(x+1) + '\n');
                DataTitleSNR.append('SNR of Background ' + str(x+1) + '\n');
            DataTitleL.append('L of Background Average\n');
            DataTitleL.append('L of Target\n');
            DataTitleSNR.append('SNR of Background Average\n');
            DataTitleSNR.append('SNR of Target\n');
#            session_key = request.COOKIES['csrftoken']         

 #           raise Exception(str(session_key)[2:])
            for x in range(0,datasize/wchosenlength):
                dataL.insert(datasize-wchosenlength*(x+1),DataTitleL[datasize/wchosenlength-1-x])
                dataSNR.insert(datasize-wchosenlength*(x+1),DataTitleSNR[datasize/wchosenlength-1-x])

            open(path+'LBT.txt', 'wb').write(''.join(dataL))
            open(path+'SNR.txt', 'wb').write(''.join(dataSNR))
            
            dataROC.insert(0,'P detection\n')
            dataROC.insert(8,'P false alarm\n')
            open(path+'ROC.txt', 'wb').write(''.join(dataROC))
            
#            a = request.session['session_key']
#            raise Exception(request) 
            return render_to_response('result.html',{'FormRadianceChoice':FormRadianceChoice(),'FormSNRChoice':FormSNRChoice(),
                'fresult3':Pdmin[2],'fresult4':Pdmin[3],'fresult5':Pdmin[4],'fresult6':Pdmin[5],'result1':Pfa[0],'result2':Pfa[1],
                'result3':Pfa[2],'result4':Pfa[3],'result5':Pfa[4],'result6':Pfa[5],'session_key':session_key})            
 #          return HttpResponseRedirect(reverse('/mysite/helloworld/results/',kwargs = {'fresult':fresult})) 
        else:
            return render_to_response('errorpage.html')  
    else:
        return render_to_response('jump.html')  


def results(request):
    if request.method == 'POST': 
        formradiancechoice = FormRadianceChoice(request.POST)
        formSNRchoice = FormSNRChoice(request.POST)
        session_key = request.session.get('session_key',False)
        if formradiancechoice.is_valid() and formSNRchoice.is_valid():
            Radchosen = formradiancechoice.cleaned_data['BkgnameR'] 
            SNRchosen = formSNRchoice.cleaned_data['BkgnameS']         
            Wlnumbers = readfile('wavelength')
            wchosenlength = len(Wlnumbers)
            Ltnumbers = readfile('LBT')
            SNRn = readfile('SNR')
            ROC = readfile('ROC')
            
            choicesR = formradiancechoice.fields['BkgnameR'].choices        
            LegendR=[]
            if len(Radchosen)!=0:
                for i in range(0, len(Radchosen)):
                    LegendR.append(choicesR[int(Radchosen[i])][1])
                    LTdisplay = Ltnumbers[(int(Radchosen[i])*wchosenlength):(int(Radchosen[i])*wchosenlength+wchosenlength)]    
                    plt1.plot(Wlnumbers,LTdisplay)
    #            raise Exception(LegendR)    
                plt1.xlim([400, 2500]) 
                plt1.title('Scene Mean Spectral Radiance')
                plt1.xlabel('Wavelength(microns)')
                plt1.ylabel('Spectral Radiance(mW/cm^2-sr-um)')
                plt1.legend(LegendR,prop={'size':8})
                plt1.savefig("C:/Django/pysite/media/"+session_key+"/rad.png",dpi=100)
                plt1.clf()
       
#            im = Image.open("C:/Django/pysite/media/"+session_key+"/rad.png")
#            out = im.resize((800,600))
#            out.save('C:/Django/pysite/media/'+session_key+'/rad.png')
                 
            choicesS = formSNRchoice.fields['BkgnameS'].choices
            
            LegendS=[]
            
            if len(SNRchosen)!=0:
                for i in range(0, len(SNRchosen)):
                    LegendS.append(choicesR[int(SNRchosen[i])][1])
                    SNRdisplay = SNRn[int(SNRchosen[i])*wchosenlength:(int(SNRchosen[i])*wchosenlength+wchosenlength)]
                    plt2.plot(Wlnumbers,SNRdisplay)
                plt2.xlim([400, 2500]) 
                plt2.ylim([0, 105]) 
                plt2.title('Sensor Signal-to-Noise Ratio')
                plt2.xlabel('Wavelength(microns)')
                plt2.ylabel('Signal-to-Noise Ratio')
                plt2.legend(LegendS,prop={'size':8})
                plt2.savefig("C:/Django/pysite/media/"+session_key+"/snr.png",dpi=100)
                plt2.clf()
#            im = Image.open("C:/Django/pysite/media/output.png")
#            out = im.resize((800,600))
#            out.save('C:/Django/pysite/media/output.png')
        
            return render_to_response('result.html',{'session_key':session_key,'FormRadianceChoice':FormRadianceChoice(),'FormSNRChoice':FormSNRChoice()})       
    else:
        formradiancechoice = FormRadianceChoice(request.POST)
        formSNRchoice = FormSNRChoice(request.POST)
        session_key = request.session.get('session_key',False)    
#        FormRadianceChoice=FormRadianceChoice()
#        FormSNRChoice=FormSNRChoice()
        return render_to_response('result.html',{'session_key':session_key,'FormRadianceChoice':FormRadianceChoice(),'FormSNRChoice':FormSNRChoice()})
def final(request, offset):
    if os.path.exists('C:/Django/pysite/media/'+offset+'/')==False:
        raise Http404()   
           
    else:
        session_key = request.session.get('session_key',False) 
        return render_to_response('cbresult.html',{'session_key':session_key})
                
def erf(x):
    # save the sign of x
    sign = 1 if x >= 0 else -1
    x = abs(x)

    # constants
    a1 =  0.254829592
    a2 = -0.284496736
    a3 =  1.421413741
    a4 = -1.453152027
    a5 =  1.061405429
    p  =  0.3275911

    # A&S formula 7.1.26
    t = 1.0/(1.0 + p*x)
    y = 1.0 - (((((a5*t + a4)*t) + a3)*t + a2)*t + a1)*t*math.exp(-x*x)
    return sign*y # erf(-x) = -erf(x) 
def readtitledfile(filename):
    str1 = 'C:\Django\pysite\\'
    str2 = filename;
    str3 = '.txt'
    txt = open(str1+str2+str3,'r')
    txtall = txt.readlines()
    packsize=1
    while txtall[packsize][0].isdigit() and packsize<len(txtall)-1:
        packsize=packsize+1
    if packsize ==len(txtall) - 1:
        packsize = packsize + 2
    Output=[];
    packsize = packsize -2;
    for i in range(0,len(txtall)/(packsize+1)):
        Output = Output + map(float,txtall[(i*(packsize+1)+1):((i+1)*(packsize+1)+1)])    
    return Output
def parsesensor(filename,path):
#    path = 'C:/FASSP_EMMETT/v2.4/sens/'
#    filename = 'HyMap.sen'
    txt = open(path + filename,'r')
    for i in range(0,4):
        line = txt.readline()
    dim = line.split()[1]
    for i in range(0,9):
        line = txt.readline()
    out=[]
    for i in range(0,int(dim)):
        line = txt.readline()
        out.append(str(float(line.split()[1])*1000)+'\r\n')
    outs = ''
    f = open('C:/Django/pysite/wavelength.txt', 'wb')
    f.write(outs.join(out)) 
    f.close()
def findsensorname(filename,path): 
    fcm = open(path + filename,'r')
    txt = open
    for i in range(0,50):
        line = fcm.readline()
    return line.split()[1]
def parseFCM_genPrefill(filename,path):
#    path = 'C:/FASSP_EMMETT/v2.4/pfiles/'
#    filename = 'customized.fcm'
    dict = {}
    fcm = open(path + filename,'r')
    txt = open
    for i in range(0,11):
        line = fcm.readline()
        
    temp = line.split()[1]
    data = "Target Name"+"::"+temp
    dict['Target Name'] = temp
    line = fcm.readline()
    
    temp = line.split()[1]
    data = data+"\r\n"+"Target Scale"+"::"+temp
    dict['Target Scale'] = temp
    
    line = fcm.readline()
    line = fcm.readline()
    temp = line.split()[1][1:-1]
    data = data+"\r\n"+"Target Percentage"+"::"+temp
    dict['Target Percentage'] = temp
    
    line = fcm.readline()
    temp = line.split()[1]
    data = data+"\r\n"+"In Bkg No"+"::"+temp
    
    for i in range(0,6):
        line = fcm.readline()
    temp = line.split()[1][1:-1]
    data = data+"\r\n"+"Bkg Name"+"::"+temp
    dict['Bkg Name'] = temp
    
    line = fcm.readline()
    temp = line.split()[1]
    data = data+"\r\n"+"Bkg Scale"+"::"+temp
    dict['Bkg Scale'] = temp
    
    line = fcm.readline()
    line = fcm.readline()
    temp = line.split('/')[1]
    data = data+"\r\n"+"Bkg Percentage"+"::"+temp
    dict['Bkg Percentage'] = temp
    
    line = fcm.readline()
    line = fcm.readline()
    data = data+"\r\n"+"Bkg Class Count"+"::"+line.split()[1]
    for i in range(0,6):
        line = fcm.readline()
    temp = line.split()[1]
    data = data+"\r\n"+"Meteorological Range"+"::"+temp
    dict['Meteorological Range'] = temp
    
    line = fcm.readline()
    line = fcm.readline()
    temp = line.split()[1]
    data = data+"\r\n"+"Solar Angle"+"::"+temp
    dict['Solar Angle'] = temp
    
    line = fcm.readline()
    temp = line.split()[1]
    data = data+"\r\n"+"Ground Altitude"+"::"+temp
    dict['Ground Altitude'] = temp
    
    line = fcm.readline()
    temp = line.split()[1]
    data = data+"\r\n"+"Atmospheric Model"+"::"+temp
    dict['Atmospheric Model'] = temp
    
    line = fcm.readline()
    line = fcm.readline()
    line = fcm.readline()
    line = fcm.readline()
    line = fcm.readline()
    temp = line.split()[1]
    data = data+"\r\n"+"Atmospheric Haze"+"::"+temp
    dict['Atmospheric Haze'] = temp
    
    line = fcm.readline()
    line = fcm.readline()
    temp = line.split()[1]
    data = data+"\r\n"+"Cloud Index"+"::"+temp
    dict['Cloud Index'] = temp
    
    for i in range(0,7):
        line = fcm.readline()
    temp = line.split()[1]
    data = data+"\r\n"+"Sensor Name"+"::"+temp
    dict['Sensor Name'] = temp
    
    line = fcm.readline()
    temp = line.split()[1]
    data = data+"\r\n"+"View Angle"+"::"+temp
    dict['View Angle'] = temp
    
    line = fcm.readline()
    temp = line.split()[1]
    data = data+"\r\n"+"Noise Factor"+"::"+temp
    dict['Noise Factor'] = temp
    
    line = fcm.readline()
    temp = line.split()[1]
    data = data+"\r\n"+"Gain Factor"+"::"+temp
    dict['Gain Factor'] = temp
    
    line = fcm.readline()
    temp = line.split()[1]
    data = data+"\r\n"+"Rltv Calibration Error"+"::"+temp
    dict['Rltv Calibration Error'] = temp
    
    line = fcm.readline()
    temp = line.split()[1]
    data = data+"\r\n"+"Sensor Bits"+"::"+temp
    dict['Sensor Bits'] = temp
    
    line = fcm.readline()
    temp = line.split()[1]
    data = data+"\r\n"+"Sensor BER"+"::"+temp
    dict['Sensor BER'] = temp
    
    line = fcm.readline()
    temp = line.split()[1]
    data = data+"\r\n"+"Sensor Altitude"+"::"+temp
    dict['Sensor Altitude'] = temp
    
    line = fcm.readline()
    temp = line.split()[1]
    data = data+"\r\n"+"Integration Time"+"::"+temp
    dict['Integration Time'] = temp

 #   f = open('C:/Django/pysite/media/'+sessionID+'/prefill.txt', 'wb')
#    f.write(data)
 #   f.close()
    f = open('C:/Django/pysite/prefill.txt', 'wb')
    f.write(data)
    f.close()
    return dict
    
def readfile(filename):
    str1 = 'C:\Django\pysite\\'
    str2 = filename;
    str3 = '.txt'
    txt = open(str1+str2+str3,'r')
    txtall = txt.readlines()
    Output =map(float,txtall)    
    return Output
    

def modifyCustomFCM(keyword, value, data, multi = 0):
    if value.count(',')==0 and multi==0:
        data = re.sub(keyword + r'.*' +';', keyword + '\t' + value +'\t'+';',data)
    else:
        data = re.sub(keyword + r'.*' +';', keyword + '\t/' + value +'/\t'+';',data)
    return data    
    
    
def index(request):  
    return HttpResponse('Hello, Django!!!!')  
    
def helloworld(request):
    SMR = request.GET.get('SMR','0')
    SRSD = request.GET.get('SRSD','0')
    SMT = request.GET.get('SMT','0')

    fresult = int(SMR)+int(SRSD)+int(SMT)
    return render_to_response("helloworld.html", {"fresult": fresult})
#    return HttpResponseRedirect(reverse('pysite.helloworld.helloworld.results',args=(fresult,)))
    