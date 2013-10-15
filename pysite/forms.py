from django import forms

TOPIC_CHOICES = (
    ('HyMap_Test_Web_Tree.fcm','Predefined scenario BKG TREE'),
    ('Hyp_Web_Test.fcm','Predefined scenario BKG GRASS'),
    ('HyMap_Test_Web.fcm','Predefined scenario 3 BKGs'),
    ('Customized.fcm','User Customize'),
)

SENSOR_CHOICES = (
    ('HyMap.sen','Hymap'),
    ('HYDICE','HYDICE'),
    ('hyperion.sen','Hyperion'),
    ('spectir_vs2.sen','spectir_vs2'),
)

TARGET_CHOICES = (
    ('vgrnbmw.ref','Green BMW'),
    ('grnwood.ref','Green Wood'),
    ('whitetarp.ref','White Tarp'),
    ('blacktarp.ref','Black Tarp'),
    ('avongrass.ref','Avon Grass'),
)

BKG_CHOICES = (
    ('950824_05_Tree1_R.ref','TREE'),
    ('950824_05_Grass1_R.ref','Old GRASS'),
    ('urban_road.ref','ROAD'),
    ('avongrass.ref','Avon Grass'),
    ('whitetarp.ref','White Tarp'),    
    ('blacktarp.ref','Black Tarp'), 
    
    ('avongrass.ref','Bushes'),
    ('whitetarp.ref','Reflectance 10%'),    
    ('blacktarp.ref','Reflectance 30%'), 
    ('avongrass.ref','Reflectance 50%'),
    ('whitetarp.ref','Soil 1'),    
    ('blacktarp.ref','Soil 2'), 
    ('avongrass.ref','Blue Focus'),
    ('whitetarp.ref','Blue Mustang'),    
    ('blacktarp.ref','Green VW'), 
    ('avongrass.ref','White Saturn'),
    ('whitetarp.ref','White Capcor'),    
    ('blacktarp.ref','Urban Water'),     
)


wlgthpool = (
    ('HyMap_Test_Web_Tree.fcm','TREE'),
    ('Hyp_Web_Test.fcm','GRASS'),
    ('HyMap_Test_Web.fcm','BKG3'),
)
wlgthselected = (

)

#temp = list(TOPIC_CHOICES)
#temp.append(('another','AT'))
#TOPIC_CHOICES = tuple(temp)

def readfile(filename):
    str1 = 'C:\Django\pysite\sensorWV\\'
    str2 = filename;
    str3 = '.txt'
    txt = open(str1+str2+str3,'r')
    txtall = txt.readlines()
    Output = map(float,txtall)    
    txt.close()
    return Output
def getkeywordvalue(keyword):
    dir = 'C:/Django/pysite/prefill.txt'
    txt = open(dir,'r')
    a='#'
    b=['','']
    while(b[0]!=keyword and a!=''):
        a=txt.readline()
        a.strip()
        b = a.split('::')
    return b[1] if a!='' else 'NULL'

def get_choices(keyword):
    string = getkeywordvalue(keyword)
    choices_list = string.strip().split(',')
	
    out = []
    for x in range(len(choices_list)):
        if choices_list[x]!='':
            out.append([x,choices_list[x]]) 
    return tuple(out)
    
def get_choices2(keyword):
    string = keyword
    choices_list = string.strip().split(',')
	
    out = []
    for x in range(len(choices_list)):
        if choices_list[x]!='':
            out.append([x,choices_list[x]]) 
    return tuple(out)
    
def get_choiceswithAVGandTarget(keyword):
    stringA = 'Avg Background'
    stringT = getkeywordvalue('Target Name')
    string = getkeywordvalue(keyword)
            
    choices_list = string.strip().split(',')
 #   raise Exception(choices_list)   
    out = []
    for x in range(len(choices_list)):
        if choices_list[x]!='':
            out.append([x,choices_list[x]]) 
    out.append([x+1,stringA])        
    out.append([x+2,stringT])
#    raise Exception(out)     
    return tuple(out)
    
