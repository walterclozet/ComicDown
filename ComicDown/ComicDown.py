#!/usr/bin/python
#-*- coding:utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals
import urllib
import urllib2
import base64
import os
import PyV8
from PyV8 import convert
import sys
import io

# basic functions

#save image of url to file
def save_img(url, file, ref_url = '', cookie = ''):
    img_file_data = None
    if (ref_url != ''):
        img_file_data = fetch_html2(url, ref_url, cookie);
    else:
        img_file_data = fetch_html(url);
    if (len(img_file_data) == 0):
        return False
    with open(file, 'wb') as img_file:
        img_file.write(img_file_data)
    return True

def touch_file(f_name):
    open(f_name, 'w').close()

#get data from url(binary/html text)
def fetch_html2(url, ref_url, cookie):
    req=urllib2.Request(url)
    if (len(ref_url) > 0):
        req.add_header('Referer', ref_url)
    if (len(cookie) > 0):
        req.add_header('Cookie', cookie)
    req.add_header('User-Agent',"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36")
    #req.add_header('Cookie', 'UM_distinctid=15da15870546cf-0566c1e9160126-4c322f7c-7e900-15da15870553f7; Hm_lvt_645dcc265dc58142b6dbfea748247f02=1501650514; RORZ_7f25_saltkey=b4dh3gjg; RORZ_7f25_lastvisit=1501649656; RORZ_7f25_visitedfid=15; Hm_lpvt_645dcc265dc58142b6dbfea748247f02=1502871156; show_tip_1=0')
    try:
        response_data = urllib2.urlopen(req, timeout = 5)
        htmltext = response_data.read()
        response_data.close()
        #print response_data.code
    except urllib2.URLError as e:
        #print (e.reason)
        return ''
    except Exception as e:
        print ('timeout, retrying...')
        htmltext =  fetch_html2(url, ref_url, cookie)
    return htmltext

def fetch_html(url):
    try:
        req=urllib2.Request(url)
        req.add_header('User-Agent',"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36")
        response_data = urllib2.urlopen(req,timeout = 5)
        htmltext = response_data.read()
        response_data.close()
        #print response_data.code
    except urllib2.URLError as e:
        #print (e.reason)
        return ''
    except Exception as e:
        print ('timeout, retrying...')
        htmltext =  fetch_html(url)
    return htmltext

# test if the url is valid
# only try to read content
def test_url(url, time = 0):
    if time > 3 :
        return False
    try:
        req=urllib2.Request(url)
        req.add_header('User-Agent',"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36")
        response_data = urllib2.urlopen(req, timeout = 5)
        htmltext = response_data.read()
        response_data.close()
        if (len(htmltext) > 0):
            return True
        else:
            return False
    except urllib2.URLError as e:
        #print (e.reason)
        return False
    except Exception as e:
        print ('timeout, retrying...')
        return test_url(url, time + 1)
    return False

def get_title(url):
    html_text = fetch_html(url)
    start_tag = html_text.find(b'charset=') + 8
    end_tag = html_text.find(b'"', start_tag)
    charset = html_text[ start_tag : end_tag]
    html_text = html_text.decode(charset, 'ignore')
    title = get_sub_text(html_text, '<title>', '</title>')
    return title
    

def get_sub_text(text, start_s, end_s):
    start_tag = text.find(start_s)
    if (start_tag <= 0):
        return ''
    end_tag = text.find(end_s, start_tag + len(start_s))
    if (end_tag <= 0):
        return ''
    return text[start_tag + len(start_s) : end_tag]

# extent functions

def get_chapters_733dm(url):
    html_text = fetch_html(url)
    #网页源代码是GBK编码,
    html_text = html_text.decode('GBK')
    res = []
    html_text = get_sub_text(html_text, '<div id="section">', '<div class="description">')
    start_tag = html_text.find('漫画列表')
    html_text = html_text[ start_tag + 10 : ]
    start_tag = 0
    while (start_tag >= 0):
        start_tag = html_text.find('<a href="')
        if (start_tag < 0):
            break
        link = html_text[start_tag + 9 : ]
        end_tag = link.find('"')
        html_text = link[end_tag + 1: ]
        link = link[0:end_tag]
        start_tag = html_text.find('title="')
        if (start_tag < 0):
            break
        title = html_text[start_tag + 7 : ]
        end_tag = title.find('"')
        html_text = title[end_tag + 1: ]
        title = title[0:end_tag]
        print (link, title)
        res.append([title, 'http://www.733dm.net/' +link])
    return res

