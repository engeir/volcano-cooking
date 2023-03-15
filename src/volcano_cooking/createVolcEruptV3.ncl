load "$NCARG_ROOT/lib/ncarg/nclex/gsun/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclex/gsun/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/shea_util.ncl"

print("in "+get_script_name())

res=getenv("RES")

;=========================================
; Setup for CMIP6 1850-2016
;=========================================
; FirstYear=1850
LastYear=2016
; doMassScaling = True
massSO2thresh = 15 ; threshold (Tg) for eruptions scaled by MassFactor
MassFactor = 1/1.8 ; scaling factor for large eruptions
; doAltReduction = True
; altSO2thresh = 3.5 ; threshold (Tg) for altitude reduction to 18-20 km

;=========================================
; Setup for Last Millenium 850-1849
;=========================================
FirstYear = 850
; LastYear  = 1849
doMassScaling = False
doAltReduction = True
altSO2thresh = 3.5 ; threshold (Tg) for altitude reduction to 18-20 km
; res="2deg"

; Possibly set this to true?
doVEIspread=False ; spread emissions for VEI 5 & 6?
VEI6_factor=1.0 ; mass factor for VEI6 eruptions
VEI5_factor=1.0 ; mass factor for VEI6 eruptions

; Set min/max latitude of Pinatubo plume here:
PinLat=-999.0
; PinMinLat=0.0
PinMinLat=-999.0


; remove_list=(/"Cerro Hudson"/)
; remove_date=(/19910815/)

; remove_list=(/"Mount Pinatubo"/)
; remove_date=(/19910615/)

if (isvar("remove_list")) then
  nRemove=dimsizes(remove_list)
else
  nRemove=0
end if

; Constants
;
; NOTE: These are from CAM, shr_const_mod.F90.
PI      = 4.0d0 * atan(1.0d0)     ; pi
G       = 9.80616d0               ; acceleration of gravity ~ m/s^2
BOLTZ   = 1.38065d-23             ; Boltzmann's constant ~ J/K/molecule
AVOGAD  = 6.02214d26              ; Avogadro's number ~ molecules/kmole
RGAS    = AVOGAD*BOLTZ            ; Universal gas constant ~ J/K/kmole
MWDAIR  = 28.966d0                ; molecular weight dry air ~ kg/kmole
RDAIR   = RGAS/MWDAIR             ; Dry air gas constant ~ J/K/kg
MWH2O   = 18.000d0                ; molecular weight of water vapor
RearthCm  = 6.37122d8               ; Earth's radius (cm)
DG2RAD  = PI / 180.0d0            ; rad deg^-1
MWNH4HSO4 = 115.10734             ; molecular weight for MAM so4 species (ammonium sulfate) (g/mol)
MWH2SO4 = 98.0784d0               ; molecular weight of H2SO4 species (g/mol)
MWS     = 32.066d0                ; molecular weight of atomic sulfur (g/mol)
MWSO2   = 64.0648d0               ; molecular weight of SO2 (g/mol)
MWOCS   = 60.0764d0               ; molecular weight of OCS (g/mol)
MWDMS   = 62.1324d0               ; molecular weight of DMS (g/mol)
tab = str_get_tab()

SAearthCm2=4.0*PI*RearthCm*RearthCm ; Earth surface area in cm2 (CAM)
tab    = str_get_tab()

if (ismissing(res)) then
  res="1deg"
  print("Horizontal resolution not set; defaulting to 1deg (0.95x1.25). For 1.9x2.5: setenv resolution 2deg")
end if

if (res.eq."2deg".or.res.eq."1.9x2.5") then
  templateFilename = getenv("COORDS2DEG")
  print("Using 2 degree res")
else
  if (res.eq."1deg".or.res.eq."0.95x1.25") then
    templateFilename = getenv("COORDS1DEG")
    print("Using 1 degree res")
  else
    print("Illegal value for resolution: "+res)
    exit
  end if
end if
print("Creating file at "+res+" horizontal resolution")