def get_tochoose_choices():
    choices_list = readfile('wavelength')
    out = []
    for x in range(len(choices_list)):
        out.append([x,choices_list[x]]) 
    return tuple(out)
    
def get_tochoose_choices2(filename):
    choices_list = readfile(filename)
    out = []
    for x in range(len(choices_list)):
        out.append([x,choices_list[x]]) 
    return tuple(out)
    

    
class MessageForm2(forms.Form): 
    pfile_selection = forms.ChoiceField(choices=TOPIC_CHOICES)	
	
class MessageForm(forms.Form): 
    hiddentxt = forms.CharField(widget=forms.HiddenInput, required=False)

class FormBkgName(forms.Form): 
    hiddentxt = forms.CharField(widget=forms.HiddenInput, required=False)
class FormSensorName(forms.Form): 
    def __init__(self, *args, **kw):
        SensorName = kw.pop("SensorName")
        super(forms.Form, self).__init__(*args, **kw)	
        self.fields["Sensorname"] = forms.CharField(initial = SensorName, required=False,widget=forms.HiddenInput)
        
class FormScene(forms.Form): 
    def __init__(self, *args, **kw):
    
        AtmosphericHaze = kw.pop("AtmosphericHaze")
        GroundAltitude = kw.pop("GroundAltitude")
        SolarAngle = kw.pop("SolarAngle")
        AtmosphericModel = kw.pop("AtmosphericModel") 
        CloudIndex = kw.pop("CloudIndex") 
        MeteorologicalRange = kw.pop("MeteorologicalRange")         
    
        super(forms.Form, self).__init__(*args, **kw)	
        # self.fields["Atmospheric_haze"] = forms.IntegerField(label='Atmospheric Haze',initial = getkeywordvalue('Atmospheric Haze'),required=True,
		# widget=forms.TextInput(attrs={'onfocus':'writeText("0=No Aerosols, 1=Rural-clr, 2=Rural-Hazy, 3=Navy Maritime,  4=Maritime, 5=Urban, 6=Trop")'}))		
        # self.fields["Ground_altitude"] = forms.FloatField(label='Ground Altitude',initial = getkeywordvalue('Ground Altitude'),required=True,
		# widget=forms.TextInput(attrs={'onfocus':'writeText("Ground Altitude(km)")'}))		
        # self.fields["Solangle"] = forms.FloatField(label='Solar Angle',initial = getkeywordvalue('Solar Angle'), required=True,
		# widget=forms.TextInput(attrs={'onfocus':'writeText("Solar Angle,0~90")'})) 
        # self.fields["Atmospheric_model"] = forms.FloatField(label='Atmospheric Model',initial = getkeywordvalue('Atmospheric Model'), required=True, 
		# widget=forms.TextInput(attrs={'onfocus':'writeText("1=Tropical, 2=MidLat Summ, 3=MidLat Wint, 4=SubArc Summ, 5=SubArc Win, 6=US Standard")'}))
        # self.fields["icld"] = forms.FloatField(label='Cloud Index',initial = getkeywordvalue('Cloud Index'), required=True, 
		# widget=forms.TextInput(attrs={'onfocus':'writeText("0=No Cloud, 1 = Cloud")'}))       
        # self.fields["Mrange"] = forms.FloatField(label='Meteorological Range',initial = getkeywordvalue('Meteorological Range'), required=True, 
		# widget=forms.TextInput(attrs={'onfocus':'writeText("the range describe visibility, unit km")'}))      
        
        self.fields["Atmospheric_haze"] = forms.IntegerField(label='Atmospheric Haze',initial = AtmosphericHaze,required=True,
		widget=forms.TextInput(attrs={'onfocus':'writeText("0=No Aerosols, 1=Rural-clr, 2=Rural-Hazy, 3=Navy Maritime,  4=Maritime, 5=Urban, 6=Trop")'}))		
        self.fields["Ground_altitude"] = forms.FloatField(label='Ground Altitude',initial = GroundAltitude,required=True,
		widget=forms.TextInput(attrs={'onfocus':'writeText("Ground Altitude(km)")'}))		
        self.fields["Solangle"] = forms.FloatField(label='Solar Angle',initial = SolarAngle, required=True,
		widget=forms.TextInput(attrs={'onfocus':'writeText("Solar Angle,0~90")'})) 
        self.fields["Atmospheric_model"] = forms.FloatField(label='Atmospheric Model',initial = AtmosphericModel, required=True, 
		widget=forms.TextInput(attrs={'onfocus':'writeText("1=Tropical, 2=MidLat Summ, 3=MidLat Wint, 4=SubArc Summ, 5=SubArc Win, 6=US Standard")'}))
        self.fields["icld"] = forms.FloatField(label='Cloud Index',initial = CloudIndex, required=True, 
		widget=forms.TextInput(attrs={'onfocus':'writeText("0=No Cloud, 1 = Cloud")'}))       
        self.fields["Mrange"] = forms.FloatField(label='Meteorological Range',initial = MeteorologicalRange, required=True, 
		widget=forms.TextInput(attrs={'onfocus':'writeText("the range describe visibility, unit km")'}))              
        
