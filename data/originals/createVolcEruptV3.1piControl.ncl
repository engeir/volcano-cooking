load "/home/een023/programs/miniconda3/ncl/lib/common.ncl"

massSO2thresh = 15 ; threshold (Tg) for eruptions scaled by MassFactor
;MassFactor = 2./3. ; scaling factor for large eruptions
MassFactor = 1/1.8 ; scaling factor for large eruptions

tab    = str_get_tab()

firstYear=1850
lastYear=2014
doMassScaling = True
doAltReduction = True
altSO2thresh = 3.5 ; threshold (Tg) for altitude reduction to 18-20 km

nYears=lastYear-firstYear+1
nSeconds=nYears*365.*24.*3600.

res=getenv("res")
if (ismissing(res)) then
  res="2deg"
  print("Horizontal resolution not set; defaulting to 2deg (1.9x2.5). For 0.95x1.25: setenv resolution 1deg")
end if

if (res.eq."2deg".or.res.eq."1.9x2.5") then
  templateFilename = getenv("COORDS2DEG")
else
  if (res.eq."1deg".or.res.eq."0.95x1.25") then
    templateFilename = getenv("COORDS1DEG")
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

SAearth_cm2=SAearth*10000 ; Earth surface area in cm2

columnArea=conform(new((/ nLat, nLon /), double), gw, 0)
columnArea=columnArea*SAearth_cm2/nLon/sum(gw) ; area of each grid column in cm2
columnArea!0="lat"
columnArea!1="lon"
columnArea&lat=lat
columnArea&lon=lon

print("SAearth_cm2="+SAearth_cm2+"; sum(columnArea)="+sum(columnArea))

filepath=getenv("SYNTH_FILE_DIR")+"/"
outfilepath=getenv("DATA_OUT")+"/"

infilename = getenv("SYNTH_BASE")
infiletype = getenv("SYNTH_EXT")

outfilename="VolcanEESMvEnger_piControl_SO2_"+firstYear+"-"+lastYear+"average"

globalAtt = True
; For a nicer looking netCDF, create a "new line" character.
nl = integertochar(10)  ; newline character

globalAtt@data_summary = nl+\
    "Constant SO2 emissions from eruptive volcanoes, "+firstYear+"-"+lastYear+" average" +nl+\
    "Emissions in this file include only the climatically relevant SO2, after initial loss removed."

infile=filepath+infilename+"."+infiletype

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

; Adjust altitude range for SO2>5Tg if max altitude > 20 km
if (doAltReduction) then
  ; return indices if True: (inSO2 >= altSO2thresh) and (inTop > 20) and (inYear >= firstYear) and (inYear =< lastYear)
  AltInd=ind(inSO2.ge.altSO2thresh.and.inTop.gt.20.0.and.inYear.ge.firstYear.and.inYear.le.lastYear)
  if (.not.(ismissing(AltInd(0)))) then
    print("Adjusting altitude range for "+inYear(AltInd)+"-"+inMonth(AltInd)+"-"+inDay(AltInd)+" "+volcName(AltInd))
    globalAtt@data_summary = globalAtt@data_summary + nl +\
        "Altitude range adjusted for SO2>"+altSO2thresh+"Tg if max altitude > 20 km:"
    do i = 0,dimsizes(AltInd)-1
      globalAtt@data_summary = globalAtt@data_summary + nl +\
        "     "+inYear(AltInd(i))+"-"+inMonth(AltInd(i))+"-"+inDay(AltInd(i))+" "+volcName(AltInd(i))
    end do
    inTop(AltInd)=20.0
    inBot(AltInd)=where(inBot(AltInd).gt.18.0,18.0,inBot(AltInd))

  end if
end if

; Adjust SO2 mass for SO2>15 Tg
if (doMassScaling) then
  SO2Ind=ind(inSO2.ge.massSO2thresh.and.inYear.ge.firstYear.and.inYear.le.lastYear)
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
end if