def get_chapters_dmzj(url):
    # html_text charset is utf 8
    html_text = fetch_html(url)
    html_text = html_text.decode('utf-8')
    res = []
    chapter_text = get_sub_text(html_text, '<div class="cartoon_online_border"', '</ul>') 
    start_tag = 0
    while (start_tag >= 0):
        start_tag = chapter_text.find('" href="')
        if (start_tag < 0):
            break
        link = chapter_text[start_tag + 8 : ]
        end_tag = link.find('"')
        chapter_text = link[end_tag + 1: ]
        link = link[0:end_tag]
        start_tag = chapter_text.find('>')
        if (start_tag < 0):
            break
        title = chapter_text[start_tag + 1 : ]
        end_tag = title.find('<')
        chapter_text = title[end_tag + 1: ]
        title = title[0:end_tag]
        try:
            print (link, title)
        except:
            print (link, urllib2.quote(title.encode('utf-8')))


        res.append([title, 'http://manhua.dmzj.com' +link])
    # get other chapters, may be more than one section
    while True:
        chapter_text = get_sub_text(html_text, '<div class="cartoon_online_border_other"', '</ul>') 
        html_text = html_text[html_text.find('<div class="cartoon_online_border_other"') :]
        html_text = html_text[html_text.find('</ul>') : ]
        if (len(chapter_text) <= 0):
            return res
        start_tag = 0
        while (start_tag >= 0):
            start_tag = chapter_text.find('" href="')
            if (start_tag < 0):
                break
            link = chapter_text[start_tag + 8 : ]
            end_tag = link.find('"')
            chapter_text = link[end_tag + 1: ]
            link = link[0:end_tag]
            start_tag = chapter_text.find('>')
            if (start_tag < 0):
                break
            title = chapter_text[start_tag + 1 : ]
            end_tag = title.find('<')
            chapter_text = title[end_tag + 1: ]
            title = title[0:end_tag].strip()
            try:
                print (link, title)
            except:
                print (link, urllib2.quote(title.encode('utf-8')))
            res.append([title, 'http://manhua.dmzj.com' +link])
    return res
    

def get_chapters_tx(url):
    # html_text charset is utf 8
    html_text = fetch_html(url)
    html_text = html_text.decode('utf-8')
    res = []
    chapter_text = get_sub_text(html_text, '<ol class="chapter-page-all works-chapter-list">', '</ol>') 
    start_tag = 0
    while (start_tag >= 0):
        start_tag = chapter_text.find('" href="')
        if (start_tag < 0):
            break
        link = chapter_text[start_tag + 8 : ]
        end_tag = link.find('"')
        chapter_text = link[end_tag + 1: ]
        link = link[0:end_tag]
        start_tag = chapter_text.find('>')
        if (start_tag < 0):
            break
        title = chapter_text[start_tag + 1 : ]
        end_tag = title.find('<')
        chapter_text = title[end_tag + 1: ]
        title = title[4:end_tag].strip()
        print (link, title)
        res.append([title, 'http://ac.qq.com' +link])
    return res    

def get_chapters_manhuagui(url):
    # html_text charset is utf 8
    html_text = fetch_html(url)
    html_text = html_text.decode('utf-8')
    res = []
    chapter_text = get_sub_text(html_text, '<div class="chapter-tip cf">', '<div class="comment-bar">') 
    start_tag = 0
    while (start_tag >= 0):
        start_tag = chapter_text.find('<a href="')
        if (start_tag < 0):
            break
        link = chapter_text[start_tag + 9 : ]
        end_tag = link.find('"')
        chapter_text = link[end_tag + 1: ]
        link = link[0:end_tag]
        start_tag = chapter_text.find('title="')
        if (start_tag < 0):
            break
        title = chapter_text[start_tag + 7 : ]
        end_tag = title.find('"')
        chapter_text = title[end_tag + 1: ]
        title = title[0:end_tag]
        print (link, title)
        res.append([title, 'http://www.manhuagui.com' +link])
    chapter_text = get_sub_text(html_text, '<div class="chapter-list cf mt10"', '</div>') 
    start_tag = 0
    while (start_tag >= 0):
        start_tag = chapter_text.find('<a href="')
        if (start_tag < 0):
            break
        link = chapter_text[start_tag + 9 : ]
        end_tag = link.find('"')
        chapter_text = link[end_tag + 1: ]
        link = link[0:end_tag]
        start_tag = chapter_text.find('title="')
        if (start_tag < 0):
            break
        title = chapter_text[start_tag + 7 : ]
        end_tag = title.find('"')
        chapter_text = title[end_tag + 1: ]
        title = title[0:end_tag]
        print (link, title)
        res.append([title, 'http://www.manhuagui.com' +link])
    return res  

