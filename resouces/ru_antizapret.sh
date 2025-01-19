#!/bin/bash
###antizapret
# Соберите популярные правила и преобразуйте их в правила sing-box для удобства использования в Karing.
#    https://github.com/runetfreedom/russia-v2ray-rules-dat
#    https://github.com/savely-krasovsky/antizapret-sing-box

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
target_dir="${work_dir}/russia"

# ———————————————————————————————————————————————————————————————————————————————————————————————

    ## runetfreedom/russia-v2ray-rules-dat
function clone_runetfreedom(){
    #git clone -b release --single-branch --depth=1 git@github.com:runetfreedom/russia-v2ray-rules-dat.git runetfreedom
    gitclone_dir=$(dirname $work_dir)/runetfreedom
    if [[ ! -d "$gitclone_dir" ]]; then
        echo "${gitclone_dir} unkown directory"
        exit -1
    fi
    cp -r $gitclone_dir . && rm -rf runetfreedom/.git
    cd runetfreedom/sing-box/
    cp rule-set-geoip/geoip-ru-blocked.srs $work_dir/geo/geoip/blocked@ru.srs
    cp rule-set-geoip/geoip-ru-blocked-community.srs $work_dir/geo/geoip/blocked-community@ru.srs
    cp rule-set-geoip/geoip-re-filter.srs $work_dir/geo/geoip/re-filter@ru.srs
    cp rule-set-geosite/geosite-ru-blocked.srs $work_dir/geo/geosite/blocked@ru.srs
    cp rule-set-geosite/geosite-ru-available-only-inside.srs $work_dir/geo/geosite/available-only-inside@ru.srs
}

    ## savely-krasovsky/antizapret-sing-box
function download_antizapret(){
    mkdir -p $target_dir/antizapret
    cd $target_dir/antizapret/

    file_array=("antizapret.srs" "antizapret.srs.sha256sum")
    for file in "${file_array[@]}"; do
        echo $file
        wget --no-check-certificate -q -T10 -t3 -O $file "https://github.com/savely-krasovsky/antizapret-sing-box/releases/latest/download/${file}"
    done
}

# ———————————————————————————————————————————————————————————————————————————————————————————————

rm -rf $target_dir ; mkdir $target_dir ; cd $target_dir
echo "start<= ${target_dir}"

clone_runetfreedom
download_antizapret

echo "end<= ${target_dir}"
#END FILE