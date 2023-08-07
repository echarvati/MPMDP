import os
import sys

def build_system(workdir='workdir', path_mpmdp='mpmdp',Xbox='X', Ybox='Y', Zbox='Z', chain='chain', N='N', sigma='sigma',
                 length='length'):

    temps = os.path.join(path_mpmdp, 'templates')
    os.chdir(temps)

    with open('temp_build.txt', 'r') as build:
        contents_build = build.read()

    os.chdir(workdir)
    config = open('structure_paras.txt', 'w')


    if chain == True:
        struct = contents_build.replace('%Box_X%', Xbox).replace('%Box_Y%', Ybox).replace('%Box_Z%', Zbox)\
            .replace('%Polymer_Chain%', 'y').replace('%N%',N).replace('%Chain_Length%', length)\
            .replace('%sigma%', sigma).strip()
        config.write(struct)
        config.close()

    if chain == False:
        struct = contents_build.replace('%Box_X%', Xbox).replace('%Box_Y%', Ybox).replace('%Box_Z%', Zbox)\
            .replace('%Polymer_Chain%', 'n').replace('%N%',N).replace('%Chain_Length%', ' ')\
            .replace('%sigma%', sigma).strip()
        config.write(struct)
        config.close()

def write_controls(workdir='workdir', job_name='jobname', path_mpmdp='mpmdp',tstep='t-step', temp='temp',steps='steps', trj_out='trj_out', data_out='data_out', inter='inter',
                   thermostat='thermostat', SSP='SSP', MCsteps='MCsteps', MDsteps='MDsteps', k='k', r0='r0',
                   restart='restart', Collisions='Collisions', CellSize='CellSize', CollisionFreq='CollisionFreq',
                   CollisionAng='CollisionAng', Viscosity='Viscosity'):

    temps = os.path.join(path_mpmdp,'templates')
    os.chdir(temps)
    with open('temp_control.txt', 'r') as simu_temp:
        contents = simu_temp.read()

    os.chdir(workdir)
    simu_paras = 'control.txt'

    #Outpot names
    trj_file = '%s.xyz' %job_name
    log_file = '%s.dat' %job_name


    #Intermolecular parameters
    if inter == 'LJ_12_6':
        inter_params = [1.0, 1.0]
    elif inter=='original_hPF_Interactions':
        inter_params = [0.1, 8, 8, 8]

    #General features
    f = open(simu_paras, 'w')

    #Special features: SSP [OFF], MPCD[OFF]
    if SSP == False and Collisions==False :
        something = contents.replace('%timestep%', tstep).replace('%temperature%', temp).replace('%simu_steps%',steps)\
            .replace('%noutxyz%', trj_out).replace('%noutdat%', data_out).replace('%interaction_type%', inter) \
            .replace('%tjr_name%', trj_file).replace('%log_name%', log_file)\
            .replace('%interaction_paras%', (str(inter_params).strip('[').strip(']').replace(',', ''))) \
            .replace('%thermostat%', thermostat).replace('# Special features', '  ') \
            .replace('slip_springs %MDsteps% %MCsteps% %k% %r0% %restart% #MDstep MCstep k r0 restart[y/n]', '  ')\
            .replace('collisions MPCD %cell_size% %collision_freq% %collision_ang% #cell_size collision_freq collision_ang', ' ')\
            .strip()
        f.write(something)
        f.close()

    #Special features: SSP [ON], MPCD[OFF]
    elif SSP == True and Collisions==False :
        something = contents.replace('%timestep%', tstep).replace('%temperature%', temp).replace('%simu_steps%',steps)\
            .replace('%noutxyz%', trj_out).replace('%tjr_name%', trj_file).replace('%log_name%', log_file)\
            .replace('%noutdat%', data_out).replace('%interaction_type%', inter) \
            .replace('%interaction_paras%', (str(inter_params).strip('[').strip(']').replace(',', ''))) \
            .replace('%thermostat%', thermostat).replace('%MDsteps%', MDsteps).replace('%MCsteps%', MCsteps)\
            .replace('%k%', k).replace('%r0%', r0).replace('%restart%', restart)\
            .replace('collisions MPCD %cell_size% %collision_freq% %collision_ang% #cell_size collision_freq collision_ang', ' ') \
            .strip()
        f.write(something)
        f.close()

    #Special features: SSP [ON], MPCD[ON]
    elif SSP == True and Collisions == True :
        something = contents.replace('%timestep%', tstep).replace('%temperature%', temp).replace('%simu_steps%',steps)\
            .replace('%noutxyz%', trj_out).replace('%tjr_name%', trj_file).replace('%log_name%', log_file)\
            .replace('%noutdat%', data_out).replace('%interaction_type%', inter) \
            .replace('%interaction_paras%', (str(inter_params).strip('[').strip(']').replace(',', ''))) \
            .replace('%thermostat%', thermostat).replace('%MDsteps%', MDsteps).replace('%MCsteps%', MCsteps)\
            .replace('%k%', k).replace('%r0%', r0).replace('%restart%', restart).replace('%cell_size%', CellSize)\
            .replace('%collision_freq%', CollisionFreq).replace('%collision_ang%', CollisionAng).strip()
        f.write(something)
        f.close()

    # Special features: SSP [OFF], MPCD[ON]
    elif SSP == False and Collisions == True:
        something = contents.replace('%timestep%', tstep).replace('%temperature%', temp).replace('%simu_steps%', steps) \
            .replace('%noutxyz%', trj_out).replace('%tjr_name%', trj_file).replace('%log_name%', log_file)\
            .replace('%noutdat%', data_out).replace('%interaction_type%', inter) \
            .replace('%interaction_paras%', (str(inter_params).strip('[').strip(']').replace(',', ''))) \
            .replace('%thermostat%', thermostat)\
            .replace('slip_springs %MDsteps% %MCsteps% %k% %r0% %restart% #MDstep MCstep k r0 restart[y/n]', '  ' )\
            .replace('%cell_size%', CellSize).replace('%collision_freq%', CollisionFreq)\
            .replace('%collision_ang%', CollisionAng).strip()
        f.write(something)
        f.close()

