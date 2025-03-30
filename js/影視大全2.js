var rule = {
    title: '影视大全',
    host: 'https://v.qq.com',
    // homeUrl: '/x/bu/pagesheet/list?_all=1&append=1&channel=choice&listpage=1&offset=0&pagesize=21&iarea=-1&sort=18',
    homeUrl: '/x/bu/pagesheet/list?_all=1&append=1&channel=cartoon&listpage=1&offset=0&pagesize=21&iarea=-1&sort=18',
    detailUrl: 'https://node.video.qq.com/x/api/float_vinfo2?cid=fyid',
    searchUrl: '/x/search/?q=**&stag=fypage',
    searchUrl: 'https://pbaccess.video.qq.com/trpc.videosearch.smartboxServer.HttpRoundRecall/Smartbox?query=**&appID=3172&appKey=lGhFIpeD3HsO9xEp&pageNum=(fypage-1)&pageSize=10',
    searchable: 2,
    filterable: 1,
    multi: 1,
    // url:'/channel/fyclass?listpage=fypage&channel=fyclass&sort=18&_all=1',
    url: '/x/bu/pagesheet/list?_all=1&append=1&channel=fyclass&listpage=1&offset=((fypage-1)*21)&pagesize=21&iarea=-1',
    // filter_url: 'sort={{fl.sort or 18}}&year={{fl.year}}&pay={{fl.pay}}',
    // filter_url: 'sort={{fl.sort or 75}}&year={{fl.year}}&pay={{fl.pay}}',
    filter_url: 'sort={{fl.sort or 75}}&iyear={{fl.iyear}}&year={{fl.year}}&itype={{fl.type}}&ifeature={{fl.feature}}&iarea={{fl.area}}&itrailer={{fl.itrailer}}&gender={{fl.sex}}',
    // filter: 'H4sIAAAAAAAAAA+2UzUrDQBC32XOEZLUJrGvIj0saaDBNisxBkIJCG3Fi4oepIg3EQoieqiH+vM23Zq+hRuaZLZ4ce9z2/lmd2d2+NgR+H0e+gF0DkdwFGTQgRMeJ2BAxIaSwvrqVnxc3zhlg9PttqjED2c/45cSy8DyIDcav557q/lBw8XTd/E6qbnT8M3zTFyc72RtC/Jumd+2c8wy7KZ4nxSL5Z9uxHS+Gcr+83sWVp1eVtt4Dluk1h93YuWZWwdupAYuxoFguVp+P/y5om/V+/YxyqfAW8pbKbeS2yi3kO/ebyE2Fy1nXXBm7DDzknspd5K7KHeSOytvI2+XAugYkKWlD2mhrM+RpSB8OmaNvTsriMEgycoFc0XbHZ3HCeUTukDv67vTDQY/MIXO0zelxn5M4JI6mOPkvgswSEpgPAAAA=',
    filter: {
        "choice": [{
            "key": "sort",
            "name": "排序",
            "value": [{
                "n": "最新",
                "v": "75"
            }, {
                "n": "最热",
                "v": "83"
            }, {
                "n": "评分",
                "v": "81"
            }]
        }, {
            "key": "iyear",
            "name": "年份",
            "value": [{
                "n": "全部",
                "v": "-1"
            }, {
                "n": "2025",
                "v": "2025"
            }, {
                "n": "2024",
                "v": "2024"
            }, {
                "n": "2023",
                "v": "2023"
            }, {
                "n": "2022",
                "v": "2022"
            }, {
                "n": "2021",
                "v": "2021"
            }, {
                "n": "2020",
                "v": "2020"
            }, {
                "n": "2019",
                "v": "2019"
            }, {
                "n": "2018",
                "v": "2018"
            }, {
                "n": "2017",
                "v": "2017"
            }, {
                "n": "2016",
                "v": "2016"
            }, {
                "n": "2015",
                "v": "2015"
            }]
        }],
        "tv": [{
            "key": "sort",
            "name": "排序",
            "value": [{
                "n": "最新",
                "v": "75"
            }, {
                "n": "最热",
                "v": "79"
            }, {
                "n": "评分",
                "v": "16"
            }]
        }, {
            "key": "feature",
            "name": "特色",
            "value": [{
                "n": "全部",
                "v": "-1"
            }, {
                "n": "喜剧",
                "v": "1"
            }, {
                "n": "动作",
                "v": "2"
            }, {
                "n": "爱情",
                "v": "3"
            }, {
                "n": "科幻",
                "v": "4"
            }, {
                "n": "悬疑",
                "v": "5"
            }, {
                "n": "犯罪",
                "v": "6"
            }, {
                "n": "冒险",
                "v": "7"
            }, {
                "n": "奇幻",
                "v": "8"
            }, {
                "n": "武侠",
                "v": "9"
            }, {
                "n": "历史",
                "v": "10"
            }, {
                "n": "古装",
                "v": "11"
            }, {
                "n": "战争",
                "v": "13"
            }, {
                "n": "青春",
                "v": "14"
            }, {
                "n": "都市",
                "v": "15"
            }, {
                "n": "动画",
                "v": "16"
            }, {
                "n": "真人",
                "v": "17"
            }, {
                "n": "运动",
                "v": "18"
            }]
        }, {
            "key": "iyear",
            "name": "年份",
            "value": [{
                "n": "全部",
                "v": "-1"
            }, {
                "n": "2025",
                "v": "2025"
            }, {
                "n": "2024",
                "v": "2024"
            }, {
                "n": "2023",
                "v": "2023"
            }, {
                "n": "2022",
                "v": "2022"
            }, {
                "n": "2021",
                "v": "2021"
            }, {
                "n": "2020",
                "v": "2020"
            }, {
                "n": "2019",
                "v": "2019"
            }, {
                "n": "2018",
                "v": "2018"
            }, {
                "n": "2017",
                "v": "2017"
            }, {
                "n": "2016",
                "v": "2016"
            }, {
                "n": "2015",
                "v": "2015"
            }]
        }],
        "movie": [{
            "key": "sort",
            "name": "排序",
            "value": [{
                "n": "最新",
                "v": "75"
            }, {
                "n": "最热",
                "v": "83"
            }, {
                "n": "评分",
                "v": "81"
            }]
        }, {
            "key": "type",
            "name": "类型",
            "value": [{
                "n": "全部",
                "v": "-1"
            }, {
                "n": "剧情",
                "v": "4"
            }, {
                "n": "动作",
                "v": "2"
            }, {
                "n": "犯罪",
                "v": "100004"
            }, {
                "n": "历史",
                "v": "100061"
            }, {
                "n": "奇幻",
                "v": "100009"
            }, {
                "n": "冒险",
                "v": "100005"
            }, {
                "n": "动画",
                "v": "100012"
            }, {
                "n": "喜剧",
                "v": "100010"
            }, {
                "n": "家庭",
                "v": "100015"
            }, {
                "n": "爱情",
                "v": "100006"
            }, {
                "n": "悬疑",
                "v": "100017"
            }, {
                "n": "传记",
                "v": "100022"
            }, {
                "n": "惊悚",
                "v": "100016"
            }, {
                "n": "奇幻",
                "v": "100011"
            }, {
                "n": "科幻",
                "v": "100021"
            }, {
                "n": "战争",
                "v": "100013"
            }, {
                "n": "纪录",
                "v": "3"
            }, {
                "n": "运动",
                "v": "100020"
            }]
        }, {
            "key": "year",
            "name": "年份",
            "value": [{
                "n": "全部",
                "v": "-1"
            }, {
                "n": "2025",
                "v": "2025"
            }, {
                "n": "2024",
                "v": "2024"
            }, {
                "n": "2023",
                "v": "2023"
            }, {
                "n": "2022",
                "v": "2022"
            }, {
                "n": "2021",
                "v": "2021"
            }, {
                "n": "2020",
                "v": "2020"
            }, {
                "n": "2019",
                "v": "2019"
            }, {
                "n": "2018",
                "v": "2018"
            }, {
                "n": "2017",
                "v": "2017"
            }, {
                "n": "2016",
                "v": "2016"
            }, {
                "n": "2015",
                "v": "2015"
            }]
        }],
        "variety": [{
            "key": "sort",
            "name": "排序",
            "value": [{
                "n": "最新",
                "v": "75"
            }, {
                "n": "最热",
                "v": "23"
            }]
        }, {
            "key": "iyear",
            "name": "年份",
            "value": [{
                "n": "全部",
                "v": "-1"
            }, {
                "n": "2025",
                "v": "2025"
            }, {
                "n": "2024",
                "v": "2024"
            }, {
                "n": "2023",
                "v": "2023"
            }, {
                "n": "2022",
                "v": "2022"
            }, {
                "n": "2021",
                "v": "2021"
            }, {
                "n": "2020",
                "v": "2020"
            }, {
                "n": "2019",
                "v": "2019"
            }, {
                "n": "2018",
                "v": "2018"
            }, {
                "n": "2017",
                "v": "2017"
            }, {
                "n": "2016",
                "v": "2016"
            }, {
                "n": "2015",
                "v": "2015"
            }]
        }],
        "cartoon": [{
            "key": "sort",
            "name": "排序",
            "value": [{
                "n": "最新",
                "v": "75"
            }, {
                "n": "最热",
                "v": "83"
            }, {
                "n": "评分",
                "v": "81"
            }]
        }, {
            "key": "area",
            "name": "地区",
            "value": [{
                "n": "全部",
                "v": "-1"
            }, {
                "n": "中国",
                "v": "1"
            }, {
                "n": "欧美",
                "v": "2"
            }, {
                "n": "日本",
                "v": "3"
            }, {
                "n": "韩国",
                "v": "4"
            }]
        }, {
            "key": "type",
            "name": "特色",
            "value": [{
                "n": "全部",
                "v": "-1"
            }, {
                "n": "运动",
                "v": "9"
            }, {
                "n": "剧情",
                "v": "4"
            }, {
                "n": "战争",
                "v": "13"
            }, {
                "n": "纪录",
                "v": "3"
            }, {
                "n": "犯罪",
                "v": "5"
            }, {
                "n": "喜剧",
                "v": "1"
            }, {
                "n": "冒险",
                "v": "7"
            }, {
                "n": "古装",
                "v": "6"
            }, {
                "n": "真人",
                "v": "20"
            }, {
                "n": "爱情",
                "v": "17"
            }, {
                "n": "日韩",
                "v": "15"
            }, {
                "n": "奇幻",
                "v": "16"
            }, {
                "n": "动画",
                "v": "18"
            }, {
                "n": "科幻",
                "v": "14"
            }, {
                "n": "悬疑",
                "v": "19"
            }, {
                "n": "都市",
                "v": "3"
            }, {
                "n": "韩国",
                "v": "12"
            }]
        }, {
            "key": "iyear",
            "name": "年份",
            "value": [{
                "n": "全部",
                "v": "-1"
            }, {
                "n": "2025",
                "v": "2025"
            }, {
                "n": "2024",
                "v": "2024"
            }, {
                "n": "2023",
                "v": "2023"
            }, {
                "n": "2022",
                "v": "2022"
            }, {
                "n": "2021",
                "v": "2021"
            }, {
                "n": "2020",
                "v": "2020"
            }, {
                "n": "2019",
                "v": "2019"
            }, {
                "n": "2018",
                "v": "2018"
            }, {
                "n": "2017",
                "v": "2017"
            }, {
                "n": "2016",
                "v": "2016"
            }, {
                "n": "2015",
                "v": "2015"
            }]
        }],
        "child": [{
            "key": "sort",
            "name": "排序",
            "value": [{
                "n": "最新",
                "v": "75"
            }, {
                "n": "最热",
                "v": "76"
            }, {
                "n": "评分",
                "v": "20"
            }]
        }, {
            "key": "sex",
            "name": "性别",
            "value": [{
                "n": "全部",
                "v": "-1"
            }, {
                "n": "男孩",
                "v": "1"
            }, {
                "n": "女孩",
                "v": "2"
            }]
        }, {
            "key": "area",
            "name": "地区",
            "value": [{
                "n": "全部",
                "v": "-1"
            }, {
                "n": "中国",
                "v": "3"
            }, {
                "n": "欧美",
                "v": "2"
            }, {
                "n": "韩国",
                "v": "1"
            }]
        }, {
            "key": "iyear",
            "name": "年龄段",
            "value": [{
                "n": "全部",
                "v": "-1"
            }, {
                "n": "0-3岁",
                "v": "1"
            }, {
                "n": "4-6岁",
                "v": "2"
            }, {
                "n": "7-9岁",
                "v": "3"
            }, {
                "n": "10岁以上",
                "v": "4"
            }, {
                "n": "全年龄段",
                "v": "7"
            }]
        }],
        "doco": [{
            "key": "sort",
            "name": "排序",
            "value": [{
                "n": "最新",
                "v": "75"
            }, {
                "n": "最热",
                "v": "74"
            }]
        }, {
            "key": "itrailer",
            "name": "预告分类",
            "value": [{
                "n": "全部",
                "v": "-1"
            }, {
                "n": "BBC",
                "v": "1"
            }, {
                "n": "国家地理",
                "v": "4"
            }, {
                "n": "HBO",
                "v": "3175"
            }, {
                "n": "NHK",
                "v": "2"
            }, {
                "n": "探索发现",
                "v": "7"
            }, {
                "n": "ITV",
                "v": "3530"
            }, {
                "n": "动物星球",
                "v": "3174"
            }, {
                "n": "ZDF",
                "v": "3176"
            }, {
                "n": "时代不同",
                "v": "15"
            }, {
                "n": "法国电视",
                "v": "6"
            }, {
                "n": "韩国",
                "v": "5"
            }]
        }, {
            "key": "type",
            "name": "类型",
            "value": [{
                "n": "全部",
                "v": "-1"
            }, {
                "n": "美食",
                "v": "4"
            }, {
                "n": "科技",
                "v": "10"
            }, {
                "n": "探险",
                "v": "3"
            }, {
                "n": "自然",
                "v": "6"
            }, {
                "n": "科幻",
                "v": "1"
            }, {
                "n": "历史",
                "v": "2"
            }, {
                "n": "人文",
                "v": "8"
            }, {
                "n": "犯罪",
                "v": "14"
            }, {
                "n": "奇幻",
                "v": "15"
            }, {
                "n": "古装",
                "v": "7"
            }, {
                "n": "真人",
                "v": "12"
            }, {
                "n": "武侠",
                "v": "11"
            }]
        }]
    },
    headers: {
        'User-Agent': 'PC_UA'
    },
    timeout: 5000,
    // class_parse:'.site_channel a;a&&Text;a&&href;channel/(.*)',
    cate_exclude: '专题视频|动画片|全部',
    // class_name: '热播&电视剧&电影&综艺&动漫&少儿',
    // class_url: 'choice&tv&movie&variety&cartoon&child',
    class_name: '电影&电视剧&综艺&动漫&少儿&纪录',
    class_url: 'movie&tv&variety&cartoon&child&doco',
    limit: 20,
    // play_parse:true,
    // 播放器解析，需要解析url，增加lazy解析
    play_parse: true,
    lazy: $js.toString(() => {
        try {
            let api = "" + input.split("?")[0];
            console.log(api);
            let response = fetch(api, {
                method: 'get',
                headers: {
                    'User-Agent': 'okhttp/3.14.9',
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            });
            let bata = JSON.parse(response);
            if (bata.url.includes("qq")) {
                input = {
                    parse: 0,
                    url: bata.url,
                    jx: 0,
                    danmaku: "http://103.45.162.207:25252/hbdm.php?key=7894561232&id=" + input.split("?")[0]
                };
            } else {
                input = {
                    parse: 0,
                    url: input.split("?")[0],
                    jx: 1,
                    danmaku: "http://103.45.162.207:25252/hbdm.php?key=7894561232&id=" + input.split("?")[0]
                };
            }
        } catch {
            input = {
                parse: 0,
                url: input.split("?")[0],
                jx: 1,
                danmaku: "http://103.45.162.207:25252/hbdm.php?key=7894561232&id=" + input.split("?")[0]
            };
        }
    }),
    一级: '.list_item;img&&alt;img&&src;a&&Text;a&&data-float',
    二级: '.list_item;img&&alt;img&&src;a&&Text;a&&data-float',
    二级: $js.toString(() => {
        VOD = {};
        let d = [];
        let video_list = [];
        let video_lists = [];
        let list = [];
        let QzOutputJson;
        let html = fetch(input, fetch_params);
        let sourceId = /get_playsource/.test(input) ? input.match(/id=(\d*?)&/)[1] : input.split("cid=")[1];
        let cid = sourceId;
        let detailUrl = "https://v.qq.com/detail/m/" + cid + ".html";
        log("二级地址:" + detailUrl);
        pdfh = jsp.pdfh;
        pd = jsp.pd;
        try {
            let json = JSON.parse(html);
            VOD = {
                vod_url: input,
                vod_name: json.c.title,
                type_name: json.type.join(","),
                vod_actor: json.nam.join(","),
                vod_year: json.c.year,
                vod_content: json.c.description,
                vod_remarks: json.rec,
                vod_pic: urljoin2(input, json.c.pic)
            };
        } catch (e) {
            log("二级解析出错，请检查数据结构是否变动:" + e.message);
        }
        if (/get_playsource/.test(input)) {
            eval(html);
            let indexList = QzOutputJson.PlaylistItem.indexList;
            indexList.forEach(function(it) {
                let dataUrl = "https://s.video.qq.com/get_playsource?id=" + sourceId + "&plat=2&type=4&data_type=3&range=" + it + "&video_type=10&plname=qq&otype=json";
                eval(fetch(dataUrl, fetch_params));
                let vdata = QzOutputJson.PlaylistItem.videoPlayList;
                vdata.forEach(function(item) {
                    d.push({
                        title: item.title,
                        pic_url: item.pic,
                        desc: item.episode_number + "\t\t集数:" + item.thirdLine,
                        url: item.playUrl
                    });
                });
                video_lists = video_lists.concat(vdata);
            });
        } else {
            let json = JSON.parse(html);
            video_lists = json.c.video_ids;
            let url = "https://v.qq.com/x/cover/" + sourceId + ".html";
            if (video_lists.length === 1) {
                let vid = video_lists[0];
                url = "https://v.qq.com/x/cover/" + cid + "/" + vid + ".html";
                d.push({
                    title: "在线播放全集-4K画质",
                    url: url
                });
            } else if (video_lists.length > 1) {
                for (let i = 0; i < video_lists.length; i += 30) {
                    video_list.push(video_lists.slice(i, i + 30));
                }
                video_list.forEach(function(it, idex) {
                    let o_url = "https://union.video.qq.com/fcgi-bin/data?otype=json&tid=1804&appid=20001238&appkey=6c03bbe9658448a4&union_platform=1&idlist=" + it.join(",");
                    let o_html = fetch(o_url, fetch_params);
                    eval(o_html);
                    QzOutputJson.results.forEach(function(it1) {
                        it1 = it1.fields;
                        let url = "https://v.qq.com/x/cover/" + cid + "/" + it1.vid + ".html";
                        d.push({
                            title: it1.title,
                            pic_url: it1.pic160x90.replace("/160", ""),
                            desc: it1.video_checkup_time,
                            url: url,
                            type: it1.category_map && it1.category_map.length > 1 ? it1.category_map[1] : ""
                        });
                    });
                });
            }
        }
        let yg = d.filter(function(it) {
            return it.type && it.type !== "综艺";
        });
        let zp = d.filter(function(it) {
            return !(it.type && it.type !== "综艺");
        });
        VOD.vod_play_from = yg.length < 1 ? "在线播放全集-4K画质" : "4K画质$在线播放全集";
        VOD.vod_play_url = yg.length < 1 ? d.map(function(it) {
            return it.title + "$" + it.url;
        }).join("#") : [zp, yg].map(function(it) {
            return it.map(function(its) {
                return its.title + "$" + its.url;
            }).join("#");
        }).join("$$$");
    }),
    搜索: $js.toString(() => {
        let d = [];
        pdfa = jsp.pdfa;
        pdfh = jsp.pdfh;
        pd = jsp.pd;
        let html = request(input);
        let baseList = pdfa(html, "body&&.result_item_v");
        log(baseList.length);
        baseList.forEach(function(it) {
            let longText = pdfh(it, ".result_title&&a&&Text");
            let shortText = pdfh(it, ".type&&Text");
            let fromTag = pdfh(it, ".result_source&&Text");
            let score = pdfh(it, ".figure_info&&Text");
            let content = pdfh(it, ".desc_text&&Text");
            // let url = pdfh(it, ".result_title&&a&&href");
            let url = pdfh(it, "div&&data-id");
            // log(longText);
            // log(shortText);
            // log('url:'+url);
            let img = pd(it, ".figure_pic&&src");
            url = "https://node.video.qq.com/x/api/float_vinfo2?cid=" + url.match(/.+\/(.+?)\.html/)[1];
            log(shortText + "|" + url);
            if (fromTag.match(/时代不同/)) {
                d.push({
                    title: longText.split(shortText)[0],
                    img: img,
                    url: url,
                    content: content,
                    desc: shortText + " " + score
                });
            }
        });
        setResult(d);
    }),
    搜索: $js.toString(() => {
        let d = [];
        let html = request(input);
        let json = JSON.parse(html);
        if (json.data.smartboxItemList.length > 0) {
            let cid = json.data.smartboxItemList[0].basicDoc.id;
            let url = 'https://node.video.qq.com/x/api/float_vinfo2?cid=' + cid;
            let html1 = request(url);
            let data = JSON.parse(html1);
            d.push({
                title: data.c.title,
                img: data.c.pic,
                url: url,
                content: data.c.description,
                desc: data.rec
            });
        }
        setResult(d);
    })
};