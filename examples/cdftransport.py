from climaf.api import *

if not atCNRM: exit

# Declare "NEMO" project, both for Nemo raw outputs and for Monitoring outputs
# (with VT-files : mean values of vt, vs, ut, us for heat and salt transport)
#
cproject('NEMO')

# For 'standard' Nemo output files (actually, they are better accessible using project "EM")
root1="/cnrm/aster/data3/aster/senesi/NO_SAVE/expes/PRE6/${simulation}/O/"
suffix="${simulation}_1m_YYYYMMDD_YYYYMMDD_${variable}.nc"
url_nemo_standard=root1+suffix  

# For VT files from Monitoring
root2="/cnrm/aster/data3/aster/chevalli/Monitoring/PRE6/SORTIE/PRE6/${simulation}/MONITOR/VT/"
url_nemo_monitoring=root2+suffix
#
dataloc(project='NEMO', organization='generic', url=[url_nemo_standard,url_nemo_monitoring])
# 
# Declare how variables are scattered/groupes among files
# (and with mixed variable names conventions - CNRM and  MONITORING)
calias("NEMO","uo",filenameVar="grid_U_table2.3")
calias("NEMO","vo",filenameVar="grid_V_table2.3")
calias("NEMO","so",filenameVar="grid_T_table2.2")
calias("NEMO","thetao",filenameVar="grid_T_table2.2")

# Declare a special variable, composed of variables grouped in a file
products="vomevt,vomevs,vozout,vozous"
calias("NEMO",products,filenameVar="VT")

# Define defaults facets for datasets 
cdef("project","NEMO")
cdef("frequency","monthly")
cdef("simulation","PRE6CPLCr2alb")
cdef("period","199807")

# Define datasets 
duo=ds(variable="uo")
dvo=ds(variable="vo")
dx=ds(variable=products)

# Tell how to bring required fixed files to cdftransport
# this can be auto-adapted to model, project, simulation
tpath='/cnrm/aster/data3/aster/chevalli/Monitoring/MONITORING_v3.1/config/'
fixed_fields('ccdftransport',
             ('mask.nc',tpath+'ORCA1_mesh_mask.nc'),
             ('mesh_hgr.nc',tpath+'ORCA1_mesh_hgr.nc'),
             ('mesh_zgr.nc',tpath+'ORCA1_mesh_zgr.nc'))

# Compute transport
trsp=ccdftransport(dx,duo,dvo)

# Create files for the various cdftransport outputs
cfile(my_cdftransport)
cfile(my_cdftransport.htrp)
cfile(my_cdftransport.strp)

# Compute products another way, and transport 
dso=ds(variable="so")
dtho=ds(variable="thetao")
dx2=ccdfvT(duo,dvo,dso,dtho)
trsp2=ccdftransport(dx2,duo,dvo)

# A possible trick 
dut=ccdo(dx,operator="selname,vozout")