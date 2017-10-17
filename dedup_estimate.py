import sys
import os
import hashlib
import pdb

#This program computes dedup% for all files contained under input directory

def main():
    path = ""
    chunk_size = 0
    try:
        path = sys.argv[1]
        chunk_size = int(sys.argv[2])
    except:
        print "Usage: ./prog_name.py path chunk_size"
        if not chunk_size:
            print "using default chunk_size, 4096 bytes"
            chunk_size = 4096
        if not path:
            sys.exit()
    checksum_map = {}       #key: checksum (md5), value: filenames containing the checksum
    intra_file_sim = {}
    deduped_bytes = 0
    non_deduped_bytes = 0
    total_bytes = 0
    num_files_processed = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            filename = root+"/"+file
            try:
                file = open(filename, 'r')
            except Exception as e:
                print "Exception:", e, ". Continuing though...."
                continue
            num_files_processed += 1
            if num_files_processed%100000 == 0:
                print "processed", num_files_processed, "files", \
                    "so far dedup bytes =", deduped_bytes, \
                    (deduped_bytes*100.0)/total_bytes
            while(1):
                chunk = file.read(chunk_size)
                chunk_len = len(chunk)
                if not chunk:
                    file.close()
                    break
                total_bytes += chunk_len
                checksum = hashlib.md5(chunk).hexdigest()
                if checksum in checksum_map:
                    #found a duplicate
                    if filename not in checksum_map[checksum]:
                        checksum_map[checksum].append(filename)
                    else:
                        if filename in intra_file_sim:
                            intra_file_sim[filename] = intra_file_sim[filename] + 1
                        else:
                            intra_file_sim[filename] = 1
                    deduped_bytes += chunk_len
                else:
                    #found a new block
                    non_deduped_bytes += chunk_len
                    checksum_map[checksum] = []
                    checksum_map[checksum].append(filename)
    total_intra_sim = 0
    for filename in intra_file_sim:
        total_intra_sim += intra_file_sim[filename]

    print "Path:", path, "\nChunk size:", chunk_size, "\ndeduped bytes:", \
            deduped_bytes, "\nnon dedup bytes:", non_deduped_bytes, "\ntotal bytes:", \
            total_bytes, "\noverall dedup%age:", \
            (deduped_bytes*100.0)/total_bytes, \
            "\ntotal intra file similarity:", total_intra_sim, \
            "\nnum of files processed:", num_files_processed
main()
