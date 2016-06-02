# -*- coding: utf-8 -*-
import recastdb.models as models
from flask import Flask
from frontendconfig import config as frontendconf
import uuid


from recastfrontend.server import app
with app.app_context():
    from recastfrontend.server import db
    db.create_all()

app.app_context().push()

christian = models.User(
    name='Christian Bora',
    email='borachristian@gmail.com'
    )

lukas = models.User(
    name='Lukas Heinrich',
    email='lukas.heinrich@cern.ch'
    )

db.session.add(christian)
db.session.commit()

db.session.add(lukas)
db.session.commit()

run_condition1 = models.RunCondition(
    name='7TeV',
    description='2.2/fb'
    )
db.session.add(run_condition1)
db.session.commit()

run_condition2 = models.RunCondition(
    name='8TeV', 
    description=' '
    )
db.session.add(run_condition2)
db.session.commit()


##### ----------------- ATLAS analysis 1 -------------------

analysis2 = models.Analysis(
    title='Search for massive supersymmetric particles decaying to many jets using the ATLAS detector in pp collisions at √s = 8 TeV',
    collaboration='ATLAS',
    e_print='arXiv:1502.05686',
    description='Results of a search for decays of massive particles to fully hadronic final states are presented. This search uses 20.3 fb−1 of data collected by the ATLAS detector in √s = 8 TeV proton–proton collisions at the LHC. Signatures based on high jet multiplicities without requirements on the missing transverse momentum are used to search for R-parity-violating supersymmetric gluino pair production with subsequent decays to quarks. The analysis is performed using a requirement on the number of jets, in combination with separate requirements on the number of b-tagged jets, as well as a topological observable formed from the scalar sum of the mass values of large-radius jets in the event. Results are interpreted in the context of all possible branching ratios of direct gluino decays to various quark flavors. No significant deviation is observed from the expected Standard Model backgrounds estimated using jet-counting as well as data- driven templates of the total-jet-mass spectra. Gluino pair decays to ten or more quarks via intermediate neutralinos are excluded for a gluino with mass mg ̃ < 1 TeV for a neutralino mass mχ ̃01 = 500 GeV. Direct gluino decays to six quarks are excluded for mg ̃ < 917 GeV for light-flavor final states, and results for various flavor hypotheses are presented.',
    owner_id=lukas.id,
    run_condition_id=run_condition1.id,
    uuid = '3cd5259a-6473-4616-9b86-23e609ce0f95'
)
db.session.add(analysis2)
db.session.commit()


###############
###############
##### ----------------- ATLAS analysis 1 REQUEST -------------------
###############
###############

request2 = models.ScanRequest(
    title="The ATLAS multijet search, 1502.05686", 
    description_of_model='stealth supersymmetry',
    reason_for_request='The ATLAS multijet search, 1502.05686, counts events with many jets. This inclusive strategy can be used to constrain any model with new particles with large cross sections that produce many jets. So far it has been interpreted in terms of 2 RPV scenarios. In order to assess the general coverage of the search, it would be interesting to recast more topologies. Stealth SUSY is an R-parity preserving SUSY framework that also leads to multijets, with low missing energy, but leads to different topologies with different phase space for jets and different numbers of jets than the RPV cases considered. No limits have been set on purely hadronic Stealth SUSY scenarios with prompt decays, so recasting 1502.05686 would allow for the first limits on these models. ',
    additional_information='Stealth SUSY is described in: 1105.5135 and 1201.4875. Existing LHC searches require photons (1210.2052) and/or leptons (1411.7255) or displaced decays (1504.03634), there have been no searches for the challenging case of prompt purely hadronic topologies. An LHE file will be provided upon request (contact: ruderman@nyu.edu). The first topology to consider is gluino decay to gluon + singlino, singlino decay to two jets plus soft gravitino (the left topology of figure 10 of 1201.4875). The parameters to vary are the gluino and singlino masses (fixing the singlet mass near the singlino mass). This leads to 3 jets on each side, but with different kinematics than the gluino > 3jet RPV topology. Additional topologies with more jets can also be considered. ', 
    analysis_id=analysis2.id,
    requester_id=christian.id, 
    zenodo_deposition_id="110959",
    uuid='56d3f353-a5aa-4c1a-a341-9efa1eefbb2d'
)

db.session.add(request2)
db.session.commit()

#####
##### ----------------- ATLAS analysis 1 ... add point requests -------------------
#####

point_request2 = models.PointRequest(
    scan_request_id=request2.id, 
    requester_id=christian.id
    )
db.session.add(point_request2)
db.session.commit()

point_coordinate2_1 = models.PointCoordinate(
    title = 'mGluino',
    value=250,
    point_request_id=point_request2.id
    )
db.session.add(point_coordinate2_1)
db.session.commit()

point_coordinate2_2 = models.PointCoordinate(
    title = 'mSinglino',
    value=500,
    point_request_id=point_request2.id
)
db.session.add(point_coordinate2_2)
db.session.commit()

#####
##### ----------------- ATLAS analysis 1 ... add basic requests -------------------
#####

basic_request2 = models.BasicRequest(
    point_request_id=point_request2.id,
    requester_id=christian.id
)
db.session.add(basic_request2)
db.session.commit()

zip_file2 = models.RequestArchive(
    file_name = "999f6d26-1171-11e6-a07c-3a398e598637",
    path = './',
    zenodo_file_id = "a537b4ec-4f8f-48c9-8f38-652a0fa20051",
    original_file_name = "db_populate_sample.txt",
    basic_request_id = basic_request2.id
    )
db.session.add(zip_file2)
db.session.commit()


###############
###############
##### ----------------- CMS analysis 4 -------------------
###############
###############


analysis4 = models.Analysis(
    title='Search for new physics with same-sign isolated dilepton events with jets and missing energy',
    collaboration='CMS',
    journal='CMS PAS SUS-11-010', 
    inspire_URL='http://cdsweb.cern.ch/record/1370064',
    description='The results of a search for new physics in events with two same-sign isolated leptons (electrons, muons, or hadronically decaying tau-leptons), hadronic jets, and missing transverse energy in the final state are presented. These results are based on analysis of a data sample with a corresponding integrated luminosity of 0.98~fb−1 produced in \Pp\Pp collisions at a center-of-mass energy of 7~TeV collected by the CMS experiment at the LHC. The observed numbers of events agree with the standard model predictions, and no evidence for new physics is found. These observations are used to set upper limits on the number of events from new physics contributions and to constrain supersymmetric models.',
    owner_id=lukas.id, 
    run_condition_id=run_condition2.id,
    uuid = 'b92bc3d1-cf6f-402f-9ae1-bf210842983c'
    )
db.session.add(analysis4)
db.session.commit()