templateFile=addfile(templateFilename,"r")
gw=templateFile->gw ; [lat | 96]
lat=templateFile->lat
lon=templateFile->lon
slat=templateFile->slat
slon=templateFile->slon
nLat=dimsizes(lat)
nLon=dimsizes(lon)

columnArea=conform(new((/ nLat, nLon /), double), gw, 0)
columnArea=columnArea*SAearthCm2/nLon/sum(gw) ; area of each grid column in cm2
columnArea!0="lat"
columnArea!1="lon"
columnArea&lat=lat
columnArea&lon=lon

print("SAearthCm2="+SAearthCm2+"; sum(columnArea)="+sum(columnArea))

filepath=getenv("SYNTH_FILE_DIR")+"/"
outfilepath=getenv("DATA_OUT")+"/"
infilename = getenv("SYNTH_BASE")
infiletype = getenv("SYNTH_EXT")
outfilename="VolcanEESMv3.11Enger_SO2_"+FirstYear+"-"+LastYear

if (.not.isvar("LastYear")) then
  LastYear = 2016
end if

if (LastYear.lt.FirstYear) then
  LastYear = 2016
end if

if (doMassScaling) then
  outfilename=outfilename+"_Mscale"
end if

if (doAltReduction) then
  outfilename=outfilename+"_Zreduc"
end if

if (doVEIspread) then
  outfilename=outfilename+"_VEIspread"
end if

globalAtt = True
; For a nicer looking netCDF, create a "new line" character.
nl = integertochar(10)  ; newline character

globalAtt@data_summary = nl+\
    "Each day of eruption, the emission occurs over 6 hours from 1200 to 1800UT."

infile=filepath+infilename+"."+infiletype

if (infiletype.eq."txt") then

  header=readAsciiHead(infile, TermStr)
  print((/header/))
  nhead=dimsizes(header)
  print("nhead="+nhead)

  lines  = asciiread(infile,-1,"string")
  ; print((/lines(nhead)/))
  ncols = str_fields_count(lines(nhead),delim)
  print("ncols="+ncols)

  fields=str_split(header(nhead-1),delim)
  ; print(fields)
  yearCol    =ind(fields.eq."Start_Year")+1
  monthCol   =ind(fields.eq."Start_Month")+1
  dayCol     =ind(fields.eq."Start_Day")+1
  SO2MassCol =ind(fields.eq."SO2_flux_Tg")+1
  latCol     =ind(fields.eq."Lat")+1
  lonCol     =ind(fields.eq."Lon")+1
  VEICol     =ind(fields.eq."VEI")+1
  altTopCol  =ind(fields.eq."Upper_column_height_km")+1
  altBotCol  =ind(fields.eq."Lower_column_height_km")+1
  volcNameCol=ind(fields.eq."Volcano")+1

  ; print("yearCol="+yearCol)
  ; print("monthCol="+monthCol)

  inYear =toint(str_get_field(lines(nhead:),yearCol,delim))
  inMonth=toint(str_get_field(lines(nhead:),monthCol,delim))
  inDay  =toint(str_get_field(lines(nhead:),dayCol,delim))
  inSO2  =todouble(str_get_field(lines(nhead:),SO2MassCol,delim))
  inLat  =tofloat(str_get_field(lines(nhead:),latCol,delim))
  inLon  =tofloat(str_get_field(lines(nhead:),lonCol,delim))
  inVEI  =toint(str_get_field(lines(nhead:),VEICol,delim))
  inTop  =tofloat(str_get_field(lines(nhead:),altTopCol,delim))
  inBot  =tofloat(str_get_field(lines(nhead:),altBotCol,delim))
  volcName = str_get_field(lines(nhead:),volcNameCol,delim)

else ; netCDF

  ncid = addfile(infile,"r")
  inSO2    = ncid->Total_Emission
  inVEI    = ncid->VEI
  inYear   = ncid->Year_of_Emission
  inMonth  = ncid->Month_of_Emission
  inDay    = ncid->Day_of_Emission
  inLat    = ncid->Latitude
  inLon    = ncid->Longitude
  inTop    = ncid->Maximum_Injection_Height
  inBot    = ncid->Minimum_Injection_Height
  Volcano_Name =ncid->Eruption@Volcano_Name
  volcName = str_strip(str_split(Volcano_Name,","))

  ; printVarSummary(volcName)
  ; printVarSummary(inSO2)