def write_slurm(workdir='workdir',path_mpmdp='mpmdp', path_tools='tools', job_name='title'):

    temps = os.path.join(mpmdp, 'templates')
    os.chdir(temps)
    with open('temp_slurm.txt', 'r') as run_temp:
        contents_slurm = run_temp.read()

    path_make = os.path.join(path_tools, 'coords')

    os.chdir(workdir)
    slurm_script = '_run.sh'

    r = open(slurm_script, 'w')

    hello = contents_slurm.replace('%build_system%', path_make).replace('%source%', path_mpmdp)\
        .replace('%tools%', path_tools).replace('%this_is_a_job%', job_name)
    r.write(hello)
    r.close()

#########################################################################################################
#########################################################################################################
#########################################################################################################
#########################################################################################################

#Configuation paths
mpmdp='/home/echarvati/MPMDP/MPMDP/source/' #source
tools='/home/echarvati/MPMDP/MPMDP/tools/' #tools
workdir = os.getcwd() #current working directory

#Simulation

##Job ttle
job_name = 'test_build'

##Build system
X_box = '10'
Y_box = '10'
Z_box = '10'
Polymer_chain = False #chain switch
N = '200' #total number of particles
sigma = '1.0' #tolerance distance
Length = '20' #chain length

##MD parameters
tstep = '0.005'
temp = '1.0'
nstep = '100000'
trj_out = '1000'
data_out = '1000'
inter = 'LJ_12_6'
thermostat = 'Berendsen_Thermostat'

##Additional features
###SSP paarmters
SSP = False #switch
MCsteps = '10'
MDsteps = '500'
k = '20'
r0 = '2.0'
restart = 'n'

###MPDC parameters
Collisions = True #switch
CellSize = '2'
CollisionFreq = '1' #collisions happen ever N step
CollisionAng = '130'

###Viscosity
#TODO Add viscosity parameters
Viscosity = False #switch

#Write inputs

##Initial configuration
build_system(workdir=workdir, path_mpmdp=mpmdp,Xbox=X_box, Ybox=Y_box, Zbox=Z_box, chain=Polymer_chain, N=N,
             sigma=sigma, length=Length)

##Simulation control
write_controls(workdir=workdir,job_name=job_name, path_mpmdp=mpmdp,tstep=tstep, temp=temp, steps=nstep,trj_out=trj_out, data_out=data_out, inter=inter, thermostat=thermostat,
               SSP=SSP, MCsteps=MCsteps, MDsteps=MDsteps, k=k, r0=r0, restart=restart,
               Collisions=Collisions, CellSize=CellSize, CollisionFreq=CollisionFreq, CollisionAng=CollisionAng,
               Viscosity=Viscosity)

##Job file
write_slurm(workdir=workdir,path_mpmdp=mpmdp, path_tools=tools, job_name=job_name)

#Run
os.system('sbatch _run.sh')