def extrac_code(htmltext):
    packed_code = get_sub_text(htmltext, 'packed="', '";')
    return packed_code

def extrac_code_dmzj(htmltext):
    packed_code = get_sub_text(htmltext, '<script type="text/javascript">', '</script>')
    return packed_code

def extrac_code_tx(htmltext):
    packed_code = get_sub_text(htmltext, 'var DATA        = \'', '\'')
    return packed_code

def extrac_code_manhuagui(htmltext):
    packed_code = 'eval' + get_sub_text(htmltext, '<script type="text/javascript">window', '</script>')[20:]
    return packed_code

def decode_code_733dm(packed_code):
    #packed_code = base64.b64decode(packed_code)

    js_code = """
        (function(){
	        function base64decode(str){var base64EncodeChars="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";var base64DecodeChars=new Array(-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,62,-1,-1,-1,63,52,53,54,55,56,57,58,59,60,61,-1,-1,-1,-1,-1,-1,-1,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,-1,-1,-1,-1,-1,-1,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,-1,-1,-1,-1,-1);var c1,c2,c3,c4;var i,len,out;len=str.length;i=0;out="";while(i<len){do{c1=base64DecodeChars[str.charCodeAt(i++)&255]}while(i<len&&c1==-1);if(c1==-1){break}do{c2=base64DecodeChars[str.charCodeAt(i++)&255]}while(i<len&&c2==-1);if(c2==-1){break}out+=String.fromCharCode((c1<<2)|((c2&48)>>4));do{c3=str.charCodeAt(i++)&255;if(c3==61){return out}c3=base64DecodeChars[c3]}while(i<len&&c3==-1);if(c3==-1){break}out+=String.fromCharCode(((c2&15)<<4)|((c3&60)>>2));do{c4=str.charCodeAt(i++)&255;if(c4==61){return out}c4=base64DecodeChars[c4]}while(i<len&&c4==-1);if(c4==-1){break}out+=String.fromCharCode(((c3&3)<<6)|c4)}return out};
	        function GetImg(){
	                var photosr = new Array();
                    packed='""" + packed_code + """';eval(eval(base64decode(packed).slice(4)));
		            return photosr;
	            }
            return GetImg();
        })
    """
    #print js_code
    ctxt = PyV8.JSContext()
    ctxt.enter()
    func = ctxt.eval(js_code)
    return func()


def decode_code_dmzj(js_code):
    #packed_code = base64.b64decode(packed_code)

    js_code = """
        (function(){
	        function base64decode(str){var base64EncodeChars="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";var base64DecodeChars=new Array(-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,62,-1,-1,-1,63,52,53,54,55,56,57,58,59,60,61,-1,-1,-1,-1,-1,-1,-1,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,-1,-1,-1,-1,-1,-1,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,-1,-1,-1,-1,-1);var c1,c2,c3,c4;var i,len,out;len=str.length;i=0;out="";while(i<len){do{c1=base64DecodeChars[str.charCodeAt(i++)&255]}while(i<len&&c1==-1);if(c1==-1){break}do{c2=base64DecodeChars[str.charCodeAt(i++)&255]}while(i<len&&c2==-1);if(c2==-1){break}out+=String.fromCharCode((c1<<2)|((c2&48)>>4));do{c3=str.charCodeAt(i++)&255;if(c3==61){return out}c3=base64DecodeChars[c3]}while(i<len&&c3==-1);if(c3==-1){break}out+=String.fromCharCode(((c2&15)<<4)|((c3&60)>>2));do{c4=str.charCodeAt(i++)&255;if(c4==61){return out}c4=base64DecodeChars[c4]}while(i<len&&c4==-1);if(c4==-1){break}out+=String.fromCharCode(((c3&3)<<6)|c4)}return out};
	        function GetImg(){
	                """ + js_code + """
		            return arr_pages;
	            }
            return GetImg();
        })
    """
    #print js_code
    ctxt = PyV8.JSContext()
    ctxt.enter()
    func = ctxt.eval(js_code)
    return func()

