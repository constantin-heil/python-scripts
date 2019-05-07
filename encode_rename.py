from pathlib import Path
import argparse

"""Script to change the names of ENCODE downloaded fastq files to more relevant names based on a table of metadata

USAGE: run with two required options -m and -f. Use option -t to simply write empty files as a test.
"""

parse = argparse.ArgumentParser(description = "run in directory with fastq.gz files and metadata table")
parse.add_argument("--metadata-file", "-m", type = str, required=True, dest="mdf")
parse.add_argument("--fields", "-f", type = str, nargs = "+", required=True, dest = "fl", help = "space separated names of fields from metadata")
parse.add_argument("--touch", "-t", action = "store_true", help = "flag for testing behavior")
args = parse.parse_args()


md_dict = {}
with open(args.mdf, 'r') as fh:
    header = fh.readline()
    for e in header.split("\t"):
        md_dict[e.strip()] = []


with open(args.mdf, 'r') as fh:
    fh.readline()
    for line in fh:
        for key, entry in zip(md_dict.keys(), line.split("\t")):
            md_dict[key].append(entry.strip())

            

def make_outnames(keys):
    try:
        field_list = [md_dict[k] for k in keys] 
    except:
        raise RuntimeError("requested field not in dictionary")
    
    basename_list = []
    for i in range(len(field_list[0])):
        current_basename = ""
        for field in field_list:
            current_basename += (field[i] + "_")
        basename_list.append(current_basename)
    return basename_list


filenames = [entry.split("/")[-1] for entry in md_dict["File download URL"]]
filebases = [entry.split(".")[0] for entry in filenames]

basenames_out = make_outnames(args.fl)
filenames_out = [bn.replace("/", "") + ".fastq.gz" for bn in basenames_out]


assert len(filenames_out) == len(set(filenames_out)), "non unique entries in filename out list"
assert len(filenames) == len(filenames_out), "name lists must have same length"

if not args.touch:
    for fni, fno in zip(filenames, filenames_out):
        currentpath = Path(fni)
        currentpath.rename(fno)

else:
    for fno in filenames_out:
        currentpath = Path(fno + ".testfile")
        currentpath.touch()

print("Successfully finished!")