end if

print(inYear+tab+inMonth+tab+inDay+tab+inLat+tab+inLon+tab+inSO2+tab+volcName)

inDate=10000*inYear+100*inMonth+inDay

; Not important, no volcanoes will be removed
if (nRemove.gt.0) then
  do r=0,nRemove-1
    print("removing "+remove_date(r)+remove_list(r))
    indRemove=ind(volcName.eq.remove_list(r).and.inDate.eq.remove_date(r))
    print("==================================================================")
    print("indRemove="+indRemove)
    print("ind(volcName.eq.remove_list(r))="+ind(volcName.eq.remove_list(r)))
    print("ind(inDate.eq.remove_date(r))="+ind(inDate.eq.remove_date(r)))
    print("inDate(ind(volcName.eq.remove_list(r)))="+inDate(ind(volcName.eq.remove_list(r))))
    print("==================================================================")
    inSO2(indRemove)=0.0
    outfilename=outfilename+"_remove"+remove_date(r)+str_sub_str(remove_list(r)," ","")
  end do
end if

; Adjust altitude range for SO2>5Tg if max altitude > 20 km
if (doAltReduction) then
  AltInd=ind(inSO2.ge.altSO2thresh.and.inTop.gt.20.0.and.inYear.ge.FirstYear.and.inYear.le.LastYear)
  if (.not.(ismissing(AltInd(0)))) then

    print("Adjusting altitude range for "+inYear(AltInd)+"-"+inMonth(AltInd)+"-"+\
           inDay(AltInd)+" "+volcName(AltInd)+" "+inBot(AltInd)+"-"+inTop(AltInd)+"km")

    globalAtt@data_summary = globalAtt@data_summary + nl +\
        "Altitude range adjusted for SO2>"+altSO2thresh+"Tg if max altitude > 20 km:"

    do i = 0,dimsizes(AltInd)-1
      globalAtt@data_summary = globalAtt@data_summary + nl +\
        "     "+inYear(AltInd(i))+"-"+inMonth(AltInd(i))+"-"+inDay(AltInd(i))+" "+volcName(AltInd(i))
    end do

    inTop(AltInd)=20.0
    inBot(AltInd)=where(inBot(AltInd).gt.18.0,18.0,inBot(AltInd))

    print("New altitude range for "+inYear(AltInd)+"-"+inMonth(AltInd)+"-"+\
           inDay(AltInd)+" "+volcName(AltInd)+" "+inBot(AltInd)+"-"+inTop(AltInd)+"km")

  end if
end if

; Adjust SO2 mass for SO2>15 Tg
if (doMassScaling) then
  SO2Ind=ind(inSO2.ge.massSO2thresh.and.inYear.ge.FirstYear.and.inYear.le.LastYear)
  if (.not.(ismissing(SO2Ind(0)))) then
    print("Adjusting SO2 for "+inYear(SO2Ind)+"-"+inMonth(SO2Ind)+"-"+inDay(SO2Ind)+" "+volcName(SO2Ind))
    globalAtt@data_summary = globalAtt@data_summary + nl+\
        "For eruptions with SO2>"+massSO2thresh+"Tg, mass scaled by factor "+MassFactor
    do i = 0,dimsizes(SO2Ind)-1
      globalAtt@data_summary = globalAtt@data_summary + nl+\
        "     "+inYear(SO2Ind(i))+"-"+inMonth(SO2Ind(i))+"-"+inDay(SO2Ind(i))+" "+volcName(SO2Ind(i))
    end do
    inSO2(SO2Ind)=inSO2(SO2Ind)*MassFactor
  end if
else
  globalAtt@data_summary = globalAtt@data_summary + nl+\
      "No SO2 mass scaling is included; all masses are as provided by VolcanEESM."
end if