class FormSensor(forms.Form): 
    def __init__(self, *args, **kw):
    
        SensorName = kw.pop("SensorName")
        NoiseFactor = kw.pop("NoiseFactor")
        GainFactor = kw.pop("GainFactor")
        RltvCalibrationError = kw.pop("RltvCalibrationError")
        IntegrationTime = kw.pop("IntegrationTime") 
        SensorAltitude = kw.pop("SensorAltitude") 

        super(forms.Form, self).__init__(*args, **kw)	
        
        self.fields["Sensorname"] = forms.CharField(label='Sensor Name',initial = SensorName, required=False,
		widget=forms.TextInput(attrs={'onmouseover':'writeText("Sensor File Name (read only)")','readonly':'readonly'}))          
        self.fields["Noisefac"] = forms.FloatField(label='Noise Factor',initial = NoiseFactor,required=False,
		widget=forms.TextInput(attrs={'onfocus':'writeText("Noise Factor(default 1)")'})) 
        self.fields["Gainfac"] = forms.FloatField(label='Gain Factor',initial = GainFactor,required=False,
		widget=forms.TextInput(attrs={'onfocus':'writeText("Gain Factor(default 1)")'})) 
        self.fields["Relcal"] = forms.FloatField(label='Rltv Calibration Error(%)',initial = RltvCalibrationError,required=False,
		widget=forms.TextInput(attrs={'onfocus':'writeText("Relative Calibration Error (percent)")'})) 
        self.fields["Tint"] = forms.FloatField(label='Integration Time(s)',initial = IntegrationTime,required=False,
		widget=forms.TextInput(attrs={'onfocus':'writeText("Sensor Integration Time")'}))
        self.fields["Platalt"] = forms.FloatField(label='Sensor Altitude(km)',initial = SensorAltitude,required=False,
		widget=forms.TextInput(attrs={'onfocus':'writeText("Sensor Altitude(km)")'}))            
    
        # super(forms.Form, self).__init__(*args, **kw)	
        # self.fields["Noisefac"] = forms.FloatField(label='Noise Factor',initial = getkeywordvalue('Noise Factor'),required=False,
		# widget=forms.TextInput(attrs={'onfocus':'writeText("Noise Factor(default 1)")'})) 
        # self.fields["Gainfac"] = forms.FloatField(label='Gain Factor',initial = getkeywordvalue('Gain Factor'),required=False,
		# widget=forms.TextInput(attrs={'onfocus':'writeText("Gain Factor(default 1)")'})) 
        # self.fields["Relcal"] = forms.FloatField(label='Rltv Calibration Error(%)',initial = getkeywordvalue('Rltv Calibration Error'),required=False,
		# widget=forms.TextInput(attrs={'onfocus':'writeText("Relative Calibration Error (percent)")'})) 
        # self.fields["Tint"] = forms.FloatField(label='Integration Time(s)',initial = getkeywordvalue('Integration Time'),required=False,
		# widget=forms.TextInput(attrs={'onfocus':'writeText("Sensor Integration Time")'}))
        # self.fields["Platalt"] = forms.FloatField(label='Sensor Altitude(km)',initial = getkeywordvalue('Sensor Altitude'),required=False,
		# widget=forms.TextInput(attrs={'onfocus':'writeText("Sensor Altitude(km)")'}))        
