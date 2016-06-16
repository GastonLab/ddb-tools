library(ballgown)
bg = ballgown(dataDir='./', samplePattern='_stringtie_final', meas='all')
save(bg, file='bg.rda')