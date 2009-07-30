import FWCore.ParameterSet.Config as cms

process = cms.Process("testJET")
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.default.limit = 10
process.MessageLogger.cerr.FwkReport.reportEvery = 10
process.MessageLogger.categories.append('VBFHZZllbbSimpleNtpleSummary')
process.MessageLogger.cerr.INFO = cms.untracked.PSet(
    default                   = cms.untracked.PSet( limit = cms.untracked.int32(0)  ),
    VBFHZZllbbSimpleNtpleSummary = cms.untracked.PSet( limit = cms.untracked.int32(-1) )
)

## debugging porpose
cms.Service('Tracer')
## if you get bad_alloc problems or you just observe increasing memory needs
## [for the real big problems use valgrind (http://valgrind.org) or igtools]
cms.Service('SimpleMemoryCheck', 
    ignoreTotal = cms.untracked.int32(1)
) 
## quickly identification on how fast your process and single modules are 
cms.Service('Timing')


process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1000)
)

## this defines the input files
from HiggsAnalysis.VBFHiggsToZZto2l2b.Data.H150_ZZ_qqllSummer08_IDEALV9v2_GENSIMRECO_Input_cfi import * 
#from HiggsAnalysis.VBFHiggsToZZto2l2b.Data.PYTHIA6_SM_H_ZZ_qqll_mH150_10TeV_RECO_IDEAL_legnaro_cfi import *

# this inputs the input files from the previous function
process.source = RecoInput()

process.load("HiggsAnalysis.VBFHiggsToZZto2l2b.vbfHZZllbbIC5CaloCorrections_cff")

process.load("HiggsAnalysis.VBFHiggsToZZto2l2b.vbfhzzllbbMCprocessFilter_cfi")

process.caloJetCollectionClone = cms.EDProducer("CaloJetShallowCloneProducer",
#    src = cms.InputTag("iterativeCone5CaloJets")
    src = cms.InputTag("L2L3CorJetIC5Calo")                                                
)

process.genJetCollectionClone = cms.EDProducer("GenJetShallowCloneProducer",
    src = cms.InputTag("iterativeCone5GenJets")
)

process.caloJetSele = cms.EDFilter("PtMinCandSelector",
    src = cms.InputTag("caloJetCollectionClone"),
    ptMin = cms.double(15.0)
)

process.genJetSele = cms.EDFilter("PtMinCandSelector",
    src = cms.InputTag("genJetCollectionClone"),
    ptMin = cms.double(15.0)
)

process.jetMatchOne = cms.EDFilter("CandOneToOneDeltaRMatcher",
    src = cms.InputTag("iterativeCone5GenJets"),
    algoMethod = cms.string('SwitchMode'),
#    matched = cms.InputTag("iterativeCone5CaloJets")
    matched = cms.InputTag("L2L3CorJetIC5Calo")
)

process.jetMatchMany = cms.EDFilter("CandOneToManyDeltaRMatcher",
    printDebug = cms.untracked.bool(True),
    src = cms.InputTag("genJetSele"),
    matched = cms.InputTag("caloJetSele")
)

process.printJet = cms.EDFilter("VBFHZZllbbJetMatchAnalyzer",
    source       = cms.InputTag("genJetSele"),
    matchMapMany = cms.InputTag("jetMatchMany"),
    matchMapOne  = cms.InputTag("jetMatchOne","src2mtc"),
    matched      = cms.InputTag("caloJetSele"),
    histomakerFlag = cms.bool(True),                            
    dRcut = cms.double(0.5)
)

process.effMatchedJet03 = cms.EDFilter("VBFHZZllbbJetMatchAnalyzer",
    source       = cms.InputTag("genJetSele"),
    matchMapMany = cms.InputTag("jetMatchMany"),
    matchMapOne  = cms.InputTag("jetMatchOne","src2mtc"),
    matched      = cms.InputTag("caloJetSele"),
    histomakerFlag = cms.bool(True),                            
    dRcut = cms.double(0.3)
)
process.effMatchedJet04 = cms.EDFilter("VBFHZZllbbJetMatchAnalyzer",
    source       = cms.InputTag("genJetSele"),
    matchMapMany = cms.InputTag("jetMatchMany"),
    matchMapOne  = cms.InputTag("jetMatchOne","src2mtc"),
    matched      = cms.InputTag("caloJetSele"),
    histomakerFlag = cms.bool(True),                            
    dRcut = cms.double(0.4)
)
process.effMatchedJet06 = cms.EDFilter("VBFHZZllbbJetMatchAnalyzer",
    source       = cms.InputTag("genJetSele"),
    matchMapMany = cms.InputTag("jetMatchMany"),
    matchMapOne  = cms.InputTag("jetMatchOne","src2mtc"),
    matched      = cms.InputTag("caloJetSele"),
    histomakerFlag = cms.bool(True),                            
    dRcut = cms.double(0.6)
)

## talk to TFileService for output histograms
process.TFileService = cms.Service("TFileService",
    fileName = cms.string('myPlots.root')
)

process.printEventNumber = cms.OutputModule("AsciiOutputModule")

process.p = cms.Path( process.ic5CaloJetMETCorrections  *
                      process.caloJetCollectionClone    *
                      process.genJetCollectionClone     *
                      process.caloJetSele               *
                      process.genJetSele                *
                      process.jetMatchOne               *
                      process.jetMatchMany              *
                      process.vbfhzzllbbMCprocessFilter *
                      process.printJet                  *
                      process.effMatchedJet03           *
                      process.effMatchedJet04           *
                      process.effMatchedJet06           
                      )

process.outpath = cms.EndPath(process.printEventNumber)


