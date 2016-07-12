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

user1 = models.User(
    name='Christian Bora',
    email='borachristian@gmail.com'
    )
db.session.add(user1)
db.session.commit()


user2 = models.User(
    name='Admin',
    email='admin@recast',
    orcid_id = 'example123'
    )
db.session.add(user2)
db.session.commit()

token = models.AccessToken(
    token = 'abcdef',
    token_name = 'master token',
    user_id = user2.id
    )
db.session.add(user2)
db.session.commit()
    

run_condition1 = models.RunCondition(
    name='7TeV',
    description='2.2/fb'
    )
db.session.add(run_condition1)
db.session.commit()

analysis1 = models.Analysis(
    title='Search for New Physics in the Paired Dijet Mass Spectrum',
    collaboration='CMS',
    e_print='http://cdsweb.cern.ch/record/1416058/',
    description="We report on a search for pair-produced particles both decaying into two jets, based on a data sample of 2.2/fb of proton-proton collisions collected at √s=7 TeV with the CMS detector at the LHC. We select events with at least four jets, require pairs of dijets with equal mass, and search for pair production of new particles. We set upper limits on the product of the resonance cross section, branching fraction into dijets, and acceptance. The cross section limit is compared with the predictions of a model of pair-produced colorons in which each coloron decays to qq~. We exclude pair production of colorons with mass between 320 and 580 GeV at 95% confidence level.",
    owner_id=user1.id, 
    run_condition_id=run_condition1.id, 
    doi="DOI:/example",
    uuid=str(uuid.uuid4())
    )
db.session.add(analysis1)
db.session.commit()

##
run_condition2 = models.RunCondition(
    name='8TeV', 
    description=' '
    )
db.session.add(run_condition2)
db.session.commit()

analysis2 = models.Analysis(
    title='Search for massive supersymmetric particles decaying to many jets using the ATLAS detector in pp collisions at √s = 8 TeV',
    collaboration='ATLAS',
    e_print='http://recast.perimeterinstitute.ca/1502.05686',
    description='Results of a search for decays of massive particles to fully hadronic final states are presented. This search uses 20.3 fb−1 of data collected by the ATLAS detector in √s = 8 TeV proton–proton collisions at the LHC. Signatures based on high jet multiplicities without requirements on the missing transverse momentum are used to search for R-parity-violating supersymmetric gluino pair production with subsequent decays to quarks. The analysis is performed using a requirement on the number of jets, in combination with separate requirements on the number of b-tagged jets, as well as a topological observable formed from the scalar sum of the mass values of large-radius jets in the event. Results are interpreted in the context of all possible branching ratios of direct gluino decays to various quark flavors. No significant deviation is observed from the expected Standard Model backgrounds estimated using jet-counting as well as data- driven templates of the total-jet-mass spectra. Gluino pair decays to ten or more quarks via intermediate neutralinos are excluded for a gluino with mass mg ̃ < 1 TeV for a neutralino mass mχ ̃01 = 500 GeV. Direct gluino decays to six quarks are excluded for mg ̃ < 917 GeV for light-flavor final states, and results for various flavor hypotheses are presented.',
    owner_id=user1.id,
    run_condition_id=run_condition2.id,
    uuid = str(uuid.uuid4())
    )
db.session.add(analysis2)
db.session.commit()

request2 = models.ScanRequest(
    title="The ATLAS multijet search, 1502.05686", 
    description_of_model='stealth supersymmetry',
    reason_for_request='The ATLAS multijet search, 1502.05686, counts events with many jets. This inclusive strategy can be used to constrain any model with new particles with large cross sections that produce many jets. So far it has been interpreted in terms of 2 RPV scenarios. In order to assess the general coverage of the search, it would be interesting to recast more topologies. Stealth SUSY is an R-parity preserving SUSY framework that also leads to multijets, with low missing energy, but leads to different topologies with different phase space for jets and different numbers of jets than the RPV cases considered. No limits have been set on purely hadronic Stealth SUSY scenarios with prompt decays, so recasting 1502.05686 would allow for the first limits on these models. ',
    additional_information='Stealth SUSY is described in: 1105.5135 and 1201.4875. Existing LHC searches require photons (1210.2052) and/or leptons (1411.7255) or displaced decays (1504.03634), there have been no searches for the challenging case of prompt purely hadronic topologies. An LHE file will be provided upon request (contact: ruderman@nyu.edu). The first topology to consider is gluino decay to gluon + singlino, singlino decay to two jets plus soft gravitino (the left topology of figure 10 of 1201.4875). The parameters to vary are the gluino and singlino masses (fixing the singlet mass near the singlino mass). This leads to 3 jets on each side, but with different kinematics than the gluino > 3jet RPV topology. Additional topologies with more jets can also be considered. ', 
    analysis_id=analysis2.id,
    requester_id=user1.id, 
    zenodo_deposition_id="110959",
    uuid=str(uuid.uuid4())
    )
