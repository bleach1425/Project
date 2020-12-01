import json
import os
import math
import librosa

DATASET_PATH = "C:/Users/PC06/Downloads/lili colins"
# DATASET_PATH = "Z:/虛擬會議室/意軒/解決"
JSON_PATH = "./json/test_1130.json"
SAMPLE_RATE = 16000
TRACK_DURATION = 10  # measured in seconds
SAMPLES_PER_TRACK = SAMPLE_RATE * TRACK_DURATION

# 1~10
def save_mfcc(dataset_path, json_path , sr ,num_mfcc=13, n_fft=2048, hop_length=512, num_segments=5):
    # dictionary to store mapping, labels, and MFCCs
    data = {
        "name":[],
        "mapping": [],
        "labels": [],
        "mfcc": []
    }

    samples_per_segment = int(SAMPLES_PER_TRACK / num_segments)
    num_mfcc_vectors_per_segment = math.ceil(samples_per_segment / hop_length)
    index = 1

    # loop through all genre sub-folder
    for i, (dirpath, dirnames, filenames) in enumerate(os.walk(dataset_path)):
        # ensure we're processing a genre sub-folder level
        if dirpath is not dataset_path:

            # save genre label (i.e., sub-folder name) in the mapping
            semantic_label = dirpath.split("/")[-1]
            data["mapping"].append(semantic_label)
            print("\nProcessing: {}".format(semantic_label))

            # process all audio files in genre sub-dir
            for f in filenames:

                # load audio file
                file_path = os.path.join(dirpath, f)
                signal, sample_rate = librosa.load(file_path, sr=SAMPLE_RATE)

                # process all segments of audio file
                for id, d in enumerate(range(num_segments)):

                    # calculate start and finish sample for current segment
                    start = samples_per_segment * d
                    finish = start + samples_per_segment

                    # extract mfcc
                    mfcc = librosa.feature.mfcc(signal[start:finish], sample_rate, n_mfcc=num_mfcc, n_fft=n_fft,
                                                hop_length=hop_length)
                    mfcc = mfcc.T
                    mfcc_cut = mfcc.copy()
                    mfcc_cut[abs(mfcc_cut)<10]=0
                    # store only mfcc feature with expected number of vectors
                    if len(mfcc_cut) == num_mfcc_vectors_per_segment:
                        name = f.split('.')[0]
                        if (id+1)%4 == 0:
                            data["name"].append(name)

                        data["mfcc"].append(mfcc_cut.tolist())
                        data["labels"].append(i - 1)
                        if (id+1)%4 ==0:
                            print("{}, 第 {} 個檔案".format(file_path, index))
                            index+=1

    # save MFCCs to json file
    with open(json_path, "w") as fp:
        json.dump(data, fp, indent=4)

# num_segment(將音檔切成幾份)
if __name__ == "__main__":
    save_mfcc(DATASET_PATH, JSON_PATH,sr=16000 ,num_segments= 4)