; Adjust Pinatubo latitude range?
if (PinLat.ge.-90.or.PinMinLat.ge.-90) then
  Pind=str_match_ind(volcName,"Pinatubo")
  print(Pind+" "+volcName(Pind)+" Lat:"+PinLat);+", "+PinBot+"-"+PinTop+" km")
  if (PinLat.gt.-90) then
    inLat(Pind)=PinLat
  end if
  if (inLat(Pind).ge.0) then
    PinLatStr=str_strip(sprintf("%2.0f",inLat(Pind)))+"N"
  else
    PinLatStr=str_strip(sprintf("%2.0f",abs(inLat(Pind))))+"S"
  end if
  if (PinMinLat.ge.-90) then
    if (PinMinLat.ge.0) then
      PinLatStr=str_strip(sprintf("%2.0f",PinMinLat))+"N-"+PinLatStr
    else
      PinLatStr=str_strip(sprintf("%2.0f",abs(PinMinLat)))+"S-"+PinLatStr
    end if
  end if
  outfilename=outfilename+"_Pin"+PinLatStr
else
  PinLatStr=""
end if
print(" ")
print("outfilename="+outfilename)
print(" ")

; Shift longitude from -180,180 to 0,360
inLon=where(inLon.ge.0,inLon,inLon+360.)

; print(sprinti("%4.4i",inYear)+" "+sprinti("%3.2i",inMonth)+sprinti("%3.2i",inDay)+" "+\
;       sprintf("%7.3f",inLat)+" "+sprintf("%7.3f",inLon)+" "+\
;       sprintf("%5.2f",inTop)+" "+sprintf("%5.2f",inBot)+" "+\
;       sprinti("%2.1i",inVEI)+" "+\
;       sprintf("%8.5f",inSO2)+" "+volcName)

indVolcs=ind(inSO2.gt.0.and.inYear.ge.FirstYear.and.inYear.le.LastYear)
nVolc=dimsizes(indVolcs)
print(nVolc+" eruptions for years "+FirstYear+" to "+LastYear)

; Manually add new eruptions
; if (volcName(indVolcs(nVolc-1)).eq."Calbuco".and.inYear(indVolcs(nVolc-1)).eq.2015) then
;   newVolcName=(/"Etna","Pavlof"/)
;   newDate=(/20151203,20160327/)
;   newSO2=(/0.053,0.02/)
;   newLat=(/37.73,55.42/)
;   newLon=(/15.00,198.10/)
;   newTop=(/12,11/)
;   newBot=(/8,6.1/)
;   nVolcTot=nVolc+dimsizes(newVolcName)
; else
nVolcTot=nVolc
; end if

; print((/newVolcName/))

nTimes=nVolcTot*4+2
date=new(nTimes,integer)
date!0="time"
date@long_name = "date" ;
date@units = "YYYYMMDD" ;
date@standard_name = "date" ;

datesec=date
datesec@long_name = "datesec" ;
datesec@units = "seconds since midnight" ;
datesec@standard_name = "datesec" ;

date(0)=10101 ; yyyymmdd
datesec(0) = 1800

; Seems to be important! Model keeps crashing if altitude range is set dynamically.
; altmax=toint(max(inTop(indVolcs))+0.5)
altmax=29
; altmin=toint(min(inBot(indVolcs)))
altmin=0
nalts=altmax-altmin+1

altitude = fspan(altmin,altmax,nalts)
altitude!0="altitude"
altitude@long_name = "altitude midlevel" ;
altitude@units = "km" ;
altitude@standard_name = "altitude midlevel" ;

altitude_int = fspan(altmin-0.5,altmax+0.5,nalts+1)
altitude_int!0="altitude_int"
altitude_int@long_name = "altitude interval" ;
altitude_int@units = "km" ;
altitude_int@standard_name = "altitude interval" ;