db.session.add(request2)
db.session.commit()

point_request2 = models.PointRequest(
    scan_request_id=request2.id, 
    requester_id=user1.id,
    uuid = str(uuid.uuid4())
    )
db.session.add(point_request2)
db.session.commit()

point_coordinate2 = models.PointCoordinate(
    value=21.21,
    point_request_id=point_request2.id
    )
db.session.add(point_coordinate2)
db.session.commit()

basic_request2 = models.BasicRequest(
    point_request_id=point_request2.id,
    requester_id=user1.id
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

scan_response2 = models.ScanResponse(
    scan_request_id = request2.id,
    uuid = str(uuid.uuid4())
    )
db.session.add(scan_response2)
db.session.commit()

parameter_response2 = models.PointResponse(
    uuid = str(uuid.uuid4()),
    lower_1sig_expected_CLs = 1.2,
    lower_2sig_expected_CLs = 0.2,
    expected_CLs = 21.1,
    upper_1sig_expected_CLs = 21.2,
    upper_2sig_expected_CLs = 12.1,
    observed_CLs = 21.3,
    log_likelihood_at_reference = 21.1,
    scan_response_id = scan_response2.id,
    point_request_id = point_request2.id
    )
db.session.add(parameter_response2)
db.session.commit()


basic_response2 = models.BasicResponse(
    uuid = str(uuid.uuid4()),
    lower_1sig_expected_CLs = 9.2,
    lower_2sig_expected_CLs = 121.12,
    expected_CLs = 21.1,
    upper_1sig_expected_CLs = 1.1,
    upper_2sig_expected_CLs = 1.4,
    observed_CLs = 21.2,
    log_likelihood_at_reference = 3.21,
    point_response_id =  parameter_response2.id,
    basic_request_id = basic_request2.id
    )
db.session.add(basic_response2)
db.session.commit()

parameter_archive2 = models.ResponseArchive(
    file_name = "999f6d26-1171-11e6-a07c-3a398e598637",
    file_path = './',
    original_file_name = "sample_response_file.txt",
    point_response_id = parameter_response2.id
    )
db.session.add(parameter_archive2)
db.session.commit()

basic_archive2 = models.ResponseArchive(
    file_name = "999f6d26-1171-11e6-a07c-3a398e598637",
    file_path = './',
    original_file_name = "sample_response_file.txt",
    basic_response_id = basic_response2.id
    )
db.session.add(basic_archive2)
db.session.commit()
    


##
run_condition3 = models.RunCondition(
    name='8TeV',
    description='20.1 fb-1 of pp collisions at sqrt{s}=8TeV'
    )
db.session.add(run_condition3)
db.session.commit()

analysis3 = models.Analysis(
    title='Search for direct third-generation squark pair production in final states with missing transverse momentum and two b-jets in √s= 8 TeV pp collisions with the ATLAS detector',
    collaboration='ATLAS',
    e_print='http://arxiv.org/abs/arXiv:1308.2631', 
    journal='JHEP 1310 (2013) 189 (2013)', 
    inspire_URL='http://inspirehep.net/record/1247462', 
    doi='10.1007/JHEP10(2013)189', 
    description='The results of a search for pair production of supersymmetric partners of the Standard Model third-generation quarks are reported. This search uses 20.1 fb-1 of pp collisions at sqrt{s}=8 TeV collected by the ATLAS experiment at the Large Hadron Collider. The lightest bottom and top squarks (b1 and t1 respectively) are searched for in a final state with large missing transverse momentum and two jets identified as originating from b-quarks. No excess of events above the expected level of Standard Model background is found. The results are used to set upper limits on the visible cross section for processes beyond the Standard Model. Exclusion limits at the 95% confidence level on the masses of the third-generation squarks are derived in phenomenological supersymmetric R-parity-conserving models in which either the bottom or the top squark is the lightest squark. The b1 is assumed to decay via b1->b chi0 and the t via t1->b chipm, with undetectable products of the subsequent decay of the chipm due to the small mass splitting between the chipm and the chi0.',
    owner_id=user1.id,
    run_condition_id=run_condition3.id,
    uuid=str(uuid.uuid4())
    )
db.session.add(analysis3)
db.session.commit()

request3 = models.ScanRequest(
    title="my title for request 3",
    description_of_model='3-body decay of sbottom into b-quark and two invisible final states',
    reason_for_request="Reinterpretation of analysis for 3-body decay topology of sbottoms, sb -> b chi chi', where chi and chi' are invisible decay products. For motivation, see arXiv:1312.4965. ',", 
    additional_information='Additional files can be provided upon request.', 
    analysis_id=analysis3.id, 
    requester_id=user1.id,
    zenodo_deposition_id="110959", 
    uuid=str(uuid.uuid4())
    )
db.session.add(request3)
db.session.commit()

point_request3 = models.PointRequest(
    scan_request_id=request3.id,
    requester_id=user1.id,
    uuid = str(uuid.uuid4())
    )
db.session.add(point_request3)
db.session.commit()

point_coordinate3  = models.PointCoordinate(
    value = 121.131,
    point_request_id = point_request3.id,
    )
db.session.add(point_coordinate3)
db.session.commit()

basic_request3 = models.BasicRequest(
    point_request_id=point_request3.id, 
    requester_id=user1.id,
    )
db.session.add(basic_request3)
db.session.commit()

zip_file3 = models.RequestArchive(
    file_name = "999f6d26-1171-11e6-a07c-3a398e598637",
    path = './',
    zenodo_file_id = "a537b4ec-4f8f-48c9-8f38-652a0fa20051",
    original_file_name = "db_populate_sample.txt",
    basic_request_id = basic_request3.id
    )
db.session.add(zip_file3)
db.session.commit()

##
run_condition4 = models.RunCondition(
    name='7TeV', 
    description=''
    )
db.session.add(run_condition4)
db.session.commit()

analysis4 = models.Analysis(
    title='Search for new physics with same-sign isolated dilepton events with jets and missing energy',
    collaboration='CMS',
    journal='CMS PAS SUS-11-010', 
    inspire_URL='http://cdsweb.cern.ch/record/1370064',
    description='The results of a search for new physics in events with two same-sign isolated leptons (electrons, muons, or hadronically decaying tau-leptons), hadronic jets, and missing transverse energy in the final state are presented. These results are based on analysis of a data sample with a corresponding integrated luminosity of 0.98~fb−1 produced in \Pp\Pp collisions at a center-of-mass energy of 7~TeV collected by the CMS experiment at the LHC. The observed numbers of events agree with the standard model predictions, and no evidence for new physics is found. These observations are used to set upper limits on the number of events from new physics contributions and to constrain supersymmetric models.',
    owner_id=user1.id, 
    run_condition_id=run_condition4.id,
    uuid=str(uuid.uuid4())
    )
db.session.add(analysis4)
db.session.commit()

request4 = models.ScanRequest(
    title="title for request 4", 
    description_of_model='Sbottom -> Stop Cascade Decay', 
    reason_for_request='Natural supersymmetry, which cancels the largest divergences in the Higgs mass in the Standard Model, favors spectra with light scalar top quarks. In particular, the left-handed scalar top is associated with the left-handed scalar bottom quark, which should also be light. Spectra with a decay chain sbottom -> stop + W followed by stop -> top + neutralino or gravitino can give rise to same-sign leptons. Thus, it would be worthwhile to reanalyze the same-sign lepton searches to understand how they can constrain natural supersymmetry. (See also request 1203.0026.)', 
    additional_information='I will provide ZIP files upon request', 
    analysis_id=analysis4.id, 
    requester_id=user1.id, 
    zenodo_deposition_id="110959", 
    uuid=str(uuid.uuid4())
    )
db.session.add(request4)
db.session.commit()

point_request4 = models.PointRequest(
    scan_request_id=request4.id, 
    requester_id=user1.id,
    uuid=str(uuid.uuid4())
    )
db.session.add(point_request4)
db.session.commit()

point_coordinate4 = models.PointCoordinate(
    value = 121.3423,
    point_request_id = point_request4.id
    )
db.session.add(point_coordinate4)
db.session.commit()

basic_request4 = models.BasicRequest(
    point_request_id=point_request4.id, 
    requester_id=user1.id
    )
db.session.add(basic_request4)
db.session.commit()

zip_file4 = models.RequestArchive(
    file_name = "999f6d26-1171-11e6-a07c-3a398e598637",
    path = "./",
    zenodo_file_id = "a537b4ec-4f8f-48c9-8f38-652a0fa20051",
    original_file_name = "db_populate_sample.txt",
    basic_request_id = basic_request4.id
    )
db.session.add(zip_file4)
db.session.commit()

scan_response4 = models.ScanResponse(
    uuid = str(uuid.uuid4()),
    scan_request_id = request4.id
    )
db.session.add(scan_response4)
db.session.commit()

parameter_response4 = models.PointResponse(
    uuid = str(uuid.uuid4()),
    lower_1sig_expected_CLs = 12.1,
    lower_2sig_expected_CLs = 21.4,
    expected_CLs = 0.1,
    upper_1sig_expected_CLs = 14.12,
    upper_2sig_expected_CLs = 32.1,
    observed_CLs = 21.1,
    log_likelihood_at_reference = 21.2,
    scan_response_id = scan_response4.id,
    point_request_id = point_coordinate4.id
    )
db.session.add(parameter_response4)
db.session.commit()

basic_response4 = models.BasicResponse(
    uuid = str(uuid.uuid4()),
    lower_1sig_expected_CLs = 1.2,
    lower_2sig_expected_CLs = 21.3,
    expected_CLs = 21.3,
    upper_1sig_expected_CLs = 3.3,
    upper_2sig_expected_CLs = 32.3,
    observed_CLs = 32.3,
    log_likelihood_at_reference = 32.3,
    point_response_id = parameter_response4.id,
    basic_request_id = basic_request4.id
    )
db.session.add(basic_response4)
db.session.commit()

parameter_archive4 = models.ResponseArchive(
    file_name = "999f6d26-1171-11e6-a07c-3a398e598637",
    file_path = './',
    original_file_name = "db_populate_sample.txt",
    point_response_id = parameter_response4.id
    )
db.session.add(parameter_archive4)
db.session.commit()

basic_archive4 = models.ResponseArchive(
    file_name = "999f6d26-1171-11e6-a07c-3a398e598637",
    file_path = './',
    original_file_name = "db_populate_sample.txt",
    basic_response_id = basic_response4.id
    )
db.session.add(basic_archive4)
db.session.commit()


request4_2 = models.ScanRequest(
    title="title for request 4.2",
    description_of_model='Naturally evasive SUSY',
    reason_for_request='Gluinos that result in classic large missing transverse momentum signatures at the LHC have been excluded by 2011 searches if they are lighter than around 800 GeV. This adds to the tension between experiment and supersymmetric solutions of the naturalness problem, since the gluino is required to be light if the electroweak scale is to be natural. Here, we examine natural scenarios where supersymmetry is present, but was hidden from 2011 searches due to violation of $R$-parity and the absence of a large missing transverse momentum signature. Naturalness suggests that third generation states should dominate gluino decays and we argue that this leads to a generic signature in the form of same-sign, flavour-ambivalent leptons, without large missing transverse momentum. As a result, searches in this channel are able to cover a broad range of scenarios with some generality and one should seek gluinos that decay in this way with masses below a TeV. We encourage the LHC experiments to tailor a search for supersymmetry in this form. We consider a specific case that is good at hiding: baryon number violation. The only light sparticles are right-handed stops and gluinos. ',
    additional_information='Request follows http://arxiv.org/abs/1202.6616', 
    analysis_id=analysis4.id, 
    requester_id=user1.id, 
    zenodo_deposition_id="110959", 
    uuid=str(uuid.uuid4())
    )
db.session.add(request4_2)
db.session.commit()

point_request4_2 = models.PointRequest(
    scan_request_id=request4_2.id,
    requester_id=user1.id,
    uuid=str(uuid.uuid4())
    )
db.session.add(point_request4_2)
db.session.commit()

point_coordinate4_2= models.PointCoordinate(
    value = 2121.21,
    point_request_id = point_request4_2.id
    )
db.session.add(point_coordinate4_2)
db.session.commit()

basic_request4_2 = models.BasicRequest(
    point_request_id=point_request4_2.id, 
    requester_id=user1.id
    )
db.session.add(basic_request4_2)
db.session.commit()

zip_file4_2 = models.RequestArchive(
    file_name = "999f6d26-1171-11e6-a07c-3a398e598637",
    path = './',
    zenodo_file_id = "a537b4ec-4f8f-48c9-8f38-652a0fa20051",
    basic_request_id = basic_request4_2.id
    )
db.session.add(zip_file4_2)
db.session.commit()

scan_response4_2 = models.ScanResponse(
    uuid = str(uuid.uuid4()),
    scan_request_id = request4_2.id
    )
db.session.add(scan_response4_2)
db.session.commit()

parameter_response4_2 = models.PointResponse(
    uuid = str(uuid.uuid4()),
    lower_1sig_expected_CLs = 12.2,
    lower_2sig_expected_CLs = 10.1,
    expected_CLs = 32.1,
    upper_1sig_expected_CLs = 32.3,
    upper_2sig_expected_CLs = 43.4,
    observed_CLs = 32.3,
    log_likelihood_at_reference = 21.2,
    scan_response_id = scan_response4_2.id,
    point_request_id = point_request4_2.id
    )
db.session.add(parameter_response4_2)
db.session.commit()

basic_response4_2 = models.BasicResponse(
    uuid = str(uuid.uuid4()),
    lower_1sig_expected_CLs = 21.2,
    lower_2sig_expected_CLs = 32.1,
    expected_CLs = 32.2,
    upper_1sig_expected_CLs = 32.2,
    upper_2sig_expected_CLs = 45.3,
    observed_CLs = 32.2,
    log_likelihood_at_reference = 32.1,
    point_response_id = parameter_response4_2.id,
    basic_request_id = basic_request4_2.id
    )
db.session.add(basic_response4_2)
db.session.commit()

parameter_archive4_2 = models.ResponseArchive(
    file_name = "999f6d26-1171-11e6-a07c-3a398e598637",
    file_path = './',
    original_file_name = "sample_file.txt",
    point_response_id = parameter_response4_2.id
    )
db.session.add(parameter_archive4_2)
db.session.commit()

basic_archive4_2 = models.ResponseArchive(
    file_name = "999f6d26-1171-11e6-a07c-3a398e598637",
    file_path = './',
    original_file_name = "db_populate_sample.txt",
    basic_response_id = basic_response4_2.id
    )
db.session.add(basic_archive4_2)
db.session.commit()


##
run_condition5 = models.RunCondition(
    name='7TeV'
    )
db.session.add(run_condition5)
db.session.commit()

analysis5 = models.Analysis(
    title='Search for anomalous production of prompt like-sign muon pairs and constraints on physics beyond the Standard Model with the ATLAS detector', 
    collaboration='ATLAS',
    e_print='unknown', 
    journal='Phys. Rev. D 88 (2012) 032004 ', 
    inspire_URL='http://inspirehep.net/search?p=find%20eprint%201201.109',
    description='An inclusive search for anomalous production of two prompt, isolated muons with the same electric charge is presented. The search is performed in a data sample corresponding to 1.6 fb^-1 of integrated luminosity collected in 2011 at sqrt(s) = 7 TeV with the ATLAS detector at the LHC. Muon pairs are selected by requiring two isolated muons of the same electric charge with pT > 20 GeV and abs(eta) < 2.5. Minimal requirements are placed on the rest of the event activity. The distribution of the invariant mass of the muon pair m(mumu) is found to agree well with the background expectation. Upper limits on the cross section for anomalous production of two muons with the same electric charge are placed as a function of m(mumu) within a fiducial region defined by the event selection. The fiducial cross- section limit constrains the like-sign top-quark pair-production cross section to be below 3.7 pb at 95% confidence level. The data are also analyzed to search for a narrow like-sign dimuon resonance as predicted for e.g. doubly charged Higgs bosons (H++/H--). Assuming pair production of H++/H-- bosons and a branching ratio to muons of 100% (33%), this analysis excludes masses below 355 (244) GeV and 251 (209) GeV for H++/H-- bosons coupling to left-handed and right-handed fermions, respectively.',
    owner_id=user1.id, 
    run_condition_id=run_condition5.id,
    uuid=str(uuid.uuid4())
    )
db.session.add(analysis5)
db.session.commit()

request5 = models.ScanRequest(
    title="title for request 5",
    description_of_model='Sbottom -> Stop Cascade Decay',
    reason_for_request='Natural supersymmetry, which cancels the largest divergences in the Higgs mass in the Standard Model, favors spectra with light scalar top quarks. In particular, the left-handed scalar top is associated with the left-handed scalar bottom quark, which should also be light. Spectra with a decay chain sbottom -> stop + W followed by stop -> top + neutralino or gravitino can give rise to same-sign leptons. Thus, it would be worthwhile to reanalyze the same-sign lepton searches to understand how they can constrain natural supersymmetry. (See also request 1203.0026.)',
    additional_information='I will provide LHE files upon request', 
    analysis_id=analysis5.id, 
    requester_id=user1.id,
    zenodo_deposition_id="110959", 
    uuid=str(uuid.uuid4())
    )
db.session.add(request5)
db.session.commit()

point_request5 = models.PointRequest(
    scan_request_id=request5.id,
    requester_id=user1.id,
    uuid=str(uuid.uuid4())
    )
db.session.add(point_request5)
db.session.commit()

point_coordinate5 = models.PointCoordinate(
    value = 1121.121,
    point_request_id = point_request5.id
    )
db.session.add(point_coordinate5)
db.session.commit()

basic_request5 = models.BasicRequest(
    point_request_id=point_request5.id, 
    requester_id=user1.id
    )
db.session.add(basic_request5)
db.session.commit()

zip_file5 = models.RequestArchive(
    file_name = "999f6d26-1171-11e6-a07c-3a398e598637",
    path = './',
    zenodo_file_id = "a537b4ec-4f8f-48c9-8f38-652a0fa20051",
    original_file_name = "db_populate_sample.txt",
    basic_request_id = basic_request5.id
    )
db.session.add(zip_file5)
db.session.commit()

request5_2 = models.ScanRequest(
    title="title for request 5.2",
    description_of_model='Naturally evasive SUSY',
    reason_for_request='Gluinos that result in classic large missing transverse momentum signatures at the LHC have been excluded by 2011 searches if they are lighter than around 800 GeV. This adds to the tension between experiment and supersymmetric solutions of the naturalness problem, since the gluino is required to be light if the electroweak scale is to be natural. Here, we examine natural scenarios where supersymmetry is present, but was hidden from 2011 searches due to violation of $R$-parity and the absence of a large missing transverse momentum signature. Naturalness suggests that third generation states should dominate gluino decays and we argue that this leads to a generic signature in the form of same-sign, flavour-ambivalent leptons, without large missing transverse momentum. As a result, searches in this channel are able to cover a broad range of scenarios with some generality and one should seek gluinos that decay in this way with masses below a TeV. We encourage the LHC experiments to tailor a search for supersymmetry in this form. We consider a specific case that is good at hiding: baryon number violation. The only light sparticles are right-handed stops and gluinos. ',
    additional_information='Request follows http://arxiv.org/abs/1202.6616',
    analysis_id=analysis5.id,
    requester_id=user1.id,
    zenodo_deposition_id="110959",
    uuid=str(uuid.uuid4())
    )
db.session.add(request5_2)
db.session.commit()

point_request5_2 = models.PointRequest(
    scan_request_id=request5_2.id, 
    requester_id=user1.id,
    uuid=str(uuid.uuid4())
    )
db.session.add(point_request5_2)
db.session.commit()

point_coordinate5_2 = models.PointCoordinate(
    value = 121.21121,
    point_request_id = point_request5_2.id
    )
db.session.add(point_coordinate5_2)
db.session.commit()

basic_request5_2 = models.BasicRequest(
    point_request_id=point_request5_2.id, 
    requester_id=user1.id
    )
db.session.add(basic_request5_2)
db.session.commit()

zip_file5_2 = models.RequestArchive(
    file_name = "999f6d26-1171-11e6-a07c-3a398e598637",
    path = './',
    zenodo_file_id = "a537b4ec-4f8f-48c9-8f38-652a0fa20051",
    original_file_name = "db_populate_sample.txt",
    basic_request_id = basic_request5_2.id
    )
db.session.add(zip_file5_2)
db.session.commit()

##
run_condition6 = models.RunCondition(
    name='7TeV',
    description='1.04fb^-1'
    )
db.session.add(run_condition6)
db.session.commit()

analysis6 = models.Analysis(
    title='Search for squarks and gluinos using final states with jets and missing transverse momentum with the ATLAS detector in sqrt(s) = 7 TeV proton-proton collisions',
    collaboration='ATLAS',
    journal='Physics Letters B',
    inspire_URL='http://inspirehep.net/record/930002',
    description='A search for squarks and gluinos in events containing jets, missing transverse momentum and no electrons or muons is presented. The data were recorded in 2011 by the ATLAS experiment in sqrt(s)=7 TeV proton-proton collisions at the Large Hadron Collider. No excess above the Standard Model background expectation is observed in 1.04 fb^-1 of data. Gluino and squark masses below 700 GeV and 875 GeV respectively are excluded at the 95% confidence level in simplified models containing only squarks of the first two generations, a gluino octet and a massless neutralino. The exclusion limit increases to 1075 GeV for squarks and gluinos of equal mass. In MSUGRA/CMSSM models with tan(beta)=10, A_0=0 and mu> 0, squarks and gluinos of equal mass are excluded for masses below 950 GeV. These limits extend the region of supersymmetric parameter space excluded by previous measurements.',
    owner_id=user1.id, 
    run_condition_id=run_condition6.id,
    uuid=str(uuid.uuid4())
    )
db.session.add(analysis6)
db.session.commit()

request6 = models.ScanRequest(
    title="title for request 6",
    description_of_model='Gluino->Higgsino',
    reason_for_request='Searches for gluinos decaying to pairs of light-flavor quarks and missing energy set strong limits on many scenarios, while searches for like-sign dileptons constrain gluinos decaying to stops. Another scenario, less constrained by official LHC results, is a gluino decaying dominantly through the third generation but to a mixture of tops and bottoms. Gluino -> higgsino decays, through off-shell stops and sbottoms, are an example. My simulations indicate that this search can set an interesting limit on the gluino mass in such scenarios, but a more official result would be interesting. (See also request 1203.0028.) ',
    additional_information='I will provide LHE files on request.',
    analysis_id=analysis6.id,
    requester_id=user1.id,
    zenodo_deposition_id="110959",
    uuid=str(uuid.uuid4())
    )
db.session.add(request6)
db.session.commit()

point_request6 = models.PointRequest(
    scan_request_id=request6.id, 
    requester_id=user1.id,
    uuid=str(uuid.uuid4())
    )
db.session.add(point_request6)
db.session.commit()

point_coordinate6 = models.PointCoordinate(
    value = 4303.2,
    point_request_id = point_request6.id
    )
db.session.add(point_coordinate6)
db.session.commit()

basic_request6 = models.BasicRequest(
    point_request_id=point_request6.id,
    requester_id=user1.id
    )
db.session.add(basic_request6)
db.session.commit()

zip_file6 = models.RequestArchive(
    file_name = "999f6d26-1171-11e6-a07c-3a398e598637",
    path = "./",
    zenodo_file_id = "a537b4ec-4f8f-48c9-8f38-652a0fa20051",
    original_file_name = "db_populate_sample.txt", 
    basic_request_id = basic_request6.id
    )
db.session.add(zip_file6)
db.session.commit()

request6_2 = models.ScanRequest(
    title="title for request 6.2",
    description_of_model='Cascade Decaying Squark Simplified Model', 
    reason_for_request='Limits on light flavor squarks are now approaching 1 TeV. However, the limits should be greatly reduced if the spectrum is altered by including an intermediate particle in the decay chain. In this simplified model, only light flavor squarks are accessible and the gluinos are decoupled, and thus the main production mode is squark-antisquark pair-production. The squarks now decay to an intermediate particle, to a chargino/wino triplet, plus a jet. The chargino/wino then decays to a vector boson and a neutral state. This scenario can occur in the MSSM where the right handed squarks are decoupled from the left-handed ones, and in the NMSSM where the LSP is a singlino. It would be interesting to see the limits of the all-hadronic analyses to this challenging topology.',
    additional_information='No information available',
    analysis_id=analysis6.id,
    requester_id=user1.id,
    zenodo_deposition_id="110959",
    uuid=str(uuid.uuid4())
    )
db.session.add(request6_2)
db.session.commit()

point_request6_2 = models.PointRequest(
    scan_request_id=request6_2.id,
    requester_id=user1.id,
    uuid=str(uuid.uuid4())
    )
db.session.add(point_request6_2)
db.session.commit()

point_coordinate6_2 = models.PointCoordinate(
    value = 2121.433,
    point_request_id = point_request6_2.id
    )
db.session.add(point_coordinate6_2)
db.session.commit()

basic_request6_2 = models.BasicRequest(
    point_request_id=point_request6_2.id,
    requester_id=user1.id
    )
db.session.add(basic_request6_2)
db.session.commit()

zip_file6_2 = models.RequestArchive(
    file_name = "999f6d26-1171-11e6-a07c-3a398e598637",
    path = "./",
    zenodo_file_id = "a537b4ec-4f8f-48c9-8f38-652a0fa20051",
    original_file_name = "db_populate_sample.txt",
    basic_request_id = basic_request6_2.id
    )
db.session.add(zip_file6_2)
db.session.commit()

request6_3 = models.ScanRequest(
    title="title for request 6.3",
    description_of_model='Universal Extra Dimensions',
    reason_for_request='The Universal Extra Dimensions (UED) model is a viable picture for explaining the identity of dark matter, which leads to signatures of missing energy plus jets (the underlying process is production of Kaluza-Klein (KK) quarks and/or gluons which decay into the LKP (KK photon -- the dark matter) and colored SM particles). The SUSY searches for jets plus missing energy will thus directly place limits on the parameter space of the masses of the KK quarks (typically degenerate), KK gluon, and LKP.',
    additional_information='Useful initial results could assume that the LKP mass is much less than the KK squark or KK gluon masses. In this regime the bounds are roughly independent of the precise LKP mass. The production cross sections will be larger for the KK particles than for SUSY analogues, because they contain more spin degrees of freedom, and the efficiencies for detecting the signal events are likely to be somewhat different from SUSY analogues because of the differing spins. ',
    analysis_id=analysis6.id,
    requester_id=user1.id,
    zenodo_deposition_id="110959", 
    uuid=str(uuid.uuid4())
    )
db.session.add(request6_3)
db.session.commit()

point_request6_3 = models.PointRequest(
    scan_request_id=request6_3.id, 
    requester_id=user1.id,
    uuid=str(uuid.uuid4())
    )
db.session.add(point_request6_2)
db.session.commit()

point_coordinate6_3 = models.PointCoordinate(
    value = 323.2323,
    point_request_id = point_request6_3.id
    )
db.session.add(point_coordinate6_3)
db.session.commit()

basic_request6_3 = models.BasicRequest(
    point_request_id=point_request6_3.id,
    requester_id=user1.id
    )
db.session.add(basic_request6_3)
db.session.commit()

zip_file6_3 = models.RequestArchive(
    file_name = "999f6d26-1171-11e6-a07c-3a398e598637",
    path = "./",
    zenodo_file_id = "a537b4ec-4f8f-48c9-8f38-652a0fa20051",
    original_file_name = "db_populate_sample.txt",
    basic_request_id = basic_request6_3.id
)
db.session.add(zip_file6_3)
db.session.commit()