class FormTarget(forms.Form): 
    def __init__(self, *args, **kw):
    
        TargetName = kw.pop("TargetName")
        TargetScale = kw.pop("TargetScale")
        TargetPercentage = kw.pop("TargetPercentage")
        BkgName = kw.pop("BkgName")
        
        super(forms.Form, self).__init__(*args, **kw)	
        
        # self.fields["Targname"] = forms.CharField(label='Target file Name',initial = getkeywordvalue('Target Name'),required=False,
        # widget=forms.TextInput(attrs={'onmouseover':'writeText("Target File Name (readonly)")','readonly':'readonly'}))
        # self.fields["Targscale"] = forms.FloatField(label='Target Scale',initial = getkeywordvalue('Target Scale'),required=False,
        # widget=forms.TextInput(attrs={'onfocus':'writeText("Target Covariance Scale Factor (default 1)")'})) 
        # self.fields["Targperc"] = forms.FloatField(label='Target Percentage(%)',initial = getkeywordvalue('Target Percentage'),required=False,
        # widget=forms.TextInput(attrs={'onfocus':'writeText("Target Percentage IFOV")'})) 
        # self.fields["Targinback"] = forms.ChoiceField(label='Target In which bkg',choices=get_choices('Bkg Name'), initial=int(getkeywordvalue('In Bkg No'))-1, required=False,
        # widget=forms.Select(attrs={'onfocus':'writeText("Background Class Number Target Embedded in")'}))  
       
        self.fields["Targname"] = forms.CharField(label='Target file Name',initial = TargetName, required=False,
		widget=forms.TextInput(attrs={'onmouseover':'writeText("Target File Name (readonly)")','readonly':'readonly'}))      
        self.fields["Targscale"] = forms.FloatField(label='Target Scale',initial = TargetScale,required=False,
		widget=forms.TextInput(attrs={'onfocus':'writeText("Target Covariance Scale Factor (default 1)")'})) 
        self.fields["Targperc"] = forms.FloatField(label='Target Percentage(%)',initial = TargetPercentage,required=False,
		widget=forms.TextInput(attrs={'onfocus':'writeText("Target Percentage IFOV")'})) 
        self.fields["Targinback"] = forms.ChoiceField(label='Target In which bkg',choices=get_choices2(BkgName), initial=int(getkeywordvalue('In Bkg No'))-1, required=False,
		widget=forms.Select(attrs={'onfocus':'writeText("Background Class Number Target Embedded in")'})) 

class FormBackground(forms.Form): 
    def __init__(self, *args, **kw):

        BkgName = kw.pop("BkgName")
        BkgName2 = kw.pop("BkgName2")
        BkgScale = kw.pop("BkgScale")
        BkgPercentage = kw.pop("BkgPercentage")
        
        super(forms.Form, self).__init__(*args, **kw)
        # self.fields["Bkgname"] = forms.MultipleChoiceField(label='Bkg file Name',choices=get_choices('Bkg Name'),required=False,
		# widget=forms.SelectMultiple(attrs={'onfocus':'writeText("Background Reflectance Filename")'}))
        # self.fields["Bkgscale"] = forms.FloatField(label='Bkg Scale',initial = getkeywordvalue('Bkg Scale'),required=False,
		# widget=forms.TextInput(attrs={'onfocus':'writeText("Background Covariance Scale Factor (default 1)")'})) 
        # self.fields["Backperc"] = forms.CharField(label='Bkg Percentage(%)',initial = getkeywordvalue('Bkg Percentage'), required=False,
		# widget=forms.TextInput(attrs={'onfocus':'writeText("Background Class Percent of Scene")'}))		        
