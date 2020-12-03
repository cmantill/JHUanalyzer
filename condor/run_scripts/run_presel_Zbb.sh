#!/bin/bash
source /cvmfs/cms.cern.ch/cmsset_default.sh
xrdcp root://cmseos.fnal.gov//store/user/lcorcodi/10XwithNano.tgz ./
export SCRAM_ARCH=slc7_amd64_gcc820
scramv1 project CMSSW CMSSW_10_6_14
tar xzf 10XwithNano.tgz
rm 10XwithNano.tgz

mkdir tardir; cp tarball.tgz tardir/; cd tardir
tar xzvf tarball.tgz
cp -r * ../CMSSW_10_6_14/src/
cd ../CMSSW_10_6_14/src/
eval `scramv1 runtime -sh`

echo make_preselection_HbbX.py $*
echo $*
python make_preselection_HbbX.py $*
xrdcp Hbbpreselection*.root root://cmseos.fnal.gov//store/user/cmantill/hbb/
