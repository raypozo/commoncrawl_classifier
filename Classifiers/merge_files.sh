#***************************************************
#This script merge single wiki files inside a folder to produce larger size files. 
#Reason: better Hadoop performance
#***************************************************
mkdir decompressed2
cd decompressed
for dir in */;
do
    dir="${dir%/}"		# strip trailing slash
	dir="${dir##*/}"	# strip path and leading slash
	mkdir ../decompressed2/"$dir"
	cd "$dir"
	counter=0
	for subdir in */;
	do
		 echo "Merging folder files in $subdir of language $dir"
		 subdir="${subdir%/}"
		 subdir="${subdir##*/}"
		 cd "$subdir"
		 cat wiki_* > merged_wiki
		 cd ..
		 mkdir ../../decompressed2/"$dir"/"$subdir"
		 mv "$subdir"/merged_wiki ../../decompressed2/"$dir"/"$subdir"/
		 mv ../../decompressed2/"$dir"/"$subdir"/merged_wiki ../../decompressed2/"$dir"/"$subdir"/wiki_00
		 if [ $counter == 9 ]; #Number of folders we want to do the merge per language
		 then
			break
		 fi
		 counter=$((counter+1))

	done
	cd ..
done
echo "Merge process complete"