def decode_code_tx(js_code):
    js_code = """
    (function(){
	        
function Base() {
    _keyStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
    this.decode = function(c) {
        var a = "",
            b, d, h, f, g, e = 0;
        for (c = c.replace(/[^A-Za-z0-9\+\/\=]/g, ""); e < c.length;) b = _keyStr.indexOf(c.charAt(e++)), d = _keyStr.indexOf(c.charAt(e++)), f = _keyStr.indexOf(c.charAt(e++)), g = _keyStr.indexOf(c.charAt(e++)), b = b << 2 | d >> 4, d = (d & 15) << 4 | f >> 2, h = (f & 3) << 6 | g, a += String.fromCharCode(b), 64 != f && (a += String.fromCharCode(d)), 64 != g && (a += String.fromCharCode(h));
        return a = _utf8_decode(a)
    };
    _utf8_decode = function(c) {
        for (var a = "", b = 0, d = c1 = c2 = 0; b < c.length;) d = c.charCodeAt(b), 128 > d ? (a += String.fromCharCode(d), b++) : 191 < d && 224 > d ? (c2 = c.charCodeAt(b + 1), a += String.fromCharCode((d & 31) << 6 | c2 & 63), b += 2) : (c2 = c.charCodeAt(b + 1), c3 = c.charCodeAt(b + 2), a += String.fromCharCode((d & 15) << 12 | (c2 & 63) << 6 | c3 & 63), b += 3);
        return a
    }
}
function GetImg() {
    var DATA = '""" + js_code + """';
    var B = new Base;
    var imgs = new Array;
    DATA = (new Function("return " + B.decode(DATA.substring(1))))();
	for (var i = 0; i < DATA.picture.length; i++) {
        imgs[i] = DATA.picture[i].url;
    }
    return imgs;
}
            return GetImg();
        })
    """
    #print js_code
    ctxt = PyV8.JSContext()
    ctxt.enter()
    func = ctxt.eval(js_code)
    ret = func()
    return ret