#        self.fields["Numback"] = forms.IntegerField(label='Bkg Class Count',initial = getkeywordvalue('Bkg Class Count'),required=False)

        self.fields["Bkgname"] = forms.MultipleChoiceField(label='Bkg file Name',choices = get_choices2(BkgName),required=False,
		widget=forms.SelectMultiple(attrs={'onfocus':'writeText("Background Reflectance Filename")'}))
        self.fields["Bkgscale"] = forms.FloatField(label='Bkg Scale',initial = BkgScale,required=False,
		widget=forms.TextInput(attrs={'onfocus':'writeText("Background Covariance Scale Factor (default 1)")'})) 
        self.fields["Backperc"] = forms.CharField(label='Bkg Percentage(%)',initial = BkgPercentage, required=False,
		widget=forms.TextInput(attrs={'onfocus':'writeText("Background Class Percent of Scene")'}))		
        
        self.fields["Bkgname2"] = forms.CharField(label='Bkg Percentage(%)',initial = BkgName, required=False,
        widget=forms.HiddenInput)	      
        
class FormWavelength_chosen(forms.Form): 
    wavelength_chosen = forms.MultipleChoiceField(label='Wavelength Chosen',required=False)	
class FormWavelength_to_choose(forms.Form): 
    def __init__(self, *args, **kw):
    #first remove my custom keyword from the list of keyword args
        SensorName = kw.pop("SensorName")
        super(forms.Form, self).__init__(*args, **kw)
        #now we dynamically add the customer choices - accepts partners as an input
        self.fields["wavelength_to_choose"] = forms.MultipleChoiceField(label='Wavelength To Choose',choices=get_tochoose_choices2(SensorName))
#        self.fields['MultipleChoiceField'].choices = get_tochoose_choices()
#    wavelength_to_choose = forms.MultipleChoiceField(label='Wlgth to choose',choices=get_tochoose_choices())
class FormRadianceChoice(forms.Form): 
    def __init__(self, *args, **kw):
        super(forms.Form, self).__init__(*args, **kw)
        self.fields["BkgnameR"] = forms.MultipleChoiceField(label='Choose to plot',choices=get_choiceswithAVGandTarget('Bkg Name'),widget=forms.CheckboxSelectMultiple,required=False)
class FormSNRChoice(forms.Form): 
    def __init__(self, *args, **kw):
        super(forms.Form, self).__init__(*args, **kw)
        self.fields["BkgnameS"] = forms.MultipleChoiceField(label='Choose to plot',choices=get_choiceswithAVGandTarget('Bkg Name'),widget=forms.CheckboxSelectMultiple,required=False)


class FormCustomize(forms.Form): 
    sensor_selection = forms.ChoiceField(choices=SENSOR_CHOICES)
    target_selection = forms.ChoiceField(choices=TARGET_CHOICES)
    hiddentxt = forms.CharField(widget=forms.HiddenInput, required=False)
class FormBKG_tochoose(forms.Form): 
    BKG_tochoose = forms.MultipleChoiceField(label='Background to Choose',required=False, choices = BKG_CHOICES)
class FormBKG_chosen(forms.Form): 
    BKG_chosen = forms.MultipleChoiceField(label='Background Chosen',required=False)	
class FormFinalSubmition(forms.Form): 
    Atmospheric_haze = forms.IntegerField(required=True)
    Solangle = forms.FloatField(required=True)
    Atmospheric_model = forms.FloatField(required=True) 
    icld = forms.FloatField(required=True)
    Ground_altitude = forms.FloatField(required=True)
    Mrange = forms.FloatField(required=True)   

    Sensorname = forms.CharField(required=True)
    Noisefac = forms.FloatField(required=True)
    Gainfac = forms.FloatField(required=True)
    Relcal = forms.FloatField(required=True)
    Platalt = forms.FloatField(required=True)
    Tint = forms.FloatField(required=True)

    Targname = forms.CharField(required=True)
    Targscale = forms.FloatField(required=True)
    Targperc = forms.FloatField(required=True)
    Targinback = forms.ChoiceField(required=True)
    
    BkgName2 = forms.CharField(required=False)
    Bkgscale = forms.FloatField(required=True)
    Backperc = forms.CharField(required=True)