nAlt=dimsizes(altitude)
stratvolc=new((/nTimes,nAlt,nLat,nLon/),double)
stratvolc@long_name = "SO2 elevated emissions from explosive volcanoes" ;
stratvolc@units = "molecules/cm3/s" ;
stratvolc@standard_name = "SO2 elevated emissions from explosive volcanoes" ;
stratvolc(:,:,:,:)=0.0d0
stratvolc!0="time"
stratvolc!1="altitude"
stratvolc!2="lat"
stratvolc!3="lon"
stratvolc&altitude=altitude
stratvolc&lat=lat
stratvolc&lon=lon

latArr=conform_dims((/nLat,nLon/),lat,0)
lonArr=conform_dims((/nLat,nLon/),lon,1)
maskArr=new((/nLat,nLon/),double)
maskArr!0="lat"
maskArr!1="lon"
maskArr&lat=lat
maskArr&lon=lon

if (doVEIspread) then
  globalAtt@data_summary = globalAtt@data_summary +nl+\
    "Emission area and initial SO2 loss depend on volcanic explosivity index (VEI) as follows:"+nl+\
    "  VEI <= 4 : 1 column, SO2 emitted = total from data_source_files"+nl+\
    "  VEI  = 5 : 1.20e6 km2 circle centered on volcano, SO2 emitted = "+VEI5_factor+" * total from data_source_files"+nl+\
    "  VEI  = 6 : 2.75e6 km2 circle centered on volcano, SO2 emitted = "+VEI6_factor+" * total from data_source_files"
else
  if (VEI6_factor.eq.1.and.VEI5_factor.eq.1) then
    globalAtt@data_summary = globalAtt@data_summary +nl+\
      "No SO2 loss based on volcanic explosivity index (VEI)."
  else
    globalAtt@data_summary = globalAtt@data_summary +nl+\
      "Initial SO2 loss depends on volcanic explosivity index (VEI) as follows:"+nl+\
      "  VEI <= 4 : SO2 emitted = total from data_source_files"+nl+\
      "  VEI  = 5 : SO2 emitted = "+VEI5_factor+" * total from data_source_files"+nl+\
      "  VEI  = 6 : SO2 emitted = "+VEI6_factor+" * total from data_source_files"
  end if
  globalAtt@data_summary = globalAtt@data_summary +nl+\
      "All volcanic emissions occur in 1 column (no VEI-based spreading)."
  if (PinMinLat.ge.-90) then
    globalAtt@data_summary = globalAtt@data_summary +nl+\
      "Pinatubo emissions spread: "+PinLatStr
  end if
end if

print(globalAtt@data_summary)

outstring = "This file is for the following volcanoes:"
print((/outstring/))
globalAtt@data_summary = globalAtt@data_summary + nl +\
    "======================================================================" + nl \
    + outstring

if ((PinMinLat.ge.-90).or.(doVEIspread)) then
  outstring = "YYYYMMDD  MinLat  Lat    Lon     AltMin AltMax SO2(Tg) VEI nCol  Area(km2) Em(cm-3s-1) Name"
else
  outstring = "YYYYMMDD  Lat    Lon     AltMin AltMax SO2(Tg) VEI Area(km2) Em(cm-3s-1) Name"
end if

print((/outstring/))
globalAtt@data_summary = globalAtt@data_summary + nl + outstring