def decode_code_manhuagui(packed_code):
    js_code = """
        (function(){
	        function GetImg(){
                    var LZString=(function(){var f=String.fromCharCode;var keyStrBase64="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";var baseReverseDic={};function getBaseValue(alphabet,character){if(!baseReverseDic[alphabet]){baseReverseDic[alphabet]={};for(var i=0;i<alphabet.length;i++){baseReverseDic[alphabet][alphabet.charAt(i)]=i}}return baseReverseDic[alphabet][character]}var LZString={decompressFromBase64:function(input){if(input==null)return"";if(input=="")return null;return LZString._0(input.length,32,function(index){return getBaseValue(keyStrBase64,input.charAt(index))})},_0:function(length,resetValue,getNextValue){var dictionary=[],next,enlargeIn=4,dictSize=4,numBits=3,entry="",result=[],i,w,bits,resb,maxpower,power,c,data={val:getNextValue(0),position:resetValue,index:1};for(i=0;i<3;i+=1){dictionary[i]=i}bits=0;maxpower=Math.pow(2,2);power=1;while(power!=maxpower){resb=data.val&data.position;data.position>>=1;if(data.position==0){data.position=resetValue;data.val=getNextValue(data.index++)}bits|=(resb>0?1:0)*power;power<<=1}switch(next=bits){case 0:bits=0;maxpower=Math.pow(2,8);power=1;while(power!=maxpower){resb=data.val&data.position;data.position>>=1;if(data.position==0){data.position=resetValue;data.val=getNextValue(data.index++)}bits|=(resb>0?1:0)*power;power<<=1}c=f(bits);break;case 1:bits=0;maxpower=Math.pow(2,16);power=1;while(power!=maxpower){resb=data.val&data.position;data.position>>=1;if(data.position==0){data.position=resetValue;data.val=getNextValue(data.index++)}bits|=(resb>0?1:0)*power;power<<=1}c=f(bits);break;case 2:return""}dictionary[3]=c;w=c;result.push(c);while(true){if(data.index>length){return""}bits=0;maxpower=Math.pow(2,numBits);power=1;while(power!=maxpower){resb=data.val&data.position;data.position>>=1;if(data.position==0){data.position=resetValue;data.val=getNextValue(data.index++)}bits|=(resb>0?1:0)*power;power<<=1}switch(c=bits){case 0:bits=0;maxpower=Math.pow(2,8);power=1;while(power!=maxpower){resb=data.val&data.position;data.position>>=1;if(data.position==0){data.position=resetValue;data.val=getNextValue(data.index++)}bits|=(resb>0?1:0)*power;power<<=1}dictionary[dictSize++]=f(bits);c=dictSize-1;enlargeIn--;break;case 1:bits=0;maxpower=Math.pow(2,16);power=1;while(power!=maxpower){resb=data.val&data.position;data.position>>=1;if(data.position==0){data.position=resetValue;data.val=getNextValue(data.index++)}bits|=(resb>0?1:0)*power;power<<=1}dictionary[dictSize++]=f(bits);c=dictSize-1;enlargeIn--;break;case 2:return result.join('')}if(enlargeIn==0){enlargeIn=Math.pow(2,numBits);numBits++}if(dictionary[c]){entry=dictionary[c]}else{if(c===dictSize){entry=w+w.charAt(0)}else{return null}}result.push(entry);dictionary[dictSize++]=w+entry.charAt(0);enlargeIn--;w=entry;if(enlargeIn==0){enlargeIn=Math.pow(2,numBits);numBits++}}}};return LZString})();String.prototype.splic=function(f){return LZString.decompressFromBase64(this).split(f)};
	                """ + packed_code + """
                    var imgs = new Array;

                    for (var i = 0; i < cInfo.files.length; i++) {
                        imgs[i] = encodeURI(cInfo.path + cInfo.files[i]);
                    }
                    return imgs;
	            }
            return GetImg();
        })
    """
    #print js_code
    ctxt = PyV8.JSContext()
    ctxt.enter()
    func = ctxt.eval(js_code)
    return func()

def comic_down_733dm(url, dest_dir):
    base_url = fetch_html('http://www.733dm.net/skin/2014mh/global.js')
    base_url = base_url.decode('GBK')
    base_url = get_sub_text(base_url, 'WebimgServerURL[0]="', '";')
    chapters = get_chapters_733dm(url)
    for i in range(len(chapters)):
        title = chapters[len(chapters) - 1 - i][0]
        link = chapters[len(chapters) - 1 - i][1]
        print (link)
        html_text = fetch_html(link)
        html_text = html_text.decode('GBK')
        code = extrac_code(html_text)
        ch_dir = dest_dir + '\\chapter_' + str(i + 1).zfill(3) + '_' + title + '\\'
        if (not os.path.exists(ch_dir)):
            os.makedirs(ch_dir)
        #build_html(i + 1, code)
        js_images = decode_code_733dm(code)
        for j in range(0, len(js_images)):
            if (js_images[j] is None):
                continue
            img_url = base_url + js_images[j]
            img_file = ch_dir + 'P_{:0>3d}.jpg'.format(j)    
            print ('saving ' + img_url)
            res = save_img(img_url, img_file)
                
        touch_file(ch_dir + '.finish')       
        print ('chapter ' + str(i) + ' end')




def comic_down_dmzj(url, dest_dir):
    book_html = fetch_html(url)
    chapters = get_chapters_dmzj(url)
    for i in range(0, len(chapters)):
        title = chapters[i][0]
        link = chapters[i][1]
        print (link)
        html_text = fetch_html(link)
        html_text = html_text.decode('utf-8')
        code = extrac_code_dmzj(html_text)
        ch_dir = dest_dir + '\\chapter_' + str(i + 1).zfill(3) + '_' + title + '\\'
        if (not os.path.exists(ch_dir)):
            os.makedirs(ch_dir)
        #build_html(i + 1, code)
        js_images = decode_code_dmzj(code)
        for j in range(0, len(js_images)):
            if (js_images[j] is None):
                continue
            img_url = 'http://images.dmzj.com/' + js_images[j]
            img_file = ch_dir + 'P_{:0>3d}.jpg'.format(j)    
            print ('saving ' + img_url)
            res = save_img(img_url, img_file, link)
            if (not res):
                print ('saving failed')
         
        touch_file(ch_dir + '.finish')       
        print ('chapter ' + str(i + 1) + ' end')

