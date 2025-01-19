#!/bin/bash
##adblockfilters
#   adblockclashlite.list 更新至 ACL:BanAD
#   https://github.com/217heidai/adblockfilters
#

CURRENT_DIR=$(cd $(dirname $0); pwd)

target_dir=$1
if [ -z "$target_dir" ]; then
    target_dir=$CURRENT_DIR
fi

if [ ! -d "$target_dir" ]; then
    echo "${target_dir} unkown directory"
    exit 1
fi

work_dir=$(realpath "$target_dir")
target_dir="${work_dir}/chinese"
sing_exe="${work_dir}/sing-box"

# ———————————————————————————————————————————————————————————————————————————————————————————————


function download_adblockfilters() {
    mkdir -p $target_dir/adblockfilters
    cd $target_dir/adblockfilters/
    aclssr_dir=$(dirname $work_dir)/ACL4SSR

    file_array=("AdGuard_Base_filter.txt" "AdGuard_Chinese_filter.txt" "AdGuard_DNS_filter.txt" "AdGuard_Mobile_Ads_filter.txt" "adblockclashlite.list" "adblockclash.list")
    for file in "${file_array[@]}"; do
        # --show-progress
        wget --no-check-certificate -q -T10 -t3 -O $file "https://github.com/217heidai/adblockfilters/raw/refs/heads/main/rules/${file}"

        if [[ "$file" == *.list ]]; then
            basename=${file%.list}
            echo "source << ${basename}"

            # ad keys
            if [[ "$file" == "adblockclashlite.list" ]]; then
                # 合并文件
                cat "${aclssr_dir}/Clash/BanAD.list" > temp_file && cat "$file" >> temp_file
                sort -u temp_file > "$file"
            fi

            #convert to json
            python $CURRENT_DIR/convert_json.py --single  $target_dir/adblockfilters/$file $basename.json

            #convert to srs
            srs_file=${basename}.srs
            $sing_exe rule-set compile $basename.json -o $srs_file
            echo -e "output >> ${srs_file}\n"
        fi
    done

    # BanAD
    acl_dir=$work_dir/ACL4SSR
    echo "copy adblockclashlite:BanAD to ${acl_dir}"
    cp ./adblockclashlite.json $acl_dir/BanAD.json
    cp ./adblockclashlite.srs $acl_dir/BanAD.srs

    # AdGuard
    adguard_dir=$work_dir/AdGuard
    if [ -d "$adguard_dir" ]; then
        echo "move AdGuard files to ${adguard_dir}"
        mv ./AdGuard* $adguard_dir/
    fi

}


# ———————————————————————————————————————————————————————————————————————————————————————————————
chmod +x $sing_exe
# rm -rf $target_dir
mkdir $target_dir ; cd $target_dir
echo "start<= ${target_dir}"

download_adblockfilters

echo "end<= ${target_dir}"
#END FILE