dt=0
date_volc=new(nVolcTot,integer)
totalArea=new(nVolcTot,double)
do t=0,nVolcTot-1
  maskArr(:,:)=0.0d0
  t1=dt*4+1
  t2=dt*4+2
  t3=dt*4+3
  t4=dt*4+4

  if (t.lt.nVolc) then
    tv=indVolcs(t)
    date_volc(dt)=10000*inYear(tv)+100*inMonth(tv)+inDay(tv)

    ; ================================
    ; Corrections for v3.11:
    ; Change date for Askja
    if (date_volc(dt).eq.18750101) then
      print("Changed date for Askja")
      date_volc(dt)=18750329
    end if

    ; Change date for Pelee
    if (date_volc(dt).eq.19020506) then
      print("Changed date for Pelee")
      date_volc(dt)=19020508
      tv=indVolcs(t-1)
     end if

    if (date_volc(dt).eq.19020423) then
      ; print("Changed date for Pelee")
      ; date_volc(dt)=19020508
      tv=indVolcs(t+1)
      date_volc(dt)=10000*inYear(tv)+100*inMonth(tv)+inDay(tv)
    end if

    ; Change date for Calbuco
    if (date_volc(dt).eq.19310630) then
      print("Changed date for Calbuco")
      date_volc(dt)=19320630
    end if

    ; Change date for Bezymianny
    if (date_volc(dt).eq.19551022) then
      print("Changed date for Bezymianny")
      date_volc(dt)=19560330
    end if

    ; Change date for Agung
    if (date_volc(dt).eq.19630218) then
      print("Changed date for Agung")
      date_volc(dt)=19630317
    end if
    ; ================================

    if (t.gt.0) then
      if (date_volc(dt).lt.date_volc(dt-1)) then
        print("FATAL: eruption dates out of order "+date_volc(dt-1)+" "+date_volc(dt))
        exit
      end if
      if (date_volc(dt).eq.date_volc(dt-1)) then
        dt=dt-1
        print("repeat date "+date_volc(dt)+" "+volcName(tv-1)+", "+volcName(tv))
      end if
    end if

    date(t1:t4)=date_volc(dt)
    datesec(t1:t4)=(/43199, 43200, 64799, 64800/) ; 6-hour emissions from 12:00 to 18:00 UT

    SO2=inSO2(tv)
    VEI=toint(inVEI(tv))
    Lat=inLat(tv)
    Lon=inLon(tv)
    Top=inTop(tv)
    Bot=inBot(tv)
    Name=volcName(tv)
    if (Top.lt.Bot) then
      Top=inBot(tv)
      Bot=inTop(tv)
      print("Min/max altitudes swapped for "+Name+" "+date_volc(dt)+", fixing: Bot="+Bot+", Top="+Top)
    end if
  else
    print("t="+t+" dt="+dt+" nVolc="+nVolc+" t1="+t1+" t4="+t4)
    date_volc(dt)=newDate(t-nVolc)
    date(t1:t4)=date_volc(dt)
    datesec(t1:t4)=(/43199, 43200, 64799, 64800/) ; 6-hour emissions from 12:00 to 18:00 UT
    SO2=(/newSO2(t-nVolc)/)
    ; print(VEI)
    VEI=1
    Lat=(/newLat(t-nVolc)/)
    Lon=(/newLon(t-nVolc)/)
    Top=(/newTop(t-nVolc)/)
    Bot=(/newBot(t-nVolc)/)
    Name=(/newVolcName(t-nVolc)/)
  end if

  if (VEI.eq.5) then
    SO2=SO2*VEI5_factor
  end if

  if (VEI.eq.6) then
    SO2=SO2*VEI6_factor
  end if

  print("date: "+date_volc(tv)+" Lat: "+Lat+" Lon: "+Lon+" Name: "+Name)
  if (Lon.ge.360.or.Lat.gt.90.or.Lat.lt.-90.or.Lon.lt.0) then
    print("FATAL: latitude or longitude out of range")
    exit
  end if

  maskArr({Lat},{Lon})=1.0d0
  if (PinMinLat.ge.-90.and.t.eq.Pind) then
    maskArr({PinMinLat:Lat},{Lon})=1.0d0
    MinLat=(/PinMinLat/)
  else
    if (doVEIspread) then
      if (VEI.eq.5) then
        VolcArea=1.20d6 ; km2
      else
        VolcArea=2.76d6 ; km2
      end if
      VolcRadius=sqrt(VolcArea/PI)
      ; calculate Great Circle distance from eruption for each column:
      distance=gc_latlon(Lat,Lon,latArr,lonArr,2,4)
      ; select columns within radius defined by eruption area:
      maskArr=where(distance.le.VolcRadius,1.0d0,0.0d0)
    end if
    MinLat=(/Lat/)
  end if

  nCol=toint(sum(maskArr))
  ; print("t="+t+" tv="+tv+" nVolcTot="+nVolcTot)
  totalArea(t)=sum(columnArea*maskArr)
  totalAreaKm2 =  totalArea(t) / 1d10

  columnEmis=SO2/totalArea(t)/6./3600. ; Tg/cm2/s for 6-hour emission
  columnEmis=columnEmis*1e9*AVOGAD/MWSO2 ; molec/cm2/s
  depth=(Top-Bot)*1e5 ; emission depth in cm
  emisRate=columnEmis/depth ; molec/cm3/s

  if ((PinMinLat.ge.-90).or.(doVEIspread)) then
    outstring=\
      sprinti("%8.8i",date_volc(dt))+" "+\
        sprintf("%7.3f",MinLat)+" "+sprintf("%7.3f",Lat)+" "+sprintf("%7.3f",Lon)+" "+\
        sprintf("%6.3f",Bot)+" "+sprintf("%6.3f",Top)+" "+\
        sprintf("%7.4f",SO2)+"  "+VEI+"   "+sprinti("%3.0i",nCol)+"  "+\
        sprintf("%7.3e",totalAreaKm2)+" "+sprintf("%9.5e",emisRate)+" "+Name
  else
    outstring=\
      sprinti("%8.8i",date_volc(dt))+" "+\
        sprintf("%7.3f",Lat)+" "+sprintf("%7.3f",Lon)+" "+\
        sprintf("%6.3f",Bot)+" "+sprintf("%6.3f",Top)+" "+\
        sprintf("%7.4f",SO2)+"  "+VEI+"  "+\
        sprintf("%7.3e",totalAreaKm2)+" "+sprintf("%9.5e",emisRate)+" "+Name
  end if
  print((/outstring/))
  globalAtt@data_summary = globalAtt@data_summary+nl+outstring

  do k=0,nAlt-1
    ; print(k+" "+Bot+" "+altitude_int(k+1)+" "+Top+" "+altitude_int(k))
    if (Bot.lt.altitude_int(k+1).and.Top.ge.altitude_int(k)) then
      top=min((/Top,altitude_int(k+1)/))
      bot=max((/Bot,altitude_int(k)/))
      factor=todouble((top-bot)/(altitude_int(k+1)-altitude_int(k)))

      ; printVarSummary(maskArr)
      ; printVarSummary(stratvolc(t2,k,:,:))
      stratvolc(t2,k,:,:) = stratvolc(t2,k,:,:)+maskArr*emisRate*factor
      stratvolc(t3,k,:,:) = stratvolc(t2,k,:,:)

      ; print(stratvolc(t2,k,{Lat},{Lon}))
      ; print(maskArr({Lat},{Lon}))
      ; print(emisRate+" "+factor+" "+emisRate*factor)

    end if
  end do

  sumEmis=sum(stratvolc(t2,:,{Lat},{Lon}))*1d5 ; integrate column, vertical resolution 1 km = 1e5 cm
  ratio=sumEmis/columnEmis
  print(Name+" "+columnEmis+" "+sumEmis+" "+ratio+" "+Bot+" "+Top+" "+emisRate+" "+factor)

  if (abs(ratio-1.d0).ge.1e-6) then
    print("FATAL emission mismatch:")
    print("    "+Name+" columnEmis="+sprintf("%7.3e",columnEmis)+" sumEmis="+sprintf("%7.3e",sumEmis)+" ratio="+ratio)
    print("      Bot="+Bot+" Top="+Top+" emisRate="+emisRate)
    exit
  end if

  dt=dt+1