def comic_down_tx(url, dest_dir):
    cookie = '__AC__=1; pgv_pvid=3217031234; pt2gguin=o0453916104; ptcz=9e06459eafbf93db6b914f25ef4bac2c30072d699927028dff812cf0276515e9; o_cookie=453916104; pac_uid=1_453916104; tvfe_boss_uuid=4faddc1b6dbe82a9; pgv_pvi=8835530752; RK=JNMCS9NPVf; theme=dark; readRecord=%5B%5B543782%2C%22%E5%B9%B2%E7%89%A9%E5%A6%B9%EF%BC%81%E5%B0%8F%E5%9F%8B%22%2C193%2C%22%E7%AC%AC192%E8%AF%9D%22%2C192%5D%2C%5B505436%2C%22%E9%BE%99%E7%8F%A0%22%2C2%2C%22%E7%AC%AC2%E8%AF%9D%20%E9%BE%99%E7%8F%A0%E4%B8%8D%E8%A7%81%E4%BA%86%EF%BC%9F%22%2C2%5D%2C%5B530449%2C%22%E5%A6%96%E9%AD%94%E5%90%88%E4%BC%99%E4%BA%BA%22%2C1%2C%2201.%E5%91%BD%E4%B8%AD%E6%B3%A8%E5%AE%9A%E6%88%91%E5%90%83%E4%BD%A0%EF%BC%81%22%2C1%5D%5D; readLastRecord=%5B%5D; ts_uid=3915367972; lw_user_info=%7B%22uin%22%3A%22453916104%22%2C%22nick%22%3A%22Walter%22%2C%22head%22%3A%22http%3A%5C%2F%5C%2Fq1.qlogo.cn%5C%2Fg%3Fb%3Dqq%26k%3DEQnpNfd6AwUlPlo0EEOReg%26s%3D640%26t%3D1493263596%22%7D; ptui_loginuin=453916104; roastState=2; pgv_si=s975148032; pgv_info=ssid=s5999862154; ts_last=ac.qq.com/VIP/pay; pc_userinfo_cookie=%7B%22uin%22%3A%22453916104%22%2C%22uinCrypt%22%3A%22RnpnYWRpVkdqMm5hR2hIUDM5RmVydz09%22%2C%22nick%22%3A%22Walter%22%2C%22avatar%22%3A%22http%3A%2F%2Fq1.qlogo.cn%2Fg%3Fb%3Dqq%26k%3DEQnpNfd6AwUlPlo0EEOReg%26s%3D640%26t%3D1493263596%22%2C%22hasLogin%22%3A%221%22%2C%22token%22%3A%226po9oJ4vSkxG%2F2Y48GWZKT6jtFgD2zJ3D6Nf5BCTYHT5GMV%2BvEqmK5SiV23Q4V9KgeQdtCEfezJy%2BhM0fNUhRMOfCS9Xr5alj3CdQzrRPtM%3D%22%7D; _qpsvr_localtk=0.18567182099000745; ptisp=cnc; uin=o0453916104; skey=@w1MYwkVzE; p_uin=o0453916104; p_skey=yVAHlTbtwdr40QqBuCAxWOONgIo8*1bPe46T0j6DP0E_; pt4_token=zQszq7LkTowpK0NAbft36ecFjLZztLVGD-Wr-vGasyk_'
    book_html = fetch_html(url)
    chapters = get_chapters_tx(url)
    start_chapter = 0   	
    for i in range(0, len(chapters)):
        title = chapters[i][0]
        link = chapters[i][1]
        print (link)
        ch_dir = dest_dir + '\\chapter_' + str(i + 1).zfill(3) + '_' + title + '\\'
        if os.path.exists(ch_dir + '\\.finish'):
            print ('skipping...')
            continue
        html_text = fetch_html2(link, url, cookie)
        html_text = html_text.decode('utf-8')
        code = extrac_code_tx(html_text)
        if (not os.path.exists(ch_dir)):
            os.makedirs(ch_dir)
        #build_html(i + 1, code)
        js_images = decode_code_tx(code)
        for j in range(0, len(js_images)):
            if (js_images[j] is None):
                continue
            img_url = js_images[j]
            img_file = ch_dir + 'P_{:0>3d}.jpg'.format(j)    
            print ('saving ' + img_url)
            res = save_img(img_url, img_file, link, cookie)
            if (not res):
                print ('saving failed')
                
        touch_file(ch_dir + '.finish')
        print ('chapter ' + str(i + 1) + ' end')
        

