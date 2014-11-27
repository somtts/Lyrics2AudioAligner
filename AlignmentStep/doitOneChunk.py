'''
Created on Apr 15, 2014
With .txtTur file given
@author: joro
'''
from CodeWarrior.Standard_Suite import file
import glob
from macpath import splitext
import os
import sys


from Adapt import PATH_TO_OUTPUT, MODEL_NAME, PATH_TO_CLEAN_ADAPTDATA, adapt, \
    MLLR_EXT, MAP_EXT, NUM_MAP_ITERS
from Aligner import PHRASE_ANNOTATION_EXT, openAlignmentInPraat
from RecordingSegmenter import RecordingSegmenter
from doit import PATH_TEST_DATASET

parentDir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(sys.argv[0]) ), os.path.pardir)) 
pathEvaluation = os.path.join(parentDir, 'AlignmentEvaluation')
sys.path.append(pathEvaluation)

from WordLevelEvaluator import evalAlignmentError
import sonicVisTextPhnDir2mlf


 # modelURI from adaptation script
MODEL_URI = os.path.join(PATH_TO_OUTPUT, MODEL_NAME  + MAP_EXT + str(NUM_MAP_ITERS) )

MODEL_URI = os.path.join(PATH_TO_OUTPUT, MODEL_NAME +  MAP_EXT + '3' )

# speech model
# MODEL_URI = '/Users/joro/Documents/Phd/UPF/METUdata/model_output/multipleGaussians/hmmdefs9/iter9/hmmdefs'
      



''' lazy mathod on top of doit
NOTE: first run AdaptationStep/Adapt.adapt(). THen URI to model  is constructed directly from there by the global variable. MODEL_NAME
'''
        
def doitForOneFile(pathTodata,  audioName):
        ################### ADAPTATION: ################
        
        pathToAudio =    pathTodata + audioName + '.wav'
        
        
        phraseAnnoURI = pathTodata +  audioName + PHRASE_ANNOTATION_EXT
        
      
        outputHTKPhoneAlignedURI = RecordingSegmenter.alignOneChunk(MODEL_URI, '/tmp/audioTur', "", pathToAudio, 1)
        alignmentErrors  = evalAlignmentError(phraseAnnoURI, outputHTKPhoneAlignedURI)
        
        mean, stDev = getMeanAndStDevError(alignmentErrors)
        
#         print "mean : ", mean, "st dev: " , stDev
        print "(", mean, ",", stDev, ")"
        
        
           ### OPTIONAL : open in praat
        openAlignmentInPraat(phraseAnnoURI, outputHTKPhoneAlignedURI, 0, pathToAudio)
        
        return mean, stDev, alignmentErrors


if __name__ == '__main__':
    
    fullURIAudio = sys.argv[1];
    outputHTKPhoneAlignedURI = RecordingSegmenter.alignOneChunk(MODEL_URI, '/tmp/audioTur', "", fullURIAudio, 1)
    print outputHTKPhoneAlignedURI;
    
    
    basenAudioFile = os.path.splitext(fullURIAudio)[0]
    phraseAnnoURI = basenAudioFile  + PHRASE_ANNOTATION_EXT
                
                
    currChunkAlignmentErrors = evalAlignmentError(phraseAnnoURI, outputHTKPhoneAlignedURI)
    print currChunkAlignmentErrors

        #########  MALE all ##########################      
#         PATH_TEST_DATASET = '/Users/joro/Documents/Phd/UPF/test_data_soloVoice_male/' 
#          
#          
#        
#         audioName1 = 'amaury_3_slow1'
#         audioName2 = 'alf_3_slow1'
#         audioName3 = 'este_3_slow1'
#          
#         audioName4 = 'nitech_jp_song060_m001_003'
#         audioName5 = 'nitech_jp_song060_m001_007'
#          
#         audioName6 = 'GEORGI_20_Koklasam_Saclarini_zemin_from_19.292461_to_32.514873'
#         audioName7 = '1-05_Ruzgar_Soyluyor_Simdi_O_Yerlerde_zemin_from_0_143205_to_38_756510'
#          
#         audioNames = [audioName1, audioName2, audioName3, audioName4, audioName5, audioName6, audioName7]
#          
#         totalAlignementError = []
#          
# #         mean, stDev, alignmentErrors = doitForOneFile(PATH_TEST_DATASET  , audioName7)
#          
#         for i in range(7):
#             mean, stDev, alignmentErrors = doitForOneFile(PATH_TEST_DATASET  , audioNames[i])
#             totalAlignementError.extend(alignmentErrors)
#  
# #         total statistics:    
#         totalMean, totalStDev =  getMeanAndStDevError(totalAlignementError)  
#         print "(", totalMean, ",", totalStDev, ")" 


############# MALE ALL FILES OF KANI iN A GIVEN DIR: 

#         PATH_TEST_DATASET = '/Users/joro/Documents/Phd/UPF/test_data_soloVoice_kani_karaca-cargah_tevsih/'
#         
#         os.chdir(PATH_TEST_DATASET)
#         
#         totalAlignementError = []
#         for fileN in glob.glob("*.wav"):
#             baseName = splitext(fileN)[0]
#             mean, stDev, alignmentErrors = doitForOneFile(PATH_TEST_DATASET  , baseName)
#             totalAlignementError.extend(alignmentErrors)
#         
#         totalMean, totalStDev =  getMeanAndStDevError(totalAlignementError)  
#         print "(", totalMean, ",", totalStDev, ")" 



################################### test with one chunk of sarki recording. Use lazy function ####################################

#     PATH_TEST_DATASET = '/Users/joro/Documents/Phd/UPF/test_data_synthesis'
# 
#     compositionName = 'nihavent--sarki--aksak--bakmiyor_cesm-i--haci_arif_bey'
#     recordingDir = '04_Hamiyet_Yuceses_-_Bakmiyor_Cesm-i_Siyah_Feryade'
# 
#     
#         
#            
#     error = doitForOneFile(PATH_TEST_DATASET, recordingDir)
#      
#     print error