end do

dlast=t4+1
date(dlast)=99991231
datesec(dlast)=23*3600+1800

print("dates:"+dt+" eruptions:"+nVolcTot+" dlast="+dlast)

savefile=True
if (savefile) then

  creation_date=systemfunc("date +%Y%m%d-%H%M%S")
  outfilename=outfilename+"_"+res+"_c"+creation_date+".nc"
  outfile=outfilepath+outfilename
  if (fileexists(outfile)) then
    command="rm "+outfile
    print((/command/))
    system(command)
  end if

  print("creating "+outfile)
  ; setfileoption("nc","Format","LargeFile")
  setfileoption("nc","Format","NetCDF4Classic")
  ncid=addfile(outfile,"c")

  ; Create UNLIMITED Record Dimension
  ;  An UNLIMITED record dimension in a netCDF file is critical if the user
  ;  plans to ever use the netCDF operators (NCO) to concatenate the file
  ;  along the time/record dimension.
  filedimdef(ncid,"time",-1,True)

  ; Define global attributes.
  ; globalAtt can be of any type. Here logical is used by convention.
  globalAtt@input_method = "SERIAL" ; used per file if others are INTERP_MISSING_MONTHS
  globalAtt@data_script = nl+\
       "Converted from data_source_files by program "+get_script_name()+nl+\
       "SVN path to original: https://svn.code.sf.net/p/codescripts/code/trunk/ncl/emission"+nl+\
       "Edited version found in repository: https://github.com/engeir/volcano-cooking"
  globalAtt@cesm_contact = nl+\
      "Mike Mills, NCAR ACOM, mmills@ucar.edu"
  globalAtt@creation_date     = nl+\
      systemfunc("date")
  globalAtt@data_source_files = nl+\
      infile
  globalAtt@data_reference    = nl+\
      "Mills, M. J. et al. (2016), Global volcanic aerosol properties "+nl+\
      "     derived from emissions, 1990-2014, using CESM1(WACCM), "+nl+\
      "     J Geophys Res-Atmos, 121(5), 2332-2348, doi:10.1002/2015jd024290."+nl+\
      "Neely III, R.R.; Schmidt, A. (2016): VolcanEESM (Volcanic Emissions"+nl+\
      "     for Earth System Models): Volcanic sulphur dioxide (SO2) emissions"+nl+\
      "     database from 1850 to present. Centre for Environmental Data Analysis"
  globalAtt@data_source_url    = nl+\
      "http://catalogue.ceda.ac.uk/uuid/bfbd5ec825fa422f9a858b14ae7b2a0d"+nl+\
      "This file was generated from volcano-cooking at https://github.com/engeir/volcano-cooking"
  globalAtt@data_doi    = nl+\
      "10.5285/76ebdc0b-0eed-4f70-b89e-55e606bcd568"
  globalAtt@data_creator = nl+\
      "Ryan Neely, University of Leeds, UK, earrn@leeds.ac.uk, eruption database for 850-1976"+nl+\
      "Anja Schmidt University of Leeds, UK, a.schmidt@leeds.ac.uk, eruption database for 1977-present"+nl+\
      "Mike Mills, NCAR ACOM, mmills@ucar.edu"+nl+\
      "Eirik Rolland Enger, University of Tromsø, eirik.r.enger@uit.no, synthetic eruption database"
  globalAtt@title = nl+\
      "SO2 emissions from stratospheric volcanoes, "+inYear(0)+"."+inMonth(0)+"."+inDay(0)+"-"\
        +inYear(tv)+"."+inMonth(tv)+"."+inDay(tv)
      ; date(t4)
  globalAtt@filename = nl+\
      outfilename
  fileattdef( ncid, globalAtt )

  print("saving altitude_int")
  ncid!0="altitude_int"
  ncid&altitude_int=altitude_int
  print("saving date")
  ncid->date=date(0:dlast)
  print("saving datesec")
  ncid->datesec=datesec(0:dlast)

  print("converting stratvolc to float")
  stratvolcFloat=tofloat(stratvolc)
  stratvolcFloat@long_name = "SO2 elevated emissions from explosive volcanoes" ;
  stratvolcFloat@units = "molecules/cm3/s" ;
  stratvolcFloat@standard_name = "SO2 elevated emissions from explosive volcanoes" ;
  stratvolcFloat!0="time"
  stratvolcFloat!1="altitude"
  stratvolcFloat!2="lat"
  stratvolcFloat!3="lon"
  stratvolcFloat&altitude=altitude
  stratvolcFloat&lat=lat
  stratvolcFloat&lon=lon
  printVarSummary(stratvolcFloat)

  print("saving stratvolc")
  ncid->stratvolc=stratvolcFloat(0:dlast,:,:,:)

  print("File creation complete: "+outfile)

  delete(ncid)

end if