def comic_down_manhuagui(url, dest_dir):
    book_html = fetch_html(url)
    chapters = get_chapters_manhuagui(url)
    start_chapter = 0
    print(chapters)
   	
    for i in range(len(chapters)):
        title = chapters[len(chapters) - 1 - i][0]
        link = chapters[len(chapters) - 1 - i][1]
        print (link)
        html_text = fetch_html(link)
        html_text = html_text.decode('utf-8')
        code = extrac_code_manhuagui(html_text)
        ch_dir = dest_dir + '\\chapter_' + str(i + 1).zfill(3) + '_' + title + '\\'
        if (not os.path.exists(ch_dir)):
            os.makedirs(ch_dir)
        #build_html(i + 1, code)
        js_images = decode_code_manhuagui(code)
        for j in range(0, len(js_images)):
            if (js_images[j] is None):
                continue
            img_url = 'http://i.hamreus.com:8080' + js_images[j].decode('utf-8')
            img_url = img_url[0: len(img_url) - 5]
            img_file = ch_dir + 'P_{:0>3d}.jpg'.format(j)    
            print ('saving ' + img_url)
            res = save_img(img_url, img_file, link)
            if (not res):
                print ('saving failed')
                
        touch_file(ch_dir + '.finish')       
        print ('chapter ' + str(i + 1) + ' end')

def comic_down():
    url = 'http://www.733dm.net/mh/'
    id = raw_input('input comic id:')
    url = url + id
    dest_dir = 'd:\\book_'+ str(id).zfill(7)
    if (not os.path.exists(dest_dir)):
        os.makedirs(dest_dir)
    os.chdir(dest_dir)
    match = []
    if (test_url(url)):
        title = get_title(url)
        match.append(['733dm', url, title])
    url = 'http://www.manhuagui.com/comic/'
    url = url + id + '/'
    if test_url(url):
        title = get_title(url)
        match.append(['manhuagui', url, title])
    url = 'http://manhua.dmzj.com/'
    url = url + id + '/'
    if test_url(url):
        title = get_title(url)
        match.append(['dmzj', url, title])
    url = 'http://ac.qq.com/Comic/comicInfo/id/'
    url = url + id + '/'
    if test_url(url):
        title = get_title(url)
        if title != '错误提示 - 腾讯动漫':
            match.append(['tx', url, title])
    for i in range(len(match)):
        print (i, match[i][2])
    num = 0
    if len(match) > 0:
        if len(match) > 1:
            num = input('which one? ')
            if num < 0 or num >= len(match):
                num = 0
        url = match[num][1]
        eval('comic_down_{}(url, dest_dir)'.format(match[num][0]))
    else:
        print('item not found')


def tmp_fetch():
    url = 'mhpic.zymkcdn.com/comic/Q/呛辣校园俏女生/{:0>2d}话/{}.jpg-kmw.middle'

    if (not os.path.exists('y:\\ql')):
        os.makedirs('y:\\ql')

    for ch in range(31, 50):
        if (not os.path.exists('y:\\ql\\ch_' + str(ch).zfill(2))):
            os.makedirs('y:\\ql\\ch_' + str(ch).zfill(2))
        for page in range(1, 100):
            f_url = url.format(ch, page)
            f_name = 'y:\\ql\\ch_{:02d}\\P_{:03d}.jpg'.format(ch, page)
            f_url='http://' + urllib2.quote(f_url)
            res = save_img(f_url, f_name)
            if (not res):
                break
#tmp_fetch()
comic_down()


    