; Shift longitude from -180,180 to 0,360
inLon=where(inLon.ge.0,inLon,inLon+360.)

indVolcs=ind(inSO2.gt.0.and.inYear.ge.firstYear.and.inYear.le.lastYear)
;printVarSummary(indVolc)
nVolc=dimsizes(indVolcs)
;print(nVolc)
nVolcTot=nVolc
;print(nVolcTot)

;date=(/101,99991231/)
date=(/18500116, 18500216, 18500316, 18500416, 18500516, 18500616, 18500716, \
    18500816, 18500916, 18501016, 18501116, 18501216/)
date!0="time"
date@long_name = "date" ;
date@units = "YYYYMMDD" ;
date@standard_name = "date" ;
nTimes=dimsizes(date)

altitude = todouble(fspan(1,31,31))
altitude!0="altitude"
altitude@long_name = "altitude midlevel" ;
altitude@units = "km" ;
altitude@standard_name = "altitude midlevel" ;

altitude_int = todouble(fspan(0.5,31.5,32))
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
;printVarSummary(stratvolc)

latArr=conform_dims((/nLat,nLon/),lat,0)
lonArr=conform_dims((/nLat,nLon/),lon,1)
maskArr=new((/nLat,nLon/),double)
maskArr!0="lat"
maskArr!1="lon"
maskArr&lat=lat
maskArr&lon=lon

outstring = "This file is for the following volcanoes:"
print((/outstring/))
globalAtt@data_summary = globalAtt@data_summary + nl +\
    "======================================================================" + nl \
    + outstring

outstring = "YYYYMMDD  Lat    Lon     AltMin AltMax SO2(Tg) VEI Area(km2) Em(cm-3s-1) Name"

print((/outstring/))
globalAtt@data_summary = globalAtt@data_summary + nl + outstring

totalArea=new(nVolcTot,double)
SO2_total=0.0
do t=0,nVolcTot-1
  maskArr(:,:)=0.0d0
  tv=indVolcs(t)
;  print(tv)
  SO2=inSO2(tv)
  SO2_total=SO2_total+SO2
  VEI=toint(inVEI(tv))
  Lat=inLat(tv)
  Lon=inLon(tv)
  Top=inTop(tv)
  Bot=inBot(tv)
  Name=volcName(tv)
;  print(inYear(tv))
;  print(inMonth(tv))
;  printVarSummary(inDay)
  date_volc=10000*toint(inYear(tv))+100*toint(inMonth(tv))+toint(inDay(tv))
;  printVarSummary(date_volc)
  maskArr({Lat},{Lon})=1.0d0
  totalArea(t)=sum(columnArea*maskArr)
  totalAreaKm2 =  totalArea(t) / 1d10
  columnEmis=SO2/totalArea(t)/nSeconds ; Tg/cm2/s (averaged over historical period)
  columnEmis=columnEmis*1e9*AVOGAD/MWSO2 ; molec/cm2/s
  depth=(Top-Bot)*1e5 ; emission depth in cm
  emisRate=columnEmis/depth ; molec/cm3/s

;  printVarSummary(Lat)
;  printVarSummary(Lon)
;  printVarSummary(Bot)
;  printVarSummary(Top)
;  printVarSummary(SO2)
;  printVarSummary(VEI)
;  printVarSummary(totalAreaKm2)
;  printVarSummary(emisRate)

  outstring=\
    sprinti("%8.8i",date_volc)+" "+\
      sprintf("%7.3f",Lat)+" "+sprintf("%7.3f",Lon)+" "+\
      sprintf("%6.3f",Bot)+" "+sprintf("%6.3f",Top)+" "+\
      sprintf("%7.4f",SO2)+"  "+VEI+"  "+\
      sprintf("%7.3e",totalAreaKm2)+" "+sprintf("%9.5e",emisRate)+" "+Name
  print((/outstring/))
  globalAtt@data_summary = globalAtt@data_summary+nl+outstring

  do k=0,nAlt-1
;    print(k+" "+Bot+" "+altitude_int(k+1)+" "+Top+" "+altitude_int(k))
    if (Bot.lt.altitude_int(k+1).and.Top.ge.altitude_int(k)) then
      top=min((/Top,altitude_int(k+1)/))
      bot=max((/Bot,altitude_int(k)/))
      factor=todouble((top-bot)/(altitude_int(k+1)-altitude_int(k)))
      stratvolc(0,k,:,:) = stratvolc(0,k,:,:)+maskArr*emisRate*factor
    end if
  end do
end do

; Initial year is repeated
do i = 1,nTimes-1
  stratvolc(i,:,:,:)=stratvolc(0,:,:,:)
end do

SO2_per_year=SO2_total/nYears

title="Time-averaged SO2 emissions from stratospheric volcanoes, "+firstYear+"-"+lastYear+nl+\
      SO2_total+" Tg SO2 emitted over "+nYears+" years = "+SO2_per_year+" Tg/year"
print((/title/))

savefile=True
if (savefile) then

  creation_date=systemfunc("date +%Y%m%d")
  outfilename=outfilename+"_"+res+"_c"+creation_date+".nc"
  outfile=outfilepath+outfilename
  if (fileexists(outfile)) then
    command("rm "+outfile)
  end if

  print("creating "+outfile)
  ncid=addfile(outfile,"c")

  ;Create UNLIMITED Record Dimension
  ;  An UNLIMITED record dimension in a netCDF file is critical if the user
  ;  plans to ever use the netCDF operators (NCO) to concatenate the file
  ;  along the time/record dimension.
  filedimdef(ncid,"time",-1,True)

  ; Define global attributes.
  ; globalAtt can be of any type. Here logical is used by convention.
  globalAtt@data_script = nl+\
       "Converted from data_source_files by program "+get_script_name()+nl+\
       "SVN path: https://svn.code.sf.net/p/codescripts/code/trunk/ncl/emission"
  globalAtt@cesm_contact = nl+"Mike Mills, NCAR ACOM, mmills@ucar.edu"
  globalAtt@creation_date     = nl+systemfunc("date")
  globalAtt@data_source_files = nl+infile
  globalAtt@data_reference    = nl+\
      "Mills, M. J. et al. (2016), Global volcanic aerosol properties "+nl+\
      "     derived from emissions, 1990-2014, using CESM1(WACCM), "+nl+\
      "     J Geophys Res-Atmos, 121(5), 2332-2348, doi:10.1002/2015jd024290."+nl+\
      "Neely III, R.R.; Schmidt, A. (2016): VolcanEESM (Volcanic Emissions"+nl+\
      "     for Earth System Models): Volcanic sulphur dioxide (SO2) emissions"+nl+\
      "     database from 1850 to present. Centre for Environmental Data Analysis"
  globalAtt@data_source_url    = nl+\
      "http://catalogue.ceda.ac.uk/uuid/bfbd5ec825fa422f9a858b14ae7b2a0d"
  globalAtt@data_doi    = nl+\
      "10.5285/76ebdc0b-0eed-4f70-b89e-55e606bcd568"
  globalAtt@data_creator = nl+\
      "Ryan Neely, University of Leeds, UK, earrn@leeds.ac.uk, eruption database for 1850-1976"+nl+\
      "Anja Schmidt University of Leeds, UK, a.schmidt@leeds.ac.uk, eruption database for 1977-present"+nl+\
      "Mike Mills, NCAR ACOM, mmills@ucar.edu"
  globalAtt@title = nl+title
  globalAtt@filename = nl+outfilename
  fileattdef( ncid, globalAtt )

  print("saving altitude_int")
  ncid->altitude_int=altitude_int
  print("saving date")
  ncid->date=date

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
  ncid->stratvolc=stratvolcFloat

  print("File creation complete: "+outfile)

  delete(ncid)

end if
